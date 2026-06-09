## ADDED Requirements

### Requirement: StateGraph definition and execution
The system SHALL define a LangGraph `StateGraph` parameterised by `IngestionState` (a `TypedDict`) and `context_schema=IngestionContext` (a `@dataclass`). The graph SHALL sequentially execute format detection, text extraction, normalisation, requirement filtering (RFA), and output assembly.

#### Scenario: Normal pipeline execution
- **WHEN** the orchestrator invokes the ingestion graph with `graph.invoke({"file_path": path, ...}, config={"configurable": {"thread_id": tid}}, context=IngestionContext(llm=llm))`
- **THEN** the graph executes the nodes sequentially and returns the final `extracted_requirements` in the output state.

### Requirement: Conditional routing by file format
The system SHALL use `add_conditional_edges` after the Format Detection node to route execution to the appropriate extraction node based on the `file_format` state value. A path map dictionary SHALL map format strings to node names.

#### Scenario: Routing a PDF file
- **WHEN** the format detector sets `file_format` to `"pdf"`
- **THEN** the graph routes execution to the PDF Extractor node.

#### Scenario: Routing a DOCX file
- **WHEN** the format detector sets `file_format` to `"docx"`
- **THEN** the graph routes execution to the DOCX Extractor node.

#### Scenario: Routing a TXT file
- **WHEN** the format detector sets `file_format` to `"txt"`
- **THEN** the graph routes execution to the TXT Extractor node.

#### Scenario: Routing a JSON file
- **WHEN** the format detector sets `file_format` to `"json"`
- **THEN** the graph routes execution to the JSON Validator node.

### Requirement: Typed state schema
The system SHALL define an `IngestionState` TypedDict as the graph state containing `file_path`, `file_format`, `extracted_blocks`, `ingestion_config`, `filter_config`, `filter_report`, and `extracted_requirements`, using default overwrite semantics (no custom reducers via `Annotated`).

#### Scenario: State modification
- **WHEN** a node completes execution and returns a state update
- **THEN** the state channel is overwritten with the new value rather than merged.

### Requirement: Checkpointing for durability
The system SHALL employ a `SqliteSaver` checkpointer (from `langgraph-checkpoint-sqlite`) passed to `builder.compile(checkpointer=saver)`. The `thread_id` SHALL be formatted as `"ing-" + sha256(file_path + timestamp)[:16]` and passed via `config={"configurable": {"thread_id": "<computed_id>"}}`.

#### Scenario: Successful checkpoint resume
- **WHEN** the pipeline is interrupted mid-execution during RFA and restarted with the same `thread_id` and `db_path`
- **THEN** the graph resumes execution from the last committed super-step checkpoint without re-running completed nodes.

#### Scenario: Checkpoint database unavailable
- **WHEN** the checkpointer database cannot be accessed at startup
- **THEN** the graph logs a WARNING and starts a fresh execution from the entry node.

### Requirement: LLM context injection
The system SHALL access the Language Model instance exclusively through LangGraph's `Runtime` object. The graph SHALL be created with `StateGraph(IngestionState, context_schema=IngestionContext)` where `IngestionContext` is a `@dataclass` holding the `llm: BaseChatModel` field. Nodes that need the LLM SHALL declare `runtime: Runtime[IngestionContext]` as their second parameter and access `runtime.context.llm`.

#### Scenario: RFA node accessing LLM
- **WHEN** the Requirement Filtering Agent node needs to call the LLM
- **THEN** it retrieves the LLM instance from `runtime.context.llm` (imported from `langgraph.runtime`).

### Requirement: Fine-grained RFA checkpointing via @task
The system SHALL wrap each batch classification call inside the RFA node with the `@task` decorator (from `langgraph.func`). Task results are automatically checkpointed by LangGraph when a checkpointer is present, so resuming a thread skips completed task work inside the node.

#### Scenario: Partial RFA completion and resume
- **WHEN** the RFA node has completed 3 out of 5 batch tasks and the process crashes
- **THEN** on resume, the 3 completed batch task results are restored from the checkpoint and only the remaining 2 tasks re-execute.

### Requirement: Output Assembly validation
The system SHALL include an Output Assembly node (Node 5) that validates the final pipeline result before completion.

#### Scenario: Empty output rejection
- **WHEN** Node 5 receives `extracted_requirements` with zero entries
- **THEN** it raises an `EmptyRequirementsError`.

#### Scenario: Valid output acceptance
- **WHEN** Node 5 receives `extracted_requirements` containing one or more entries
- **THEN** it completes execution successfully and the graph terminates via the `END` edge.
