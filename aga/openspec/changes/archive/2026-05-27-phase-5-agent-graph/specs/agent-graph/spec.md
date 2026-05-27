## ADDED Requirements

### Requirement: Graph Definition
The system SHALL define a LangGraph `StateGraph` that correctly wires all nodes together, using `AGAState` as a `TypedDict` schema.

#### Scenario: Graph execution starts
- **WHEN** the graph is invoked with an initial `AGAState` and a `config={"configurable": {"thread_id": "..."}}`
- **THEN** it begins execution at the `server_guard` node and conditionally routes to `input_parsing`

### Requirement: Graph Conditional Routing
The system SHALL correctly conditionally route the execution based on state properties using `add_conditional_edges`.

#### Scenario: Guard check fails
- **WHEN** the `server_guard` node raises a `ServerUnavailableException`
- **THEN** the graph execution halts immediately without attempting to process diagrams

#### Scenario: Graph traverses queue
- **WHEN** a diagram processing loop finishes (success or failure)
- **THEN** the graph checks if more diagrams exist; if yes, it routes to `agent_node`; if no, it routes to `output_assembly`

### Requirement: Persistent Checkpointing
The graph SHALL utilize `SqliteSaver` from `langgraph-checkpoint-sqlite` to persist the state, passed to `graph.compile(checkpointer=checkpointer)`.

#### Scenario: State is check-pointed
- **WHEN** the processing of a single diagram concludes (success or failure) and a super-step boundary is reached
- **THEN** LangGraph automatically saves a checkpoint of the `AGAState` via the configured `SqliteSaver`

### Requirement: Runtime Context Injection
The graph nodes SHALL receive runtime dependencies (e.g., LLM model reference) via the `Runtime` object from `langgraph.runtime`, not via state channels.

#### Scenario: Node accesses runtime context
- **WHEN** a node function is invoked with `runtime: Runtime[Context]`
- **THEN** it accesses the LLM and other dependencies through `runtime.context`
