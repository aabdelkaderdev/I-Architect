## ADDED Requirements

### Requirement: Expose Public API
The AGA module SHALL expose its primary entry points via `__init__.py`.

#### Scenario: Orchestrator imports AGA
- **WHEN** the orchestrator imports the AGA module
- **THEN** it can successfully access the graph factory function (`create_aga_graph`), the `AGAOutput` TypedDict, and data models (`CompletedDiagram`, `FailedDiagram`, `SessionReport`).

### Requirement: Respect Orchestrator Configuration
The AGA module's graph nodes SHALL read output and checkpoint paths dynamically from `RunnableConfig` via `config["configurable"]` and SHALL NOT hardcode any output paths or attempt to create directories. This follows the standard LangGraph `StateGraph` pattern where node functions accept `config: RunnableConfig` as a parameter.

#### Scenario: Running the graph with config
- **WHEN** the compiled graph is invoked with `config={"configurable": {"thread_id": "run1:aga", "output_dir": "/custom/path/", "checkpoint_db_path": "/custom/db.sqlite"}}`
- **THEN** the AGA graph nodes save PNGs, PUML files, and sidecar JSON files directly into `/custom/path/` and the checkpointer uses `/custom/db.sqlite` for persistence.

### Requirement: Use Correct Checkpointer
The AGA module SHALL use `SqliteSaver` from `langgraph.checkpoint.sqlite` (package: `langgraph-checkpoint-sqlite`) for local persistence, instantiated with `SqliteSaver(sqlite3.connect(db_path))`. Tests SHALL use `InMemorySaver` from `langgraph.checkpoint.memory`.

#### Scenario: Graph compiled with SqliteSaver
- **WHEN** the orchestrator creates the checkpointer with `SqliteSaver(sqlite3.connect("aga.db"))`
- **THEN** the compiled graph correctly persists state at each super-step boundary.

### Requirement: Finalize Output Contract
The AGA module SHALL produce an output strictly conforming to the `AGAOutput` TypedDict, containing `completed_diagrams`, `failed_diagrams`, and a `session_report`.

#### Scenario: Successful execution returns correct schema
- **WHEN** the AGA module completes its generation successfully
- **THEN** the returned state dict contains the populated `AGAOutput` conforming to the defined schema.
