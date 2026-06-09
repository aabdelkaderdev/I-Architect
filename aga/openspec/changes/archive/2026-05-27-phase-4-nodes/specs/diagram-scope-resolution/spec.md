## ADDED Requirements

### Requirement: Derive Diagram Work Queue
The system SHALL parse a flat JSON architectural model and derive a complete diagram work queue (`diagram_queue` of `DiagramSpec` objects).

#### Scenario: Valid flat JSON with systems and containers
- **WHEN** the `input_parsing` node receives a flat JSON model with `system` and `container` entities
- **THEN** it derives context, container, and component diagrams mapped to the appropriate focus entities and populates the `diagram_queue`.

### Requirement: Diagram Scope Filtering
The system SHALL NOT generate diagrams for entities that have no relationships in the target `diagram_scope`.

#### Scenario: Entity with no scoped relationships
- **WHEN** evaluating an entity for a specific diagram type (e.g., `context`) but no relationships have `diagram_scope = "context"` involving that entity
- **THEN** the system skips generating that specific diagram.

### Requirement: Canonical Diagram ID Assignment
The system SHALL assign standardized IDs and target file paths to the derived `DiagramSpec` items based on the focus entity.

#### Scenario: Generating Diagram IDs
- **WHEN** creating a `DiagramSpec` for a system or container
- **THEN** the system applies the prefixes `ctx-` (Context), `cnt-` (Container), or `cmp-` (Component) to the entity ID, and configures the target PNG, PUML, and JSON metadata file paths accordingly.
