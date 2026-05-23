"""
Unit tests for pure SAAM fragment scoring (Story 2.3).

Uses deterministic inputs — no live LLM, SQLite, or embedding access.
"""
from __future__ import annotations

import pytest

from raa.judge.scoring import (
    _normalize_quality_keys,
    _resolve_arch_fragment,
    _satisfaction_factor,
    _score_scenario,
    _score_by_requirement_coverage,
    rank_batch_fragments,
    score_fragment_record,
)
from raa.state.models import (
    ArchFragment,
    C4Entity,
    FragmentScore,
    SAAMScenario,
)


# ── Test data helpers ─────────────────────────────────────────────────────────


def _make_quality_weights() -> dict[str, int]:
    return {
        "Performance Efficiency": 5,
        "Security": 3,
        "Reliability": 4,
        "Maintainability": 1,
        "Usability": 2,
    }


def _make_scenario(
    scenario_id: str = "S1",
    description: str = "Test scenario",
    quality_attributes: list[str] | None = None,
    satisfaction: str = "satisfied",
) -> SAAMScenario:
    return SAAMScenario(
        id=scenario_id,
        description=description,
        quality_attributes=quality_attributes or ["Performance Efficiency"],
        satisfaction=satisfaction,
    )


def _make_fragment(
    entities: list[C4Entity] | None = None,
    relationships: list | None = None,
    saam_scenarios: list[SAAMScenario] | None = None,
) -> ArchFragment:
    return ArchFragment(
        entities=entities or [],
        relationships=relationships or [],
        saam_scenarios=saam_scenarios or [],
    )


def _make_record(
    batch_id: str = "batch-1",
    batch_index: int = 0,
    strategy: str = "raa_a",
    thread_id: str = "thread-1-0-raa_a",
    reduced_confidence: bool = False,
    arch_fragment: dict | None = None,
    skipped: bool = False,
    skip_reason: str | None = None,
) -> dict:
    return {
        "batch_id": batch_id,
        "batch_index": batch_index,
        "strategy": strategy,
        "thread_id": thread_id,
        "reduced_confidence": reduced_confidence,
        "arch_fragment": arch_fragment,
        "skipped": skipped,
        "skip_reason": skip_reason,
    }


# ── Task 6.2: Scoring with multiple SAAM scenarios ───────────────────────────


def test_score_fragment_with_multiple_scenarios():
    """Fragment with multiple scenarios should sum contributions correctly."""
    scenario1 = _make_scenario(
        "S1", "Performance scenario",
        ["Performance Efficiency"], "satisfied",
    )
    scenario2 = _make_scenario(
        "S2", "Security scenario",
        ["Security"], "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario1, scenario2])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    # S1: 5 * 1.0 = 5.0, S2: 3 * 1.0 = 3.0, raw = 8.0
    assert result.raw_score == pytest.approx(8.0)
    assert result.final_score == pytest.approx(8.0)
    assert result.multiplier == 1.0
    assert result.is_primary is False
    assert len(result.scenario_contributions) == 2


def test_score_fragment_scenario_matches_multiple_quality_attributes():
    """Scenario with multiple quality attributes should sum all weights."""
    scenario = _make_scenario(
        "S1", "Multi-attr scenario",
        ["Performance Efficiency", "Reliability", "Security"],
        "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    # 5 + 4 + 3 = 12 * 1.0 = 12.0
    assert result.raw_score == pytest.approx(12.0)


# ── Task 6.3: Satisfaction factors ───────────────────────────────────────────


def test_partial_satisfaction_factor():
    """Partially satisfied scenario gets 0.5 factor."""
    scenario = _make_scenario(
        "S1", "Partial scenario",
        ["Performance Efficiency"], "partial",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    # 5 * 0.5 = 2.5
    assert result.raw_score == pytest.approx(2.5)


def test_unsatisfied_satisfaction_factor():
    """Unsatisfied scenario gets 0.0 factor."""
    scenario = _make_scenario(
        "S1", "Unsatisfied scenario",
        ["Security"], "unsatisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    # 3 * 0.0 = 0.0
    assert result.raw_score == pytest.approx(0.0)


def test_unknown_satisfaction_factor():
    """Unknown satisfaction is handled explicitly (0.0 factor)."""
    scenario = _make_scenario(
        "S1", "Unknown scenario",
        ["Reliability"], "unknown",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(0.0)


def test_partially_satisfied_alias():
    """'partially_satisfied' also maps to 0.5."""
    scenario = _make_scenario(
        "S1", "Partially satisfied alias",
        ["Performance Efficiency"], "partially_satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(2.5)


# ── Task 6.4: Reduced-confidence multiplier ──────────────────────────────────


def test_reduced_confidence_applies_exact_multiplier():
    """Reduced-confidence record gets the named 0.5 multiplier applied."""
    scenario = _make_scenario(
        "S1", "Performance scenario",
        ["Performance Efficiency"], "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(
        arch_fragment=fragment.model_dump(), reduced_confidence=True,
    )
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(5.0)
    assert result.multiplier == 0.5
    assert result.final_score == pytest.approx(2.5)


def test_normal_confidence_no_multiplier():
    """Non-reduced-confidence record has multiplier 1.0."""
    scenario = _make_scenario(
        "S1", "Performance scenario",
        ["Performance Efficiency"], "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump(), reduced_confidence=False)
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.multiplier == 1.0
    assert result.raw_score == result.final_score


# ── Task 6.5: Skipped records and null fragments ─────────────────────────────


def test_skipped_record_excluded():
    """Skipped records return None from score_fragment_record."""
    record = _make_record(skipped=True, skip_reason="reduced_confidence")
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is None


def test_null_arch_fragment_excluded():
    """Records with arch_fragment=None return None."""
    record = _make_record(arch_fragment=None)
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is None


def test_rank_batch_fragments_tracks_skipped():
    """rank_batch_fragments should include skipped in metadata."""
    valid_fragment = _make_fragment(saam_scenarios=[_make_scenario()])
    records = [
        _make_record(strategy="raa_a", arch_fragment=valid_fragment.model_dump()),
        _make_record(strategy="raa_b", skipped=True, skip_reason="reduced_confidence"),
        _make_record(strategy="raa_c", arch_fragment=None),
    ]
    qw = _make_quality_weights()

    result = rank_batch_fragments(records, qw)

    assert len(result["scored_fragments"]) == 1
    assert len(result["skipped_fragments"]) == 2
    assert result["primary_fragment"] is not None
    assert result["primary_fragment"].strategy == "raa_a"


# ── Task 6.6: Single RAA-A fallback ──────────────────────────────────────────


def test_single_raa_a_fallback():
    """When only RAA-A produced a fragment, it becomes primary."""
    fragment = _make_fragment(saam_scenarios=[_make_scenario()])
    records = [
        _make_record(strategy="raa_a", arch_fragment=fragment.model_dump()),
        _make_record(strategy="raa_b", skipped=True, skip_reason="reduced_confidence"),
        _make_record(strategy="raa_c", skipped=True, skip_reason="reduced_confidence"),
    ]
    qw = _make_quality_weights()

    result = rank_batch_fragments(records, qw)

    assert result["primary_fragment"] is not None
    assert result["primary_fragment"].strategy == "raa_a"
    assert result["primary_fragment"].is_primary is True
    assert len(result["scored_fragments"]) == 1


# ── Task 6.7: Deterministic tie-breaking ─────────────────────────────────────


def test_tie_break_by_strategy_order():
    """Equal scores break by strategy order: raa_a > raa_b > raa_c."""
    scenario = _make_scenario(
        "S1", "Performance scenario",
        ["Performance Efficiency"], "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    frag_dict = fragment.model_dump()

    records = [
        _make_record(strategy="raa_c", thread_id="t-c", arch_fragment=frag_dict),
        _make_record(strategy="raa_a", thread_id="t-a", arch_fragment=frag_dict),
        _make_record(strategy="raa_b", thread_id="t-b", arch_fragment=frag_dict),
    ]
    qw = _make_quality_weights()

    result = rank_batch_fragments(records, qw)

    scores = result["scored_fragments"]
    assert len(scores) == 3
    # All have same final_score, so sorted by strategy order
    assert scores[0].strategy == "raa_a"
    assert scores[1].strategy == "raa_b"
    assert scores[2].strategy == "raa_c"
    assert scores[0].is_primary is True


def test_tie_break_by_thread_id():
    """Same strategy and score break by thread_id alphabetically."""
    scenario = _make_scenario(
        "S1", "Performance scenario",
        ["Performance Efficiency"], "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    frag_dict = fragment.model_dump()

    records = [
        _make_record(strategy="raa_a", thread_id="t-z", arch_fragment=frag_dict),
        _make_record(strategy="raa_a", thread_id="t-a", arch_fragment=frag_dict),
        _make_record(strategy="raa_a", thread_id="t-m", arch_fragment=frag_dict),
    ]
    qw = _make_quality_weights()

    result = rank_batch_fragments(records, qw)

    scores = result["scored_fragments"]
    assert scores[0].thread_id == "t-a"
    assert scores[1].thread_id == "t-m"
    assert scores[2].thread_id == "t-z"


# ── Task 6.8: Input order independence ───────────────────────────────────────


def test_input_order_does_not_affect_result():
    """Shuffling input records should not change primary selection or order."""
    scenario_a = _make_scenario("SA", "A scenario", ["Security"], "satisfied")
    scenario_b = _make_scenario("SB", "B scenario", ["Performance Efficiency"], "satisfied")
    frag_a = _make_fragment(saam_scenarios=[scenario_a]).model_dump()
    frag_b = _make_fragment(saam_scenarios=[scenario_b]).model_dump()

    records_order1 = [
        _make_record(strategy="raa_a", arch_fragment=frag_a),
        _make_record(strategy="raa_b", arch_fragment=frag_b),
    ]
    records_order2 = [
        _make_record(strategy="raa_b", arch_fragment=frag_b),
        _make_record(strategy="raa_a", arch_fragment=frag_a),
    ]
    qw = _make_quality_weights()

    result1 = rank_batch_fragments(records_order1, qw)
    result2 = rank_batch_fragments(records_order2, qw)

    # Primary should be the same (raa_b has higher score: 5 > 3)
    assert result1["primary_fragment"].strategy == result2["primary_fragment"].strategy
    assert result1["primary_fragment"].final_score == result2["primary_fragment"].final_score
    # Score ordering should be identical
    assert [s.strategy for s in result1["scored_fragments"]] == [
        s.strategy for s in result2["scored_fragments"]
    ]


# ── Task 6.9: Dict and ArchFragment inputs ───────────────────────────────────


def test_score_fragment_record_accepts_dict_input():
    """Dict input should work correctly."""
    scenario = _make_scenario("S1", "Dict scenario", ["Reliability"], "satisfied")
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(4.0)


def test_score_fragment_record_accepts_arch_fragment_input():
    """Direct ArchFragment input should work correctly."""
    scenario = _make_scenario("S1", "Model scenario", ["Reliability"], "satisfied")
    fragment = _make_fragment(saam_scenarios=[scenario])
    qw = _make_quality_weights()

    result = score_fragment_record(fragment, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(4.0)


def test_score_fragment_record_accepts_dict_with_arch_fragment_instance():
    """Dict with ArchFragment instance as arch_fragment should work."""
    scenario = _make_scenario("S1", "Nested scenario", ["Security"], "satisfied")
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment)
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(3.0)


# ── Utility function tests ───────────────────────────────────────────────────


def test_normalize_quality_keys_case_insensitive():
    """Quality keys should be matched case-insensitively."""
    qw = {"Performance Efficiency": 5, "SECURITY": 3}
    normalized = _normalize_quality_keys(qw)

    assert "performance efficiency" in normalized
    assert "security" in normalized
    assert normalized["performance efficiency"] == 5
    assert normalized["security"] == 3


def test_satisfaction_factor_unrecognized():
    """Unrecognized satisfaction strings should return 0.0."""
    assert _satisfaction_factor("garbled") == 0.0
    assert _satisfaction_factor("") == 0.0


def test_resolve_arch_fragment_dict():
    """_resolve_arch_fragment should handle dict with model_dump'd fragment."""
    fragment = _make_fragment()
    record = _make_record(arch_fragment=fragment.model_dump())

    result = _resolve_arch_fragment(record)

    assert isinstance(result, ArchFragment)


def test_resolve_arch_fragment_direct():
    """_resolve_arch_fragment should return ArchFragment directly."""
    fragment = _make_fragment()

    result = _resolve_arch_fragment(fragment)

    assert result is fragment


def test_resolve_arch_fragment_none():
    """_resolve_arch_fragment should return None for null arch_fragment."""
    record = _make_record(arch_fragment=None)

    result = _resolve_arch_fragment(record)

    assert result is None


# ── Fallback scoring tests ───────────────────────────────────────────────────


def test_fallback_scoring_no_scenarios():
    """Fragment without SAAM scenarios falls back to requirement coverage."""
    entity = C4Entity(
        id="c1", name="Test Container", requirement_ids=["R1", "R2"],
    )
    fragment = _make_fragment(entities=[entity])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(2.0)  # 2 requirements * 1.0
    assert len(result.scenario_contributions) == 3
    assert result.scenario_contributions[-1]["source"] == "fallback_note"
    assert "score computed by requirement coverage" in result.scenario_contributions[-1]["note"]


def test_fallback_scoring_no_scenarios_no_requirements():
    """Fragment with no scenarios and no requirement coverage returns 0.0."""
    fragment = _make_fragment(entities=[], saam_scenarios=[])
    record = _make_record(arch_fragment=fragment.model_dump())
    qw = _make_quality_weights()

    result = score_fragment_record(record, qw)

    assert result is not None
    assert result.raw_score == pytest.approx(0.0)
    assert len(result.scenario_contributions) == 1
    assert result.scenario_contributions[0]["source"] == "fallback_note"
    assert "score is 0.0" in result.scenario_contributions[0]["note"]


# ── Edge cases ────────────────────────────────────────────────────────────────


def test_empty_quality_weights():
    """Empty quality_weights should produce zero scores."""
    scenario = _make_scenario(
        "S1", "Any scenario",
        ["Performance Efficiency"], "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())

    result = score_fragment_record(record, {})

    assert result is not None
    assert result.raw_score == pytest.approx(0.0)


def test_empty_records():
    """Empty record list should return no primary."""
    result = rank_batch_fragments([], _make_quality_weights())

    assert result["scored_fragments"] == []
    assert result["skipped_fragments"] == []
    assert result["primary_fragment"] is None


def test_quality_attribute_not_in_weights():
    """Scenario referencing an attribute absent from quality_weights should get 0."""
    scenario = _make_scenario(
        "S1", "Unknown attr",
        ["NonExistent Attribute"], "satisfied",
    )
    fragment = _make_fragment(saam_scenarios=[scenario])
    record = _make_record(arch_fragment=fragment.model_dump())

    result = score_fragment_record(record, _make_quality_weights())

    assert result is not None
    assert result.raw_score == pytest.approx(0.0)


def test_fragment_score_model_fields():
    """FragmentScore should have all required AC #8 metadata fields."""
    score = FragmentScore(
        batch_id="b1",
        batch_index=0,
        strategy="raa_a",
        thread_id="t1",
        raw_score=10.0,
        multiplier=1.0,
        final_score=10.0,
        scenario_contributions=[{"scenario_id": "S1", "contribution": 10.0}],
        is_primary=True,
    )

    assert score.batch_id == "b1"
    assert score.batch_index == 0
    assert score.strategy == "raa_a"
    assert score.thread_id == "t1"
    assert score.raw_score == 10.0
    assert score.multiplier == 1.0
    assert score.final_score == 10.0
    assert len(score.scenario_contributions) == 1
    assert score.is_primary is True
