"""RAA main LangGraph skeleton.

Wires the Section 3 pipeline steps 1-5: Preparation -> Batch Construction ->
Overlap Bridging -> Coherence Gate -> Batch Queue Ordering.

Steps 6 (execution loop) and 7 (final merge) are documented but NOT wired here
— they belong to future downstream graph phases.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Any, Callable

from langgraph.graph import END, START, StateGraph

from raa.state.channels import RAAState

logger = logging.getLogger(__name__)

# ---- Node name constants ---------------------------------------------------

NODE_PREPARE_EMBEDDINGS = "prepare_embeddings"
NODE_EMBEDDINGS_READY_GATE = "embeddings_ready_gate"
NODE_CONSTRUCT_BATCHES = "construct_batches"
NODE_OVERLAP_BRIDGING = "apply_overlap_bridging"
NODE_COHERENCE_GATE = "apply_coherence_gate"
NODE_BATCH_QUEUE_ORDERING = "order_batch_queue"

# All seven Section 3 steps; 6 and 7 are not wired by this skeleton.
SECTION_3_PIPELINE_STEPS: list[str] = [
    NODE_PREPARE_EMBEDDINGS,
    NODE_CONSTRUCT_BATCHES,
    NODE_OVERLAP_BRIDGING,
    NODE_COHERENCE_GATE,
    NODE_BATCH_QUEUE_ORDERING,
    "execute_batch_subgraphs",  # step 6 — future phase
    "final_merge",  # step 7 — future phase
]

# ---- Gate ------------------------------------------------------------------


def embeddings_ready_gate(state: RAAState) -> dict[str, Any]:
    """Return {} only when embeddings are ready; otherwise raise ValueError."""
    if not state.get("embeddings_ready", False):
        raise ValueError(
            "embeddings_ready is False or missing — ASR/non-ASR embeddings "
            "must be available before the RAA pipeline proceeds."
        )
    return {}


# ---- Node resolution -------------------------------------------------------


def _default_node_map() -> dict[str, Callable[..., Any]]:
    """Return the production node callables for steps 1-5."""
    from raa.nodes import (  # noqa: PLC0415 — lazy import avoids circular deps
        apply_coherence_gate,
        apply_overlap_bridging,
        construct_batches,
        order_batch_queue,
        prepare_embeddings,
    )

    return {
        NODE_PREPARE_EMBEDDINGS: prepare_embeddings,
        NODE_CONSTRUCT_BATCHES: construct_batches,
        NODE_OVERLAP_BRIDGING: apply_overlap_bridging,
        NODE_COHERENCE_GATE: apply_coherence_gate,
        NODE_BATCH_QUEUE_ORDERING: order_batch_queue,
    }


def _resolve_node_map(
    node_overrides: dict[str, Callable[..., Any]] | None,
) -> dict[str, Callable[..., Any]]:
    """Merge user-supplied overrides on top of the default production nodes."""
    nodes = _default_node_map()
    if node_overrides:
        nodes.update(node_overrides)
    return nodes


# ---- Graph construction ----------------------------------------------------


def build_raa_graph(
    node_overrides: dict[str, Callable[..., Any]] | None = None,
) -> StateGraph:
    """Build the main RAA StateGraph wired to Section 3 steps 1-5.

    Args:
        node_overrides: Optional mapping of node name to callable. Use this
            in tests to inject mock nodes without patching module globals.

    Returns:
        An uncompiled langgraph StateGraph built with RAAState.
    """
    nodes = _resolve_node_map(node_overrides)

    graph = StateGraph(RAAState)

    graph.add_node(NODE_PREPARE_EMBEDDINGS, nodes[NODE_PREPARE_EMBEDDINGS])
    graph.add_node(NODE_EMBEDDINGS_READY_GATE, embeddings_ready_gate)
    graph.add_node(NODE_CONSTRUCT_BATCHES, nodes[NODE_CONSTRUCT_BATCHES])
    graph.add_node(NODE_OVERLAP_BRIDGING, nodes[NODE_OVERLAP_BRIDGING])
    graph.add_node(NODE_COHERENCE_GATE, nodes[NODE_COHERENCE_GATE])
    graph.add_node(NODE_BATCH_QUEUE_ORDERING, nodes[NODE_BATCH_QUEUE_ORDERING])

    # Fixed linear edges: preparation -> gate -> construction -> bridging ->
    # coherence -> ordering -> END
    graph.add_edge(START, NODE_PREPARE_EMBEDDINGS)
    graph.add_edge(NODE_PREPARE_EMBEDDINGS, NODE_EMBEDDINGS_READY_GATE)
    graph.add_edge(NODE_EMBEDDINGS_READY_GATE, NODE_CONSTRUCT_BATCHES)
    graph.add_edge(NODE_CONSTRUCT_BATCHES, NODE_OVERLAP_BRIDGING)
    graph.add_edge(NODE_OVERLAP_BRIDGING, NODE_COHERENCE_GATE)
    graph.add_edge(NODE_COHERENCE_GATE, NODE_BATCH_QUEUE_ORDERING)
    graph.add_edge(NODE_BATCH_QUEUE_ORDERING, END)

    return graph


# ---- Compilation -----------------------------------------------------------


def compile_raa_graph(
    node_overrides: dict[str, Callable[..., Any]] | None = None,
    checkpointer: object | None = None,
):
    """Build and compile the RAA graph.

    Args:
        node_overrides: Optional node callable overrides for testing.
        checkpointer: Optional LangGraph checkpointer. When provided, passed
            to ``StateGraph.compile(checkpointer=checkpointer)``.

    Returns:
        A compiled, invokable LangGraph app.
    """
    graph = build_raa_graph(node_overrides)
    if checkpointer is not None:
        return graph.compile(checkpointer=checkpointer)
    return graph.compile()


# ---- Production compilation with SQLite checkpointing -----------------------


def _validate_db_path(db_path: str) -> None:
    """Validate that the orchestrator-provided SQLite database path is usable.

    Raises ValueError when *db_path* is empty or its parent directory does
    not exist (directory creation is the orchestrator's responsibility per
    Section 22A).
    """
    if not db_path:
        raise ValueError("db_path must be a non-empty string")
    parent = Path(db_path).parent
    if not parent.exists():
        raise ValueError(
            f"Parent directory does not exist for db_path: {db_path}. "
            f"The orchestrator must create the directory before invoking RAA."
        )


def _open_sqlite_checkpointer(db_path: str):
    """Open a SqliteSaver checkpointer on *db_path* with WAL journal mode.

    Returns a ready-to-use ``SqliteSaver`` instance.
    """
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    from langgraph.checkpoint.sqlite import SqliteSaver  # noqa: PLC0415

    checkpointer = SqliteSaver(conn)
    checkpointer.setup()
    return checkpointer


def compile_for_production(
    db_path: str,
    node_overrides: dict[str, Callable[..., Any]] | None = None,
    durability: str = "sync",
):
    """Build and compile the RAA graph with a SQLite checkpointer.

    Args:
        db_path: Absolute path to the orchestrator-provided SQLite database.
            The parent directory must already exist.
        node_overrides: Optional node callable overrides (for testing).
        durability: Checkpoint durability mode (default ``"sync"``).

    Returns:
        A compiled LangGraph app with ``SqliteSaver`` as its checkpointer.
    """
    _ = durability  # reserved for future SqliteSaver durability config
    _validate_db_path(db_path)
    checkpointer = _open_sqlite_checkpointer(db_path)
    graph = build_raa_graph(node_overrides)
    return graph.compile(checkpointer=checkpointer)
