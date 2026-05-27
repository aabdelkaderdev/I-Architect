## ADDED Requirements

### Requirement: Define C4 PlantUML syntax rules
The system SHALL provide a comprehensive guide on C4 PlantUML syntax, including element macros (`Person`, `System`, `Container`, `Component`), relationship syntax (`Rel`, `Rel_D`, `Rel_U`), and layout directives (`LAYOUT_WITH_LEGEND`, `LAYOUT_TOP_DOWN`).

#### Scenario: Agent requests C4 rules
- **WHEN** the skill tag `c4:rules` is resolved by `skill_loader.py`
- **THEN** the loader returns the "Rules" section content from `aga/Skills/references/c4.md`

### Requirement: Provide C4 diagram examples
The system SHALL provide structural examples for context, container, and component diagrams in C4 PlantUML format, each wrapped in `@startuml`/`@enduml` with the appropriate C4 include.

#### Scenario: Agent requests context example
- **WHEN** the skill tag `c4:context_example` is resolved by `skill_loader.py`
- **THEN** the loader returns the context diagram example from `aga/Skills/references/c4.md`

#### Scenario: Agent requests container example
- **WHEN** the skill tag `c4:container_example` is resolved by `skill_loader.py`
- **THEN** the loader returns the container diagram example from `aga/Skills/references/c4.md`

#### Scenario: Agent requests component example
- **WHEN** the skill tag `c4:component_example` is resolved by `skill_loader.py`
- **THEN** the loader returns the component diagram example from `aga/Skills/references/c4.md`

### Requirement: Skill manifest with YAML frontmatter
The skill manifest (`aga/Skills/SKILL.md`) SHALL declare the skill name, description, and metadata in YAML frontmatter, and SHALL list available tags with their reference file paths.

#### Scenario: Parsing the skill manifest
- **WHEN** `skill_loader.py` reads `aga/Skills/SKILL.md`
- **THEN** it extracts the YAML frontmatter (`name`, `description`, `metadata`) and the tag-to-reference mapping from the References table
