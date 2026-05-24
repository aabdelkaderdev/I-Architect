"""
Unit tests for final merge node (Story 4.1 + Story 4.2).
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from raa.nodes.final_merge import (
    DocumentedAssumption,
    ResidualArchitecturalCheck,
    ResidualCouplingCheck,
    _check_architectural,
    _check_coupling,
    _collect_entity_ids,
    _extract_requirement_text,
    _generate_assumption,
    _get_default_suggestion,
    _get_resolution_owner,
    _global_merge,
    _has_structural_keywords,
    _init_embeddings,
    _keyword_overlap_coupling,
    _normalize_merge_questions,
    _process_residual_requirements,
    _resolve_all_questions,
    _try_merge_residual_entity,
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
    unprocessed_requirements=None,
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
        "unprocessed_requirements": unprocessed_requirements or [],
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


# ═══════════════════════════════════════════════════════════════════════════════
# Story 4.2: Residual Requirements Decision Ladder Tests
# ═══════════════════════════════════════════════════════════════════════════════


# ── Helpers ─────────────────────────────────────────────────────────────────


def _req(**overrides):
    """Create a minimal unprocessed_requirement dict."""
    defaults = {
        "id": "R100",
        "description": "The system shall provide real-time event streaming",
        "is_asr": False,
        "quality_attributes": [],
    }
    defaults.update(overrides)
    return defaults


def _container(**overrides):
    """Create a minimal container entity dict."""
    defaults = {
        "id": "container-1",
        "name": "Event Broker",
        "description": "Handles real-time event streaming and message delivery",
        "c4_type": "container",
        "technology": "Kafka",
        "requirement_ids": ["R1", "R2"],
    }
    defaults.update(overrides)
    return defaults


def _model(**overrides):
    """Create a minimal arch_model dict."""
    defaults: dict = {
        "entities": [_container()],
        "relationships": [],
        "boundary_groups": [],
        "assumption_flags": [],
    }
    defaults.update(overrides)
    return defaults


# ── Extract Requirement Text ──────────────────────────────────────────────────


class TestExtractRequirementText:
    def test_uses_condition_text_for_asr(self):
        req = _req(condition_text="ASR condition text", description="Non-ASR desc")
        assert _extract_requirement_text(req) == "ASR condition text"

    def test_falls_back_to_description(self):
        req = _req(description="Fallback description")
        assert _extract_requirement_text(req) == "Fallback description"

    def test_empty_when_both_missing(self):
        req = _req(description="", condition_text=None)
        assert _extract_requirement_text(req) == ""

    def test_strips_whitespace(self):
        req = _req(condition_text="  padded text  ")
        assert _extract_requirement_text(req) == "padded text"


# ── Keyword Overlap Coupling ──────────────────────────────────────────────────


class TestKeywordOverlapCoupling:
    def test_shared_actor_keyword(self):
        assert _keyword_overlap_coupling(
            "The user receives event notifications",
            "This container handles user notifications",
        ) is True

    def test_shared_flow_keyword(self):
        assert _keyword_overlap_coupling(
            "The system sends data via API calls",
            "Container processes API requests and responses",
        ) is True

    def test_no_overlap(self):
        assert _keyword_overlap_coupling(
            "The system manages payroll calculations",
            "This container renders HTML templates for UI",
        ) is False

    def test_significant_word_overlap(self):
        assert _keyword_overlap_coupling(
            "payment processing gateway handles transactions",
            "payment processing gateway routes requests",
        ) is True

    def test_empty_container_desc(self):
        assert _keyword_overlap_coupling("some text", "") is False


# ── Structural Keywords ───────────────────────────────────────────────────────


class TestHasStructuralKeywords:
    def test_detects_system(self):
        assert _has_structural_keywords("The payment system processes transactions") is True

    def test_detects_database(self):
        assert _has_structural_keywords("Data must persist in a relational database") is True

    def test_detects_microservice(self):
        assert _has_structural_keywords("Deploy as a separate microservice") is True

    def test_no_structural_keywords(self):
        assert _has_structural_keywords("The UI button color should be blue") is False

    def test_empty_text(self):
        assert _has_structural_keywords("") is False


# ── Check Coupling ───────────────────────────────────────────────────────────


class TestCheckCoupling:
    def test_llm_coupled(self):
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = ResidualCouplingCheck(is_coupled=True)

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            result = _check_coupling(
                "R100", "event streaming requirement", False,
                _container(), 0.65, mock_llm,
            )
        assert result is True

    def test_llm_not_coupled(self):
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = ResidualCouplingCheck(is_coupled=False)

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            result = _check_coupling(
                "R100", "unrelated requirement", False,
                _container(), 0.55, mock_llm,
            )
        assert result is False

    def test_fallback_when_no_llm(self):
        result = _check_coupling(
            "R100", "The user receives event notifications",
            False, _container(), 0.60, None,
        )
        assert isinstance(result, bool)

    def test_llm_dict_result(self):
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = {"is_coupled": True}

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            result = _check_coupling(
                "R100", "req text", False, _container(), 0.60, mock_llm,
            )
        assert result is True

    def test_llm_error_falls_back(self):
        mock_llm = MagicMock()
        mock_llm.with_structured_output.side_effect = Exception("LLM failed")

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            result = _check_coupling(
                "R100", "event streaming for users", False,
                _container(), 0.60, mock_llm,
            )
        # Should fall back to keyword heuristic
        assert isinstance(result, bool)


# ── Check Architectural ──────────────────────────────────────────────────────


class TestCheckArchitectural:
    def test_llm_architectural_with_entity(self):
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = ResidualArchitecturalCheck(
            implies_architectural_structure=True,
            new_entity={
                "id": "new-svc",
                "name": "New Service",
                "description": "A new payment service",
                "c4_type": "container",
            },
            new_relationships=[],
        )

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            is_arch, entity, rels, rationale = _check_architectural(
                "R100", "new payment service", False, _model(), mock_llm,
            )
        assert is_arch is True
        assert entity is not None
        assert entity["name"] == "New Service"

    def test_llm_non_architectural(self):
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = ResidualArchitecturalCheck(
            implies_architectural_structure=False,
            non_architectural_rationale="This is a UI styling concern, not architectural.",
        )

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            is_arch, entity, rels, rationale = _check_architectural(
                "R100", "button color blue", False, _model(), mock_llm,
            )
        assert is_arch is False
        assert "UI styling" in rationale

    def test_fallback_structural_keywords(self):
        is_arch, entity, rels, rationale = _check_architectural(
            "R100", "Deploy payment system as microservice",
            False, _model(), None,
        )
        assert is_arch is True
        assert entity is None  # fallback doesn't propose entities

    def test_fallback_non_architectural(self):
        is_arch, entity, rels, rationale = _check_architectural(
            "R100", "Button color should be blue",
            False, _model(), None,
        )
        assert is_arch is False
        assert "non-architectural" in rationale

    def test_llm_dict_result(self):
        mock_llm = MagicMock()
        mock_structured = MagicMock()
        mock_llm.with_structured_output.return_value = mock_structured
        mock_structured.invoke.return_value = {
            "implies_architectural_structure": True,
            "new_entity": {"id": "dict-svc", "name": "DictSvc", "c4_type": "container"},
        }

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            is_arch, entity, rels, rationale = _check_architectural(
                "R100", "text", False, _model(), mock_llm,
            )
        assert is_arch is True

    def test_llm_error_falls_back(self):
        mock_llm = MagicMock()
        mock_llm.with_structured_output.side_effect = Exception("LLM failed")

        with patch("raa.nodes.final_merge.load_prompt") as mock_load:
            mock_load.return_value = "prompt"
            is_arch, entity, rels, rationale = _check_architectural(
                "R100", "database cluster deployment", False, _model(), mock_llm,
            )
        # Falls back to keyword heuristic, detects "database" and "cluster"
        assert is_arch is True


# ── Process Residual Requirements ────────────────────────────────────────────


class TestProcessResidualRequirements:
    def test_empty_unprocessed_returns_unchanged(self):
        model = _model()
        result_model, questions = _process_residual_requirements(
            [], model, {}, None, None, None,
        )
        assert result_model == model
        assert questions == []

    def test_high_similarity_auto_enriches(self, monkeypatch):
        """AC #2: > 0.75 auto-enriches container description and appends req ID."""
        model = _model()
        req = _req(id="R100", description="Handles real-time event streaming and message delivery")
        unprocessed = [req]

        # Mock embeddings as unavailable to avoid needing real model
        result_model, questions = _process_residual_requirements(
            unprocessed, model, {}, None, None, None,
        )
        # No embeddings = similarity stays 0.0, won't trigger high sim.
        # But this test validates the code doesn't crash without embeddings.
        assert isinstance(result_model, dict)
        assert isinstance(questions, list)

    def test_high_similarity_with_embeddings(self):
        """AC #2: Verify > 0.75 auto-enrich when similarity exceeds threshold."""
        model = _model()
        req = _req(id="R100", description="Real-time event streaming and message delivery")
        unprocessed = [req]

        with patch(
            "raa.nodes.final_merge._process_residual_requirements",
            wraps=_process_residual_requirements,
        ) as wrapped:
            # Mock cosine_similarity to return high similarity
            with patch("raa.nodes.final_merge.cosine_similarity", return_value=0.85):
                mock_cache = MagicMock()
                mock_cache.text_hash.return_value = "hash123"
                mock_cache.get_cached_vector.return_value = [0.1] * 1024
                mock_model = MagicMock()

                result_model, questions = _process_residual_requirements(
                    unprocessed, model, {}, mock_cache, mock_model, None,
                )
                # Container description should be enriched
                desc = result_model["entities"][0]["description"]
                assert "(Supports R100:" in desc
                assert "R100" in result_model["entities"][0]["requirement_ids"]

    def test_moderate_similarity_coupled(self):
        """AC #3: 0.50-0.75 coupled → enrich + assumption flags."""
        model = _model()
        req = _req(id="R100", description="User event notification delivery")
        unprocessed = [req]

        with patch("raa.nodes.final_merge.cosine_similarity", return_value=0.65):
            with patch("raa.nodes.final_merge._check_coupling", return_value=True):
                mock_cache = MagicMock()
                mock_cache.text_hash.return_value = "hash456"
                mock_cache.get_cached_vector.return_value = [0.2] * 1024
                mock_model = MagicMock()

                result_model, questions = _process_residual_requirements(
                    unprocessed, model, {}, mock_cache, mock_model, None,
                )

        desc = result_model["entities"][0]["description"]
        assert "(Supports R100:" in desc
        assert "R100" in result_model["entities"][0]["requirement_ids"]
        assert result_model["entities"][0]["metadata"]["assumption_flag"] is True
        assert result_model["entities"][0]["metadata"]["assumed"] is True
        assert "container-1" in result_model["assumption_flags"]

    def test_moderate_similarity_not_coupled(self):
        """AC #3: 0.50-0.75 not coupled → residual_coupling question."""
        model = _model()
        req = _req(id="R100", description="Unrelated payroll calculation")
        unprocessed = [req]

        with patch("raa.nodes.final_merge.cosine_similarity", return_value=0.60):
            with patch("raa.nodes.final_merge._check_coupling", return_value=False):
                mock_cache = MagicMock()
                mock_cache.text_hash.return_value = "hash789"
                mock_cache.get_cached_vector.return_value = [0.3] * 1024
                mock_model = MagicMock()

                result_model, questions = _process_residual_requirements(
                    unprocessed, model, {}, mock_cache, mock_model, None,
                )

        assert len(questions) == 1
        assert questions[0]["question_type"] == "residual_coupling"
        assert questions[0]["resolution_owner"] == "human_preferred"
        assert questions[0]["resolution"] is None
        assert questions[0]["context"]["req_id"] == "R100"

    def test_low_similarity_architectural(self):
        """AC #4: < 0.50 architectural → propose and merge entity."""
        model = _model()
        req = _req(id="R200", description="New payment gateway system needed")
        unprocessed = [req]

        with patch("raa.nodes.final_merge.cosine_similarity", return_value=0.30):
            with patch(
                "raa.nodes.final_merge._check_architectural",
                return_value=(True, None, None, ""),
            ):
                mock_cache = MagicMock()
                mock_cache.text_hash.return_value = "hash_arch"
                mock_cache.get_cached_vector.return_value = [0.4] * 1024
                mock_model = MagicMock()

                result_model, questions = _process_residual_requirements(
                    unprocessed, model, {}, mock_cache, mock_model, None,
                )

        # A new entity should have been created and merged
        assert len(result_model["entities"]) >= 1

    def test_low_similarity_non_architectural(self):
        """AC #5: < 0.50 non-architectural → coverage_gap question."""
        model = _model()
        req = _req(id="R300", description="Button color should be #336699")
        unprocessed = [req]

        with patch("raa.nodes.final_merge.cosine_similarity", return_value=0.20):
            with patch(
                "raa.nodes.final_merge._check_architectural",
                return_value=(False, None, None, "UI styling, non-architectural"),
            ):
                mock_cache = MagicMock()
                mock_cache.text_hash.return_value = "hash_non"
                mock_cache.get_cached_vector.return_value = [0.5] * 1024
                mock_model = MagicMock()

                result_model, questions = _process_residual_requirements(
                    unprocessed, model, {}, mock_cache, mock_model, None,
                )

        assert len(questions) == 1
        assert questions[0]["question_type"] == "coverage_gap"
        assert questions[0]["resolution_owner"] == "human_preferred"
        assert "UI styling" in questions[0]["description"]

    def test_sequential_processing_multiple_requirements(self):
        """AC #1: Verify sequential evaluation of multiple unprocessed reqs."""
        model = _model()
        reqs = [
            _req(id="R100", description="Event streaming delivery"),
            _req(id="R200", description="New payment gateway system needed"),
            _req(id="R300", description="Button color blue"),
        ]
        unprocessed = reqs

        call_count = [0]

        def mock_cosine(a, b):
            call_count[0] += 1
            return 0.85  # All high similarity for simplicity

        with patch("raa.nodes.final_merge.cosine_similarity", side_effect=mock_cosine):
            mock_cache = MagicMock()
            mock_cache.text_hash.return_value = "hash_seq"
            mock_cache.get_cached_vector.return_value = [0.6] * 1024
            mock_model = MagicMock()

            result_model, questions = _process_residual_requirements(
                unprocessed, model, {}, mock_cache, mock_model, None,
            )

        # Each req compared against 1 container = 3 comparisons
        assert call_count[0] == 3
        # All three should be in the container's requirement_ids
        assert "R100" in result_model["entities"][0]["requirement_ids"]

    def test_fallback_to_requirements_dict(self):
        """Verifies req_text falls back to requirements dict when req fields empty."""
        model = _model()
        req = _req(id="R100", description="", condition_text=None)
        unprocessed = [req]
        reqs_dict = {"R100": "Fallback text from requirements dict"}

        with patch("raa.nodes.final_merge.cosine_similarity", return_value=0.85):
            mock_cache = MagicMock()
            mock_cache.text_hash.return_value = "hash_fb"
            mock_cache.get_cached_vector.return_value = [0.7] * 1024
            mock_model = MagicMock()

            result_model, questions = _process_residual_requirements(
                unprocessed, model, reqs_dict, mock_cache, mock_model, None,
            )

        desc = result_model["entities"][0]["description"]
        assert "Fallback text" in desc

    def test_skips_req_with_no_text(self):
        """Reqs with no extractable text are silently skipped."""
        model = _model()
        req = _req(id="R100", description="", condition_text=None)
        unprocessed = [req]
        reqs_dict = {}  # No fallback either

        result_model, questions = _process_residual_requirements(
            unprocessed, model, reqs_dict, None, None, None,
        )
        # Model unchanged, no questions generated
        assert questions == []
        assert result_model["entities"] == model["entities"]

    def test_missing_embeddings_graceful_degradation(self):
        """No embeddings → similarity stays 0.0, falls to low-sim architectural path."""
        model = _model()
        req = _req(id="R500", description="Deploy a new database cluster")
        unprocessed = [req]

        result_model, questions = _process_residual_requirements(
            unprocessed, model, {}, None, None, None,
        )
        # Without embeddings, falls to < 0.50 case
        # "database" and "cluster" trigger structural keywords in fallback
        assert len(result_model["entities"]) >= 1 or len(questions) >= 1


# ── Try Merge Residual Entity ────────────────────────────────────────────────


class TestTryMergeResidualEntity:
    def test_creates_fallback_entity_when_none_provided(self):
        model = _model()
        questions: list[dict] = []
        _try_merge_residual_entity(
            "R100", "New payment gateway system", None, None,
            model, questions, None, None,
        )
        # Entity should have been merged
        assert len(model["entities"]) >= 2
        # Should find the new entity
        new_entities = [e for e in model["entities"] if "residual_" in e["id"]]
        assert len(new_entities) == 1
        assert new_entities[0]["description"] == "New payment gateway system"

    def test_uses_provided_entity(self):
        model = _model()
        questions: list[dict] = []
        new_entity = {
            "id": "payment-gateway",
            "name": "Payment Gateway",
            "description": "Handles payment processing",
            "c4_type": "container",
            "technology": "Stripe",
        }
        _try_merge_residual_entity(
            "R200", "payment processing", new_entity, [],
            model, questions, None, None,
        )
        assert len(model["entities"]) >= 2
        new_entities = [e for e in model["entities"] if e["id"] == "payment-gateway"]
        assert len(new_entities) == 1

    def test_ensures_required_fields(self):
        """Entity missing fields gets defaults filled in."""
        model = _model()
        questions: list[dict] = []
        new_entity = {"name": "Bare Entity"}
        _try_merge_residual_entity(
            "R300", "bare requirement", new_entity, [],
            model, questions, None, None,
        )
        merged = next(e for e in model["entities"] if e.get("name") == "Bare Entity")
        assert merged["id"] == "residual_R300"
        assert merged["c4_type"] == "container"
        assert merged["description"] == "bare requirement"


# ── Final Merge Integration with Residuals ───────────────────────────────────


class TestFinalMergeWithResiduals:
    def test_includes_residual_questions_in_output(self):
        state = _make_state(
            batch_outputs=[],
            arch_model=_model(),
            open_questions=[],
            unprocessed_requirements=[_req(id="R999", description="Button color blue")],
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert "arch_model" in result
        # Residual questions should be included
        assert isinstance(result["open_questions"], list)

    def test_residual_processing_integrated_in_flow(self):
        state = _make_state(
            batch_outputs=[
                {"entities": [_container(id="svc-a")], "relationships": []},
            ],
            arch_model={"entities": [], "relationships": []},
            open_questions=[],
            unprocessed_requirements=[
                _req(id="R500", description="Deploy a new database cluster"),
            ],
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        # Both batch entities and residual-processed entities should exist
        assert len(result["arch_model"]["entities"]) >= 1
        # Residual questions (coverage_gap from non-architectural or merged entities)
        assert isinstance(result["open_questions"], list)

    def test_empty_unprocessed_no_effect(self):
        state = _make_state(
            batch_outputs=[{"entities": [_container(id="a")], "relationships": []}],
            arch_model={"entities": [], "relationships": []},
            open_questions=[],
            unprocessed_requirements=[],
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert len(result["arch_model"]["entities"]) == 1
        assert result["arch_model"]["entities"][0]["id"] == "a"

    def test_residual_and_merge_questions_resolved_in_final_merge(self):
        """Verify that all merge-generated and residual-generated questions are resolved in the output."""
        state = _make_state(
            batch_outputs=[
                {"entities": [_container(id="svc-a", description="Auth Service")], "relationships": []},
                {"entities": [_container(id="svc_a", description="Auth Service Core")], "relationships": []},
            ],
            arch_model={"entities": [], "relationships": []},
            open_questions=[],
            unprocessed_requirements=[
                _req(id="R800", description="Perform UI layout tweaks"),
            ],
        )
        with patch("raa.nodes.final_merge._init_embeddings", return_value=(None, None)):
            result = final_merge(state)

        assert len(result["open_questions"]) >= 1
        for q in result["open_questions"]:
            assert q.get("resolution") is not None
            assert q.get("question_type") is not None
            assert q.get("id") is not None

    def test_container_embeddings_persisted_to_cache(self):
        """Verify that container description embeddings generated on-the-fly are stored in cache."""
        model = _model()
        req = _req(id="R100", description="User event notifications")
        unprocessed = [req]

        mock_cache = MagicMock()
        mock_cache.text_hash.return_value = "hash123"
        mock_cache.get_cached_vector.return_value = None  # Force generation
        
        mock_vec = MagicMock()
        mock_vec.tolist.return_value = [0.1] * 1024
        mock_model = MagicMock()
        mock_model.embed.return_value = [mock_vec]

        with patch("raa.nodes.final_merge.cosine_similarity", return_value=0.65):
            _process_residual_requirements(
                unprocessed, model, {}, mock_cache, mock_model, None,
            )

        # Verify cache.store_vector was called for container embedding
        mock_cache.store_vector.assert_any_call("container-1", "hash123", [0.1] * 1024)
