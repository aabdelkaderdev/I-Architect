## ADDED Requirements

### Requirement: Orchestrator Input Provisioning
The orchestrator SHALL provide all required inputs before invoking the ingestion graph: `file_path` (written to the `file_path` state channel), `ingestion_config` (serialised `IngestionConfig`), `filter_config` (serialised `FilterConfig`), a `BaseChatModel` instance (passed via the `context=` kwarg), `db_path` (passed to `build_ingestion_graph()`), and `thread_id` (passed via `config={"configurable": {"thread_id": ...}}`).

#### Scenario: Graph Invocation with LangGraph v1 API
- **WHEN** the orchestrator calls `build_ingestion_graph(db_path=db_path)` and invokes the compiled graph
- **THEN** it passes `file_path`, `ingestion_config`, and `filter_config` in the input state dict, the `BaseChatModel` via `context=IngestionContext(llm=llm_instance)`, and `thread_id` via `config={"configurable": {"thread_id": thread_id}}`.

### Requirement: Orchestrator Infrastructure Responsibilities
The orchestrator SHALL handle all infrastructure concerns including checkpoint directory creation, configuration validation against Phase 2 rules, file existence checks, error handling, and checkpoint lifecycles (7-day retention).

#### Scenario: Infrastructure Pre-checks
- **WHEN** the orchestrator prepares to invoke the pipeline
- **THEN** it verifies the file exists at `file_path`, validates `IngestionConfig` and `FilterConfig` against Phase 2 §6 rules, and ensures the `projects/{name}/checkpoints/` directory exists.

### Requirement: Orchestrator Output Processing
The orchestrator SHALL read the `extracted_requirements` (`dict[str, str]`) and `filter_report` (`dict | None`) from the final graph state, passing the requirements to ARLO and storing the report for downstream audit.

#### Scenario: Handoff to ARLO
- **WHEN** the ingestion graph completes successfully
- **THEN** the orchestrator maps `extracted_requirements` to `ARLOInput.requirements` and preserves passthrough channels (`experiment_config`, `matrix`).

### Requirement: Runtime Context via LangGraph context_schema
The ingestion graph SHALL define a `context_schema` dataclass (`IngestionContext`) containing a single `llm: BaseChatModel` field. The LLM instance SHALL be accessed by nodes via `runtime.context.llm` using `langgraph.runtime.Runtime[IngestionContext]`. The LLM MUST NEVER appear in a state channel.

#### Scenario: RFA Node Accesses LLM via Runtime Context
- **WHEN** the RFA node executes with filtering enabled
- **THEN** it obtains the LLM instance from `runtime.context.llm` (not from state) and uses it for classification.
