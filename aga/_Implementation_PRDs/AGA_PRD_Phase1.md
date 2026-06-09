# Product Requirements Document
## Architecture Generation Agent (AGA) — Phase 1: Module Scaffold & Configuration
**Version:** 1.0
**Status:** Draft
**Scope:** High-level module structure. Covers the creation of the AGA package skeleton, the `AGAConfig` Pydantic model, and the bare `graph.py` entry-point shell. No nodes, tools, or prompts are defined here — those are delegated to subsequent phases.

---

## 1. Overview

The AGA is a standalone LangGraph subgraph invoked by an external Orchestrator. Its sole responsibility is to receive the RAA output, derive a diagram generation queue, and render C4 PlantUML diagrams using an LLM-backed ReAct agent. This phase establishes the physical file layout, the importable package boundary, and the runtime configuration model that all later phases build upon.

**Pipeline position:**

```
Orchestrator → aga_graph.invoke({...}) → [AGA subgraph] → AGAOutput
```

The AGA is agnostic to how the Orchestrator is implemented. It exposes one public surface: a compiled `StateGraph` object that the Orchestrator calls via `.invoke()` or `.stream()`.

---

## 2. Files Created in This Phase

| File | Purpose |
|------|---------|
| `aga/__init__.py` | Public package surface — re-exports `build_graph` and `AGAConfig` |
| `aga/config.py` | `AGAConfig` Pydantic model — full runtime configuration |
| `aga/graph.py` | `build_graph(config: AGAConfig) → CompiledStateGraph` — empty shell with `START → END` only |

No other files are created. All other concerns (schemas, nodes, tools, prompts) are addressed in later phases.

---

## 3. `aga/config.py` — `AGAConfig`

### 3.1 Purpose

A single Pydantic `BaseModel` that carries every runtime knob the AGA exposes to the Orchestrator. The Orchestrator instantiates one `AGAConfig` and passes it to `build_graph`. The graph and all its nodes receive configuration exclusively through this object — no environment variable reads or global singletons inside AGA nodes.

### 3.2 Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `llm` | `BaseChatModel` | *(required)* | Any LangChain `BaseChatModel` instance (e.g. `ChatOpenAI`, `ChatAnthropic`, `ChatOllama`). The Orchestrator constructs and configures the model externally — `AGAConfig` does not instantiate it. |
| `max_retries` | `int` | `5` | Maximum render attempts per diagram, including the first render attempt and any correction attempts. Once this many `render_plantuml_tool` calls have occurred, the diagram is recorded as failed and the queue advances. |
| `plantuml_base_url` | `str` | `"https://www.plantuml.com/plantuml"` | Base URL of the PlantUML rendering server. Override to a self-hosted instance if needed. |
| `output_dir` | `str` | `"aga/output"` | Filesystem directory where rendered PNGs and metadata sidecars are written. The directory is created at startup if it does not exist. |

### 3.3 Validation Rules

- `llm` is required — there is no default. The Orchestrator must always pass a pre-constructed `BaseChatModel` instance. Passing `None` raises a `ValidationError` at construction time.
- `max_retries` must be `>= 1`.
- `output_dir` is accepted as a raw string. Path creation (and failure handling) is deferred to graph execution in Phase 6 — `AGAConfig` itself does not perform filesystem operations.
- `plantuml_base_url` must be a non-empty string. No URL format validation is applied at the config level — the server availability guard (Phase 6) validates reachability at runtime.

### 3.4 Design Notes

- `AGAConfig` uses `model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)`. `frozen=True` prevents mutation after construction; `arbitrary_types_allowed=True` permits Pydantic to accept the `BaseChatModel` instance (a non-primitive type) without raising a schema error.
- Accepting `BaseChatModel` externally is intentional: it gives the Orchestrator full control over model provider, temperature, timeout, retry logic, and any provider-specific options (e.g., `response_format`, `tool_choice`). The AGA never needs to know which provider is in use.
- `build_graph` receives the ready model from `config.llm` and passes it into node closures via capture. No model instantiation happens inside `build_graph`.
- No `@validator` or `@field_validator` beyond the `max_retries` check. The config intentionally stays thin — it is not a full application settings registry.

### 3.5 Example

```python
from langchain_openai import ChatOpenAI
from aga.config import AGAConfig

# Orchestrator builds the model with whatever options it needs
llm = ChatOpenAI(model="gpt-4o", temperature=0.1, timeout=60)

cfg = AGAConfig(
    llm=llm,
    max_retries=3,
    plantuml_base_url="https://www.plantuml.com/plantuml",
    output_dir="projects/my_project/diagrams",
)
```

The same pattern works for any LangChain-supported provider:

```python
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

# Anthropic
cfg = AGAConfig(llm=ChatAnthropic(model="claude-3-5-sonnet-20241022"), output_dir="out/")

# Local Ollama
cfg = AGAConfig(llm=ChatOllama(model="llama3.1"), output_dir="out/")
```

---

## 4. `aga/graph.py` — `build_graph`

### 4.1 Purpose

The single public factory function that constructs and compiles the AGA `StateGraph`. In Phase 1 it is an intentionally empty shell: `START → END` only, with no nodes. Later phases add nodes and edges incrementally without changing this function's signature or the module's public API.

### 4.2 Signature

```python
from langgraph.graph import StateGraph, START, END
from aga.config import AGAConfig

def build_graph(config: AGAConfig):
    """
    Build and compile the AGA StateGraph.

    Parameters
    ----------
    config : AGAConfig
        Runtime configuration. Passed into node closures at build time.

    Returns
    -------
    CompiledStateGraph
        Ready to call via .invoke() or .stream().
    """
    builder = StateGraph(...)   # state schema added in Phase 2
    builder.add_edge(START, END)
    return builder.compile()
```

### 4.3 Design Constraints

- `build_graph` must not perform any I/O (network, filesystem, subprocess) at call time. All I/O happens inside nodes at graph execution time.
- The returned compiled graph is stateless: calling `build_graph` twice with the same config produces two independent graphs. No module-level cache or singleton is created.
- The LLM is **not** instantiated inside `build_graph`. `build_graph` captures the already-constructed `config.llm` instance and passes it into node / agent closures via Python closure capture. This avoids re-instantiating the model on every node call and keeps model ownership with the Orchestrator.

---

## 5. `aga/__init__.py` — Public Surface

The package `__init__.py` exposes exactly two names to the Orchestrator:

```python
from aga.config import AGAConfig
from aga.graph import build_graph

__all__ = ["AGAConfig", "build_graph"]
```

No other AGA-internal symbols are part of the public API. Orchestrator code should only ever import from `aga` directly:

```python
from aga import AGAConfig, build_graph
```

---

## 6. What This Phase Defers

The following are out of scope for Phase 1 and are addressed in later phases:

| Concern | Phase |
|---------|-------|
| State schema (`AGAInputState`, `AGAInternalState`, `AGAOutputState`) | Phase 2 |
| RAA output type definitions (`RAAOutput`, `DiagramSpec`, entity types) | Phase 2 |
| Diagram queue builder (derives `DiagramSpec` list from RAA output) | Phase 3 |
| LangGraph tool adapter for `render_plantuml` | Phase 4 |
| Mustache prompt template revision for real RAA schema | Phase 5 |
| Full node wiring, entry node, error handling, output assembly | Phase 6 |

---

## 7. Design Constraints Summary

| Constraint | Rule |
|------------|------|
| Public API | Only `AGAConfig` and `build_graph` are exported from the `aga` package |
| Config immutability | `AGAConfig` is frozen after construction (`ConfigDict(frozen=True, arbitrary_types_allowed=True)`) |
| LLM ownership | The Orchestrator constructs and owns the `BaseChatModel`; AGA only uses it |
| I/O in `build_graph` | None — all I/O deferred to graph execution time |
| LLM capture | `config.llm` is captured into node closures at `build_graph` call time |
| Orchestrator contract | Orchestrator imports only from `aga` — no internal module paths |
