## ADDED Requirements

### Requirement: LangGraph Sequential Pipeline
The system SHALL execute a 5-node StateGraph pipeline in sequence from `START` to `END`: Prep -> Functional -> ASR -> SAAM -> Report.

#### Scenario: Normal Execution
- **WHEN** the orchestrator invokes the compiled SA graph (`graph.invoke()`) with valid input state
- **THEN** the pipeline nodes execute sequentially without parallel branches or cycles and return the final state

### Requirement: SA Mock Nodes
The system SHALL provide mock implementations for the subjective scoring nodes (Functional, ASR, SAAM) to enable end-to-end processing.

#### Scenario: Mock Node Execution
- **WHEN** a mock scoring node is executed
- **THEN** it injects a score of 0 and an empty reasoning string into the state
