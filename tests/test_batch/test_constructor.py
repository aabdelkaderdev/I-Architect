"""Tests for BatchConstructor. Per FG-Phase-44 §2."""

from __future__ import annotations

import pytest

from raa.batch.constructor import BatchConstructor


class TestBatchConstructor:
    def test_build_concern_batches(self, empty_registry):
        """Concern batches are built from condition groups where cluster != -1."""
        constructor = BatchConstructor()
        raa_input = {
            "condition_groups": [
                {
                    "cluster": 1,
                    "nominal_condition": "high traffic",
                    "requirements": [],
                },
            ],
            "concerns": [],
            "non_asr": [],
            "quality_weights": {"Performance Efficiency": 40},
        }
        assignments: list = []
        batches = constructor.build_batches(raa_input, assignments, empty_registry)
        # Should have 1 concern batch + 1 foundation batch
        assert len(batches) >= 1

    def test_build_foundation_batch(self, empty_registry):
        """Foundation batch is always the last batch, even with no concerns."""
        constructor = BatchConstructor()
        raa_input = {
            "condition_groups": [],
            "concerns": [],
            "non_asr": [],
            "quality_weights": {},
        }
        assignments: list = []
        batches = constructor.build_batches(raa_input, assignments, empty_registry)
        assert len(batches) == 1
        assert batches[0]["batch_type"] == "foundation"

    def test_batch_ordering(self, empty_registry):
        """Concern batches precede the foundation batch."""
        constructor = BatchConstructor()
        raa_input = {
            "condition_groups": [
                {"cluster": 2, "nominal_condition": "condition B", "requirements": []},
                {"cluster": 1, "nominal_condition": "condition A", "requirements": []},
            ],
            "concerns": [],
            "non_asr": [],
            "quality_weights": {},
        }
        assignments: list = []
        batches = constructor.build_batches(raa_input, assignments, empty_registry)
        types = [b["batch_type"] for b in batches]
        # Foundation batch last
        assert types[-1] == "foundation"
        # All concern batches come before foundation
        for bt in types[:-1]:
            assert bt == "concern"

    def test_empty_condition_groups(self, empty_registry):
        """Empty condition groups produce only a foundation batch."""
        constructor = BatchConstructor()
        raa_input = {
            "condition_groups": [],
            "concerns": [],
            "non_asr": [],
            "quality_weights": {},
        }
        assignments: list = []
        batches = constructor.build_batches(raa_input, assignments, empty_registry)
        assert len(batches) == 1
        assert batches[0]["batch_type"] == "foundation"

    def test_duplicate_clusters_get_unique_batch_ids(self, empty_registry):
        """Cluster is metadata; duplicate clusters must not duplicate batch IDs."""
        constructor = BatchConstructor()
        raa_input = {
            "condition_groups": [
                {"cluster": 0, "nominal_condition": "condition A", "requirements": []},
                {"cluster": 0, "nominal_condition": "condition B", "requirements": []},
                {"cluster": 0, "nominal_condition": "condition C", "requirements": []},
            ],
            "concerns": [],
            "non_asr": [],
            "quality_weights": {},
        }

        batches = constructor.build_batches(raa_input, [], empty_registry)

        assert [b["batch_id"] for b in batches] == [
            "concern_batch_1",
            "concern_batch_2",
            "concern_batch_3",
            "foundation_batch",
        ]

    def test_duplicate_cluster_decisions_are_not_dropped(self, empty_registry):
        """All concerns matching a duplicate cluster remain available to each batch."""
        constructor = BatchConstructor()
        raa_input = {
            "condition_groups": [
                {"cluster": 0, "nominal_condition": "condition A", "requirements": []},
                {"cluster": 0, "nominal_condition": "condition B", "requirements": []},
            ],
            "concerns": [
                {"ccg_id": 0, "decisions": [{"selected_pattern": "Microservices"}]},
                {"ccg_id": 0, "decisions": [{"selected_pattern": "Offline First"}]},
            ],
            "non_asr": [],
            "quality_weights": {},
        }

        batches = constructor.build_batches(raa_input, [], empty_registry)

        for batch in batches[:2]:
            assert batch["decisions"] == [
                {"selected_pattern": "Microservices"},
                {"selected_pattern": "Offline First"},
            ]
