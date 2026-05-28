## Why

The ingestion pipeline requires a top-level orchestrator to wire together the individual phase components (Format Detection, PDF/DOCX/TXT Extractors, JSON Validator, Normaliser, and RFA). This LangGraph StateGraph acts as the integration layer, managing conditional routing, state channels, and checkpointing for durable execution and recovery from mid-process interruptions.

## What Changes

- Implement the top-level `StateGraph` for the ingestion module with `context_schema=IngestionContext`.
- Define a single conditional branch routing based on `file_format` using `add_conditional_edges`.
- Implement `SqliteSaver` checkpointing (from `langgraph-checkpoint-sqlite`), keyed by a `thread_id` and project-scoped `db_path`.
- Define the typed state schema `IngestionState` (TypedDict) with channels: `file_path`, `file_format`, `extracted_blocks`, `ingestion_config`, `filter_config`, `filter_report`, `extracted_requirements`.
- Inject the LLM via LangGraph's `context` kwarg (passed to `invoke`/`stream`) using a `@dataclass`-based `IngestionContext` schema and accessed in nodes via `runtime: Runtime[IngestionContext]`.
- Implement Node 5 (Output Assembly) to validate the final output and ensure at least one requirement is extracted.

## Capabilities

### New Capabilities
- `ingestion-graph`: The top-level LangGraph workflow orchestrating file extraction, format routing, normalisation, and RFA filtering.

### Modified Capabilities

## Impact

- The `ingestion` module will now expose a compiled LangGraph application (a `Pregel` instance).
- The orchestrator will need to pass `db_path` during compilation and `thread_id` via `config={"configurable": {"thread_id": ...}}` at runtime.
- The LLM is passed via `context=IngestionContext(llm=llm_instance)` at invocation time.
- Links all existing isolated nodes into a unified pipeline.
