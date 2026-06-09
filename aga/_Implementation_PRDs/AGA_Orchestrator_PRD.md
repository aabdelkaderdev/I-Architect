# Product Requirements Document
## AGA Orchestrator — Phase 1: External Invocation & Integration
**Version:** 1.0
**Status:** Draft
**Scope:** The Orchestrator-side contract for constructing, invoking, and consuming the AGA subgraph. Covers configuration assembly, input preparation, graph lifecycle, output interpretation, error handling, and checkpointing — all from the Orchestrator's perspective.

---

## 1. Overview

The AGA is a standalone LangGraph subgraph. It exposes exactly two public symbols — `AGAConfig` and `build_graph` — and a single invocation contract: pass `{"raa_output": raw_dict}` in, get `{completed_diagrams, failed_diagrams, session_report}` out.

The Orchestrator is the **owner** of the LLM, the configuration, the input data, and the output destination. The AGA never instantiates a model, never reads environment variables, and never decides where files go. Every runtime choice flows into the AGA through `AGAConfig`.

### Pipeline position

```
[RAA] → raa_output.pkl
              │
              ▼
      [Orchestrator]
              │
              ├── loads raa_output.pkl
              ├── constructs AGAConfig(llm=..., output_dir=...)
              ├── builds graph = build_graph(config)
              ├── invokes  graph.invoke({"raa_output": raw_dict})
              │       │
              │       ├── normalise    (parse dict → RAAOutput)
              │       ├── build_queue  (derive 7 DiagramSpecs)
              │       ├── agent_loop   (×7 ReAct render passes)
              │       └── assemble_output (SessionReport + aga_report.json)
              │
              ▼
      AGAOutputState {completed_diagrams, failed_diagrams, session_report}
              │
              ├── PNGs + sidecar JSONs in output_dir/
              ├── aga_report.json in output_dir/
              └── Orchestrator routes results downstream
```

---

## 2. AGA Public API Surface

The Orchestrator imports only from `aga`:

```python
from aga import AGAConfig, build_graph
```

No internal module paths are part of the contract.

---

## 3. Configuration — `AGAConfig`

The Orchestrator constructs one `AGAConfig` instance and passes it to `build_graph`. The config is **frozen** after construction — nodes cannot mutate it at runtime.

### 3.1 Fields

| Field | Type | Default | Orchestrator responsibility |
|-------|------|---------|---------------------------|
| `llm` | `BaseChatModel` | *(required)* | Construct and configure the model. Choose provider (`ChatOpenAI`, `ChatAnthropic`, `ChatOllama`, etc.), set temperature, timeout, and any provider-specific options. |
| `max_retries` | `int` | `5` | Maximum render attempts per diagram. Each attempt is one `render_plantuml_tool` call. The agent's recursion limit is derived as `(2 × max_retries) + 1`. |
| `plantuml_base_url` | `str` | `"https://www.plantuml.com/plantuml"` | Override to a self-hosted PlantUML server. The URL is injected into every agent prompt so the LLM always knows which server to call. |
| `output_dir` | `str` | `"aga/output"` | Directory for rendered PNGs, metadata sidecars, and `aga_report.json`. Created at graph startup (`build_queue_node`) via `mkdir -p`. |

### 3.2 Construction Examples

```python
from langchain_openai import ChatOpenAI
from aga import AGAConfig

# Minimal — model + defaults
config = AGAConfig(llm=ChatOpenAI(model="gpt-4o", temperature=0.1))

# Full control — custom retries, self-hosted PlantUML, custom output dir
config = AGAConfig(
    llm=ChatOpenAI(model="gpt-4o", temperature=0.1, timeout=120),
    max_retries=3,
    plantuml_base_url="https://plantuml.internal.company.com/plantuml",
    output_dir="projects/sprint-42/diagrams",
)
```

```python
from langchain_anthropic import ChatAnthropic

config = AGAConfig(
    llm=ChatAnthropic(model="claude-sonnet-4-6", temperature=0.0),
    output_dir="out/aga",
)
```

### 3.3 Config Immutability

`AGAConfig` uses `ConfigDict(frozen=True, arbitrary_types_allowed=True)`. Once constructed, fields cannot be mutated. If the Orchestrator needs different configs for different runs, it constructs a new instance each time.

### 3.4 LLM Ownership

The LLM instance is **fully owned** by the Orchestrator. The AGA:
- Never instantiates a model
- Never reads `OPENAI_API_KEY` or any environment variable
- Never applies provider-specific options

This means the Orchestrator controls cost, rate-limiting, model selection, and fallback logic entirely from the outside.

---

## 4. Graph Lifecycle

### 4.1 Building the Graph

```python
from aga import AGAConfig, build_graph

config = AGAConfig(llm=my_model, output_dir="out/")
graph = build_graph(config)
```

- **When to call:** Once per configuration. Build the graph, then invoke it as many times as needed with different inputs.
- **Cost:** `build_graph` constructs the ReAct agent and compiles the `StateGraph`. It performs no I/O, no LLM calls, and no filesystem access.
- **Statelessness:** Calling `build_graph` twice with the same config produces two independent graphs. No module-level cache or singleton.

### 4.2 Invoking the Graph

```python
result = graph.invoke({"raa_output": raa_dict})
```

- **Input:** A dict with exactly one key — `"raa_output"` — whose value is the raw RAA output dict (as returned by `raa_graph.invoke()` or loaded from `raa_output.pkl`).
- **Output:** A dict with exactly three keys — `"completed_diagrams"`, `"failed_diagrams"`, `"session_report"` — matching `AGAOutputState`.
- **Duration:** Wall-clock time depends on the number of diagrams (7 for the reference RAA output), the LLM provider's latency, and the PlantUML server's response time. A full 7-diagram run with a fast cloud model typically completes in 30–120 seconds.

### 4.3 Streaming

The Orchestrator can observe progress per diagram via `.stream()`:

```python
for chunk in graph.stream(
    {"raa_output": raa_dict},
    stream_mode="values",
    output_keys=["completed_diagrams", "failed_diagrams", "session_report"],
):
    c = len(chunk.get("completed_diagrams", []))
    f = len(chunk.get("failed_diagrams", []))
    if "session_report" in chunk:
        print(f"Done: {chunk['session_report'].completed_count} completed, "
              f"{chunk['session_report'].failed_count} failed")
    else:
        print(f"Progress: {c} completed, {f} failed so far")
```

The `output_keys` parameter restricts streamed values to the output schema, keeping internal channels (`parsed_raa`, `diagram_queue`, etc.) out of the Orchestrator's view.

### 4.4 Per-Diagram Monitoring (updates mode)

For fine-grained progress, use `stream_mode="updates"` to receive only the delta from each node execution:

```python
for chunk in graph.stream(
    {"raa_output": raa_dict},
    stream_mode="updates",
):
    if "agent_loop" in chunk:
        update = chunk["agent_loop"]
        if "completed_diagrams" in update:
            cd = update["completed_diagrams"][0]
            print(f"✓ {cd.diagram_id} ({cd.diagram_type}) — {cd.retry_count} retries")
        elif "failed_diagrams" in update:
            fd = update["failed_diagrams"][0]
            print(f"✗ {fd.diagram_id} — {fd.last_error}")
```

---

## 5. Input — `AGAInputState`

### 5.1 Schema

```python
class AGAInputState(TypedDict):
    raa_output: dict
```

### 5.2 Source

The Orchestrator obtains `raa_output` from one of:

| Source | When |
|--------|------|
| `raa_graph.invoke(...)` | Running the RAA inline in the same pipeline process |
| `pickle.load(open("raa_output.pkl", "rb"))` | Resuming from a checkpoint after RAA completion |

The AGA does not care which source was used — it only requires that the dict has the expected top-level keys.

### 5.3 Required Structure

The dict must contain these four top-level keys (enforced by `normalise_raa_output`):

| Key | Type | Description |
|-----|------|-------------|
| `l1_description` | `dict` | System context description |
| `l2_descriptions` | `list[dict]` | Container-level descriptions (one per concern) |
| `l3_descriptions` | `list[dict]` | Component-level descriptions |
| `entity_registry` | `dict[str, dict]` | Entity registry keyed by `ENT-NNN` |

Optional keys passed through unmodified:
- `coverage_gaps` — `list[dict]`
- `conflicts` — `list[dict]`

### 5.4 Validation at the Boundary

The AGA's `normalise_node` (first node in the graph) validates the input dict and raises `NormalisationError(ValueError)` if:

- A required top-level key is missing
- A sub-structure cannot be parsed into its expected Pydantic type
- The input is not a dict

The Orchestrator should wrap `graph.invoke()` in a `try/except NormalisationError` block to surface structural issues immediately. There is no recovery path for malformed input — the Orchestrator must fix the RAA output or abort the pipeline.

---

## 6. Output — `AGAOutputState`

### 6.1 Schema

```python
class AGAOutputState(TypedDict):
    completed_diagrams: list[CompletedDiagram]
    failed_diagrams:    list[FailedDiagram]
    session_report:     SessionReport
```

### 6.2 `CompletedDiagram`

```python
class CompletedDiagram(BaseModel):
    diagram_id:      str          # "ctx", "cnt-concern_batch_1", ...
    diagram_type:    Literal["context", "container", "component"]
    output_path:     str          # absolute path to the rendered PNG
    plantuml_source: str          # final PlantUML code that rendered successfully
    retry_count:     int          # 0 = first attempt succeeded
```

For each `CompletedDiagram`, the AGA also writes a sidecar JSON file at `{output_path}.json`:

```json
{
  "diagram_id": "ctx",
  "diagram_type": "context",
  "plantuml_source": "@startuml\n...",
  "render_timestamp": "2026-06-09T14:30:00.123456Z",
  "retry_count": 0
}
```

### 6.3 `FailedDiagram`

```python
class FailedDiagram(BaseModel):
    diagram_id:      str
    diagram_type:    Literal["context", "container", "component"]
    last_puml_code:  str          # last PlantUML code that was attempted
    last_error:      str          # human-readable error from the agent
    retry_count:     int          # total render attempts made (equals max_retries)
```

Failure reasons the Orchestrator may encounter:

| `last_error` value | Meaning |
|--------------------|---------|
| `"planturl exited N: ..."` | PlantUML server returned an error for the generated code |
| `"File path error: ..."` | Output directory or path problem |
| `"Agent exceeded max render attempts."` | Agent loop hit the recursion limit |
| `"Agent did not call render_plantuml_tool."` | Agent produced text but never invoked the tool |

### 6.4 `SessionReport`

```python
class SessionReport(BaseModel):
    completed_count:          int
    failed_count:             int
    total_diagrams_expected:  int      # always == completed_count + failed_count
    output_dir:               str
    plantuml_base_url:        str
    wall_clock_seconds:       float
```

**Invariant:** `completed_count + failed_count == total_diagrams_expected`. No diagram is silently dropped.

The report is also written to `{output_dir}/aga_report.json`:

```json
{
  "completed_count": 5,
  "failed_count": 2,
  "total_diagrams_expected": 7,
  "output_dir": "projects/my_project/diagrams",
  "plantuml_base_url": "https://www.plantuml.com/plantuml",
  "wall_clock_seconds": 47.312
}
```

### 6.5 Filesystem Outputs

After a successful graph invocation, `output_dir` contains:

```
output_dir/
├── ctx.png                          # context diagram
├── ctx.json                         # sidecar
├── cnt-concern_batch_1.png          # container diagram
├── cnt-concern_batch_1.json
├── cnt-concern_batch_2.png
├── cnt-concern_batch_2.json
├── ... (one PNG + JSON per diagram)
├── cmp-ENT-010-concern_batch_2.png  # component diagram
├── cmp-ENT-010-concern_batch_2.json
├── cmp-ENT-002-concern_batch_4.png
├── cmp-ENT-002-concern_batch_4.json
└── aga_report.json                  # session summary
```

Only successfully rendered diagrams have PNG + sidecar files. Failed diagrams appear only in `failed_diagrams` and `aga_report.json`.

---

## 7. Error Handling

### 7.1 Input Validation Errors

```python
from aga.normaliser import NormalisationError

try:
    result = graph.invoke({"raa_output": raa_dict})
except NormalisationError as e:
    # Structural problem with the RAA output — cannot proceed.
    # The error message includes the failing key path.
    logger.error(f"AGA input validation failed: {e}")
    raise
```

`NormalisationError` propagates uncaught through the graph. The Orchestrator owns the recovery decision: abort, retry with corrected input, or flag for human review.

### 7.2 Agent-Level Failures

Individual diagram failures are **not** exceptions — they are accumulated in `failed_diagrams`. The graph always runs to completion. The Orchestrator inspects `session_report.failed_count` after invocation:

```python
result = graph.invoke({"raa_output": raa_dict})
if result["session_report"].failed_count > 0:
    for fd in result["failed_diagrams"]:
        logger.warning(f"Diagram {fd.diagram_id} failed: {fd.last_error}")
```

### 7.3 LLM Provider Errors

The Orchestrator owns the LLM instance. If the LLM provider returns an error (rate limit, authentication failure, timeout), that exception propagates from `graph.invoke()` uncaught. The Orchestrator should wrap invocation with its own retry/fallback logic:

```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def invoke_aga(graph, raa_dict):
    return graph.invoke({"raa_output": raa_dict})
```

### 7.4 PlantUML Server Errors

The PlantUML server is called by `render_plantuml_tool` via the `planturl` binary. Server errors (timeout, connection refused) surface as `PlantURLError` inside the tool, converted to `"ERROR:planturl exited N: ..."` strings, and recorded as `FailedDiagram` entries. No exception reaches the Orchestrator.

### 7.5 Summary — What Reaches the Orchestrator

| Failure mode | Reaches Orchestrator as |
|-------------|------------------------|
| Malformed RAA dict | `NormalisationError` (exception) |
| LLM provider error | Provider-specific exception (e.g. `RateLimitError`) |
| PlantUML server error | `FailedDiagram` with `last_error = "ERROR:planturl exited..."` |
| Agent recursion limit hit | `FailedDiagram` with `last_error = "Agent exceeded max render attempts."` |
| Agent gave up without calling tool | `FailedDiagram` with `last_error = "Agent did not call render_plantuml_tool."` |
| Diagram rendered successfully | `CompletedDiagram` in `completed_diagrams` |

---

## 8. Checkpointing

### 8.1 RAA Output Checkpoint

The Orchestrator should persist `raa_output` before invoking the AGA. This enables:

- **Re-running the AGA** with different configs (model, retry count, output dir) without re-running the RAA
- **Debugging** failed diagram renders by inspecting the input data
- **Pipeline recovery** if the AGA invocation is interrupted

```python
import pickle

# After RAA completes, before AGA invocation
with open("checkpoints/raa_output.pkl", "wb") as f:
    pickle.dump(raa_dict, f)
```

### 8.2 AGA Output Checkpoint

The Orchestrator may also persist `AGAOutputState` for downstream routing:

```python
result = graph.invoke({"raa_output": raa_dict})

with open("checkpoints/aga_output.pkl", "wb") as f:
    pickle.dump(result, f)
```

Note that `CompletedDiagram` and `FailedDiagram` contain Pydantic models — use `model_dump()` for JSON serialisation if a human-readable checkpoint is preferred over pickle.

---

## 9. End-to-End Orchestrator Pseudocode

```python
import pickle
from aga import AGAConfig, build_graph
from aga.normaliser import NormalisationError
from langchain_openai import ChatOpenAI


def run_aga_pipeline(raa_output_path: str, output_dir: str):
    # 1. Load RAA output from checkpoint
    with open(raa_output_path, "rb") as f:
        raa_dict = pickle.load(f)

    # 2. Construct configuration
    config = AGAConfig(
        llm=ChatOpenAI(model="gpt-4o", temperature=0.1, timeout=120),
        max_retries=5,
        plantuml_base_url="https://www.plantuml.com/plantuml",
        output_dir=output_dir,
    )

    # 3. Build the graph
    graph = build_graph(config)

    # 4. Invoke with error handling
    try:
        result = graph.invoke({"raa_output": raa_dict})
    except NormalisationError as e:
        raise RuntimeError(f"RAA output is malformed — cannot render diagrams: {e}")

    # 5. Inspect results
    report = result["session_report"]
    print(f"AGA complete: {report.completed_count}/{report.total_diagrams_expected} "
          f"diagrams rendered in {report.wall_clock_seconds:.1f}s")

    for fd in result["failed_diagrams"]:
        print(f"  FAILED {fd.diagram_id}: {fd.last_error[:120]}")

    # 6. Route outputs downstream
    #    - PNGs + sidecars are already in output_dir/
    #    - aga_report.json is already in output_dir/
    #    - result["completed_diagrams"] can be used for further processing

    return result
```

---

## 10. Configurability Checklist

Every knob the Orchestrator may need to tune is either an `AGAConfig` field or a model constructor argument:

| What to tune | Where | Example |
|-------------|-------|---------|
| LLM provider & model | `AGAConfig.llm` constructor | `ChatOpenAI(model="gpt-4o")` |
| Temperature | `AGAConfig.llm` constructor | `ChatOpenAI(model="gpt-4o", temperature=0.1)` |
| LLM timeout | `AGAConfig.llm` constructor | `ChatOpenAI(model="gpt-4o", timeout=120)` |
| Max render attempts | `AGAConfig.max_retries` | `max_retries=3` |
| PlantUML server URL | `AGAConfig.plantuml_base_url` | `plantuml_base_url="https://..."` |
| Output directory | `AGAConfig.output_dir` | `output_dir="projects/foo/diagrams"` |
| Run the same input with different configs | Build new graph, re-invoke | `build_graph(config2).invoke(...)` |
| Stream progress | `.stream()` with `output_keys` | See §4.3 |
| Per-diagram updates | `.stream()` with `stream_mode="updates"` | See §4.4 |

---

## 11. Design Constraints Summary

| Constraint | Rule |
|------------|------|
| Public API | Only `AGAConfig` and `build_graph` are imported from `aga` |
| LLM ownership | Orchestrator constructs, configures, and owns the `BaseChatModel` |
| Config immutability | `AGAConfig` is frozen — construct a new one for different settings |
| Input format | `{"raa_output": raw_dict}` — exactly one key |
| Output format | `{completed_diagrams, failed_diagrams, session_report}` — exactly three keys |
| No diagram dropped | `completed_count + failed_count == total_diagrams_expected` always |
| Filesystem outputs | PNGs + sidecar JSONs + `aga_report.json` in `output_dir` |
| Error propagation | `NormalisationError` propagates; diagram failures accumulate; LLM errors propagate |
| Checkpointing | Orchestrator persists `raa_output` before AGA invocation |
| Graph statelessness | Two `build_graph` calls produce independent graphs |

---

## 12. What the Orchestrator Does NOT Do

- It does not parse or validate `raa_output` — the AGA's `normalise_node` handles that.
- It does not construct or manage the ReAct agent — `build_graph` builds it internally.
- It does not write PNGs, sidecars, or `aga_report.json` — those are written by AGA nodes inside the graph.
- It does not modify PlantUML code or diagram content — that is the LLM agent's job.
- It does not retry failed diagram renders — the agent loop already handles retries up to `max_retries`.
- It does not need to understand C4 levels, entity registries, or diagram queue ordering — all opaque to the Orchestrator.
