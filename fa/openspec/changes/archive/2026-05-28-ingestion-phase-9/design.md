## Context

The ingestion pipeline previously comprised isolated components defined in Phases 1 through 8 (format router, PDF/DOCX/TXT extractors, JSON validator, normaliser, and RFA filtering logic). To form a cohesive, executable pipeline, a top-level orchestrator must be introduced to wire these components together, manage state passing, handle conditional branching based on the uploaded file format, and ensure robustness across long-running or interrupted tasks (e.g., during LLM-based filtering). This design defines that LangGraph-based integration layer.

## Goals / Non-Goals

**Goals:**
- Wire all nodes (Format Routing, Extractors, Normaliser, RFA, Output Assembly) into a single, cohesive LangGraph `StateGraph`.
- Implement a strictly typed state schema (`IngestionState` TypedDict) reflecting the defined channels.
- Support durable execution via SQLite-based checkpointing using `thread_id` (via `config["configurable"]`) and `db_path`.
- Enforce that output requirements are validated (at least one valid requirement) before the orchestrator consumes them.

**Non-Goals:**
- Modifying the internals of the individual nodes (e.g., how the RFA classifies).
- Defining the orchestrator that actually invokes this graph.

## Decisions

- **LangGraph StateGraph for Orchestration**: Chosen over standard sequential execution because of the need for conditional routing and mid-process checkpointing, especially to prevent losing partial results during the expensive RFA step.
- **LLM via `context_schema` + `Runtime`, Not State**: The graph is created with `StateGraph(IngestionState, context_schema=IngestionContext)` where `IngestionContext` is a `@dataclass` holding the LLM. Nodes access it via `runtime: Runtime[IngestionContext]` (from `langgraph.runtime`). The caller passes it as `graph.invoke(input_state, context=IngestionContext(llm=llm_instance))`. This ensures state remains serialisable and follows the patterns established by other pipeline agents (ARLO, RAA, AGA, SA).
- **Project-Scoped Checkpointing**: Using `SqliteSaver` (from `langgraph-checkpoint-sqlite`) with a project-specific database path provided by the caller ensures that ingestion state is correctly segmented by project.
- **Thread ID Convention**: Identifying runs via `ing-` prefixed SHA256 hashes of the filepath and timestamp, passed via `config={"configurable": {"thread_id": "<computed_id>"}}` to uniquely trace ingestion runs separately from other agent tasks.
- **`@task` for fine-grained RFA checkpointing**: Inside the RFA node, each batch classification is wrapped with the `@task` decorator (from `langgraph.func`). Task results are checkpointed, so resuming a thread can skip completed task work inside the node without needing to split the RFA into multiple graph nodes.
- **Output Assembly Node**: Adding Node 5 as a final gatekeeper to explicitly check for `EmptyRequirementsError` before the orchestrator continues, ensuring upstream errors or edge-cases don't result in silent failures propagating into ARLO.

## Risks / Trade-offs

- **Risk: Checkpointer Failure** → If the SQLite database is unavailable, the pipeline falls back to a fresh start instead of crashing, emitting a WARNING log. This trades optimal resumption for robustness.
- **Risk: Long Checkpoint Sizes** → Default `overwrite` semantics simplify the reducer logic but might mean large document sets duplicate some state history. The 7-day retention policy ensures we periodically prune old runs to mitigate disk bloat.
