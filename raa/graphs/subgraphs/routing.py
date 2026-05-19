"""Send fan-out routing for RAA parallel subgraphs (Section 12).

Reads the current batch from batch_queue[batch_cursor], extracts LLM instances
from runtime config context, and emits Send objects for parallel execution.
"""

from __future__ import annotations

from typing import Any

from langgraph.types import Send

from raa.graphs.subgraphs.common import (
    ALL_SEND_TARGETS,
    LLM_RAA_A_KEY,
    TARGET_LLM_KEY_MAP,
    SEND_TARGET_RAA_A,
    STRATEGY_ENTITY_DRIVEN,
    STRATEGY_PATTERN_DRIVEN,
    STRATEGY_SAAM_FIRST,
    SubgraphPayload,
)
from raa.utils.model_serialiser import build_model_constraint_block

# Which strategy each target node runs
TARGET_STRATEGY_MAP: dict[str, str] = {
    SEND_TARGET_RAA_A: STRATEGY_SAAM_FIRST,
    "raa_b": STRATEGY_PATTERN_DRIVEN,
    "raa_c": STRATEGY_ENTITY_DRIVEN,
}


# ---- T036: Current batch accessor -------------------------------------------


def _current_batch(state: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    """Return (batch_index, batch_dict) from batch_queue at batch_cursor."""
    batch_queue = state.get("batch_queue", [])
    batch_cursor = state.get("batch_cursor", 0)
    if not batch_queue:
        raise IndexError("batch_queue is empty — cannot fan out subgraphs")
    if batch_cursor >= len(batch_queue):
        raise IndexError(
            f"batch_cursor {batch_cursor} out of range for batch_queue length {len(batch_queue)}"
        )
    return batch_cursor, batch_queue[batch_cursor]


# ---- T037: Context extraction ------------------------------------------------


def _context_dict(config: dict | None) -> dict[str, Any]:
    """Extract runtime context dict from graph config without reading state."""
    if config is None:
        return {}
    return config.get("context", {})


# ---- T038: LLM requirement helper --------------------------------------------


def _require_llm(context: dict[str, Any], key: str) -> object:
    """Get an LLM from context by key; raise if missing."""
    llm = context.get(key)
    if llm is None:
        raise RuntimeError(
            f"Required LLM context key '{key}' is missing. "
            f"Ensure the config dict includes config['context']['{key}'] with a ChatModel instance."
        )
    return llm


# ---- T039: Common Send payload builder ---------------------------------------


def _common_send_payload(
    state: dict[str, Any],
    batch_index: int,
    batch: dict[str, Any],
) -> dict[str, Any]:
    """Build the base Send payload shared across all targets."""
    running = state.get("running_arch_model")
    return {
        "batch": batch,
        "batch_index": batch_index,
        "quality_weights": state.get("quality_weights", {}),
        "running_arch_model": running,
        "bridge_requirements": state.get("bridge_requirements", {}),
        "model_constraints": build_model_constraint_block(running),
    }


# ---- T040: Main Send fan-out ------------------------------------------------


def fan_out_subgraphs(
    state: dict[str, Any],
    config: dict | None = None,
) -> list[Send]:
    """Emit Send objects for the current batch.

    Normal batch → 3 Send objects (raa_a, raa_b, raa_c).
    Reduced-confidence batch → 1 Send object (raa_a only).
    """
    ctx = _context_dict(config)
    batch_index, batch = _current_batch(state)
    base = _common_send_payload(state, batch_index, batch)
    reduced = batch.get("reduced_confidence", False)

    if reduced:
        llm = _require_llm(ctx, LLM_RAA_A_KEY)
        payload: SubgraphPayload = {**base, "strategy": STRATEGY_SAAM_FIRST, "llm": llm}  # type: ignore[assignment]
        return [Send(SEND_TARGET_RAA_A, payload)]

    sends: list[Send] = []
    for target in ALL_SEND_TARGETS:
        llm_key = TARGET_LLM_KEY_MAP[target]
        llm = _require_llm(ctx, llm_key)
        strategy = TARGET_STRATEGY_MAP.get(target, STRATEGY_SAAM_FIRST)
        payload = {**base, "strategy": strategy, "llm": llm}
        sends.append(Send(target, payload))

    return sends
