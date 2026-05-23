"""
Unit tests for Judge reconciliation node (Story 2.3).
"""
from __future__ import annotations

import pytest

from raa.judge.reconcile import select_primary_fragment
from raa.state.models import ArchFragment, SAAMScenario


def _make_fragment():
    scenario = SAAMScenario(
        id="S1",
        description="Test scenario",
        quality_attributes=["Performance Efficiency"],
        satisfaction="satisfied",
    )
    return ArchFragment(saam_scenarios=[scenario])


def _make_state(batch_outputs=None, batch_cursor=0, quality_weights=None):
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


def test_select_primary_fragment_returns_only_state_updates():
    """Node must return only state updates, not the full state."""
    frag = _make_fragment()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    # Should be a partial update dict, not contain the full state keys
    assert "judge_rankings" in result
    assert "batch_cursor" not in result
    assert "arch_model" not in result
    assert "batch_outputs" not in result


def test_select_primary_fragment_does_not_advance_batch_cursor():
    """Node must not return batch_cursor in the update."""
    frag = _make_fragment()
    records = [
        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
    ]
    state = _make_state(batch_outputs=records, batch_cursor=0)

    result = select_primary_fragment(state)

    assert "batch_cursor" not in result


def test_select_primary_fragment_empty_batch():
    """Empty or missing batch outputs should not crash."""
    state = _make_state(batch_outputs=[], batch_cursor=0)

    result = select_primary_fragment(state)

    assert "judge_rankings" in result
    rankings = result["judge_rankings"]
    assert rankings[0]["primary_fragment"] is None


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
    )
    state2["judge_rankings"] = intermediate["judge_rankings"]

    result = select_primary_fragment(state2)

    rankings = result["judge_rankings"]
    assert 0 in rankings  # preserved
    assert 1 in rankings  # new
    assert rankings[0]["primary_fragment"].strategy == "raa_a"
    assert rankings[1]["primary_fragment"].strategy == "raa_b"
