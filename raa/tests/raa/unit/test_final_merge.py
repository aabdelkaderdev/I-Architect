"""
Unit tests for final merge node (Story 4.1).
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from raa.nodes.final_merge import (
    DocumentedAssumption,
    _collect_entity_ids,
    _generate_assumption,
    _get_default_suggestion,
    _get_resolution_owner,
    _global_merge,
    _init_embeddings,
    _normalize_merge_questions,
    _resolve_all_questions,
    final_merge,
)
from raa.state.models import C4Entity, C4Relationship


# ── Helpers ─────────────────────────────────────────────────────────────────


def _make_state(
    batch_outputs=None,
    arch_model=None,
    open_questions=None,
    human_answers=None,
    review_mode="interactive",
):
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
        "batch_outputs": batch_outputs or [],
        "open_questions": open_questions or [],
        "incoherent_batches": [],
        "arch_model": arch_model or {},
        "judge_rankings": {},
        "human_answers": human_answers or {},
        "human_review_payload": {},
    }


def _entity_dict(**overrides):
    defaults = {
        "id": "svc-1",
        "name": "Service 1",
        "description": "A backend service for user management",
        "c4_type": "container",
        "technology": "Python",
        "requirement_ids": ["R1"],
    }
    defaults.update(overrides)
    return defaults


def _rel_dict(**overrides):
    defaults = {
        "id": "rel-1",
        "source_id": "svc-1",
        "target_id": "svc-2",
        "description": "uses",
        "relationship_type": "uses",
    }
    defaults.update(overrides)
    return defaults


# ── Embedding Init ──────────────────────────────────────────────────────────


class TestInitEmbeddings:
    def test_returns_none_when_model_unavailable(self):
        with patch(
            "raa.nodes.final_merge.EmbeddingCache",
            side_effect=Exception("no model"),
        ):
            cache, model = _init_embeddings()
            assert cache is None
            assert model is None


# ── Merge Question Normalization ────────────────────────────────────────────


class TestNormalizeMergeQuestions:
    def test_orphan_container_converted(self):
        questions = [{"reason": "orphan_container", "entity_id": "e1"}]
        result = _normalize_merge_questions(questions)
        assert result[0]["question_type"] == "hierarchy_conflict"
        assert result[0]["resolution_owner"] == "judge_resolvable"
        assert result[0]["resolution"] is not None
        assert result[0]["assumption_flag"] is False

    def test_orphan_component_converted(self):
        questions = [{"reason": "orphan_component", "entity_id": "e1"}]
        result = _normalize_merge_questions(questions)
        assert result[0]["question_type"] == "hierarchy_conflict"
        assert result[0]["resolution_owner"] == "judge_resolvable"

    def test_unresolved_relationship_endpoint_converted(self):
        questions = [{"reason": "unresolved_relationship_endpoint", "relationship_id": "r1"}]
        result = _normalize_merge_questions(questions)
        assert result[0]["question_type"] == "hierarchy_conflict"

    def test_mismatching_parent_description_converted(self):
        questions = [{
            "question_type": "change_risk",
            "description": "Merged entities 'A' and 'B' have mismatching C4 parent hierarchy: parent_system_id ('sys-a' vs 'sys-b')",
        }]
        result = _normalize_merge_questions(questions)
        assert result[0]["question_type"] == "hierarchy_conflict"
        assert result[0]["resolution_owner"] == "judge_resolvable"

    def test_non_hierarchy_questions_unchanged(self):
        questions = [{
            "question_type": "change_risk",
            "description": "Entities have moderate semantic similarity",
            "reason": "boundary_group",
        }]
        result = _normalize_merge_questions(questions)
        assert result[0]["question_type"] == "change_risk"

    def test_empty_list(self):
        assert _normalize_merge_questions([]) == []


# ── Resolution Owner ────────────────────────────────────────────────────────


class TestGetResolutionOwner:
    def test_uses_explicit_field(self):
        q = {"resolution_owner": "human_preferred"}
        assert _get_resolution_owner(q) == "human_preferred"

    def test_falls_back_to_classification(self):
        q = {"question_type": "tie"}
        assert _get_resolution_owner(q) == "judge_resolvable"

    def test_unknown_type_defaults_to_human_preferred(self):
        q = {"question_type": "bogus"}
        assert _get_resolution_owner(q) == "human_preferred"

    def test_uses_type_key_as_fallback(self):
        q = {"type": "contention"}
        assert _get_resolution_owner(q) == "judge_resolvable"


# ── Default Suggestion ──────────────────────────────────────────────────────


class TestGetDefaultSuggestion:
    def test_hierarchy_conflict(self):
        q = {"question_type": "hierarchy_conflict"}
        assert "parent hierarchy" in _get_default_suggestion(q).lower()

    def test_scope_conflict(self):
        q = {"question_type": "scope_conflict"}
        assert "fallback" in _get_default_suggestion(q).lower()

    def test_unknown_type_gets_generic(self):
        q = {"question_type": "bogus"}
        result = _get_default_suggestion(q)
        assert "primary strategy" in result


# ── Collect Entity IDs ──────────────────────────────────────────────────────


class TestCollectEntityIds:
    def test_root_level_ids(self):
        q = {"entity_a_id": "e1", "entity_b_id": "e2"}
        ids = _collect_entity_ids(q)
        assert ids == {"e1", "e2"}

    def test_context_ids(self):
        q = {"context": {"entity_id": "e3", "promoted_component_id": "cc_1"}}
        ids = _collect_entity_ids(q)
        assert ids == {"e3", "cc_1"}

    def test_combined_root_and_context(self):
        q = {"entity_a_id": "e1", "context": {"entity_id": "e3"}}
        ids = _collect_entity_ids(q)
        assert ids == {"e1", "e3"}

    def test_skips_non_string_values(self):
        q = {"entity_a_id": 42, "context": {"entity_id": None}}
        ids = _collect_entity_ids(q)
        assert ids == set()


# ── Generate Assumption ─────────────────────────────────────────────────────


class TestGenerateAssumption:
    def test_fallback_template_no_config(self):
        q = {"question_type": "change_risk", "description": "Risk of coupling"}
        result = _generate_assumption(q, {}, {}, None)
        assert "Assumed default resolution" in result
        assert "change_risk" in result
        assert "Risk of coupling" in result

    def test_fallback_template_no_judge_llm(self):
        q = {"question_type": "high_coupling", "description": "High coupling risk"}
        config = {"configurable": {}}
        result = _generate_assumption(q, {}, {}, config)
        assert "Assumed default resolution" in result
        assert "high_coupling" in result

    def test_llm_assumption_when_judge_available(self):
        q = {"question_type": "change_risk", "description": "A risky merge"}
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = DocumentedAssumption(
            assumption="The merge is safe because requirements are orthogonal.",
            rationale="Requirements target different subsystems.",
        )
        config = {"configurable": {"judge_llm": mock_llm}}

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "Rendered prompt"
            result = _generate_assumption(q, {}, {}, config)

        assert "The merge is safe" in result
        assert "Rationale:" in result
        assert "requirements are orthogonal" in result

    def test_llm_error_falls_back_to_template(self):
        q = {"question_type": "coverage_gap", "description": "Missing coverage"}
        mock_llm = MagicMock()
        mock_llm.with_structured_output.side_effect = Exception("boom")
        config = {"configurable": {"judge_llm": mock_llm}}

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            result = _generate_assumption(q, {}, {}, config)

        assert "Assumed default resolution" in result

    def test_truncates_long_description_in_fallback(self):
        q = {"question_type": "change_risk", "description": "X" * 500}
        result = _generate_assumption(q, {}, {}, None)
        assert len(result) < 800  # should be truncated


# ── Resolve All Questions ───────────────────────────────────────────────────


class TestResolveAllQuestions:
    def test_applies_human_answers(self):
        questions = [
            {
                "id": "q_0_change_risk",
                "question_type": "change_risk",
                "description": "Risk",
                "entity_a_id": "svc-1",
                "resolution_owner": "human_preferred",
            },
        ]
        arch_model = {
            "entities": [
                {"id": "svc-1", "name": "Svc", "metadata": {"assumption_flag": True}},
            ],
            "relationships": [],
            "assumption_flags": ["svc-1"],
        }
        result = _resolve_all_questions(
            questions,
            {"q_0_change_risk": "Human decision: approve"},
            arch_model,
            {},
            None,
        )
        assert questions[0]["resolution"] == "Human decision: approve"
        assert questions[0]["assumption_flag"] is False
        assert result["entities"][0]["metadata"]["assumption_flag"] is False
        assert "svc-1" not in result.get("assumption_flags", [])

    def test_resolves_unresolved_judge_resolvable(self):
        questions = [
            {
                "id": "q_0",
                "question_type": "hierarchy_conflict",
                "description": "Parent mismatch",
                "resolution_owner": "judge_resolvable",
            },
        ]
        _resolve_all_questions(questions, {}, {"entities": []}, {}, None)
        assert questions[0]["resolution"] is not None
        assert "parent hierarchy" in questions[0]["resolution"].lower()
        assert questions[0]["assumption_flag"] is False

    def test_resolves_unresolved_human_preferred(self):
        questions = [
            {
                "id": "q_0",
                "question_type": "coverage_gap",
                "description": "Missing requirement coverage",
                "entity_a_id": "e1",
            },
        ]
        arch_model = {
            "entities": [
                {"id": "e1", "name": "E1", "metadata": {}},
            ],
            "relationships": [],
            "assumption_flags": [],
        }
        result = _resolve_all_questions(questions, {}, arch_model, {}, None)
        assert questions[0]["resolution"] is not None
        assert questions[0]["assumption_flag"] is True
        assert "e1" in result.get("assumption_flags", [])
        assert result["entities"][0]["metadata"]["assumption_flag"] is True
        assert result["entities"][0]["metadata"]["assumed"] is True

    def test_skips_already_resolved_questions(self):
        questions = [
            {
                "id": "q_0",
                "question_type": "change_risk",
                "description": "Already done",
                "resolution": "Pre-resolved by conflict_resolution",
                "assumption_flag": False,
            },
        ]
        _resolve_all_questions(questions, {}, {"entities": []}, {}, None)
        # Should be unchanged
        assert questions[0]["resolution"] == "Pre-resolved by conflict_resolution"
        assert questions[0]["assumption_flag"] is False

    def test_mixed_resolution_scenarios(self):
        questions = [
            {
                "id": "q_0",
                "question_type": "change_risk",
                "description": "Human needed",
                "resolution_owner": "human_preferred",
            },
            {
                "id": "q_1",
                "question_type": "hierarchy_conflict",
                "description": "Auto resolvable",
                "resolution_owner": "judge_resolvable",
            },
        ]
        _resolve_all_questions(
            questions,
            {"q_0": "Human says OK"},
            {"entities": []},
            {},
            None,
        )
        assert "Human says OK" in questions[0]["resolution"]
        assert questions[0]["assumption_flag"] is False
        assert questions[1]["resolution"] is not None
        assert questions[1]["assumption_flag"] is False

    def test_preserves_arch_model_keys(self):
        arch_model = {
            "entities": [],
            "relationships": [],
            "boundary_groups": [{"group_id": "bg-1"}],
            "cross_cutting_candidates": ["security"],
            "assumption_flags": [],
        }
        result = _resolve_all_questions([], {}, arch_model, {}, None)
        assert result["boundary_groups"] == [{"group_id": "bg-1"}]
        assert result["cross_cutting_candidates"] == ["security"]

    def test_no_questions_returns_unchanged_model(self):
        model = {"entities": [{"id": "e1", "name": "E1"}], "relationships": []}
        result = _resolve_all_questions([], {}, model, {}, None)
        assert result["entities"] == model["entities"]
        assert result["relationships"] == model["relationships"]


# ── Global Merge ────────────────────────────────────────────────────────────


class TestGlobalMerge:
    def test_empty_batch_outputs_preserves_model(self):
        model = {"entities": [_entity_dict()], "relationships": []}
        result, questions = _global_merge(model, [], None, None)
        assert len(result["entities"]) == 1
        assert questions == []

    def test_single_batch_merged(self):
        model = {"entities": [], "relationships": []}
        batch = {"entities": [_entity_dict()], "relationships": [_rel_dict()]}
        result, questions = _global_merge(model, [batch], None, None)
        assert len(result["entities"]) == 1
        assert len(result["relationships"]) == 1

    def test_multiple_batches_accumulated(self):
        model = {"entities": [], "relationships": []}
        batch1 = {"entities": [_entity_dict(id="a")], "relationships": []}
        batch2 = {"entities": [_entity_dict(id="b")], "relationships": []}
        result, questions = _global_merge(model, [batch1, batch2], None, None)
        assert len(result["entities"]) == 2

    def test_duplicate_id_merged_across_batches(self):
        model = {"entities": [], "relationships": []}
        batch1 = {"entities": [_entity_dict(id="user-service", description="First")], "relationships": []}
        batch2 = {"entities": [_entity_dict(id="user_service", description="Second longer desc")], "relationships": []}
        result, questions = _global_merge(model, [batch1, batch2], None, None)
        assert len(result["entities"]) == 1
        assert result["entities"][0]["description"] == "Second longer desc"

    def test_hierarchy_mismatch_generates_question(self):
        model = {"entities": [], "relationships": []}
        batch1 = {"entities": [_entity_dict(id="user-service", parent_system_id="sys-a")], "relationships": []}
        batch2 = {"entities": [_entity_dict(id="user_service", parent_system_id="sys-b")], "relationships": []}
        result, questions = _global_merge(model, [batch1, batch2], None, None)
        assert len(result["entities"]) == 1
        assert len(questions) >= 1
        hierarchy_qs = [q for q in questions if q.get("question_type") == "hierarchy_conflict"]
        assert len(hierarchy_qs) >= 1

    def test_preserves_cross_cutting_candidates(self):
        model = {
            "entities": [],
            "relationships": [],
            "cross_cutting_candidates": ["security", "logging"],
        }
        result, _ = _global_merge(model, [], None, None)
        assert result["cross_cutting_candidates"] == ["security", "logging"]

    def test_preserves_assumption_flags(self):
        model = {
            "entities": [],
            "relationships": [],
            "assumption_flags": ["e1", "e2"],
        }
        result, _ = _global_merge(model, [], None, None)
        assert result["assumption_flags"] == ["e1", "e2"]

    def test_preserves_boundary_groups(self):
        model = {
            "entities": [],
            "relationships": [],
            "boundary_groups": [{"group_id": "bg-1"}],
        }
        result, _ = _global_merge(model, [], None, None)
        assert result["boundary_groups"] == [{"group_id": "bg-1"}]

    def test_skips_none_batch(self):
        model = {"entities": [], "relationships": []}
        result, questions = _global_merge(model, [None, {}], None, None)
        assert result["entities"] == []

    def test_relationship_rewritten_on_merge(self):
        model = {"entities": [], "relationships": []}
        batch1 = {
            "entities": [_entity_dict(id="user-service")],
            "relationships": [_rel_dict(source_id="user-service", target_id="payment")],
        }
        batch2 = {
            "entities": [_entity_dict(id="user_service")],
            "relationships": [],
        }
        result, _ = _global_merge(model, [batch1, batch2], None, None)
        assert len(result["entities"]) == 1
        # The relationship should point to the canonical entity ID
        canonical_id = result["entities"][0]["id"]
        for rel in result["relationships"]:
            if rel["source_id"] != "payment" and rel["target_id"] != "payment":
                assert rel["source_id"] == canonical_id


# ── Full Node Integration ───────────────────────────────────────────────────


class TestFinalMerge:
    def test_empty_state_produces_empty_model(self):
        state = _make_state()
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)
        assert "arch_model" in result
        assert "open_questions" in result
        assert result["open_questions"] == []

    def test_merges_batches_and_resolves_questions(self):
        state = _make_state(
            batch_outputs=[
                {"entities": [_entity_dict(id="svc-a")], "relationships": []},
                {"entities": [_entity_dict(id="svc-b")], "relationships": []},
            ],
            open_questions=[
                {
                    "id": "q_0_change_risk",
                    "question_type": "change_risk",
                    "description": "Some risk",
                    "entity_a_id": "svc-a",
                },
            ],
            human_answers={"q_0_change_risk": "Approved"},
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert len(result["arch_model"]["entities"]) == 2
        # Question should be resolved in the output
        q = result["open_questions"][0]
        assert q["resolution"] == "Approved"
        assert q["assumption_flag"] is False

    def test_resolves_unresolved_judge_questions(self):
        state = _make_state(
            batch_outputs=[],
            open_questions=[
                {
                    "id": "q_0",
                    "question_type": "hierarchy_conflict",
                    "description": "Parent mismatch",
                    "resolution_owner": "judge_resolvable",
                },
            ],
            arch_model={"entities": [], "relationships": []},
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert result["open_questions"][0]["resolution"] is not None
        assert result["open_questions"][0]["assumption_flag"] is False

    def test_resolves_unresolved_human_questions_with_assumptions(self):
        state = _make_state(
            batch_outputs=[],
            open_questions=[
                {
                    "id": "q_0",
                    "question_type": "coverage_gap",
                    "description": "Missing something",
                    "entity_a_id": "e1",
                },
            ],
            arch_model={
                "entities": [{"id": "e1", "name": "E1", "metadata": {}}],
                "relationships": [],
            },
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert result["open_questions"][0]["resolution"] is not None
        assert result["open_questions"][0]["assumption_flag"] is True
        assert "e1" in result["arch_model"].get("assumption_flags", [])

    def test_merge_questions_returned_for_append_reducer(self):
        state = _make_state(
            batch_outputs=[
                {"entities": [_entity_dict(id="user-service")], "relationships": []},
                {"entities": [_entity_dict(id="user_service")], "relationships": []},
            ],
            open_questions=[],
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        # Merge questions from dedup should be returned for append
        assert isinstance(result["open_questions"], list)

    def test_no_questions_ensures_all_resolved(self):
        """Verify that even with zero questions, the output has no null resolutions."""
        state = _make_state(
            batch_outputs=[{"entities": [_entity_dict()], "relationships": []}],
            open_questions=[],
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert result["arch_model"]["entities"]
        # No unresolved questions
        for q in result["open_questions"]:
            assert q.get("resolution") is not None

    def test_preserves_existing_resolutions(self):
        """Questions already resolved should stay resolved."""
        state = _make_state(
            batch_outputs=[],
            open_questions=[
                {
                    "id": "q_0",
                    "question_type": "tie",
                    "description": "Already resolved",
                    "resolution": "Pre-resolved answer",
                    "assumption_flag": False,
                },
            ],
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert result["open_questions"][0]["resolution"] == "Pre-resolved answer"
        assert state["open_questions"][0]["assumption_flag"] is False
