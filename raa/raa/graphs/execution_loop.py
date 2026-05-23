"""
Phase 6 node: Concurrency orchestrator and parallel subgraph dispatch (FR-7, FR-8, FR-9).

Dispatches coherent batches to RAA-A/B/C concurrently and routes reduced-confidence
batches to RAA-A only. Each subgraph gets an isolated SQLite WAL checkpointer.
"""
from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import Any

import aiosqlite
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph

from raa.state.models import ArchFragment
from raa.state.schemas import RAAState
from raa.subgraphs.raa_a import build_raa_a_subgraph
from raa.subgraphs.raa_b import build_raa_b_subgraph
from raa.subgraphs.raa_c import build_raa_c_subgraph
from raa.subgraphs.schemas import StrategySubgraphInput

logger = logging.getLogger(__name__)

_STRATEGIES = ("raa_a", "raa_b", "raa_c")
_BUILDERS = {
    "raa_a": build_raa_a_subgraph,
    "raa_b": build_raa_b_subgraph,
    "raa_c": build_raa_c_subgraph,
}


# ── Checkpoint helpers ─────────────────────────────────────────────────────


async def _create_wal_checkpointer(db_path: str) -> AsyncSqliteSaver:
    """Open an aiosqlite connection, enable WAL mode, and wrap in AsyncSqliteSaver."""
    if db_path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = await aiosqlite.connect(db_path)
    await conn.execute("PRAGMA journal_mode=WAL")
    await conn.commit()
    saver = AsyncSqliteSaver(conn)
    await saver.setup()
    return saver


def _derive_role_paths(base_path: str) -> dict[str, str]:
    """Derive three role-specific checkpoint paths from a base path.

    e.g. ``raa_checkpoint.db`` →
      - ``raa_checkpoint_raa_a.db``
      - ``raa_checkpoint_raa_b.db``
      - ``raa_checkpoint_raa_c.db``
    """
    if base_path == ":memory:":
        return {
            "raa_a": ":memory:",
            "raa_b": ":memory:",
            "raa_c": ":memory:",
        }
    p = Path(base_path)
    stem = p.stem
    suffix = p.suffix
    parent = p.parent
    return {
        "raa_a": str(parent / f"{stem}_raa_a{suffix}"),
        "raa_b": str(parent / f"{stem}_raa_b{suffix}"),
        "raa_c": str(parent / f"{stem}_raa_c{suffix}"),
    }


def _resolve_checkpoint_paths(configurable: dict) -> dict[str, str]:
    """Resolve per-role checkpoint DB paths from configurable.

    Prefers explicit per-role keys; falls back to deriving from ``checkpoint_db_path``.
    """
    paths: dict[str, str] = {}
    for role in _STRATEGIES:
        key = f"{role}_checkpoint_db_path"
        if key in configurable:
            paths[role] = configurable[key]

    if len(paths) == 3:
        return paths

    if "checkpoint_db_path" not in configurable:
        raise KeyError(
            "Missing required configurable key: 'checkpoint_db_path' "
            "(or provide explicit raa_a_checkpoint_db_path, raa_b_checkpoint_db_path, "
            "raa_c_checkpoint_db_path)"
        )

    derived = _derive_role_paths(configurable["checkpoint_db_path"])
    for role in _STRATEGIES:
        if role not in paths:
            paths[role] = derived[role]
    return paths


# ── Private input builder ──────────────────────────────────────────────────


def _build_private_input(
    batch: dict,
    state: RAAState,
    strategy: str,
) -> StrategySubgraphInput:
    """Map parent state into private StrategySubgraphInput for a subgraph."""
    bridge_requirements = [
        br for br in (state.get("bridge_requirements") or [])
        if batch["group_id"] in br.get("batch_ids", [])
    ]
    return StrategySubgraphInput(
        batch=batch,
        quality_weights=state.get("quality_weights") or {},
        running_model=state.get("arch_model") or {},
        bridge_requirements=bridge_requirements,
        strategy=strategy,
        reduced_confidence=bool(batch.get("reduced_confidence", False)),
    )


# ── Output normalization ───────────────────────────────────────────────────


def _normalize_output(
    batch: dict,
    batch_index: int,
    strategy: str,
    child_thread_id: str,
    reduced_confidence: bool,
    result: dict | None,
    skipped: bool = False,
    skip_reason: str | None = None,
) -> dict:
    """Normalize a subgraph result into the standard output record shape."""
    if skipped:
        return {
            "batch_id": batch["group_id"],
            "batch_index": batch_index,
            "strategy": strategy,
            "thread_id": child_thread_id,
            "reduced_confidence": reduced_confidence,
            "arch_fragment": None,
            "skipped": True,
            "skip_reason": skip_reason,
        }

    arch_fragment = None
    if result is not None:
        frag = result.get("arch_fragment")
        if isinstance(frag, ArchFragment):
            arch_fragment = frag.model_dump()
        elif isinstance(frag, dict):
            arch_fragment = frag
        else:
            arch_fragment = result

    return {
        "batch_id": batch["group_id"],
        "batch_index": batch_index,
        "strategy": strategy,
        "thread_id": child_thread_id,
        "reduced_confidence": bool(reduced_confidence),
        "arch_fragment": arch_fragment,
        "skipped": False,
        "skip_reason": None,
    }


# ── Strategy invocation ────────────────────────────────────────────────────


async def _invoke_strategy(
    strategy: str,
    private_input: StrategySubgraphInput,
    child_config: RunnableConfig,
    compiled_graph,
    *,
    close_checkpointer: bool = False,
    saver: AsyncSqliteSaver | None = None,
) -> dict:
    """Invoke a single compiled subgraph asynchronously."""
    try:
        return await compiled_graph.ainvoke(private_input, child_config)
    finally:
        if close_checkpointer and saver is not None:
            try:
                await saver.conn.close()
            except Exception:
                pass


# ── Main dispatch node ─────────────────────────────────────────────────────


async def dispatch_strategy_subgraphs(
    state: RAAState, config: RunnableConfig | None = None
) -> dict:
    """Select the current batch and dispatch to strategy subgraphs.

    Config keys expected in ``config["configurable"]``:
        ``thread_id``, ``checkpoint_db_path`` (or per-role paths)

    Injected keys (optional, for testing):
        ``raa_a_graph``, ``raa_b_graph``, ``raa_c_graph``

    Returns:
        dict with key ``batch_outputs`` — list of output records.
    """
    if config is None:
        config = {}
    configurable = config.get("configurable")
    if configurable is None:
        raise KeyError("RunnableConfig is missing 'configurable' key")

    thread_id = configurable.get("thread_id")
    if not thread_id:
        raise KeyError("Missing required configurable key: 'thread_id'")

    execution_queue = state.get("execution_queue") or []
    if not execution_queue:
        raise ValueError("execution_queue is missing or empty")

    batch_cursor = state.get("batch_cursor", 0)
    if not isinstance(batch_cursor, int) or batch_cursor < 0:
        raise ValueError(
            f"batch_cursor must be a non-negative integer, got {batch_cursor!r}"
        )
    if batch_cursor >= len(execution_queue):
        raise ValueError(
            f"batch_cursor {batch_cursor} is out of range for execution_queue "
            f"of length {len(execution_queue)}"
        )

    batch = execution_queue[batch_cursor]
    reduced_confidence = bool(batch.get("reduced_confidence", False))
    batch_index = batch_cursor

    # Check for injected compiled graphs (test support)
    injected_graphs: dict[str, Any] = {}
    for role in _STRATEGIES:
        key = f"{role}_graph"
        if key in configurable:
            injected_graphs[role] = configurable[key]

    output_records: list[dict] = []

    if reduced_confidence:
        # ── Reduced-confidence path: RAA-A only ──────────────────────────
        strategies_to_run = ["raa_a"]
        skipped_strategies = ["raa_b", "raa_c"]
    else:
        strategies_to_run = list(_STRATEGIES)
        skipped_strategies = []

    # Build tasks for strategies to run
    tasks: dict[str, asyncio.Task] = {}
    savers: dict[str, AsyncSqliteSaver] = {}

    try:
        if not injected_graphs:
            checkpoint_paths = _resolve_checkpoint_paths(configurable)

        for strategy in strategies_to_run:
            child_thread_id = f"{thread_id}:{batch_index}:{strategy}"
            child_config: RunnableConfig = {
                "configurable": {
                    "thread_id": child_thread_id,
                }
            }
            # Pass through LLM slots if present
            for llm_key in ("raa_a_llm", "raa_b_llm", "raa_c_llm", "judge_llm"):
                if llm_key in configurable:
                    child_config["configurable"][llm_key] = configurable[llm_key]

            private_input = _build_private_input(batch, state, strategy)

            if strategy in injected_graphs:
                compiled = injected_graphs[strategy]
                tasks[strategy] = asyncio.create_task(
                    _invoke_strategy(strategy, private_input, child_config, compiled)
                )
            else:
                db_path = checkpoint_paths[strategy]
                saver = await _create_wal_checkpointer(db_path)
                savers[strategy] = saver
                builder = _BUILDERS[strategy]()
                compiled = builder.compile(checkpointer=saver)
                tasks[strategy] = asyncio.create_task(
                    _invoke_strategy(strategy, private_input, child_config, compiled,
                                     close_checkpointer=True, saver=saver)
                )

        # Gather results concurrently
        results: dict[str, dict] = {}
        if tasks:
            gathered = await asyncio.gather(*tasks.values(), return_exceptions=True)
            for strategy, result in zip(tasks.keys(), gathered):
                if isinstance(result, Exception):
                    logger.error("Strategy %s failed: %s", strategy, result)
                    results[strategy] = {"error": str(result)}
                else:
                    results[strategy] = result
    finally:
        # Close all savers to prevent connection leaks
        for saver in savers.values():
            if saver is not None:
                try:
                    await saver.conn.close()
                except Exception:
                    pass

    # Normalize results for strategies that ran
    for strategy in strategies_to_run:
        result = results.get(strategy)
        child_thread_id = f"{thread_id}:{batch_index}:{strategy}"
        record = _normalize_output(
            batch=batch,
            batch_index=batch_index,
            strategy=strategy,
            child_thread_id=child_thread_id,
            reduced_confidence=reduced_confidence,
            result=result,
        )
        output_records.append(record)

    # Add skip records for skipped strategies
    for strategy in skipped_strategies:
        child_thread_id = f"{thread_id}:{batch_index}:{strategy}"
        record = _normalize_output(
            batch=batch,
            batch_index=batch_index,
            strategy=strategy,
            child_thread_id=child_thread_id,
            reduced_confidence=reduced_confidence,
            result=None,
            skipped=True,
            skip_reason="reduced_confidence",
        )
        output_records.append(record)

    return {"batch_outputs": output_records}
