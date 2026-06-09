"""Full AGA StateGraph — node definitions, edge wiring, ReAct agent loop.

This is the single file that ties together all Phase 1–5 artefacts into a
runnable subgraph.  The Orchestrator calls :func:`build_graph` once to obtain
a compiled graph, then invokes it with ``{"raa_output": raw_dict}``.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph

from aga.config import AGAConfig
from aga.normaliser import normalise_raa_output
from aga.prompt_renderer import build_template_vars, render_template
from aga.queue_builder import build_diagram_queue
from aga.schemas import (
    AGAInputState,
    AGAInternalState,
    AGAOutputState,
    CompletedDiagram,
    FailedDiagram,
    SessionReport,
)
from aga.tools.render_tool import render_plantuml_tool

# ── Message-introspection helpers ────────────────────────────────────────────


def _extract_tool_result(messages: list) -> str | None:
    """Return the content of the last ToolMessage, or None."""
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            return msg.content
    return None


def _extract_last_puml(messages: list) -> str:
    """Scan AIMessage contents in reverse for the last @startuml block.

    Checks both the message's ``content`` (if the LLM inlined the code) and
    any ``tool_calls`` arguments (the normal path — the LLM passes the code
    as the ``puml_code`` parameter to ``render_plantuml_tool``).
    """
    for msg in reversed(messages):
        if not isinstance(msg, AIMessage):
            continue
        # Check direct content
        content = msg.content
        if isinstance(content, str) and "@startuml" in content:
            return content
        # Check tool call arguments (the expected path)
        for tc in getattr(msg, "tool_calls", []):
            puml = tc.get("args", {}).get("puml_code", "")
            if "@startuml" in puml:
                return puml
    return ""


def _count_tool_calls(messages: list) -> int:
    """Return the number of ToolMessage entries in *messages*."""
    return sum(1 for msg in messages if isinstance(msg, ToolMessage))


# ── Prompt file paths (resolved relative to this module) ────────────────────

_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
_AGENT_INSTRUCTION = str(_PROMPTS_DIR / "agent_instruction.md")


# ── Graph builder ────────────────────────────────────────────────────────────


def build_graph(config: AGAConfig):
    """Build and compile the AGA StateGraph.

    Parameters
    ----------
    config : AGAConfig
        Runtime configuration. Passed into node closures at build time.

    Returns
    -------
    CompiledStateGraph
        Ready to call via ``.invoke()`` or ``.stream()``.
    """
    # --- Build the ReAct agent once (not per-diagram) ---
    react_agent = create_agent(
        model=config.llm,
        tools=[render_plantuml_tool],
    )

    # --- Node definitions (closures capture config and react_agent) ---

    def normalise_node(state: AGAInputState) -> dict:
        parsed = normalise_raa_output(state["raa_output"])
        return {
            "parsed_raa": parsed,
            "completed_diagrams": [],
            "failed_diagrams": [],
        }

    def build_queue_node(state: AGAInternalState) -> dict:
        queue = build_diagram_queue(state["parsed_raa"])
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)
        return {
            "diagram_queue": queue,
            "session_start_time": time.time(),
        }

    def agent_loop_node(state: AGAInternalState) -> dict:
        queue: list = list(state["diagram_queue"])
        if not queue:
            return {}

        current = queue[0]
        remaining = queue[1:]

        # Render the instruction prompt for this diagram
        template_vars = build_template_vars(current, config)
        rendered_prompt = render_template(_AGENT_INSTRUCTION, template_vars)

        # Each retry = model call + tool call = 2 steps. Add buffer for
        # initial generation + final response + thinking-model overhead.
        agent_limit = (2 * config.max_retries) + 5
        try:
            agent_result = react_agent.invoke(
                {"messages": [{"role": "user", "content": rendered_prompt}]},
                {"recursion_limit": agent_limit},
            )
        except GraphRecursionError:
            agent_result = None

        if agent_result is None:
            return _record_failure(
                current, remaining,
                last_error="Agent exceeded max render attempts.",
            )

        messages: list = agent_result.get("messages", [])
        tool_result = _extract_tool_result(messages)

        if tool_result is None:
            return _record_failure(
                current, remaining,
                last_error="Agent did not call render_plantuml_tool.",
            )

        if tool_result.startswith("OK:"):
            return _record_success(current, remaining, messages, tool_result)
        else:
            return _record_failure(
                current, remaining, messages, tool_result,
            )

    def assemble_output_node(state: AGAInternalState) -> dict:
        completed = state.get("completed_diagrams", [])
        failed = state.get("failed_diagrams", [])
        elapsed = time.time() - state["session_start_time"]

        report = SessionReport(
            completed_count=len(completed),
            failed_count=len(failed),
            total_diagrams_expected=len(completed) + len(failed),
            output_dir=config.output_dir,
            plantuml_base_url=config.plantuml_base_url,
            wall_clock_seconds=round(elapsed, 3),
        )

        report_path = Path(config.output_dir) / "aga_report.json"
        report_path.write_text(json.dumps(report.model_dump(), indent=2))

        return {"session_report": report}

    def _should_continue(
        state: AGAInternalState,
    ) -> Literal["agent_loop", "assemble_output"]:
        return "agent_loop" if state.get("diagram_queue") else "assemble_output"

    # --- Graph wiring ---
    builder = StateGraph(
        AGAInternalState,
        input_schema=AGAInputState,
        output_schema=AGAOutputState,
    )

    builder.add_node("normalise", normalise_node)
    builder.add_node("build_queue", build_queue_node)
    builder.add_node("agent_loop", agent_loop_node)
    builder.add_node("assemble_output", assemble_output_node)

    builder.add_edge(START, "normalise")
    builder.add_edge("normalise", "build_queue")
    builder.add_conditional_edges("build_queue", _should_continue)
    builder.add_conditional_edges("agent_loop", _should_continue)
    builder.add_edge("assemble_output", END)

    return builder.compile()


# ── Internal helpers for agent_loop_node ────────────────────────────────────


def _record_success(
    current,
    remaining: list,
    messages: list,
    tool_result: str,
) -> dict:
    """Build a CompletedDiagram and return the state update."""
    output_path = tool_result[len("OK:"):]
    plantuml_source = _extract_last_puml(messages)
    tool_call_count = _count_tool_calls(messages)

    completed = CompletedDiagram(
        diagram_id=current.diagram_id,
        diagram_type=current.diagram_type,
        output_path=output_path,
        plantuml_source=plantuml_source,
        retry_count=max(0, tool_call_count - 1),
    )

    # Write metadata sidecar alongside the PNG
    _write_sidecar(completed)

    return {
        "diagram_queue": remaining,
        "completed_diagrams": [completed],
    }


def _record_failure(
    current,
    remaining: list,
    messages: list | None = None,
    last_error: str = "",
) -> dict:
    """Build a FailedDiagram and return the state update."""
    msgs = messages or []
    failed = FailedDiagram(
        diagram_id=current.diagram_id,
        diagram_type=current.diagram_type,
        last_puml_code=_extract_last_puml(msgs) or "",
        last_error=last_error,
        retry_count=_count_tool_calls(msgs),
    )
    return {
        "diagram_queue": remaining,
        "failed_diagrams": [failed],
    }


def _write_sidecar(completed: CompletedDiagram) -> None:
    sidecar = {
        "diagram_id": completed.diagram_id,
        "diagram_type": completed.diagram_type,
        "plantuml_source": completed.plantuml_source,
        "render_timestamp": datetime.now(timezone.utc).isoformat(),
        "retry_count": completed.retry_count,
    }
    sidecar_path = Path(completed.output_path).with_suffix(".json")
    sidecar_path.write_text(json.dumps(sidecar, indent=2))
