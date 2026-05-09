"""
Graph compilation, checkpointing, and execution utilities.

Provides factory functions for compiling the ARLO graph with
different persistence backends (development vs. production).
"""
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Any, Literal

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from arlo.graphs.core import build_arlo_subgraph

logger = logging.getLogger(__name__)

Durability = Literal["sync", "async", "exit"]
DEFAULT_DURABILITY: Durability = "sync"


def _thread_config(thread_id: str) -> dict:
    """Build the LangGraph checkpoint config for one logical ARLO run."""
    if not thread_id:
        raise ValueError("thread_id is required when using checkpointing.")
    return {"configurable": {"thread_id": thread_id}}


# ---------------------------------------------------------------------------
# Graph Compilation
# ---------------------------------------------------------------------------
def compile_for_development():
    """Compile the ARLO graph with in-memory checkpointing (dev/test only).

    Uses InMemorySaver — state does NOT survive process restarts.
    Suitable for unit tests and rapid iteration.
    """
    builder = build_arlo_subgraph()
    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)


def compile_for_production(
    db_path: str | Path = "checkpoints/arlo.db",
):
    """Compile the ARLO graph with SQLite checkpointing (production).

    Uses SqliteSaver — state survives crashes and process restarts.

    Args:
        db_path: Path to the SQLite database file. Parent directories
                 will be created if they don't exist.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    builder = build_arlo_subgraph()
    # `check_same_thread=False` is required because LangGraph fan-out can
    # checkpoint from worker threads.
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    checkpointer.setup()
    return builder.compile(checkpointer=checkpointer)


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------
def run_arlo(
    graph,
    *,
    requirements: dict[str, str],
    experiment_config: dict,
    matrix: dict[str, dict[str, int]],
    llm: Any,
    thread_id: str,
    durability: Durability = DEFAULT_DURABILITY,
) -> dict:
    """Execute the ARLO graph with durable checkpointing.

    Args:
        graph: Compiled ARLO StateGraph.
        requirements: Mapping of Requirement ID → description.
        experiment_config: Experiment configuration dict.
        matrix: Quality–architecture pattern matrix.
        llm: Pre-instantiated LangChain LLM instance. Passed through runtime
             context so it is not serialized into checkpoints.
        thread_id: Unique thread identifier for checkpointing.
        durability: LangGraph checkpoint durability mode. Use "sync" for
                    maximum crash resilience on the pinned LangGraph version.

    Returns:
        The ARLOOutput dict (concerns, stats, asrs, quality_weights).
    """
    initial_state = {
        "requirements": requirements,
        "experiment_config": experiment_config,
        "matrix": matrix,
    }

    return graph.invoke(
        initial_state,
        _thread_config(thread_id),
        context={"llm": llm},
        durability=durability,
    )


def resume_arlo(
    graph,
    *,
    thread_id: str,
    llm: Any,
    durability: Durability = DEFAULT_DURABILITY,
) -> dict:
    """Resume a previously interrupted ARLO run from its last checkpoint.

    Call this with the same thread_id after a crash.

    Args:
        graph: Compiled ARLO StateGraph (same as original run).
        thread_id: The thread_id from the interrupted run.
        llm: Runtime LLM dependency. Required because `llm` is intentionally
             not stored in checkpointed graph state.
        durability: LangGraph checkpoint durability mode.

    Returns:
        The ARLOOutput dict.
    """
    logger.info("Resuming ARLO run for thread_id=%s", thread_id)
    return graph.invoke(
        None,
        _thread_config(thread_id),
        context={"llm": llm},
        durability=durability,
    )
