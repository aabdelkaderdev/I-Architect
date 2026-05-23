"""
Unit tests for Judge reconciliation node (Story 2.3 + 2.4).
"""
from __future__ import annotations

import pytest

from raa.judge.reconcile import select_primary_fragment
from raa.state.models import ArchFragment, C4Entity, C4Relationship, SAAMScenario


def _make_fragment():
    scenario = SAAMScenario(
        id="S1",
        description="Test scenario",
        quality_attributes=["Performance Efficiency"],
        satisfaction="satisfied",
    )
    return ArchFragment(saam_scenarios=[scenario])


def _make_fragment_with_entities():
    """Create a fragment with entities for merge testing."""
    scenario = SAAMScenario(
        id="S1",
        description="Test scenario",
        quality_attributes=["Performance Efficiency"],
        satisfaction="satisfied",
    )
    entity = C4Entity(
        id="user_service",
        name="User Service",
        description="Handles user authentication and authorization",
        c4_type="container",
        technology="Python, FastAPI",
        requirement_ids=["R1", "R2"],
    )
    relationship = C4Relationship(
        id="rel-1",
        source_id="user_service",
        target_id="payment_service",
        description="Uses",
        relationship_type="uses",
    )
    return ArchFragment(
        entities=[entity],
        relationships=[relationship],
        saam_scenarios=[scenario],
    )


def _make_state(batch_outputs=None, batch_cursor=0, quality_weights=None, arch_model=None):
    return {
        "batch_cursor": batch_cursor,
        "quality_weights": quality_weights or {"Performance Efficiency": 5},
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "review_mode": "autonomous",
        "normalized_asrs": [],
        "normalized_non_asr": [],
        "embeddings_ready": False,
        "batch_outputs": batch_outputs or [],
        "open_questions": [],
        "incoherent_batches": [],
        "arch_model": arch_model or {},
    }


def _make_record(
    batch_id: str = "batch-1",
    batch_index: int = 0,
    strategy: str = "raa_a",
    thread_id: str = "t-1-0-raa_a",
    arch_fragment: dict | None = None,
    skipped: bool = False,
) -> dict:
    return {
        "batch_id": batch_id,
        "batch_index": batch_index,
        "strategy": strategy,
        "thread_id": thread_id,
        "reduced_confidence": False,
        "arch_fragment": arch_fragment,
        "skipped": skipped,
        "skip_reason": None,
    }


def test_select_primary_fragment_sets_primary():
    """Node should select the primary fragment for the current batch."""
    frag = _make_fragment()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
        _make_record(strategy="raa_b", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    assert "judge_rankings" in result
    rankings = result["judge_rankings"]
    assert 0 in rankings
    assert rankings[0]["primary_fragment"] is not None
    assert rankings[0]["primary_fragment"].is_primary is True


def test_select_primary_fragment_filters_by_batch_cursor():
    """Node should only score records matching the current batch_cursor."""
    frag = _make_fragment()
    batch0 = [
        _make_record(batch_index=0, strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    batch1 = [
        _make_record(batch_index=1, strategy="raa_b", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(
        batch_outputs=batch0 + batch1, batch_cursor=1,
    )

    result = select_primary_fragment(state)

    rankings = result["judge_rankings"]
    assert 1 in rankings
    assert len(rankings[1]["scored_fragments"]) == 1
    assert rankings[1]["scored_fragments"][0].batch_index == 1


def test_select_primary_fragment_increments_batch_cursor():
    """Story 2.4: Node must increment batch_cursor by 1."""
    frag = _make_fragment()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=3)

    result = select_primary_fragment(state)

    assert result["batch_cursor"] == 4


def test_select_primary_fragment_returns_arch_model():
    """Story 2.4: Node must return arch_model in state update."""
    frag = _make_fragment()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    assert "arch_model" in result
    assert "entities" in result["arch_model"]
    assert "relationships" in result["arch_model"]


def test_select_primary_fragment_empty_batch():
    """Empty or missing batch outputs should not crash."""
    state = _make_state(batch_outputs=[], batch_cursor=0)

    result = select_primary_fragment(state)

    assert "judge_rankings" in result
    rankings = result["judge_rankings"]
    assert rankings[0]["primary_fragment"] is None
    # Story 2.4: still advances cursor and returns arch_model
    assert result["batch_cursor"] == 1
    assert "arch_model" in result


def test_select_primary_fragment_preserves_existing_rankings():
    """Node should preserve rankings from previous batch cursors."""
    frag = _make_fragment()
    records0 = [
        _make_record(batch_index=0, strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    records1 = [
        _make_record(batch_index=1, strategy="raa_b", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(
        batch_outputs=records0 + records1,
        batch_cursor=0,
    )
    # First run on batch 0
    intermediate = select_primary_fragment(state)

    # Second run on batch 1 with merged state
    state2 = _make_state(
        batch_outputs=records0 + records1,
        batch_cursor=1,
        arch_model=intermediate.get("arch_model"),
    )
    state2["judge_rankings"] = intermediate["judge_rankings"]
    state2["open_questions"] = []

    result = select_primary_fragment(state2)

    rankings = result["judge_rankings"]
    assert 0 in rankings  # preserved
    assert 1 in rankings  # new
    assert rankings[0]["primary_fragment"].strategy == "raa_a"
    assert rankings[1]["primary_fragment"].strategy == "raa_b"


def test_select_primary_fragment_merges_entities():
    """Story 2.4: Primary fragment entities should be merged into arch_model."""
    frag = _make_fragment_with_entities()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    assert len(result["arch_model"]["entities"]) == 1
    assert result["arch_model"]["entities"][0]["name"] == "User Service"
    assert len(result["arch_model"]["relationships"]) == 1
    assert "open_questions" in result


# ── Story 2.5 Integration Tests ─────────────────────────────────────────────


def test_reconcile_entities_carry_saam_score():
    """Story 2.5: C4Entity objects in returned arch_model must carry saam_score."""
    frag = _make_fragment_with_entities()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    for entity in result["arch_model"]["entities"]:
        assert "saam_score" in entity
        assert isinstance(entity["saam_score"], float)
        assert 0.0 <= entity["saam_score"] <= 1.0


def test_reconcile_calls_cross_cutting_promotion():
    """Story 2.5: Cross-cutting candidates in fragment trigger promotion."""
    entity = C4Entity(
        id="auth_service",
        name="Authentication Service",
        description="Handles security and authentication",
        c4_type="container",
        technology="Python",
        requirement_ids=["R1", "R2"],
    )
    frag = ArchFragment(
        entities=[entity],
        relationships=[],
        cross_cutting_candidates=["security", "logging"],
        saam_scenarios=[],
    )
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    entity_ids = {e["id"] for e in result["arch_model"]["entities"]}
    assert "cc_security" in entity_ids
    assert "cc_logging" in entity_ids


def test_reconcile_no_cross_cutting_when_no_candidates():
    """Story 2.5: No cross-cutting candidates → no promoted components."""
    frag = _make_fragment_with_entities()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    entity_ids = {e["id"] for e in result["arch_model"]["entities"]}
    assert not any(eid.startswith("cc_") for eid in entity_ids)


def test_reconcile_passes_merge_log_to_calibration():
    """Story 2.5: merge_log from dedup flows into calibration (scores reflect merge state)."""
    entity = C4Entity(
        id="auth_service",
        name="Auth",
        description="Authentication service",
        c4_type="container",
        requirement_ids=["R1"],
    )
    frag = ArchFragment(
        entities=[entity],
        relationships=[],
        saam_scenarios=[],
    )
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    # Run first batch to add entity to arch_model
    result1 = select_primary_fragment(state)
    assert len(result1["arch_model"]["entities"]) == 1

    # Run second batch with same entity (different ID casing → exact_id merge)
    entity2 = C4Entity(
        id="auth_service",  # same normalized ID
        name="Auth v2",
        description="Updated authentication service",
        c4_type="container",
        requirement_ids=["R2"],
    )
    frag2 = ArchFragment(
        entities=[entity2],
        relationships=[],
        saam_scenarios=[],
    )
    records2 = [
        _make_record(batch_id="batch-2", batch_index=1, strategy="raa_a",
                     arch_fragment=frag2.model_dump()),
    ]
    state2 = _make_state(
        batch_outputs=records2,
        batch_cursor=1,
        arch_model=result1["arch_model"],
    )
    state2["judge_rankings"] = result1.get("judge_rankings", {})
    state2["open_questions"] = []

    result2 = select_primary_fragment(state2)
    # Entity merged → saam_score should be below base (dedup penalty applied)
    merged = result2["arch_model"]["entities"][0]
    from raa.utils.constants import SAAM_BASE_SCORE, SAAM_DEDUP_PENALTY
    assert merged["saam_score"] < SAAM_BASE_SCORE


def test_reconcile_boundary_groups_preserved():
    """Story 2.5: boundary_groups in arch_model are preserved through calibration."""
    frag = _make_fragment_with_entities()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    assert "boundary_groups" in result["arch_model"]


def test_reconcile_accumulates_cross_cutting_candidates():
    """Story 2.5: cross_cutting_candidates should accumulate across batches."""
    frag1 = ArchFragment(
        entities=[C4Entity(id="e1", name="E1", c4_type="container", requirement_ids=["R1"])],
        cross_cutting_candidates=["security"],
    )
    records1 = [_make_record(strategy="raa_a", arch_fragment=frag1.model_dump(), batch_index=0)]
    state1 = _make_state(batch_outputs=records1, batch_cursor=0)
    res1 = select_primary_fragment(state1)

    frag2 = ArchFragment(
        entities=[C4Entity(id="e2", name="E2", c4_type="container", requirement_ids=["R2"])],
        cross_cutting_candidates=["logging"],
    )
    records2 = [_make_record(strategy="raa_b", arch_fragment=frag2.model_dump(), batch_index=1)]
    state2 = _make_state(batch_outputs=records1 + records2, batch_cursor=1, arch_model=res1["arch_model"])
    state2["judge_rankings"] = res1["judge_rankings"]
    res2 = select_primary_fragment(state2)

    candidates = set(res2["arch_model"]["cross_cutting_candidates"])
    assert "security" in candidates
    assert "logging" in candidates


def test_reconcile_accumulates_merge_log():
    """Story 2.5: merge_log should accumulate in arch_model across batches."""
    frag1 = ArchFragment(
        entities=[C4Entity(id="e1", name="E1", c4_type="container")],
    )
    records1 = [_make_record(strategy="raa_a", arch_fragment=frag1.model_dump(), batch_index=0)]
    state1 = _make_state(batch_outputs=records1, batch_cursor=0)
    res1 = select_primary_fragment(state1)

    # Trigger a merge in batch 2
    frag2 = ArchFragment(
        entities=[C4Entity(id="e1", name="E1 Updated", c4_type="container")],
    )
    records2 = [_make_record(strategy="raa_a", arch_fragment=frag2.model_dump(), batch_index=1)]
    state2 = _make_state(batch_outputs=records1 + records2, batch_cursor=1, arch_model=res1["arch_model"])
    state2["judge_rankings"] = res1["judge_rankings"]
    res2 = select_primary_fragment(state2)

    assert "merge_log" in res2["arch_model"]
    assert len(res2["arch_model"]["merge_log"]) == 1


def test_reconcile_preserves_scenario_satisfaction_across_batches():
    """Story 2.5: SAAM scenarios should accumulate so previous perfect components are not degraded."""
    scenario1 = SAAMScenario(
        id="S1",
        description="S1",
        quality_attributes=["Performance"],
        satisfaction="satisfied",
        requirement_ids=["R1"],
    )
    entity1 = C4Entity(id="comp-1", name="Comp 1", c4_type="component", requirement_ids=["R1"])
    frag1 = ArchFragment(entities=[entity1], saam_scenarios=[scenario1])
    records1 = [_make_record(strategy="raa_a", arch_fragment=frag1.model_dump(), batch_index=0)]
    state1 = _make_state(batch_outputs=records1, batch_cursor=0)
    res1 = select_primary_fragment(state1)

    # Check component got perfect score in batch 1
    entities1 = res1["arch_model"]["entities"]
    comp1_batch1 = next(e for e in entities1 if e["id"] == "comp-1")
    from raa.utils.constants import SAAM_PERFECT_SCORE
    assert comp1_batch1["saam_score"] == SAAM_PERFECT_SCORE

    # Run batch 2 with a different component and scenario
    scenario2 = SAAMScenario(
        id="S2",
        description="S2",
        quality_attributes=["Security"],
        satisfaction="satisfied",
        requirement_ids=["R2"],
    )
    entity2 = C4Entity(id="comp-2", name="Comp 2", c4_type="component", requirement_ids=["R2"])
    frag2 = ArchFragment(entities=[entity2], saam_scenarios=[scenario2])
    records2 = [_make_record(strategy="raa_a", arch_fragment=frag2.model_dump(), batch_index=1)]
    state2 = _make_state(batch_outputs=records1 + records2, batch_cursor=1, arch_model=res1["arch_model"])
    state2["judge_rankings"] = res1["judge_rankings"]
    res2 = select_primary_fragment(state2)

    # Check comp-1 still has perfect score in batch 2
    entities2 = res2["arch_model"]["entities"]
    comp1_batch2 = next(e for e in entities2 if e["id"] == "comp-1")
    assert comp1_batch2["saam_score"] == SAAM_PERFECT_SCORE


