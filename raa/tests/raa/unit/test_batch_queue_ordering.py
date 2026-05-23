"""
Unit tests for batch queue ordering node (FR-6).

Covers:
- Security/reliability batches sorted first
- asr_count alternative strategy
- quality_weight_frequency alternative strategy
- Deterministic tie-break by group_id
- Unprocessed requirement collection
- Unsupported strategy raises ValueError
"""
from __future__ import annotations

import pytest

from raa.nodes.batch_queue_ordering import order_batch_queue


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_config(**overrides):
    return {
        "configurable": {
            "thread_id": "test-thread-1",
            **overrides,
        }
    }


def _make_state(batches=None, normalized_asrs=None, normalized_non_asr=None,
                quality_weights=None):
    return {
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "quality_weights": quality_weights or {},
        "review_mode": "autonomous",
        "normalized_asrs": normalized_asrs or [],
        "normalized_non_asr": normalized_non_asr or [],
        "embeddings_ready": True,
        "batches": batches or [],
        "batch_outputs": [],
        "open_questions": [],
        "incoherent_batches": [],
        "batch_cursor": 0,
    }


def _make_batch(group_id, asr_records=None, non_asr_records=None,
                asr_ids=None, non_asr_ids=None):
    return {
        "group_id": group_id,
        "centroid": [0.0],
        "asr_ids": asr_ids or [],
        "asr_records": asr_records or [],
        "non_asr_ids": non_asr_ids or [],
        "non_asr_records": non_asr_records or [],
        "similarity_scores": {},
    }


# ── Tests ────────────────────────────────────────────────────────────────────


class TestQueueOrdering:

    def test_security_batches_first(self):
        """Batches containing security quality attributes sort before others."""
        state = _make_state(
            quality_weights={"security": 10, "performance": 5},
            batches=[
                _make_batch("g2", asr_records=[{"id": "R2", "quality_attributes": ["performance"]}]),
                _make_batch("g1", asr_records=[{"id": "R1", "quality_attributes": ["security"]}]),
            ],
        )

        result = order_batch_queue(state, _make_config())
        queue = result["execution_queue"]
        assert queue[0]["group_id"] == "g1"  # security first
        assert queue[1]["group_id"] == "g2"

    def test_reliability_batches_first(self):
        """Batches containing reliability sort with security before others."""
        state = _make_state(
            quality_weights={"reliability": 10, "usability": 1},
            batches=[
                _make_batch("g2", asr_records=[{"id": "R2", "quality_attributes": ["usability"]}]),
                _make_batch("g1", asr_records=[{"id": "R1", "quality_attributes": ["reliability"]}]),
            ],
        )

        result = order_batch_queue(state, _make_config())
        queue = result["execution_queue"]
        assert queue[0]["group_id"] == "g1"

    def test_higher_risk_sorts_before_lower_within_same_category(self):
        """Within same sec/rel category, higher weighted risk sorts first."""
        state = _make_state(
            quality_weights={"security": 10, "performance": 5},
            batches=[
                _make_batch("g_low", asr_records=[{"id": "R1", "quality_attributes": ["security"]}]),
                _make_batch("g_high", asr_records=[
                    {"id": "R2", "quality_attributes": ["security", "performance"]},
                ]),
            ],
        )

        result = order_batch_queue(state, _make_config())
        queue = result["execution_queue"]
        # g_high has more weighted risk → first
        assert queue[0]["group_id"] == "g_high"
        assert queue[1]["group_id"] == "g_low"

    def test_asr_count_strategy(self):
        """asr_count strategy sorts by descending ASR count first."""
        state = _make_state(
            quality_weights={},
            batches=[
                _make_batch("g_small", asr_ids=["R1"]),
                _make_batch("g_large", asr_ids=["R1", "R2", "R3"]),
            ],
        )

        result = order_batch_queue(state, _make_config(queue_sort_strategy="asr_count"))
        queue = result["execution_queue"]
        assert queue[0]["group_id"] == "g_large"
        assert queue[1]["group_id"] == "g_small"

    def test_quality_weight_frequency_strategy(self):
        """quality_weight_frequency sorts by descending total weighted frequency."""
        state = _make_state(
            quality_weights={"perf": 3, "sec": 10},
            batches=[
                _make_batch("g_low", asr_records=[
                    {"id": "R1", "quality_attributes": ["perf"]},
                ]),
                _make_batch("g_high", asr_records=[
                    {"id": "R2", "quality_attributes": ["sec"]},
                ]),
            ],
        )

        result = order_batch_queue(state, _make_config(queue_sort_strategy="quality_weight_frequency"))
        queue = result["execution_queue"]
        assert queue[0]["group_id"] == "g_high"
        assert queue[1]["group_id"] == "g_low"

    def test_deterministic_tie_break_by_group_id(self):
        """When all scores equal, batches are ordered by ascending group_id."""
        state = _make_state(
            batches=[
                _make_batch("cluster_2_group_0"),
                _make_batch("cluster_0_group_0"),
                _make_batch("cluster_1_group_0"),
            ],
        )

        result = order_batch_queue(state, _make_config())
        queue = result["execution_queue"]
        ids = [b["group_id"] for b in queue]
        assert ids == sorted(ids)

    def test_unprocessed_requirements_collected(self):
        """Requirements not in any batch appear as unprocessed_requirements."""
        state = _make_state(
            batches=[
                _make_batch("g1", asr_ids=["R1"], asr_records=[{"id": "R1"}]),
            ],
            normalized_asrs=[
                {"id": "R1", "description": "in batch"},
                {"id": "R2", "description": "leftover"},
            ],
            normalized_non_asr=[
                {"id": "RN1", "description": "also leftover"},
            ],
        )

        result = order_batch_queue(state, _make_config())
        leftovers = result["unprocessed_requirements"]
        leftover_ids = {r["id"] for r in leftovers}
        assert "R2" in leftover_ids
        assert "RN1" in leftover_ids
        assert "R1" not in leftover_ids

    def test_unsupported_strategy_raises(self):
        state = _make_state()
        with pytest.raises(ValueError, match="Unsupported queue sort strategy"):
            order_batch_queue(state, _make_config(queue_sort_strategy="bogus"))

    def test_default_strategy_is_risk(self):
        """Default strategy is 'risk' when not specified."""
        state = _make_state(
            quality_weights={"security": 10},
            batches=[
                _make_batch("g2"),
                _make_batch("g1", asr_records=[{"id": "R1", "quality_attributes": ["security"]}]),
            ],
        )

        result = order_batch_queue(state, _make_config())
        queue = result["execution_queue"]
        assert queue[0]["group_id"] == "g1"

    def test_fallback_weight_for_unknown_attributes(self):
        """Attributes not in quality_weights get fallback weight 1."""
        state = _make_state(
            quality_weights={},  # no known weights
            batches=[
                _make_batch("g2", asr_records=[{"id": "R2", "quality_attributes": ["rare_attr"]}]),
                _make_batch("g1", asr_records=[
                    {"id": "R1", "quality_attributes": ["rare_attr", "also_rare"]},
                ]),
            ],
        )

        result = order_batch_queue(state, _make_config())
        queue = result["execution_queue"]
        # g1 has 2 attributes → fallback weight 1 each → score 2 > score 1 → first
        assert queue[0]["group_id"] == "g1"

    def test_empty_batches_returns_empty_queue(self):
        state = _make_state(batches=[])
        result = order_batch_queue(state, _make_config())
        assert result["execution_queue"] == []
        assert result["unprocessed_requirements"] == []

    def test_non_asr_records_included_in_risk_scoring(self):
        """non_asr_records quality attributes also contribute to risk scoring."""
        state = _make_state(
            quality_weights={"security": 10},
            batches=[
                _make_batch("g_no_risk"),
                _make_batch("g_risk", non_asr_records=[
                    {"id": "RN1", "quality_attributes": ["security"]},
                ]),
            ],
        )

        result = order_batch_queue(state, _make_config())
        queue = result["execution_queue"]
        assert queue[0]["group_id"] == "g_risk"

    def test_none_configurable_handled_gracefully(self):
        """None value for configurable is handled gracefully."""
        state = _make_state(batches=[])
        result = order_batch_queue(state, {"configurable": None})
        assert result["execution_queue"] == []

