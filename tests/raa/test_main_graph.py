"""Unit tests for raa.graphs.main_graph — LangGraph skeleton compilation, gated
execution, sequential traversal, and reducer verification."""

from __future__ import annotations

from operator import add
from typing import Any
from unittest.mock import MagicMock

import pytest

from raa.graphs.main_graph import (
    NODE_BATCH_QUEUE_ORDERING,
    NODE_COHERENCE_GATE,
    NODE_CONSTRUCT_BATCHES,
    NODE_EMBEDDINGS_READY_GATE,
    NODE_OVERLAP_BRIDGING,
    NODE_PREPARE_EMBEDDINGS,
    build_raa_graph,
    compile_raa_graph,
    embeddings_ready_gate,
)
from raa.state.channels import RAAState, merge_batch_outputs, merge_best_batch_output


# ---------------------------------------------------------------------------
# Shared mock helpers (T014)
# ---------------------------------------------------------------------------

def _make_visited_tracker():
    """Return (visited, mock_nodes) where visited is a list each mock appends to."""
    visited: list[str] = []

    def _mock_prepare(state):
        visited.append("prepare_embeddings")
        return {"embeddings_ready": True}

    def _mock_construct(state):
        visited.append("construct_batches")
        return {"batch_queue": [{"id": "B1"}]}

    def _mock_bridging(state):
        visited.append("apply_overlap_bridging")
        return {"batch_queue": [{"id": "B1", "bridged": True}]}

    def _mock_coherence(state):
        visited.append("apply_coherence_gate")
        return {"batch_queue": [{"id": "B1", "bridged": True, "coherent": True}]}

    def _mock_ordering(state):
        visited.append("order_batch_queue")
        return {"batch_queue": [{"id": "B1", "bridged": True, "coherent": True, "order": 1}]}

    mock_nodes = {
        NODE_PREPARE_EMBEDDINGS: _mock_prepare,
        NODE_CONSTRUCT_BATCHES: _mock_construct,
        NODE_OVERLAP_BRIDGING: _mock_bridging,
        NODE_COHERENCE_GATE: _mock_coherence,
        NODE_BATCH_QUEUE_ORDERING: _mock_ordering,
    }
    return visited, mock_nodes


def _make_minimal_input(**overrides: Any) -> dict[str, Any]:
    """Return a minimal input dict that satisfies RAAState."""
    data: dict[str, Any] = {"embeddings_ready": True}
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# T015 — build_raa_graph returns a StateGraph with RAAState
# ---------------------------------------------------------------------------

def test_build_raa_graph_returns_state_graph_with_raa_state():
    """build_raa_graph() returns a langgraph StateGraph built with RAAState."""
    from langgraph.graph import StateGraph

    graph = build_raa_graph()
    assert isinstance(graph, StateGraph)
    # StateGraph stores the schema internally; the builder's channels reflect it.
    compiled = graph.compile()
    # All RAAState keys must be present as channels
    raa_keys = set(RAAState.__annotations__)
    channel_keys = set(compiled.channels.keys())
    assert raa_keys <= channel_keys, f"Missing channels: {raa_keys - channel_keys}"


# ---------------------------------------------------------------------------
# T016 — compile_raa_graph returns invokable graph without LLM/checkpointer
# ---------------------------------------------------------------------------

def test_compile_raa_graph_returns_invokable_without_checkpointer():
    """compile_raa_graph() compiles and returns an invokable graph."""
    _, mock_nodes = _make_visited_tracker()
    app = compile_raa_graph(node_overrides=mock_nodes)
    result = app.invoke(_make_minimal_input())
    assert "batch_queue" in result


# ---------------------------------------------------------------------------
# T017 — Graph edges run nodes in the expected order
# ---------------------------------------------------------------------------

def test_graph_executes_nodes_in_expected_order():
    """Nodes must run: prepare -> gate -> construct -> bridging -> coherence -> ordering -> END."""
    visited, mock_nodes = _make_visited_tracker()
    app = compile_raa_graph(node_overrides=mock_nodes)
    app.invoke(_make_minimal_input())

    expected = [
        "prepare_embeddings",
        "construct_batches",
        "apply_overlap_bridging",
        "apply_coherence_gate",
        "order_batch_queue",
    ]
    assert visited == expected, f"Execution order: {visited}"


# ---------------------------------------------------------------------------
# T018 — Final output includes the ordered batch_queue
# ---------------------------------------------------------------------------

def test_graph_outputs_ordered_batch_queue():
    """Invoking the graph with mocked nodes returns the ordering mock's batch_queue."""
    _, mock_nodes = _make_visited_tracker()
    app = compile_raa_graph(node_overrides=mock_nodes)
    result = app.invoke(_make_minimal_input())
    expected = [{"id": "B1", "bridged": True, "coherent": True, "order": 1}]
    assert result["batch_queue"] == expected


# ---------------------------------------------------------------------------
# T019 — embeddings_ready_gate raises ValueError
# ---------------------------------------------------------------------------

def test_embeddings_ready_gate_raises_on_false():
    """Gate raises ValueError when embeddings_ready is False."""
    with pytest.raises(ValueError, match="embeddings_ready"):
        embeddings_ready_gate({"embeddings_ready": False})  # type: ignore[arg-type]


def test_embeddings_ready_gate_raises_on_missing():
    """Gate raises ValueError when embeddings_ready key is missing."""
    with pytest.raises(ValueError, match="embeddings_ready"):
        embeddings_ready_gate({})  # type: ignore[arg-type]


def test_embeddings_ready_gate_passes_when_true():
    """Gate returns empty dict when embeddings_ready is True."""
    result = embeddings_ready_gate({"embeddings_ready": True})  # type: ignore[arg-type]
    assert result == {}


# ---------------------------------------------------------------------------
# T020 — Graph does not continue past gate on failure
# ---------------------------------------------------------------------------

def test_graph_halt_on_embeddings_not_ready():
    """When prepare returns embeddings_ready=False, graph halts at the gate."""
    _, mock_nodes = _make_visited_tracker()

    # Override prepare to return False
    def _fail_prepare(state):
        return {"embeddings_ready": False}

    mock_nodes[NODE_PREPARE_EMBEDDINGS] = _fail_prepare
    app = compile_raa_graph(node_overrides=mock_nodes)

    with pytest.raises(ValueError, match="embeddings_ready"):
        app.invoke(_make_minimal_input())


# ---------------------------------------------------------------------------
# T021 — node_overrides injects mock callables
# ---------------------------------------------------------------------------

def test_node_overrides_injects_mock_callables():
    """build_raa_graph(node_overrides=...) replaces default nodes with mocks."""
    mock = MagicMock(return_value={"embeddings_ready": True, "batch_queue": [{"id": "X"}]})

    overrides = {
        NODE_PREPARE_EMBEDDINGS: mock,
        NODE_CONSTRUCT_BATCHES: mock,
        NODE_OVERLAP_BRIDGING: mock,
        NODE_COHERENCE_GATE: mock,
        NODE_BATCH_QUEUE_ORDERING: mock,
    }

    app = compile_raa_graph(node_overrides=overrides)
    app.invoke(_make_minimal_input())
    # Each node called once + gate is real (not mocked) => 5 mock calls
    assert mock.call_count == 5


# ---------------------------------------------------------------------------
# T022 — Overwrite channel introspection
# ---------------------------------------------------------------------------

def test_compiled_overwrite_channels():
    """batch_queue, batch_cursor, running_arch_model, bridge_requirements,
    embeddings_ready must be LangGraph overwrite channels."""
    from langgraph.channels.last_value import LastValue

    app = compile_raa_graph()
    channels = app.channels

    overwrite_keys = [
        "batch_queue",
        "batch_cursor",
        "running_arch_model",
        "bridge_requirements",
        "embeddings_ready",
    ]
    for key in overwrite_keys:
        assert key in channels, f"Missing channel: {key}"
        assert isinstance(channels[key], LastValue), (
            f"{key} is {type(channels[key]).__name__}, expected LastValue"
        )


# ---------------------------------------------------------------------------
# T023 — Append reducer introspection
# ---------------------------------------------------------------------------

def test_compiled_append_channels_use_operator_add():
    """open_questions and incoherent_batches must use operator.add append reducer."""
    app = compile_raa_graph()
    channels = app.channels

    for key in ("open_questions", "incoherent_batches"):
        assert key in channels, f"Missing channel: {key}"
        channel = channels[key]
        # operator.add channels are BinaryOperatorAggregate in langgraph
        assert hasattr(channel, "operator"), (
            f"{key} has no operator attr — not an append channel"
        )
        assert channel.operator is add, (
            f"{key} operator is {channel.operator}, expected operator.add"
        )


# ---------------------------------------------------------------------------
# T024 — Dict-merge reducer introspection
# ---------------------------------------------------------------------------

def test_compiled_dict_merge_channels():
    """batch_outputs uses merge_batch_outputs, best_batch_output uses merge_best_batch_output."""
    app = compile_raa_graph()
    channels = app.channels

    assert "batch_outputs" in channels
    batch_outputs_ch = channels["batch_outputs"]
    assert hasattr(batch_outputs_ch, "operator"), (
        "batch_outputs has no operator — expected BinaryOperatorAggregate"
    )
    assert batch_outputs_ch.operator is merge_batch_outputs, (
        f"batch_outputs operator is {batch_outputs_ch.operator}, expected merge_batch_outputs"
    )

    assert "best_batch_output" in channels
    best_ch = channels["best_batch_output"]
    assert hasattr(best_ch, "operator"), (
        "best_batch_output has no operator — expected BinaryOperatorAggregate"
    )
    assert best_ch.operator is merge_best_batch_output, (
        f"best_batch_output operator is {best_ch.operator}, expected merge_best_batch_output"
    )


# ---------------------------------------------------------------------------
# T025 — No LLM, embedding vectors, normalized_requirements, or batches as channels
# ---------------------------------------------------------------------------

def test_graph_excludes_out_of_scope_channels():
    """Compiled graph must NOT contain LLM instances, embedding vectors,
    normalized_requirements, or batches as state channels."""
    app = compile_raa_graph()
    channel_keys = set(app.channels.keys())

    forbidden = {"llm", "embeddings", "embedding_vectors", "normalized_requirements", "batches"}
    found = forbidden & channel_keys
    assert not found, f"Forbidden channels present: {found}"


# ---------------------------------------------------------------------------
# T042 — Compiled channel set matches RAAState + LangGraph internals
# ---------------------------------------------------------------------------

def test_channel_set_matches_raa_state_plus_internals():
    """All RAAState keys are channels; no extra user-defined channels exist."""
    app = compile_raa_graph()
    channel_keys = set(app.channels.keys())

    raa_keys = set(RAAState.__annotations__)

    # LangGraph internal channels: __pregel_*, branch:*, channel:*, ...
    internals = {
        k for k in channel_keys
        if k.startswith("__") or k.startswith("branch:") or k.startswith("channel:")
    }

    user_channels = channel_keys - internals
    assert raa_keys == user_channels, (
        f"User channels {user_channels} != RAAState keys {raa_keys}"
    )
