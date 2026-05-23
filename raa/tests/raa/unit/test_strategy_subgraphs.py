"""
Unit tests for strategy subgraph structured extraction (Story 2.2).

Uses fake LLMs and fake structured-output wrappers — no live models or network.
"""
from __future__ import annotations

import pytest
from langgraph.graph import StateGraph

from raa.state.models import ArchFragment, C4Entity, C4Relationship
from raa.subgraphs.schemas import StrategySubgraphState
from raa.subgraphs.raa_a import build_raa_a_subgraph
from raa.subgraphs.raa_b import build_raa_b_subgraph
from raa.subgraphs.raa_c import build_raa_c_subgraph


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_fake_structured_output(arch_fragment=None, include_raw_response=True):
    """Create a fake LLM whose with_structured_output().invoke() returns expected data."""

    class FakeStructuredRunnable:
        def __init__(self):
            self.schema = None
            self.include_raw = False

        def invoke(self, prompt):
            frag = arch_fragment or ArchFragment(metadata={"fake": True})
            if include_raw_response:
                return {"raw": {}, "parsed": frag, "parsing_error": None}
            return frag

    class FakeLLM:
        def with_structured_output(self, schema, include_raw=False):
            fake = FakeStructuredRunnable()
            fake.schema = schema
            fake.include_raw = include_raw
            return fake

    return FakeLLM()


def _make_state(batch=None, quality_weights=None, running_model=None,
                bridge_requirements=None, strategy="raa_a",
                reduced_confidence=False):
    return StrategySubgraphState(
        batch=batch or {"group_id": "test_batch", "asr_records": [], "non_asr_records": []},
        quality_weights=quality_weights or {},
        running_model=running_model or {},
        bridge_requirements=bridge_requirements or [],
        strategy=strategy,
        reduced_confidence=reduced_confidence,
    )


def _make_config(llm_key, llm):
    return {"configurable": {llm_key: llm}}


# ── Builder structure tests ──────────────────────────────────────────────────


class TestBuilderStructure:

    @pytest.mark.parametrize("builder_fn,expected_node", [
        (build_raa_a_subgraph, "extract_saam"),
        (build_raa_b_subgraph, "extract_patterns"),
        (build_raa_c_subgraph, "extract_entities"),
    ])
    def test_builder_returns_uncompiled_state_graph(self, builder_fn, expected_node):
        graph = builder_fn()
        assert isinstance(graph, StateGraph)
        # Compilation succeeds
        compiled = graph.compile()
        assert compiled is not None

    @pytest.mark.parametrize("builder_fn", [
        build_raa_a_subgraph,
        build_raa_b_subgraph,
        build_raa_c_subgraph,
    ])
    def test_compiled_graph_accepts_state_and_config(self, builder_fn):
        graph = builder_fn()
        compiled = graph.compile()
        state = _make_state()
        llm = _make_fake_structured_output()
        config = {"configurable": {"raa_a_llm": llm, "raa_b_llm": llm, "raa_c_llm": llm}}
        result = compiled.invoke(state, config)
        assert "arch_fragment" in result


# ── Structured extraction tests ──────────────────────────────────────────────


class TestStructuredExtraction:

    def test_raa_a_uses_raa_a_llm_key(self):
        graph = build_raa_a_subgraph()
        compiled = graph.compile()
        state = _make_state(strategy="raa_a")
        llm = _make_fake_structured_output(
            ArchFragment(entities=[C4Entity(id="e1", name="E", c4_type="system")])
        )
        config = _make_config("raa_a_llm", llm)
        result = compiled.invoke(state, config)
        assert isinstance(result["arch_fragment"], ArchFragment)
        assert len(result["arch_fragment"].entities) == 1

    def test_raa_b_uses_raa_b_llm_key(self):
        graph = build_raa_b_subgraph()
        compiled = graph.compile()
        state = _make_state(strategy="raa_b")
        llm = _make_fake_structured_output(
            ArchFragment(
                entities=[
                    C4Entity(id="sys1", name="S1", c4_type="system"),
                    C4Entity(id="sys2", name="S2", c4_type="system"),
                ],
                relationships=[
                    C4Relationship(id="r1", source_id="sys1", target_id="sys2"),
                ],
            )
        )
        config = _make_config("raa_b_llm", llm)
        result = compiled.invoke(state, config)
        assert len(result["arch_fragment"].relationships) == 1

    def test_raa_c_uses_raa_c_llm_key(self):
        graph = build_raa_c_subgraph()
        compiled = graph.compile()
        state = _make_state(strategy="raa_c")
        llm = _make_fake_structured_output(
            ArchFragment(metadata={"strategy": "raa_c", "extracted": True})
        )
        config = _make_config("raa_c_llm", llm)
        result = compiled.invoke(state, config)
        assert result["arch_fragment"].metadata.get("extracted") is True

    def test_no_llm_configured_returns_empty_fragment(self):
        graph = build_raa_a_subgraph()
        compiled = graph.compile()
        state = _make_state(strategy="raa_a")
        result = compiled.invoke(state, {})  # no config
        frag = result["arch_fragment"]
        assert isinstance(frag, ArchFragment)
        assert frag.entities == []
        assert frag.relationships == []


# ── Hierarchy enforcement in subgraphs ───────────────────────────────────────


class TestSubgraphHierarchyEnforcement:

    def test_orphan_container_excluded_and_question_emitted(self):
        """Subgraph with orphan container excludes it and returns open question."""
        graph = build_raa_a_subgraph()
        compiled = graph.compile()
        state = _make_state(
            strategy="raa_a",
            batch={"group_id": "b_orphan", "asr_records": [], "non_asr_records": []},
        )
        orphan_fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr_bad", name="Orphan", c4_type="container",
                         parent_system_id="missing"),
            ],
        )
        llm = _make_fake_structured_output(orphan_fragment)
        config = _make_config("raa_a_llm", llm)
        result = compiled.invoke(state, config)
        questions = result.get("open_questions", [])
        assert len(questions) >= 1
        assert any(q["reason"] == "orphan_container" for q in questions)
        # Cleaned fragment has no entities
        assert len(result["arch_fragment"].entities) == 0

    def test_valid_entities_pass_through(self):
        graph = build_raa_b_subgraph()
        compiled = graph.compile()
        state = _make_state(
            strategy="raa_b",
            batch={"group_id": "b_valid", "asr_records": [], "non_asr_records": []},
        )
        valid_fragment = ArchFragment(
            entities=[
                C4Entity(id="sys1", name="S", c4_type="system"),
                C4Entity(id="ctr1", name="C", c4_type="container",
                         parent_system_id="sys1"),
                C4Entity(id="comp1", name="Cmp", c4_type="component",
                         parent_container_id="ctr1"),
            ],
        )
        llm = _make_fake_structured_output(valid_fragment)
        config = _make_config("raa_b_llm", llm)
        result = compiled.invoke(state, config)
        assert len(result["arch_fragment"].entities) == 3
        assert result.get("open_questions", []) == []

    def test_scope_assigned_by_validator(self):
        graph = build_raa_c_subgraph()
        compiled = graph.compile()
        state = _make_state(
            strategy="raa_c",
            batch={"group_id": "b_scope", "asr_records": [], "non_asr_records": []},
        )
        fragment = ArchFragment(
            entities=[
                C4Entity(id="ctr1", name="C1", c4_type="container",
                         parent_system_id="sys_rm"),
                C4Entity(id="ctr2", name="C2", c4_type="container",
                         parent_system_id="sys_rm"),
            ],
            relationships=[
                C4Relationship(id="r1", source_id="ctr1", target_id="ctr2"),
            ],
        )
        running_model = {"systems": [{"id": "sys_rm"}]}
        llm = _make_fake_structured_output(fragment)
        config = _make_config("raa_c_llm", llm)
        result = compiled.invoke(
            {**state, "running_model": running_model}, config,
        )
        assert result["arch_fragment"].relationships[0].diagram_scope == "container"


# ── Open questions propagation ───────────────────────────────────────────────


class TestOpenQuestionsPropagation:

    def test_open_questions_in_subgraph_result(self):
        graph = build_raa_a_subgraph()
        compiled = graph.compile()
        state = _make_state(
            strategy="raa_a",
            batch={"group_id": "b_q", "asr_records": [], "non_asr_records": []},
        )
        fragment_with_orphan = ArchFragment(
            entities=[
                C4Entity(id="comp_orphan", name="O", c4_type="component",
                         parent_container_id="no_such_ctr"),
            ],
        )
        llm = _make_fake_structured_output(fragment_with_orphan)
        config = _make_config("raa_a_llm", llm)
        result = compiled.invoke(state, config)
        questions = result.get("open_questions", [])
        assert len(questions) >= 1
        q = questions[0]
        assert "entity_id" in q
        assert "suggested_resolution" in q

    def test_fragment_metadata_preserved_after_validation(self):
        graph = build_raa_b_subgraph()
        compiled = graph.compile()
        state = _make_state(strategy="raa_b")
        fragment = ArchFragment(
            entities=[],
            relationships=[],
            metadata={"source": "test", "version": 1},
        )
        llm = _make_fake_structured_output(fragment)
        config = _make_config("raa_b_llm", llm)
        result = compiled.invoke(state, config)
        assert result["arch_fragment"].metadata == {"source": "test", "version": 1}


# ── Fake raw parsing error handling ──────────────────────────────────────────


class TestParsingErrorHandling:

    def test_parsing_error_returns_empty_fragment(self):
        graph = build_raa_a_subgraph()
        compiled = graph.compile()
        state = _make_state(strategy="raa_a")

        class ErrorLLM:
            def with_structured_output(self, schema, include_raw=False):
                class ErrorRunnable:
                    def invoke(self, prompt):
                        return {"raw": {}, "parsed": None, "parsing_error": "bad json"}
                return ErrorRunnable()

        config = _make_config("raa_a_llm", ErrorLLM())
        result = compiled.invoke(state, config)
        frag = result["arch_fragment"]
        assert isinstance(frag, ArchFragment)
        assert frag.entities == []

    def test_direct_arch_fragment_handled(self):
        """When fake returns ArchFragment directly (not dict wrapper)."""
        graph = build_raa_a_subgraph()
        compiled = graph.compile()
        state = _make_state(strategy="raa_a")

        class DirectLLM:
            def with_structured_output(self, schema, include_raw=False):
                class DirectRunnable:
                    def invoke(self, prompt):
                        return ArchFragment(entities=[
                            C4Entity(id="e1", name="E", c4_type="system"),
                        ])
                return DirectRunnable()

        config = _make_config("raa_a_llm", DirectLLM())
        result = compiled.invoke(state, config)
        assert len(result["arch_fragment"].entities) == 1
