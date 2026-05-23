"""
Unit tests for human review gate node (Story 3.1 + 3.2).
"""
from __future__ import annotations

from unittest.mock import patch

import pytest
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.types import Command

from raa.nodes.human_review_gate import human_review_gate, prepare_human_review_payload
from raa.state.models import OpenQuestion
from raa.state.schemas import RAAState


# ── Helpers ─────────────────────────────────────────────────────────────────


def _make_state(open_questions=None, arch_model=None):
    return {
        "batch_cursor": 0,
        "quality_weights": {},
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "review_mode": "autonomous",
        "normalized_asrs": [],
        "normalized_non_asr": [],
        "embeddings_ready": False,
        "batch_outputs": [],
        "open_questions": open_questions or [],
        "incoherent_batches": [],
        "arch_model": arch_model or {},
        "judge_rankings": {},
    }


# ── Classification ──────────────────────────────────────────────────────────


class TestClassification:
    def test_change_risk_classified_as_human_preferred(self):
        state = _make_state(open_questions=[
            {"question_type": "change_risk", "description": "Risk of merging entities"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "human_preferred"

    def test_high_coupling_classified_as_human_preferred(self):
        state = _make_state(open_questions=[
            {"question_type": "high_coupling", "description": "High coupling detected"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "human_preferred"

    def test_coverage_gap_classified_as_human_preferred(self):
        state = _make_state(open_questions=[
            {"question_type": "coverage_gap", "description": "Coverage gap"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "human_preferred"

    def test_contention_classified_as_judge_resolvable(self):
        state = _make_state(open_questions=[
            {"question_type": "contention", "description": "Strategy contention"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "judge_resolvable"

    def test_tie_classified_as_judge_resolvable(self):
        state = _make_state(open_questions=[
            {"question_type": "tie", "description": "Tie between strategies"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "judge_resolvable"

    def test_hierarchy_conflict_classified_as_judge_resolvable(self):
        state = _make_state(open_questions=[
            {"question_type": "hierarchy_conflict", "description": "Parent mismatch"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "judge_resolvable"

    def test_scope_conflict_classified_as_judge_resolvable(self):
        state = _make_state(open_questions=[
            {"question_type": "scope_conflict", "description": "Scope conflict"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "judge_resolvable"

    def test_unknown_type_defaults_to_human_preferred(self):
        state = _make_state(open_questions=[
            {"question_type": "unknown_thing", "description": "Something weird"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution_owner"] == "human_preferred"


# ── Legacy Key Normalization ────────────────────────────────────────────────


class TestLegacyKeyNormalization:
    def test_maps_type_to_question_type(self):
        state = _make_state(open_questions=[
            {"type": "change_risk", "description": "Old format"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["question_type"] == "change_risk"

    def test_question_type_takes_precedence_over_type(self):
        state = _make_state(open_questions=[
            {"question_type": "tie", "type": "change_risk", "description": "Has both"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["question_type"] == "tie"

    def test_missing_both_defaults_to_unknown(self):
        state = _make_state(open_questions=[
            {"description": "No type at all"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["question_type"] == "unknown"
        assert q["resolution_owner"] == "human_preferred"


# ── Suggested Resolutions ───────────────────────────────────────────────────


class TestSuggestedResolutions:
    def test_hierarchy_conflict_suggestion(self):
        state = _make_state(open_questions=[
            {"question_type": "hierarchy_conflict", "description": "Mismatch"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution"] == "Use parent hierarchy from canonical entity."

    def test_scope_conflict_suggestion(self):
        state = _make_state(open_questions=[
            {"question_type": "scope_conflict", "description": "Scope issue"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution"] == "Apply fallback constraints to adjust relationship scope."

    def test_tie_suggestion(self):
        state = _make_state(open_questions=[
            {"question_type": "tie", "description": "Tiebreaker needed"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution"] == "Resolve tie by selecting the proposal from primary strategy (RAA-A SAAM-First)."

    def test_contention_suggestion(self):
        state = _make_state(open_questions=[
            {"question_type": "contention", "description": "Contention detected"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution"] == "Consolidate entities using the primary strategy's structure as the ground truth."

    def test_human_preferred_has_no_suggestion(self):
        state = _make_state(open_questions=[
            {"question_type": "change_risk", "description": "Risk"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["resolution"] is None


# ── Conflicting Elements ────────────────────────────────────────────────────


class TestConflictingElements:
    def test_gathers_entity_a_id_and_entity_b_id(self):
        state = _make_state(
            open_questions=[
                {
                    "question_type": "change_risk",
                    "description": "Risk",
                    "entity_a_id": "svc-a",
                    "entity_b_id": "svc-b",
                },
            ],
            arch_model={
                "entities": [
                    {"id": "svc-a", "name": "Service A", "c4_type": "container"},
                    {"id": "svc-b", "name": "Service B", "c4_type": "container"},
                ],
            },
        )
        result = prepare_human_review_payload(state)
        elements = result["human_review_payload"]["conflicting_elements"]
        assert len(elements) == 2
        names = {e["name"] for e in elements}
        assert names == {"Service A", "Service B"}

    def test_gathers_promoted_component_id(self):
        state = _make_state(
            open_questions=[
                {
                    "question_type": "change_risk",
                    "description": "No parent container",
                    "promoted_component_id": "cc_security",
                    "source": "cross_cutting_promotion",
                },
            ],
            arch_model={
                "entities": [
                    {"id": "cc_security", "name": "Security (Cross-Cutting)", "c4_type": "component"},
                ],
            },
        )
        result = prepare_human_review_payload(state)
        elements = result["human_review_payload"]["conflicting_elements"]
        assert len(elements) == 1
        assert elements[0]["name"] == "Security (Cross-Cutting)"

    def test_entity_not_in_model_is_skipped(self):
        state = _make_state(
            open_questions=[
                {"question_type": "change_risk", "description": "Risk", "entity_a_id": "nonexistent"},
            ],
            arch_model={"entities": []},
        )
        result = prepare_human_review_payload(state)
        elements = result["human_review_payload"]["conflicting_elements"]
        assert elements == []

    def test_deduplicates_referenced_ids(self):
        state = _make_state(
            open_questions=[
                {"question_type": "change_risk", "description": "Risk 1", "entity_a_id": "svc-1"},
                {"question_type": "change_risk", "description": "Risk 2", "entity_a_id": "svc-1"},
            ],
            arch_model={
                "entities": [{"id": "svc-1", "name": "Service 1", "c4_type": "container"}],
            },
        )
        result = prepare_human_review_payload(state)
        elements = result["human_review_payload"]["conflicting_elements"]
        assert len(elements) == 1


# ── Model Statistics ────────────────────────────────────────────────────────


class TestModelStatistics:
    def test_counts_entity_types(self):
        state = _make_state(
            arch_model={
                "entities": [
                    {"id": "s1", "name": "System", "c4_type": "system"},
                    {"id": "s2", "name": "External", "c4_type": "external_system"},
                    {"id": "c1", "name": "Container 1", "c4_type": "container"},
                    {"id": "c2", "name": "Container 2", "c4_type": "container"},
                    {"id": "c3", "name": "Container 3", "c4_type": "container"},
                    {"id": "comp1", "name": "Component", "c4_type": "component"},
                ],
                "relationships": [
                    {"id": "r1", "source_id": "c1", "target_id": "c2"},
                    {"id": "r2", "source_id": "c1", "target_id": "c3"},
                ],
            },
        )
        result = prepare_human_review_payload(state)
        stats = result["human_review_payload"]["model_statistics"]
        assert stats["system_count"] == 1
        assert stats["container_count"] == 3
        assert stats["component_count"] == 1
        assert stats["relationship_count"] == 2
        assert stats["total_entities"] == 6

    def test_empty_model_returns_zeros(self):
        state = _make_state(arch_model={})
        result = prepare_human_review_payload(state)
        stats = result["human_review_payload"]["model_statistics"]
        assert stats["system_count"] == 0
        assert stats["container_count"] == 0
        assert stats["component_count"] == 0
        assert stats["relationship_count"] == 0
        assert stats["total_entities"] == 0


# ── Pre-computed Resolutions ────────────────────────────────────────────────


class TestPreComputedResolutions:
    def test_maps_question_ids_to_suggestions(self):
        state = _make_state(open_questions=[
            {"question_type": "tie", "description": "Tie"},
            {"question_type": "hierarchy_conflict", "description": "Conflict"},
            {"question_type": "change_risk", "description": "Risk"},
        ])
        result = prepare_human_review_payload(state)
        resolutions = result["human_review_payload"]["pre_computed_resolutions"]
        assert len(resolutions) == 2  # only judge_resolvable
        assert "q_0_tie" in resolutions
        assert "q_1_hierarchy_conflict" in resolutions
        assert "q_2_change_risk" not in resolutions


# ── Payload Structure ───────────────────────────────────────────────────────


class TestPayloadStructure:
    def test_payload_has_all_required_keys(self):
        state = _make_state(open_questions=[
            {"question_type": "change_risk", "description": "Test"},
        ])
        result = prepare_human_review_payload(state)
        payload = result["human_review_payload"]
        assert "open_questions" in payload
        assert "conflicting_elements" in payload
        assert "model_statistics" in payload
        assert "pre_computed_resolutions" in payload

    def test_returns_dict_with_human_review_payload_key(self):
        state = _make_state()
        result = prepare_human_review_payload(state)
        assert isinstance(result, dict)
        assert "human_review_payload" in result
        assert isinstance(result["human_review_payload"], dict)


# ── Empty/Edge Cases ────────────────────────────────────────────────────────


class TestEdgeCases:
    def test_empty_open_questions_produces_empty_list(self):
        state = _make_state(open_questions=[])
        result = prepare_human_review_payload(state)
        payload = result["human_review_payload"]
        assert payload["open_questions"] == []
        assert payload["pre_computed_resolutions"] == {}
        assert payload["conflicting_elements"] == []

    def test_preserves_question_context(self):
        state = _make_state(open_questions=[
            {
                "question_type": "change_risk",
                "description": "Risk",
                "entity_a_id": "svc-1",
                "severity": "high",
                "source": "deduplication",
            },
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["context"]["entity_a_id"] == "svc-1"
        assert q["context"]["severity"] == "high"
        assert q["context"]["source"] == "deduplication"

    def test_multiple_questions_get_deterministic_ids(self):
        state = _make_state(open_questions=[
            {"question_type": "change_risk", "description": "Risk"},
            {"question_type": "tie", "description": "Tie"},
            {"question_type": "contention", "description": "Contention"},
        ])
        result = prepare_human_review_payload(state)
        ids = [q["id"] for q in result["human_review_payload"]["open_questions"]]
        assert ids == ["q_0_change_risk", "q_1_tie", "q_2_contention"]

    def test_deterministic_same_input_same_output(self):
        state = _make_state(
            open_questions=[
                {"question_type": "tie", "description": "Tie", "entity_a_id": "a", "entity_b_id": "b"},
                {"question_type": "change_risk", "description": "Risk", "entity_a_id": "c"},
            ],
            arch_model={
                "entities": [
                    {"id": "a", "name": "A", "c4_type": "system"},
                    {"id": "b", "name": "B", "c4_type": "container"},
                    {"id": "c", "name": "C", "c4_type": "component"},
                ],
            },
        )
        r1 = prepare_human_review_payload(state)
        r2 = prepare_human_review_payload(state)
        assert r1 == r2


# ── Review Patches Verification (Adversarial Code Review) ─────────────────────


class TestReviewPatches:
    def test_non_string_question_type_coercion(self):
        state = _make_state(open_questions=[
            {"question_type": 123, "description": "Integer type"},
            {"type": None, "description": "None type"},
        ])
        result = prepare_human_review_payload(state)
        questions = result["human_review_payload"]["open_questions"]
        assert questions[0]["id"] == "q_0_123"
        assert questions[0]["question_type"] == "123"
        assert questions[1]["id"] == "q_1_unknown"
        assert questions[1]["question_type"] == "unknown"

    def test_fallback_description_when_missing(self):
        state = _make_state(open_questions=[
            {"question_type": "change_risk"},
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        assert q["description"] == "Open question of type change_risk"

    def test_json_serialization_coercion(self):
        # We pass a set (non-JSON serializable) in context/metadata
        state = _make_state(open_questions=[
            {
                "question_type": "change_risk",
                "custom_set": {1, 2, 3},
                "metadata": {"some_object": object()},
            }
        ])
        result = prepare_human_review_payload(state)
        q = result["human_review_payload"]["open_questions"][0]
        # set should be coerced to list
        assert isinstance(q["context"]["custom_set"], list)
        assert sorted(q["context"]["custom_set"]) == [1, 2, 3]
        # object should be coerced to string representation
        assert isinstance(q["metadata"]["some_object"], str)
        assert "object at" in q["metadata"]["some_object"]

    def test_conflicting_elements_from_nested_context(self):
        # Even if entity IDs are inside normalized context, they should be resolved
        state = _make_state(
            open_questions=[
                {
                    "question_type": "change_risk",
                    "description": "Conflict",
                    # When normalized, context will contain entity_a_id: "svc-c"
                    "entity_a_id": "svc-c",
                }
            ],
            arch_model={
                "entities": [
                    {"id": "svc-c", "name": "Service C", "c4_type": "component"},
                ]
            }
        )
        result = prepare_human_review_payload(state)
        elements = result["human_review_payload"]["conflicting_elements"]
        assert len(elements) == 1
        assert elements[0]["name"] == "Service C"

    def test_guards_against_non_dict_elements(self):
        state = _make_state(
            open_questions=[
                {"question_type": "change_risk", "entity_a_id": "svc-a"},
                None, # non-dict in open questions
            ],
            arch_model={
                "entities": [
                    "malformed-string-entity", # non-dict
                    {"id": "svc-a", "name": "Service A", "c4_type": "container"},
                ],
                "relationships": [
                    None, # non-dict in relationships
                    {"id": "r1", "source_id": "svc-a", "target_id": "svc-b"},
                ]
            }
        )
        # Should execute successfully without raising AttributeError or TypeError
        result = prepare_human_review_payload(state)
        payload = result["human_review_payload"]
        assert len(payload["conflicting_elements"]) == 1
        assert payload["conflicting_elements"][0]["name"] == "Service A"
        assert payload["model_statistics"]["relationship_count"] == 2
        assert payload["model_statistics"]["total_entities"] == 2


# ══════════════════════════════════════════════════════════════════════════════
# Story 3.2: Indefinite LangGraph Interrupt Gate
# ══════════════════════════════════════════════════════════════════════════════


def _make_gate_state(review_mode="autonomous", human_review_payload=None):
    """Create a state dict with fields needed by human_review_gate."""
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
        "open_questions": [],
        "incoherent_batches": [],
        "arch_model": {},
        "judge_rankings": {},
        "human_review_payload": human_review_payload or {},
    }


class TestHumanReviewGateAutonomous:
    """Autonomous mode: bypass interrupt, return empty dict."""

    def test_autonomous_returns_empty_dict(self):
        state = _make_gate_state(review_mode="autonomous")
        result = human_review_gate(state)
        assert result == {}

    def test_autonomous_does_not_call_interrupt(self):
        state = _make_gate_state(review_mode="autonomous")
        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            result = human_review_gate(state)
            mock_interrupt.assert_not_called()
        assert result == {}

    def test_default_mode_is_autonomous(self):
        """When review_mode is missing, defaults to autonomous (returns {})."""
        state = _make_gate_state()
        state.pop("review_mode", None)
        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            result = human_review_gate(state)
            mock_interrupt.assert_not_called()
        assert result == {}

    def test_unknown_mode_bypasses_interrupt(self):
        """Any non-interactive value should bypass the interrupt."""
        state = _make_gate_state(review_mode="some_future_mode")
        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            result = human_review_gate(state)
            mock_interrupt.assert_not_called()
        assert result == {}

    def test_explicit_none_mode_bypasses_interrupt(self):
        """When review_mode is explicitly None, defaults to autonomous."""
        state = _make_gate_state(review_mode=None)
        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            result = human_review_gate(state)
            mock_interrupt.assert_not_called()
        assert result == {}


class TestHumanReviewGateInteractive:
    """Interactive mode: trigger interrupt, return human_answers."""

    def test_interactive_calls_interrupt_with_payload(self):
        payload = {"open_questions": [], "model_statistics": {}}
        state = _make_gate_state(review_mode="interactive", human_review_payload=payload)

        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            mock_interrupt.return_value = {"resolved": True}
            result = human_review_gate(state)
            mock_interrupt.assert_called_once_with(payload)
        assert result == {"human_answers": {"resolved": True}}

    def test_interactive_returns_human_answers(self):
        payload = {"open_questions": [{"id": "q1"}]}
        state = _make_gate_state(review_mode="interactive", human_review_payload=payload)
        resume_data = {"answers": [{"question_id": "q1", "decision": "approved"}]}

        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            mock_interrupt.return_value = resume_data
            result = human_review_gate(state)

        assert "human_answers" in result
        assert result["human_answers"] == resume_data

    def test_interactive_empty_payload_falls_back_to_empty_dict(self):
        """When human_review_payload is missing, interrupt is called with {}."""
        state = _make_gate_state(review_mode="interactive")
        state.pop("human_review_payload", None)

        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            mock_interrupt.return_value = {}
            result = human_review_gate(state)
            mock_interrupt.assert_called_once_with({})
        assert result == {"human_answers": {}}

    def test_interactive_non_dict_resume_coerced_to_dict(self):
        """When interrupt returns a non-dict, it is coerced to a dict with 'raw_response' key."""
        state = _make_gate_state(review_mode="interactive")
        with patch("raa.nodes.human_review_gate.interrupt") as mock_interrupt:
            mock_interrupt.return_value = "yes"
            result = human_review_gate(state)
        assert result == {"human_answers": {"raw_response": "yes"}}


class TestHumanReviewGateIntegration:
    """Integration tests using a minimal LangGraph StateGraph with MemorySaver."""

    def _build_graph(self, review_mode="interactive"):
        """Build a minimal graph: payload node → gate node → final node."""
        builder = StateGraph(RAAState)

        def prepare(state: RAAState) -> dict:
            return prepare_human_review_payload(state)

        def gate(state: RAAState) -> dict:
            return human_review_gate(state)

        def finalize(state: RAAState) -> dict:
            return {"embeddings_ready": True}

        builder.add_node("prepare", prepare)
        builder.add_node("gate", gate)
        builder.add_node("finalize", finalize)

        builder.set_entry_point("prepare")
        builder.add_edge("prepare", "gate")
        builder.add_edge("gate", "finalize")
        builder.set_finish_point("finalize")

        return builder.compile(checkpointer=MemorySaver())

    def test_interactive_mode_halt_and_resume(self):
        """Interactive mode halts at gate; Command(resume=...) continues past it."""
        graph = self._build_graph(review_mode="interactive")

        state = {
            "review_mode": "interactive",
            "open_questions": [
                {"question_type": "change_risk", "description": "Test risk"}
            ],
            "arch_model": {},
        }

        config = {"configurable": {"thread_id": "test-interactive-1"}}

        # First invocation — should halt at the gate
        first_result = graph.invoke(state, config)
        # After halting, graph state should contain the human_review_payload
        # from the prepare step
        assert "human_review_payload" in first_result

        # Resume with Command
        resume_data = {"answers": [{"question_id": "q_0_change_risk", "decision": "approved"}]}
        final_result = graph.invoke(Command(resume=resume_data), config)

        # After resume, graph reaches finalize — embeddings_ready should be True
        assert final_result.get("embeddings_ready") is True
        # human_answers should contain the resume data
        assert final_result.get("human_answers") == resume_data

    def test_interactive_mode_preserves_payload_in_state(self):
        """After halt, the state should preserve the human_review_payload."""
        graph = self._build_graph(review_mode="interactive")

        state = {
            "review_mode": "interactive",
            "open_questions": [
                {"question_type": "tie", "description": "Strategy tie"}
            ],
            "arch_model": {},
        }

        config = {"configurable": {"thread_id": "test-interactive-2"}}

        first_result = graph.invoke(state, config)

        payload = first_result.get("human_review_payload", {})
        assert "open_questions" in payload
        assert len(payload["open_questions"]) == 1
        assert payload["open_questions"][0]["question_type"] == "tie"

        resume_data = {"answers": []}
        final_result = graph.invoke(Command(resume=resume_data), config)
        assert final_result.get("human_answers") == resume_data

