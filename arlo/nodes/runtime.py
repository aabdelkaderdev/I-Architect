"""Runtime dependency helpers for ARLO nodes."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langgraph.runtime import Runtime

from arlo.state.schemas import ARLOContext


def get_llm(state: dict, runtime: Runtime[ARLOContext] | None = None) -> Any:
    """Return the LLM from runtime context, falling back to legacy state."""
    if runtime is not None and runtime.context and "llm" in runtime.context:
        return runtime.context["llm"]

    if "llm" in state:
        return state["llm"]

    raise ValueError(
        "ARLO requires an LLM in runtime context. Invoke with "
        "`context={'llm': llm}` when using checkpointing."
    )


def get_progress_callback(
    runtime: Runtime[ARLOContext] | None = None,
) -> Callable[[int, int], None] | None:
    """Return the orchestrator's progress callback, or None if not injected.

    The orchestrator injects a progress callback via context (§8D):
        context = {"llm": llm, "progress_callback": progress_callback}

    When running standalone (dev/test), no callback is injected and this
    returns None — callers should guard with `if callback: callback(...)`.
    """
    if runtime is not None and runtime.context:
        return runtime.context.get("progress_callback")
    return None


def is_cancelled(runtime: Runtime[ARLOContext] | None = None) -> bool:
    """Check whether the orchestrator has requested graceful cancellation.

    The orchestrator sets a threading.Event via context (§4E):
        context = {"llm": llm, "cancellation_flag": event}

    Returns False if no cancellation flag is injected (standalone mode).
    """
    if runtime is not None and runtime.context:
        flag = runtime.context.get("cancellation_flag")
        if flag is not None:
            return flag.is_set()
    return False
