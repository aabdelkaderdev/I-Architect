## ADDED Requirements

### Requirement: C4 PlantUML Parsing
The system SHALL parse PlantUML diagram strings using regex to extract C4 element aliases and macro types (System, Container, Component, Person, System_Ext).

#### Scenario: Extracting aliases from valid C4 macros
- **WHEN** a standard C4 macro is defined in the PlantUML string (e.g., `System(alias, "Label")`)
- **THEN** the parser extracts the `alias` and associates it with the `System` type

#### Scenario: Ignoring comments
- **WHEN** a line starts with a comment character (`'`)
- **THEN** the parser ignores the line and does not extract any aliases from it

### Requirement: Render Completeness Verification
The system SHALL verify that all three required PlantUML strings (Context, Container, Component) are non-empty.

#### Scenario: Missing diagram
- **WHEN** one of the three diagram strings is empty
- **THEN** a proportional deduction is applied to the diagram score and an `empty_diagram` issue is recorded

### Requirement: Entity Inclusion Verification
The system SHALL verify that expected architecture model entities appear in their respective diagrams based on the extracted aliases.

#### Scenario: Missing entity in diagram
- **WHEN** a Person defined in the architecture model is not found in the Context diagram
- **THEN** a proportional deduction is applied to the diagram score and a `missing_entity` issue is recorded

### Requirement: Hierarchy Validity Verification
The system SHALL verify that entities appear only in their appropriate architectural levels.

#### Scenario: Misplaced entity
- **WHEN** a Container alias is found at the top level of a Context diagram
- **THEN** a proportional deduction is applied to the diagram score and a `wrong_level` issue is recorded
