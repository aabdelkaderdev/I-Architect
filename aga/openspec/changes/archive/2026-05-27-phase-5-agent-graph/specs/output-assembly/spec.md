## ADDED Requirements

### Requirement: Finalizing Queue Processing
The system SHALL aggregate the final states of all processed diagrams when the queue is exhausted.

#### Scenario: Processing complete queue
- **WHEN** the diagram queue has been completely processed (no more diagrams in queue)
- **THEN** the state graph routes the flow to the `output_assembly` node

### Requirement: Output Assembly Formatting
The output assembly node SHALL collect all success and failure records and format them for the orchestrator.

#### Scenario: Output assembly generates report
- **WHEN** the `output_assembly` node executes
- **THEN** it compiles the execution results and finalizes the `AGAState` before the graph terminates
