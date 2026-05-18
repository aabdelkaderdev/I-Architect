"""
Parent pipeline wrapper node for the ARLO subgraph.

This wrapper transforms the parent pipeline's state into ARLO's
input schema and maps ARLO's output back to the parent's state.

Usage (in the parent pipeline):
    from arlo.pipeline_wrapper import create_arlo_wrapper

    wrapper = create_arlo_wrapper(arlo_graph)
    parent_builder.add_node("arlo", wrapper)
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langchain_core.runnables import RunnableConfig


def create_arlo_wrapper(
    arlo_graph,
    *,
    thread_id_key: str = "arlo_thread_id",
    default_experiment_config: dict | None = None,
) -> Callable[[dict], dict]:
    """Create a wrapper function that adapts the ARLO subgraph to a parent pipeline.

    Args:
        arlo_graph: A compiled ARLO StateGraph instance.
        thread_id_key: Parent-state key containing the ARLO checkpoint thread ID.
        default_experiment_config: Defaults used when parent state omits config.

    Returns:
        A node function compatible with the parent pipeline's StateGraph.
    """

    def call_arlo(state: dict, config: RunnableConfig | None = None) -> dict:
        """Wrapper node: invoke ARLO subgraph within the parent pipeline.

        This function transforms the parent pipeline's state to ARLO's
        input schema and maps ARLO's output back.

        Expected parent state keys:
        - extracted_requirements: Dict[str, str]
        - matrix: dict[str, dict[str, int]]
        - experiment_config: dict (optional, defaults provided)
        - arlo_thread_id: str (optional when parent config has thread_id)

        LLM, progress_callback, and cancellation_flag are read from the
        parent's runtime context (§3C, §8D, §4E) — never from state.
        """
        parent_configurable = (config or {}).get("configurable", {})
        parent_thread_id = parent_configurable.get("thread_id")
        arlo_thread_id = state.get(thread_id_key)

        if not arlo_thread_id and parent_thread_id:
            arlo_thread_id = f"{parent_thread_id}:arlo"

        if not arlo_thread_id:
            raise ValueError(
                "ARLO wrapper requires an `arlo_thread_id` in parent state "
                "or a parent LangGraph `configurable.thread_id`."
            )

        experiment_config = state.get(
            "experiment_config",
            default_experiment_config or {
                "mode": "stringent",
                "optimizer": "ILP",
                "batch_size": 10,
            },
        )

        # Build ARLO context from the parent's runtime context (§3C, §8D, §4E).
        # LLM objects are never stored in state channels — the orchestrator
        # passes them via context={} to prevent checkpoint serialization issues.
        parent_context = (config or {}).get("context", {})
        arlo_context: dict[str, Any] = {"llm": parent_context["llm"]}

        # Thread optional orchestrator callbacks
        if "progress_callback" in parent_context:
            arlo_context["progress_callback"] = parent_context["progress_callback"]
        if "cancellation_flag" in parent_context:
            arlo_context["cancellation_flag"] = parent_context["cancellation_flag"]

        arlo_output = arlo_graph.invoke(
            {
                "requirements": state["extracted_requirements"],
                "experiment_config": experiment_config,
                "matrix": state["matrix"],
            },
            {"configurable": {"thread_id": str(arlo_thread_id)}},
            context=arlo_context,
            durability="sync",
        )

        return {
            "identified_asrs": arlo_output["asrs"],
            "non_asr": arlo_output["non_asr"],
            "condition_groups": arlo_output["condition_groups"],
            "architectural_concerns": arlo_output["concerns"],
            "quality_weights": arlo_output["quality_weights"],
            "arlo_stats": arlo_output["stats"],
        }

    return call_arlo

