"""RAA pipeline runner.

Entry point for orchestrator invocation. Handles fresh-start vs resume
detection, graph compilation with checkpointer, corrupt checkpoint fallback,
archive policy, and final output dispatch.
"""

from __future__ import annotations

import hashlib
import logging
import shutil
import sqlite3
from pathlib import Path
from typing import Any, Callable

from raa.graphs.main_graph import compile_for_production

logger = logging.getLogger(__name__)


# ---- Thread ID derivation --------------------------------------------------


def derive_thread_id(arlo_output_version_hash: str, run_label: str = "default") -> str:
    """Derive a deterministic thread ID from the ARLO output version hash.

    Returns a string formatted as ``raa-{sha256[:16]}``.
    """
    payload = f"{arlo_output_version_hash}:{run_label}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:16]
    return f"raa-{digest}"


# ---- Run configuration ------------------------------------------------------


def build_run_config(
    thread_id: str, context: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Build a LangGraph run configuration dict.

    Returns ``{"configurable": {"thread_id": thread_id}, "context": context}``.
    """
    config: dict[str, Any] = {"configurable": {"thread_id": thread_id}}
    if context is not None:
        config["context"] = context
    return config


# ---- Resume detection -------------------------------------------------------


def should_resume_from_snapshot(snapshot: Any) -> bool:
    """Return True when the checkpoint snapshot indicates a resumable run.

    A run is resumable when ``batch_cursor > 0``.
    """
    if snapshot is None:
        return False
    values = getattr(snapshot, "values", None) or {}
    return values.get("batch_cursor", 0) > 0


# ---- Corrupt checkpoint handling --------------------------------------------


def _preserve_corrupt_checkpoint(db_path: str) -> None:
    """Rename a corrupt checkpoint database to ``{db_path}.corrupted``."""
    corrupt_path = f"{db_path}.corrupted"
    logger.warning(
        "Preserving corrupt checkpoint: renaming %s -> %s", db_path, corrupt_path
    )
    shutil.move(db_path, corrupt_path)


# ---- Archive policy ---------------------------------------------------------


def archive_checkpoint(db_path: str, project_name: str, thread_id: str) -> str:
    """Archive the active checkpoint database after a successful run.

    Moves the database from the active checkpoints directory into
    ``archive/{thread_id}/`` under the same checkpoints directory.

    Returns the archive path.
    """
    db_path = Path(db_path)
    archive_dir = db_path.parent / "archive" / thread_id
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / db_path.name
    shutil.move(str(db_path), str(archive_path))
    logger.info(
        "Archived checkpoint for project '%s' thread '%s' -> %s",
        project_name,
        thread_id,
        archive_path,
    )
    return str(archive_path)


def archive_after_success(
    result: dict[str, Any],
    db_path: str,
    project_name: str,
    thread_id: str,
) -> str | None:
    """Archive the checkpoint database only when the final merge result is valid.

    Returns the archive path if archiving occurred, or None if skipped.
    """
    # Archive only when the final merge node has validated the output and
    # arch_model.json has been written (indicated by "arch_model_written" in
    # the result state).
    if not result.get("arch_model_written", False):
        logger.info(
            "Skipping archive: final merge output not validated "
            "or arch_model.json not written."
        )
        return None

    if not Path(db_path).exists():
        logger.warning(
            "Skipping archive: checkpoint database not found at %s", db_path
        )
        return None

    return archive_checkpoint(db_path, project_name, thread_id)


# ---- Recovery wrapper -------------------------------------------------------


def run_with_recovery(
    graph: Any,
    initial_state: dict[str, Any],
    run_config: dict[str, Any],
    *,
    db_path: str,
    compile_graph_factory: Callable[[], Any] | None = None,
) -> dict[str, Any]:
    """Execute the graph with checkpoint-aware resume and corrupt-fallback logic.

    1. Query the checkpointer via ``graph.get_state(run_config)``.
    2. If the state shows ``batch_cursor > 0``, resume with ``None`` input.
    3. If no resumable state exists, start fresh with *initial_state*.
    4. On checkpoint corruption, preserve the corrupt database, recompile,
       and start fresh.

    Args:
        graph: A compiled LangGraph app with a checkpointer attached.
        initial_state: The full RAA initial state payload for fresh starts.
        run_config: The run configuration dict (must include
            ``configurable.thread_id``).
        db_path: Path to the active SQLite checkpoint database.
        compile_graph_factory: Optional callable that returns a freshly
            compiled graph (used after corrupt checkpoint fallback). When
            omitted and the database is corrupt, the original *graph* is
            reused after the corrupt database is renamed (a new database
            will be created by the checkpointer on next write).

    Returns:
        The final graph state after invocation.
    """
    try:
        state = graph.get_state(run_config)
    except (sqlite3.DatabaseError, Exception) as exc:
        logger.warning(
            "Checkpoint DB corruption detected at %s: %s. "
            "Falling back to fresh start.",
            db_path,
            exc,
        )
        _preserve_corrupt_checkpoint(db_path)
        if compile_graph_factory is not None:
            graph = compile_graph_factory()
        state = None

    if state is not None and should_resume_from_snapshot(state):
        thread_id = run_config.get("configurable", {}).get("thread_id", "unknown")
        cursor = state.values.get("batch_cursor", 0) if state.values else 0
        logger.info(
            "Resuming RAA pipeline from checkpoint "
            "(thread_id=%s, batch_cursor=%s)",
            thread_id,
            cursor,
        )
        return graph.invoke(None, run_config)

    logger.info("Starting fresh RAA pipeline run.")
    return graph.invoke(initial_state, run_config)


# ---- Public entrypoint ------------------------------------------------------


def run_raa_pipeline(
    initial_state: dict[str, Any],
    arlo_output_version_hash: str,
    db_path: str,
    project_name: str,
    *,
    run_label: str = "default",
    context: dict[str, Any] | None = None,
    node_overrides: dict[str, Callable[..., Any]] | None = None,
) -> dict[str, Any]:
    """Public entrypoint for the RAA pipeline.

    Compiles the production graph with SQLite checkpointing, derives a
    deterministic thread ID, handles resume vs fresh-start, and archives
    the checkpoint database after a successful run.

    Args:
        initial_state: The full RAA initial state payload.
        arlo_output_version_hash: ARLO output version hash for deterministic
            thread ID derivation.
        db_path: Absolute path to the orchestrator-provided SQLite database.
        project_name: Project name used for archive path construction.
        run_label: Run label incorporated into the thread ID (default
            ``"default"``).
        context: Optional runtime context (LLM instances etc.) passed to
            the graph invocation.
        node_overrides: Optional node callable overrides for testing.

    Returns:
        The final RAA graph state after completion.
    """
    graph = compile_for_production(db_path=db_path, node_overrides=node_overrides)
    thread_id = derive_thread_id(arlo_output_version_hash, run_label)
    run_config = build_run_config(thread_id, context)

    # Factory for recompilation after corrupt fallback
    def _recompile():
        return compile_for_production(
            db_path=db_path, node_overrides=node_overrides
        )

    result = run_with_recovery(
        graph,
        initial_state,
        run_config,
        db_path=db_path,
        compile_graph_factory=_recompile,
    )

    archive_after_success(result, db_path, project_name, thread_id)
    return result
