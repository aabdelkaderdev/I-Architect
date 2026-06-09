## ADDED Requirements

### Requirement: Handle Assumed Entities in PlantUML
The system SHALL append the tag `[assumed]` to the description string of any entity that has `assumed: true` in its metadata when rendering PlantUML source code.

#### Scenario: Assumed node is rendered
- **WHEN** an entity in the arch_model has `assumed: true`
- **THEN** the corresponding PlantUML element definition includes `[assumed]` in its description text.

#### Scenario: Normal node is rendered
- **WHEN** an entity in the arch_model does NOT have `assumed: true`
- **THEN** the corresponding PlantUML element definition does NOT include `[assumed]`.
