## Context

Phase 6 completes the Architecture Generation Agent (AGA) module. We need to expose its capabilities via `__init__.py`, finalize the structure and storage of its output data, integrate with downstream modules, gracefully handle `[assumed]` tags, and wrap the functionality in appropriate tests. The module currently builds robust representations (Phases 1-5) and now needs its "wiring".

The project uses a custom `StateGraph` (from `langgraph.graph`) compiled with a checkpointer for persistence. Per the current LangChain v1 / LangGraph APIs:
- **`create_agent`** (from `langchain.agents`) is the standard way to build agents; it replaced the deprecated `create_react_agent` from `langgraph.prebuilt`.
- **Runtime context** is now injected via the `context=` parameter at invocation time (backed by a `context_schema` dataclass), rather than `config["configurable"]`. Inside tools, it's accessed via `ToolRuntime[Context]`; inside middleware, via `Runtime[Context]` from `langgraph.runtime`.
- **`SqliteSaver`** is imported from `langgraph.checkpoint.sqlite` (package: `langgraph-checkpoint-sqlite`), and **`InMemorySaver`** from `langgraph.checkpoint.memory` (included with `langgraph-checkpoint`).
- **`RunnableConfig`** (from `langchain_core.runnables`) is still used for `thread_id` and `checkpoint_ns` in the `configurable` dict when invoking a compiled graph with a checkpointer.

Since the AGA is a custom `StateGraph` (not a `create_agent`-based agent), it accesses configuration via `RunnableConfig` passed to node functions. The orchestrator-provided context (output paths, etc.) can be threaded through the `configurable` dict in `RunnableConfig` at graph invocation, which is the standard LangGraph pattern for custom graphs.

## Goals / Non-Goals

**Goals:**
- Connect AGA seamlessly to the Orchestrator, threading runtime configuration via `RunnableConfig.configurable` for the custom `StateGraph`.
- Ensure all diagrams and metadata are consistently written to dynamically provided directories (no hardcoded paths).
- Output an `AGAOutput` object with strict types that downstream agents can consume.
- Append an `[assumed]` tag to the visual output for nodes flagged as assumed.

**Non-Goals:**
- Implementing parallel diagram generation (we are explicitly doing sequential generation).
- Deduplicating diagrams (deferred as per Open Design Decisions).
- Migrating from `StateGraph` to `create_agent`; the existing graph architecture is retained.

## Decisions

- **Sequential Generation**: We choose sequential generation using standard loops for simplicity and robustness in v1. Parallel generation can be added later as an optimization.
- **Sidecar Metadata vs Embedded**: PlantUML `.puml` files and metadata sidecar JSON files will be written alongside the PNG images, as this supports easier downstream parsing without complex file parsing heuristics.
- **Configurable Directories via `RunnableConfig`**: Output directories will NOT be created by the AGA; it assumes the Orchestrator has created them. Since the AGA uses a custom `StateGraph`, nodes receive `RunnableConfig` as a parameter and read `config["configurable"]["output_dir"]` and `config["configurable"]["checkpoint_db_path"]`. This follows the standard LangGraph pattern for custom graphs (see [Persistence docs](https://docs.langchain.com/oss/python/langgraph/persistence)).
- **Checkpointer**: The `SqliteSaver` from `langgraph.checkpoint.sqlite` is used for local/dev persistence, instantiated as `SqliteSaver(sqlite3.connect(db_path))`. For tests, `InMemorySaver` from `langgraph.checkpoint.memory` is preferred.

## Risks / Trade-offs

- [Risk] SA diagram accuracy scoring could break if the payload format changes → Mitigation: Strictly enforce the `AGAOutput` Pydantic model contract to ensure schema stability.
- [Risk] Failure in OS detection for PlantUML binary could halt execution → Mitigation: Wrap binary execution in robust fallbacks or clear structured failure reports.
- [Risk] Diagram deduplication might yield redundant files → Mitigation: Accept redundancy for now, deferring optimization until a manifest-driven deduplication strategy can be designed in future iterations.
- [Risk] `SqliteSaver` is recommended for experimentation/local only; production deployments should use `PostgresSaver` → Mitigation: Document clearly that `SqliteSaver` is dev-only; production migration path is to use Agent Server or switch to `langgraph-checkpoint-postgres`.
