# Product Requirements Document
## Architecture Generation Agent (AGA) — Phase 6: Full LangGraph Subgraph Wiring
**Version:** 1.0
**Status:** Draft
**Scope:** Full implementation of `aga/graph.py`. Covers all node definitions, edge wiring, the ReAct agent loop, output assembly, and the final compiled `StateGraph`. This phase brings together all artefacts from Phases 1–5 into a runnable subgraph.

---

## 1. Overview

This phase fills the `build_graph` shell (Phase 1) with all nodes and edges. The resulting graph is a `StateGraph` that the Orchestrator can invoke as:

```python
from aga import AGAConfig, build_graph
from langchain_openai import ChatOpenAI

config = AGAConfig(
    llm=ChatOpenAI(model="gpt-4o", temperature=0.1),
    output_dir="projects/my_project/diagrams",
)
graph = build_graph(config)
result = graph.invoke({"raa_output": raa_dict})
# result is AGAOutputState: {completed_diagrams, failed_diagrams, session_report}
```

---

## 2. Files Modified in This Phase

| File | Change |
|------|--------|
| `aga/graph.py` | Full implementation — all nodes, edges, agent construction |

All supporting modules (`config.py`, `schemas.py`, `normaliser.py`, `queue_builder.py`, `tools/render_tool.py`, `prompt_renderer.py`, `prompts/*.md`) are imported, not modified.

---

## 3. Graph Structure

```
START
  │
  ▼
normalise_node          ← parse raw RAA dict → RAAOutput (Phase 3)
  │
  ▼
build_queue_node        ← derive list[DiagramSpec], create output dir,
  │                        record session_start_time (Phase 3)
  │
  ▼
agent_loop_node ◄───┐   ← pop one DiagramSpec, run ReAct agent,
  │                 │     accumulate result (CompletedDiagram or FailedDiagram)
  │  [queue empty?] │
  ├── No ───────────┘   (loop back)
  │
  └── Yes
        │
        ▼
assemble_output_node    ← build SessionReport, write aga_report.json
        │
        ▼
       END
```

### 3.1 Conditional Edge

```python
def _should_continue(state: AGAInternalState) -> str:
    """Route back to agent_loop if diagrams remain, else assemble output."""
    return "agent_loop" if state["diagram_queue"] else "assemble_output"
```

---

## 4. Node Specifications

### 4.1 `normalise_node`

**Source:** `aga/normaliser.py::normalise_raa_output`

```python
def normalise_node(state: AGAInputState) -> dict:
    parsed = normalise_raa_output(state["raa_output"])
    return {"parsed_raa": parsed}
```

**Failure behaviour:** If `NormalisationError` is raised, it propagates to the Orchestrator uncaught — the graph has no valid input to work with and there is no recovery path. The Orchestrator is responsible for wrapping `graph.invoke()` in a try/except.

---

### 4.2 `build_queue_node`

**Sources:** `aga/queue_builder.py::build_diagram_queue`, `pathlib.Path`, `time`

```python
def build_queue_node(state: AGAInternalState) -> dict:
    import time
    from pathlib import Path

    queue = build_diagram_queue(state["parsed_raa"])

    # Create output directory now (once, before any diagram is rendered)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    return {
        "diagram_queue": queue,
        "session_start_time": time.time(),
    }
```

`config` is captured from the `build_graph` closure.

**Empty queue handling:** If `build_diagram_queue` returns an empty list (should never happen per Phase 3 §4.5 — the context diagram is always present, but defensively handled), the conditional edge immediately routes to `assemble_output_node` with no agent loop iterations.

---

### 4.3 `agent_loop_node`

This is the core node. It processes one `DiagramSpec` per invocation, loops until the queue is empty.

**Sources:** `aga/prompt_renderer.py::build_template_vars`, `aga/prompts/*.md`, the pre-built `react_agent`, `aga/schemas.py`

#### 4.3.1 Full Behaviour

```
1. Pop current_diagram = state["diagram_queue"][0]
   remaining_queue     = state["diagram_queue"][1:]

2. Render agent_instruction.md with build_template_vars(
       spec=current_diagram, config=config, retry_count=0
   )

3. Invoke `react_agent` with the rendered instruction as the user message.
   The agent's tool list contains [render_plantuml_tool].
   The agent iterates its own ReAct loop (generate → call tool → observe)
   internally. The AGA node enforces a hard LangGraph `recursion_limit`
   derived from `config.max_retries` so prompt text is not the only retry
   control.

4. Inspect the final agent message for the tool result prefix:
   - "OK:{path}"    → build CompletedDiagram, append to completed_diagrams
   - "ERROR:..."    → build FailedDiagram, append to failed_diagrams
   - "ERROR:..." after max attempts → build FailedDiagram, append to failed_diagrams
   - GraphRecursionError → build FailedDiagram with last_error =
     "Agent exceeded max render attempts."
   - No tool result found (agent gave up early) → treat as FailedDiagram
     with last_error = "Agent did not call render_plantuml_tool."

5. Return:
   {
       "diagram_queue": remaining_queue,
       "completed_diagrams": [completed_diagram],   # OR
       "failed_diagrams": [failed_diagram],
   }
```

`config.max_retries` is interpreted as the maximum number of
`render_plantuml_tool` calls for a diagram, including the first render attempt.
For the prebuilt ReAct graph, the node invokes the agent with:

```python
agent_runtime_config = {"recursion_limit": (2 * config.max_retries) + 1}
```

This allows the normal `agent → tool → agent` cadence through the final allowed
tool call, while preventing unbounded agent loops. If the limit is reached,
`GraphRecursionError` is caught inside `agent_loop_node` and converted into a
`FailedDiagram` so the outer AGA graph can continue to the next queued diagram.

#### 4.3.2 Extracting the Tool Result from Agent Output

The ReAct agent's final state contains a `messages` list. The node scans messages in reverse for the last `ToolMessage`. It reads the `content` field of that message for the `"OK:"` / `"ERROR:"` prefix.

```python
def _extract_tool_result(messages: list) -> str | None:
    """Return the last tool message content, or None if not found."""
    from langchain_core.messages import ToolMessage
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            return msg.content
    return None
```

#### 4.3.3 `CompletedDiagram` Construction

```python
CompletedDiagram(
    diagram_id=current_diagram.diagram_id,
    diagram_type=current_diagram.diagram_type,
    output_path=tool_result[len("OK:"):],   # strip the "OK:" prefix
    plantuml_source=_extract_last_puml(messages),
    retry_count=max(0, _count_tool_calls(messages) - 1),
)
```

`_extract_last_puml(messages)` scans `AIMessage` contents in reverse for the last block that begins with `@startuml` to capture the final PlantUML source that succeeded.

`_count_tool_calls(messages)` counts `ToolMessage` entries — each represents one render attempt. `CompletedDiagram.retry_count` is stored as `max(0, _count_tool_calls(messages) - 1)` so a first-attempt success reports `0`.

#### 4.3.4 `FailedDiagram` Construction

```python
FailedDiagram(
    diagram_id=current_diagram.diagram_id,
    diagram_type=current_diagram.diagram_type,
    last_puml_code=_extract_last_puml(messages) or "",
    last_error=tool_result or "Agent produced no tool call.",
    retry_count=_count_tool_calls(messages),
)
```

#### 4.3.5 Metadata Sidecar Write

On `CompletedDiagram` creation, the node also writes a JSON sidecar alongside the PNG:

```python
sidecar = {
    "diagram_id": completed.diagram_id,
    "diagram_type": completed.diagram_type,
    "plantuml_source": completed.plantuml_source,
    "render_timestamp": datetime.utcnow().isoformat() + "Z",
    "retry_count": completed.retry_count,
}
Path(completed.output_path).with_suffix(".json").write_text(
    json.dumps(sidecar, indent=2)
)
```

---

### 4.4 `assemble_output_node`

**Source:** `aga/schemas.py::SessionReport`, `json`, `time`

```python
def assemble_output_node(state: AGAInternalState) -> dict:
    import time, json
    from pathlib import Path

    elapsed = time.time() - state["session_start_time"]
    report = SessionReport(
        completed_count=len(state["completed_diagrams"]),
        failed_count=len(state["failed_diagrams"]),
        total_diagrams_expected=(
            len(state["completed_diagrams"]) + len(state["failed_diagrams"])
        ),
        output_dir=config.output_dir,
        plantuml_base_url=config.plantuml_base_url,
        wall_clock_seconds=round(elapsed, 3),
    )

    # Write session report JSON to output dir
    report_path = Path(config.output_dir) / "aga_report.json"
    report_path.write_text(json.dumps(report.model_dump(), indent=2))

    return {"session_report": report}
```

`config` is captured from the `build_graph` closure.

---

## 5. ReAct Agent Construction (inside `build_graph`)

```python
from langgraph.prebuilt import create_react_agent
from aga.tools.render_tool import render_plantuml_tool

react_agent = create_react_agent(
    model=config.llm,
    tools=[render_plantuml_tool],
)
```

`react_agent` is a compiled `StateGraph` itself. It is built **once** inside `build_graph` and captured into the `agent_loop_node` closure. It is not rebuilt per-diagram.

### 5.1 Agent Invocation per Diagram

```python
rendered_prompt = render_template(
    "aga/prompts/agent_instruction.md",
    build_template_vars(spec=current_diagram, config=config)
)

try:
    agent_result = react_agent.invoke(
        {"messages": [{"role": "user", "content": rendered_prompt}]},
        {"recursion_limit": (2 * config.max_retries) + 1},
    )
except GraphRecursionError:
    agent_result = None
```

The `agent_instruction.md` template already includes the C4 rules (via skill injection), the diagram scope, and the tool call instructions — so no separate system message is required. If `GraphRecursionError` is raised, the node records the current diagram as failed and advances the queue.

---

## 6. Full `build_graph` Implementation

```python
def build_graph(config: AGAConfig):
    from langgraph.graph import StateGraph, START, END
    from langgraph.errors import GraphRecursionError
    from langgraph.prebuilt import create_react_agent
    from aga.schemas import AGAInputState, AGAInternalState, AGAOutputState
    from aga.normaliser import normalise_raa_output
    from aga.queue_builder import build_diagram_queue
    from aga.tools.render_tool import render_plantuml_tool
    from aga.prompt_renderer import build_template_vars, render_template

    # --- Build the ReAct agent once ---
    react_agent = create_react_agent(
        model=config.llm,
        tools=[render_plantuml_tool],
    )

    # --- Node definitions (closures capture config and react_agent) ---

    def normalise_node(state):
        return {
            "parsed_raa": normalise_raa_output(state["raa_output"]),
            "completed_diagrams": [],
            "failed_diagrams": [],
        }

    def build_queue_node(state):
        import time
        from pathlib import Path
        queue = build_diagram_queue(state["parsed_raa"])
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)
        return {"diagram_queue": queue, "session_start_time": time.time()}

    def agent_loop_node(state):
        # [full implementation per §4.3]
        ...

    def assemble_output_node(state):
        # [full implementation per §4.4]
        ...

    def _should_continue(state):
        return "agent_loop" if state["diagram_queue"] else "assemble_output"

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
```

---

## 7. `aga/prompt_renderer.py` — Template Rendering

This file was specified in Phase 5 §7. In Phase 6 it is fully implemented with:

```python
import chevron   # pip install chevron — a Mustache renderer for Python

def render_template(template_path: str, variables: dict) -> str:
    """
    Render a Mustache template file with the given variables.

    Skill injection tags ({{! skill: <tag> as <var> }}) are resolved
    before passing to chevron by pre-scanning the template and loading
    the referenced content from Skills/references/c4.md.
    """
    ...
```

### 7.1 Skill Injection Pre-Processing

Before passing the template to `chevron.render`, a pre-processing step:

1. Scans the template text for `{{! skill: <tag> as <var> }}` directives.
2. Loads `aga/Skills/references/c4.md` and extracts the section identified by `<tag>` (matching the `# <Section>` heading in `c4.md`).
3. Adds the extracted content to the `variables` dict under key `<var>`.
4. Removes the directive comment line from the template text.
5. Passes the cleaned template and enriched variables to `chevron.render`.

Tag-to-section mapping (from `aga/Skills/SKILL.md`):

| Tag | Section in `c4.md` |
|-----|---------------------|
| `c4:rules` | `# Rules` |
| `c4:context_example` | `# Context Example` |
| `c4:container_example` | `# Container Example` |
| `c4:component_example` | `# Component Example` |

---

## 8. State Channel Initialisation

The AGA uses `TypedDict` state schemas for simple LangGraph integration.
`TypedDict` describes the shape of state channels; it does not provide runtime
defaults. Channels are initialised explicitly by nodes:

| Channel | Initialisation |
|---------|----------------|
| `raa_output` | Supplied by the Orchestrator input |
| `parsed_raa` | Set by `normalise_node` |
| `completed_diagrams` | Set to `[]` by `normalise_node` |
| `failed_diagrams` | Set to `[]` by `normalise_node` |
| `diagram_queue` | Set by `build_queue_node` |
| `session_start_time` | Set by `build_queue_node` |
| `session_report` | Set by `assemble_output_node` |

`current_diagram`, `current_puml_code`, and `retry_count` are optional working
channels. The recommended implementation derives them locally inside
`agent_loop_node` from the current queue item and the returned agent messages,
rather than relying on cross-iteration state.

---

## 9. Integration Test Criteria

- Given the reference `raa_output.pkl` (1 L1 + 4 L2 + 2 L3 = 7 diagrams), `graph.invoke({"raa_output": data})` returns an `AGAOutputState` where `session_report.total_diagrams_expected == 7`.
- `completed_count + failed_count == 7` always holds (no diagram silently dropped).
- Each `CompletedDiagram.output_path` points to a file that exists on disk.
- A metadata sidecar `.json` file exists alongside each PNG.
- `aga_report.json` is written to `output_dir`.
- The graph can be called twice with different `output_dir` values without shared state between calls.

---

## 10. Design Constraints Summary

| Constraint | Rule |
|------------|------|
| One diagram per `agent_loop_node` invocation | Enables the LangGraph conditional loop pattern |
| `react_agent` built once | Inside `build_graph`, not per-diagram |
| Closure capture | `config` and `react_agent` are captured into node closures |
| `diagram_queue` reducer | No reducer — replaced per iteration |
| `completed/failed_diagrams` reducer | `operator.add` — lists accumulate |
| Output dir creation | In `build_queue_node`, once, before any rendering |
| Sidecar write | In `agent_loop_node`, immediately on `CompletedDiagram` creation |
| `aga_report.json` | Written in `assemble_output_node` to `config.output_dir` |
| `NormalisationError` | Propagates uncaught — Orchestrator handles |
| Mustache library | `chevron` — installed as a project dependency |
