"""
Unit tests for conflict resolution node (Story 3.3).
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from raa.nodes.conflict_resolution import (
    HumanOverrideInstructions,
    EntityModification,
    RelationshipModification,
    _normalize_answers,
    _map_answers_to_questions,
    _apply_answer_overrides,
    _apply_structural_modifications,
    _parse_human_override,
    conflict_resolution,
)
from raa.state.models import OpenQuestion


# ── Helpers ─────────────────────────────────────────────────────────────────


def _make_state(human_answers=None, open_questions=None, arch_model=None, review_mode="interactive"):
    return {
        "batch_cursor": 0,
        "quality_weights": {},
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "review_mode": review_mode,
        "normalized_asrs": [],
        "normalized_non_asr": [],
        "embeddings_ready": False,
        "batch_outputs": [],
        "open_questions": open_questions or [],
        "incoherent_batches": [],
        "arch_model": arch_model or {},
        "judge_rankings": {},
        "human_answers": human_answers or {},
        "human_review_payload": {},
    }


# ── Answer Normalization ────────────────────────────────────────────────────


class TestNormalizeAnswers:
    def test_flat_dict(self):
        result = _normalize_answers({"q_0": "approve", "q_1": "reject"})
        assert result == {"q_0": "approve", "q_1": "reject"}

    def test_list_style(self):
        result = _normalize_answers({
            "answers": [
                {"question_id": "q_0", "answer": "approved"},
                {"question_id": "q_1", "answer": "rejected"},
            ]
        })
        assert result == {"q_0": "approved", "q_1": "rejected"}

    def test_nested_dict_style(self):
        result = _normalize_answers({"answers": {"q_0": "yes", "q_1": "no"}})
        assert result == {"q_0": "yes", "q_1": "no"}

    def test_none_returns_empty(self):
        assert _normalize_answers(None) == {}

    def test_empty_dict_returns_empty(self):
        assert _normalize_answers({}) == {}

    def test_list_item_missing_question_id_skipped(self):
        result = _normalize_answers({
            "answers": [
                {"answer": "no_id"},
                {"question_id": "q_1", "answer": "valid"},
            ]
        })
        assert result == {"q_1": "valid"}


# ── Answer Mapping ──────────────────────────────────────────────────────────


class TestMapAnswersToQuestions:
    def test_maps_answer_to_matching_question(self):
        questions = [
            {"id": "q_0", "question_type": "change_risk", "description": "Risk"},
        ]
        updated, resolved = _map_answers_to_questions({"q_0": "Resolved"}, questions)
        assert updated[0]["resolution"] == "Resolved"
        assert updated[0]["assumption_flag"] is False

    def test_no_match_leaves_unchanged(self):
        questions = [
            {"id": "q_0", "question_type": "change_risk", "description": "Risk"},
        ]
        updated, resolved = _map_answers_to_questions({"q_999": "No match"}, questions)
        assert "resolution" not in updated[0] or updated[0].get("resolution") is None

    def test_collects_entity_ids_from_matched_questions(self):
        questions = [
            {
                "id": "q_0",
                "question_type": "change_risk",
                "description": "Risk",
                "entity_a_id": "svc-a",
                "entity_b_id": "svc-b",
            },
        ]
        updated, resolved = _map_answers_to_questions({"q_0": "OK"}, questions)
        assert "svc-a" in resolved
        assert "svc-b" in resolved

    def test_collects_entity_ids_from_context(self):
        questions = [
            {
                "id": "q_0",
                "question_type": "change_risk",
                "description": "Risk",
                "context": {"entity_id": "ctx-svc", "promoted_component_id": "cc_sec"},
            },
        ]
        updated, resolved = _map_answers_to_questions({"q_0": "OK"}, questions)
        assert "ctx-svc" in resolved
        assert "cc_sec" in resolved

    def test_multiple_questions(self):
        questions = [
            {"id": "q_0", "question_type": "change_risk", "description": "R1", "entity_a_id": "e1"},
            {"id": "q_1", "question_type": "tie", "description": "T1", "entity_b_id": "e2"},
            {"id": "q_2", "question_type": "contention", "description": "C1", "entity_a_id": "e3"},
        ]
        updated, resolved = _map_answers_to_questions(
            {"q_0": "A", "q_1": "B"}, questions
        )
        assert updated[0]["resolution"] == "A"
        assert updated[1]["resolution"] == "B"
        assert "e1" in resolved
        assert "e2" in resolved
        assert "e3" not in resolved  # q_2 not matched


# ── Arch Model Overrides ────────────────────────────────────────────────────


class TestApplyAnswerOverrides:
    def test_resets_assumption_flags_on_resolved_entities(self):
        model = {
            "entities": [
                {"id": "e1", "name": "E1", "metadata": {"assumption_flag": True, "assumed": True}},
                {"id": "e2", "name": "E2", "metadata": {"assumption_flag": True}},
            ],
            "relationships": [],
            "assumption_flags": ["e1", "e2", "e3"],
        }
        result = _apply_answer_overrides(model, {"e1"})
        assert result["entities"][0]["metadata"]["assumption_flag"] is False
        assert result["entities"][0]["metadata"]["assumed"] is False
        # e2 unchanged
        assert result["entities"][1]["metadata"]["assumption_flag"] is True
        # assumption_flags list cleaned
        assert "e1" not in result["assumption_flags"]
        assert "e2" in result["assumption_flags"]
        assert "e3" in result["assumption_flags"]

    def test_no_resolved_ids_preserves_all(self):
        model = {
            "entities": [
                {"id": "e1", "name": "E1", "metadata": {"assumption_flag": True}},
            ],
            "relationships": [],
            "assumption_flags": ["e1"],
        }
        result = _apply_answer_overrides(model, set())
        assert result["entities"][0]["metadata"]["assumption_flag"] is True
        assert "e1" in result["assumption_flags"]

    def test_preserves_other_model_keys(self):
        model = {
            "entities": [],
            "relationships": [],
            "boundary_groups": [{"group_id": "bg-1"}],
            "cross_cutting_candidates": ["security"],
            "assumption_flags": [],
        }
        result = _apply_answer_overrides(model, set())
        assert result["boundary_groups"] == [{"group_id": "bg-1"}]
        assert result["cross_cutting_candidates"] == ["security"]


# ── Structural Modifications ────────────────────────────────────────────────


class TestApplyStructuralModifications:
    def test_update_parent(self):
        model = {
            "entities": [
                {"id": "e1", "name": "E1", "c4_type": "component",
                 "parent_system_id": "old-sys", "parent_container_id": "old-ctr"},
            ],
            "relationships": [],
        }
        instructions = HumanOverrideInstructions(
            entity_modifications=[
                EntityModification(
                    entity_id="e1", action="update_parent",
                    new_parent_system_id="new-sys", new_parent_container_id="new-ctr",
                )
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert result["entities"][0]["parent_system_id"] == "new-sys"
        assert result["entities"][0]["parent_container_id"] == "new-ctr"

    def test_update_name(self):
        model = {"entities": [{"id": "e1", "name": "OldName"}], "relationships": []}
        instructions = HumanOverrideInstructions(
            entity_modifications=[
                EntityModification(entity_id="e1", action="update_name", new_name="NewName")
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert result["entities"][0]["name"] == "NewName"

    def test_merge_entities(self):
        model = {
            "entities": [
                {"id": "e1", "name": "Source", "requirement_ids": ["R1"]},
                {"id": "e2", "name": "Target", "requirement_ids": ["R2"]},
            ],
            "relationships": [],
        }
        instructions = HumanOverrideInstructions(
            entity_modifications=[
                EntityModification(entity_id="e1", action="merge", target_entity_id="e2")
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert len(result["entities"]) == 1
        assert result["entities"][0]["id"] == "e2"
        assert set(result["entities"][0]["requirement_ids"]) == {"R1", "R2"}

    def test_delete_entity(self):
        model = {
            "entities": [
                {"id": "e1", "name": "Keep"},
                {"id": "e2", "name": "Delete"},
            ],
            "relationships": [],
        }
        instructions = HumanOverrideInstructions(
            entity_modifications=[
                EntityModification(entity_id="e2", action="delete")
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert len(result["entities"]) == 1
        assert result["entities"][0]["id"] == "e1"

    def test_update_technology(self):
        model = {"entities": [{"id": "e1", "name": "E1", "technology": "Old"}], "relationships": []}
        instructions = HumanOverrideInstructions(
            entity_modifications=[
                EntityModification(entity_id="e1", action="update_technology", new_technology="Python")
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert result["entities"][0]["technology"] == "Python"

    def test_add_relationship(self):
        model = {"entities": [], "relationships": []}
        instructions = HumanOverrideInstructions(
            relationship_modifications=[
                RelationshipModification(
                    action="add", source_id="a", target_id="b", description="uses"
                )
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert len(result["relationships"]) == 1
        assert result["relationships"][0]["source_id"] == "a"
        assert result["relationships"][0]["target_id"] == "b"
        assert result["relationships"][0]["metadata"]["source"] == "human_override"

    def test_remove_relationship(self):
        model = {
            "entities": [],
            "relationships": [
                {"id": "r1", "source_id": "a", "target_id": "b"},
                {"id": "r2", "source_id": "c", "target_id": "d"},
            ],
        }
        instructions = HumanOverrideInstructions(
            relationship_modifications=[
                RelationshipModification(action="remove", relationship_id="r1")
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert len(result["relationships"]) == 1
        assert result["relationships"][0]["id"] == "r2"

    def test_update_endpoints(self):
        model = {
            "entities": [],
            "relationships": [{"id": "r1", "source_id": "a", "target_id": "b"}],
        }
        instructions = HumanOverrideInstructions(
            relationship_modifications=[
                RelationshipModification(
                    action="update_endpoints", relationship_id="r1",
                    new_source_id="x", new_target_id="y",
                )
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert result["relationships"][0]["source_id"] == "x"
        assert result["relationships"][0]["target_id"] == "y"

    def test_unknown_entity_id_skipped(self):
        model = {"entities": [{"id": "e1", "name": "E1"}], "relationships": []}
        instructions = HumanOverrideInstructions(
            entity_modifications=[
                EntityModification(entity_id="nonexistent", action="delete")
            ]
        )
        result = _apply_structural_modifications(model, instructions)
        assert len(result["entities"]) == 1


# ── LLM Interpreter ─────────────────────────────────────────────────────────


class TestParseHumanOverride:
    def test_empty_answer_returns_empty_instructions(self):
        result = _parse_human_override("", {}, None)
        assert result.entity_modifications == []
        assert result.relationship_modifications == []

    def test_no_config_returns_empty_instructions(self):
        result = _parse_human_override("Move auth to backend", {}, None)
        assert result.entity_modifications == []
        assert result.relationship_modifications == []

    def test_no_judge_llm_in_config_returns_empty(self):
        config = {"configurable": {}}
        result = _parse_human_override("Some instruction", {}, config)
        assert result.entity_modifications == []

    def test_judge_llm_called_with_prompt(self):
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = HumanOverrideInstructions(
            entity_modifications=[
                EntityModification(entity_id="e1", action="update_name", new_name="Renamed")
            ]
        )

        config = {"configurable": {"judge_llm": mock_llm}}

        with patch("raa.nodes.conflict_resolution.load_prompt") as mock_load:
            mock_load.return_value = "Rendered prompt"
            result = _parse_human_override("Rename e1 to Renamed", {"entities": []}, config)

        assert len(result.entity_modifications) == 1
        assert result.entity_modifications[0].entity_id == "e1"
        assert result.entity_modifications[0].action == "update_name"
        mock_load.assert_called_once()

    def test_llm_error_returns_empty_instructions(self):
        mock_llm = MagicMock()
        mock_llm.with_structured_output.side_effect = Exception("LLM failure")
        config = {"configurable": {"judge_llm": mock_llm}}

        with patch("raa.nodes.conflict_resolution.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            result = _parse_human_override("Do something", {}, config)

        assert result.entity_modifications == []
        assert result.relationship_modifications == []


# ── Full Node Integration ───────────────────────────────────────────────────


class TestConflictResolution:
    def test_applies_answers_and_updates_questions(self):
        state = _make_state(
            human_answers={"q_0_change_risk": "Human decision: approve"},
            open_questions=[
                {
                    "id": "q_0_change_risk",
                    "question_type": "change_risk",
                    "description": "Risk of merge",
                    "entity_a_id": "svc-1",
                    "resolution": "auto_suggestion",
                    "assumption_flag": True,
                },
            ],
            arch_model={
                "entities": [
                    {"id": "svc-1", "name": "Service 1", "c4_type": "container",
                     "metadata": {"assumption_flag": True}},
                ],
                "relationships": [],
                "assumption_flags": ["svc-1"],
            },
        )
        result = conflict_resolution(state)
        # Questions updated
        q = state["open_questions"][0]
        assert q["resolution"] == "Human decision: approve"
        assert q["assumption_flag"] is False
        # Arch model updated
        e = result["arch_model"]["entities"][0]
        assert e["metadata"]["assumption_flag"] is False
        assert "svc-1" not in result["arch_model"].get("assumption_flags", [])

    def test_no_human_answers_preserves_state(self):
        state = _make_state(
            human_answers={},
            open_questions=[
                {"id": "q_0", "question_type": "change_risk", "description": "Risk"},
            ],
            arch_model={
                "entities": [{"id": "e1", "name": "E1", "metadata": {"assumption_flag": True}}],
                "relationships": [],
                "assumption_flags": ["e1"],
            },
        )
        result = conflict_resolution(state)
        assert state["open_questions"][0].get("resolution") is None
        assert result["arch_model"]["entities"][0]["metadata"]["assumption_flag"] is True

    def test_multiple_answers_applied(self):
        state = _make_state(
            human_answers={
                "q_0_change_risk": "Resolved A",
                "q_1_tie": "Resolved B",
            },
            open_questions=[
                {"id": "q_0_change_risk", "question_type": "change_risk",
                 "description": "A", "entity_a_id": "e1"},
                {"id": "q_1_tie", "question_type": "tie",
                 "description": "B", "entity_b_id": "e2"},
            ],
            arch_model={
                "entities": [
                    {"id": "e1", "name": "E1", "metadata": {"assumption_flag": True}},
                    {"id": "e2", "name": "E2", "metadata": {"assumption_flag": True}},
                ],
                "relationships": [],
                "assumption_flags": ["e1", "e2"],
            },
        )
        result = conflict_resolution(state)
        assert state["open_questions"][0]["resolution"] == "Resolved A"
        assert state["open_questions"][1]["resolution"] == "Resolved B"
        assert result["arch_model"]["assumption_flags"] == []

    def test_preserves_unmatched_questions(self):
        state = _make_state(
            human_answers={"q_1": "Only for q1"},
            open_questions=[
                {"id": "q_0", "question_type": "change_risk", "description": "Q0"},
                {"id": "q_1", "question_type": "tie", "description": "Q1"},
            ],
        )
        result = conflict_resolution(state)
        assert len(state["open_questions"]) == 2

    def test_list_style_answers_work(self):
        state = _make_state(
            human_answers={
                "answers": [
                    {"question_id": "q_0", "answer": "Approved via list"},
                ]
            },
            open_questions=[
                {"id": "q_0", "question_type": "change_risk", "description": "Risk"},
            ],
        )
        result = conflict_resolution(state)
        assert state["open_questions"][0]["resolution"] == "Approved via list"


# ── Validation Fallback ─────────────────────────────────────────────────────


class TestValidationFallback:
    def test_structural_modifications_without_llm_still_process_answers(self):
        """Even without LLM, answer mapping and assumption flag clearing work."""
        state = _make_state(
            human_answers={"q_0_change_risk": "Approved"},
            open_questions=[
                {
                    "id": "q_0_change_risk",
                    "question_type": "change_risk",
                    "description": "Risk",
                    "entity_a_id": "svc-1",
                },
            ],
            arch_model={
                "entities": [
                    {"id": "svc-1", "name": "Service", "metadata": {"assumption_flag": True}},
                ],
                "relationships": [],
                "assumption_flags": ["svc-1"],
            },
        )
        result = conflict_resolution(state)
        assert state["open_questions"][0]["resolution"] == "Approved"
        assert result["arch_model"]["assumption_flags"] == []


# ── Custom Merge Reducer & ID Assignment ────────────────────────────────────


class TestMergeQuestionsReducer:
    def test_merge_questions_appends_new(self):
        from raa.state.schemas import merge_questions
        left = [{"id": "q1", "description": "Q1"}]
        right = [{"id": "q2", "description": "Q2"}]
        res = merge_questions(left, right)
        assert len(res) == 2
        assert res[0]["id"] == "q1"
        assert res[1]["id"] == "q2"

    def test_merge_questions_updates_existing(self):
        from raa.state.schemas import merge_questions
        left = [{"id": "q1", "description": "Q1", "resolution": None}]
        right = [{"id": "q1", "resolution": "approved"}]
        res = merge_questions(left, right)
        assert len(res) == 1
        assert res[0]["id"] == "q1"
        assert res[0]["description"] == "Q1"
        assert res[0]["resolution"] == "approved"

    def test_merge_questions_handles_none(self):
        from raa.state.schemas import merge_questions
        assert merge_questions(None, [{"id": "q1"}]) == [{"id": "q1"}]
        assert merge_questions([{"id": "q1"}], None) == [{"id": "q1"}]

    def test_mapping_assigns_missing_ids(self):
        questions = [
            {"question_type": "change_risk", "description": "Risk"},
        ]
        updated, resolved = _map_answers_to_questions({"q_0_change_risk": "Approved"}, questions)
        assert updated[0]["id"] == "q_0_change_risk"
        assert updated[0]["resolution"] == "Approved"


