## ADDED Requirements

### Requirement: C4 Hierarchy Reconstruction
The system SHALL traverse the flat list of entities and reconstruct the C4 model hierarchy (systems, containers, components).

#### Scenario: Flat List Parsing
- **WHEN** Node 1 receives the architecture model input
- **THEN** it correctly identifies parent-child relationships and builds a hierarchical tree in the state

### Requirement: Traceability Matrix Construction
The system SHALL build a matrix mapping each requirement ID to the entities that reference it.

#### Scenario: Extracting Traceability
- **WHEN** Node 1 processes entity requirements
- **THEN** it constructs a mapping of `req_id` to `[entity_id, level, deepest_level]`
