"""
Unit tests for SAAM score calibration engine (Story 2.5).
"""
from __future__ import annotations

import pytest

from raa.judge.saam_calibration import calibrate_entity_saam_scores
from raa.utils.constants import (
    SAAM_BASE_SCORE,
    SAAM_BOUNDARY_GROUP_PENALTY,
    SAAM_DEDUP_PENALTY,
    SAAM_PERFECT_SCORE,
)


# ── Helpers ─────────────────────────────────────────────────────────────────


def _entity_dict(
    id="entity-1",
    name="Test",
    description="Test",
    c4_type="container",
    requirement_ids=None,
    metadata=None,
):
    return {
        "id": id,
        "name": name,
        "description": description,
        "c4_type": c4_type,
        "technology": "",
        "parent_system_id": None,
        "parent_container_id": None,
        "requirement_ids": requirement_ids or [],
        "saam_score": 0.0,
        "metadata": metadata or {},
    }


def _scenario(satisfaction="satisfied", requirement_ids=None):
    return {
        "id": "scenario-1",
        "description": "Test scenario",
        "quality_attributes": ["Performance Efficiency"],
        "satisfaction": satisfaction,
        "requirement_ids": requirement_ids or [],
        "metadata": {},
    }


# ── Base Score ──────────────────────────────────────────────────────────────


class TestBaseScore:
    def test_base_score_applied_to_non_component_entity(self):
        model = {"entities": [_entity_dict(c4_type="container")]}
        result = calibrate_entity_saam_scores(model)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE

    def test_base_score_applied_to_system_entity(self):
        model = {"entities": [_entity_dict(c4_type="system")]}
        result = calibrate_entity_saam_scores(model)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE

    def test_base_score_applied_when_no_scenarios(self):
        model = {"entities": [_entity_dict(c4_type="component", requirement_ids=["R1"])]}
        result = calibrate_entity_saam_scores(model, saam_scenarios=[])
        # No scenarios means not qualified for perfect → gets base score
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE


# ── Perfect Score ───────────────────────────────────────────────────────────


class TestPerfectScore:
    def test_perfect_score_for_qualifying_component(self):
        model = {
            "entities": [
                _entity_dict(
                    id="comp-1",
                    c4_type="component",
                    requirement_ids=["R1", "R2"],
                )
            ]
        }
        scenarios = [
            _scenario(satisfaction="satisfied", requirement_ids=["R1"]),
            _scenario(satisfaction="satisfied", requirement_ids=["R2"]),
        ]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        assert result["entities"][0]["saam_score"] == SAAM_PERFECT_SCORE

    def test_not_perfect_when_requirements_shared_in_boundary_group(self):
        """Entities in same boundary group with shared requirement IDs can't both be perfect."""
        model = {
            "entities": [
                _entity_dict(
                    id="comp-1",
                    c4_type="component",
                    requirement_ids=["R1", "R2"],
                    metadata={"boundary_group_id": "bg-1"},
                ),
                _entity_dict(
                    id="comp-2",
                    c4_type="component",
                    requirement_ids=["R2", "R3"],
                    metadata={"boundary_group_id": "bg-1"},
                ),
            ]
        }
        scenarios = [
            _scenario(satisfaction="satisfied", requirement_ids=["R1", "R2", "R3"]),
        ]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        assert result["entities"][0]["saam_score"] != SAAM_PERFECT_SCORE
        assert result["entities"][1]["saam_score"] != SAAM_PERFECT_SCORE

    def test_not_perfect_when_scenario_unsatisfied(self):
        model = {
            "entities": [
                _entity_dict(
                    id="comp-1",
                    c4_type="component",
                    requirement_ids=["R1"],
                )
            ]
        }
        scenarios = [
            _scenario(satisfaction="partial", requirement_ids=["R1"]),
        ]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        assert result["entities"][0]["saam_score"] != SAAM_PERFECT_SCORE

    def test_not_perfect_for_non_component(self):
        model = {
            "entities": [
                _entity_dict(
                    id="cont-1",
                    c4_type="container",
                    requirement_ids=["R1"],
                )
            ]
        }
        scenarios = [
            _scenario(satisfaction="satisfied", requirement_ids=["R1"]),
        ]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE

    def test_not_perfect_when_no_requirement_ids(self):
        model = {
            "entities": [
                _entity_dict(id="comp-1", c4_type="component", requirement_ids=[]),
            ]
        }
        result = calibrate_entity_saam_scores(model)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE


# ── Dedup Penalty ───────────────────────────────────────────────────────────


class TestDedupPenalty:
    def test_dedup_penalty_reduces_score(self):
        model = {"entities": [_entity_dict(id="merged-1")]}
        merge_log = [
            {
                "merged_entity_id": "merged-1",
                "source_entity_ids": ["entity-a", "entity-b"],
                "merge_type": "similarity",
            }
        ]
        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
        expected = SAAM_BASE_SCORE - SAAM_DEDUP_PENALTY
        assert result["entities"][0]["saam_score"] == round(expected, 4)

    def test_multiple_merges_stack_penalty(self):
        model = {"entities": [_entity_dict(id="multi-merged")]}
        merge_log = [
            {
                "merged_entity_id": "multi-merged",
                "source_entity_ids": ["e1", "e2"],
                "merge_type": "exact_id",
            },
            {
                "merged_entity_id": "multi-merged",
                "source_entity_ids": ["multi-merged", "e3"],
                "merge_type": "similarity",
            },
        ]
        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
        expected = SAAM_BASE_SCORE - (SAAM_DEDUP_PENALTY * 2)
        assert result["entities"][0]["saam_score"] == round(expected, 4)

    def test_source_entity_ids_count_as_merge_event(self):
        """Entity appearing in source_entity_ids also counts as merge participation."""
        model = {"entities": [_entity_dict(id="source-e1")]}
        merge_log = [
            {
                "merged_entity_id": "other",
                "source_entity_ids": ["source-e1", "e2"],
                "merge_type": "similarity",
            }
        ]
        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
        expected = SAAM_BASE_SCORE - SAAM_DEDUP_PENALTY
        assert result["entities"][0]["saam_score"] == round(expected, 4)

    def test_no_penalty_without_merge_log(self):
        model = {"entities": [_entity_dict(id="clean")]}
        result = calibrate_entity_saam_scores(model, merge_log=[])
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE


# ── Boundary Group Penalty ──────────────────────────────────────────────────


class TestBoundaryGroupPenalty:
    def test_boundary_group_penalty_reduces_score(self):
        model = {
            "entities": [_entity_dict(id="bg-entity")],
        }
        boundary_groups = [
            {"group_id": "bg-1", "entity_ids": ["bg-entity", "other"], "similarity": 0.7}
        ]
        result = calibrate_entity_saam_scores(model, boundary_groups=boundary_groups)
        expected = SAAM_BASE_SCORE - SAAM_BOUNDARY_GROUP_PENALTY
        assert result["entities"][0]["saam_score"] == round(expected, 4)

    def test_no_penalty_for_non_member(self):
        model = {
            "entities": [_entity_dict(id="loner")],
        }
        boundary_groups = [
            {"group_id": "bg-1", "entity_ids": ["other-1", "other-2"], "similarity": 0.7}
        ]
        result = calibrate_entity_saam_scores(model, boundary_groups=boundary_groups)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE

    def test_uses_model_boundary_groups_by_default(self):
        model = {
            "entities": [_entity_dict(id="bg-entity")],
            "boundary_groups": [
                {"group_id": "bg-1", "entity_ids": ["bg-entity", "other"], "similarity": 0.7}
            ],
        }
        result = calibrate_entity_saam_scores(model)
        expected = SAAM_BASE_SCORE - SAAM_BOUNDARY_GROUP_PENALTY
        assert result["entities"][0]["saam_score"] == round(expected, 4)


# ── Combined Penalties ──────────────────────────────────────────────────────


class TestCombinedPenalties:
    def test_both_penalties_apply(self):
        model = {
            "entities": [_entity_dict(id="penalized")],
        }
        boundary_groups = [
            {"group_id": "bg-1", "entity_ids": ["penalized", "other"], "similarity": 0.7}
        ]
        merge_log = [
            {
                "merged_entity_id": "penalized",
                "source_entity_ids": ["penalized", "e1"],
                "merge_type": "similarity",
            }
        ]
        result = calibrate_entity_saam_scores(
            model, boundary_groups=boundary_groups, merge_log=merge_log
        )
        expected = SAAM_BASE_SCORE - SAAM_DEDUP_PENALTY - SAAM_BOUNDARY_GROUP_PENALTY
        assert result["entities"][0]["saam_score"] == round(expected, 4)


# ── Score Clamping ──────────────────────────────────────────────────────────


class TestScoreClamping:
    def test_score_clamped_to_zero(self):
        model = {"entities": [_entity_dict(id="overpenalized")]}
        # Stack enough penalties to go below 0
        merge_log = [
            {"merged_entity_id": "overpenalized", "source_entity_ids": ["overpenalized", f"e{i}"], "merge_type": "similarity"}
            for i in range(10)
        ]
        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
        assert result["entities"][0]["saam_score"] == 0.0

    def test_score_clamped_to_one(self):
        model = {
            "entities": [
                _entity_dict(id="comp", c4_type="component", requirement_ids=["R1"]),
            ]
        }
        scenarios = [_scenario(satisfaction="satisfied", requirement_ids=["R1"])]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        assert result["entities"][0]["saam_score"] == SAAM_PERFECT_SCORE


# ── Empty/Edge Cases ────────────────────────────────────────────────────────


class TestEdgeCases:
    def test_empty_model_returns_empty_model(self):
        model = {"entities": []}
        result = calibrate_entity_saam_scores(model)
        assert result["entities"] == []

    def test_all_defaults_handled(self):
        """Call with no optional args should work."""
        model = {"entities": [_entity_dict()]}
        result = calibrate_entity_saam_scores(model)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE

    def test_preserves_non_entity_keys(self):
        model = {
            "entities": [_entity_dict()],
            "boundary_groups": [{"group_id": "bg-1", "entity_ids": ["a", "b"]}],
            "cross_cutting_candidates": ["security"],
        }
        result = calibrate_entity_saam_scores(model)
        assert "boundary_groups" in result
        assert "cross_cutting_candidates" in result

    def test_multiple_entities_scored(self):
        model = {
            "entities": [
                _entity_dict(id="e1", c4_type="component", requirement_ids=["R1"]),
                _entity_dict(id="e2", c4_type="container"),
                _entity_dict(id="e3", c4_type="system"),
            ]
        }
        scenarios = [_scenario(satisfaction="satisfied", requirement_ids=["R1"])]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        scores = {e["id"]: e["saam_score"] for e in result["entities"]}
        assert scores["e1"] == SAAM_PERFECT_SCORE
        assert scores["e2"] == SAAM_BASE_SCORE
        assert scores["e3"] == SAAM_BASE_SCORE

    def test_deterministic_same_input_same_output(self):
        model = {
            "entities": [
                _entity_dict(id="e1", c4_type="component", requirement_ids=["R1"]),
                _entity_dict(id="e2"),
            ]
        }
        scenarios = [_scenario(satisfaction="satisfied", requirement_ids=["R1"])]
        merge_log = [
            {"merged_entity_id": "e2", "source_entity_ids": ["e2", "e_old"], "merge_type": "exact_id"}
        ]
        r1 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
        r2 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
        assert r1 == r2

    def test_scenario_with_unknown_satisfaction_not_perfect(self):
        model = {
            "entities": [
                _entity_dict(id="comp", c4_type="component", requirement_ids=["R1"]),
            ]
        }
        scenarios = [_scenario(satisfaction="unknown", requirement_ids=["R1"])]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE

    def test_scenario_with_unsatisfied_not_perfect(self):
        model = {
            "entities": [
                _entity_dict(id="comp", c4_type="component", requirement_ids=["R1"]),
            ]
        }
        scenarios = [_scenario(satisfaction="unsatisfied", requirement_ids=["R1"])]
        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE

    def test_deterministic(self):
        """Same input → same output (dedicated determinism test)."""
        model = {
            "entities": [
                _entity_dict(id="e1", c4_type="component", requirement_ids=["R1"]),
                _entity_dict(id="e2", c4_type="container", requirement_ids=["R2"]),
            ],
            "boundary_groups": [
                {"group_id": "bg-1", "entity_ids": ["e1", "e2"], "similarity": 0.7}
            ],
        }
        scenarios = [
            _scenario(satisfaction="satisfied", requirement_ids=["R1"]),
            _scenario(satisfaction="partial", requirement_ids=["R2"]),
        ]
        merge_log = [
            {"merged_entity_id": "e1", "source_entity_ids": ["e1", "e_old"], "merge_type": "exact_id"}
        ]
        r1 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
        r2 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
        assert r1 == r2

    def test_recursive_transitive_merge_count(self):
        """Transitive sources folded into final entity should inherit stacked dedup penalties."""
        model = {"entities": [_entity_dict(id="e1")]}
        # e2 merged with e3 -> producing e2
        # e1 merged with e2 -> producing e1
        merge_log = [
            {"merged_entity_id": "e2", "source_entity_ids": ["e2", "e3"], "merge_type": "exact_id"},
            {"merged_entity_id": "e1", "source_entity_ids": ["e1", "e2"], "merge_type": "exact_id"},
        ]
        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
        expected = SAAM_BASE_SCORE - (SAAM_DEDUP_PENALTY * 2)
        assert result["entities"][0]["saam_score"] == round(expected, 4)

    def test_perfect_score_overlap_using_boundary_groups_list(self):
        """Should check overlap using the boundary_groups list directly, not just entity metadata."""
        model = {
            "entities": [
                _entity_dict(id="comp-1", c4_type="component", requirement_ids=["R1"]),
                _entity_dict(id="comp-2", c4_type="component", requirement_ids=["R1"]),
            ]
        }
        boundary_groups = [
            {"group_id": "bg-1", "entity_ids": ["comp-1", "comp-2"]}
        ]
        scenarios = [_scenario(satisfaction="satisfied", requirement_ids=["R1"])]
        result = calibrate_entity_saam_scores(model, boundary_groups=boundary_groups, saam_scenarios=scenarios)
        # Should not get perfect score because they are in the same boundary group and share requirement ID
        assert result["entities"][0]["saam_score"] != SAAM_PERFECT_SCORE
        assert result["entities"][1]["saam_score"] != SAAM_PERFECT_SCORE

