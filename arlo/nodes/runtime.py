"""Runtime dependency helpers for ARLO nodes."""
from __future__ import annotations

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
