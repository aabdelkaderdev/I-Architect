# prompt-templates Specification

## Purpose
TBD - created by archiving change phase-3-skills-prompts. Update Purpose after archive.
## Requirements
### Requirement: Maintain agent instruction template
The system SHALL provide an `agent_instruction.md` mustache template containing the system prompt for the AGA. The rendered output is intended for use with `create_agent(..., system_prompt=rendered_string)` or injection via a `before_model` / `@dynamic_prompt` middleware hook.

#### Scenario: Loading and rendering system prompt
- **WHEN** the agent instruction template is loaded and rendered with diagram context variables (`diagram_id`, `diagram_type`, `focus_entity_id`, `focus_entity_label`, `entities_json`, `relationships_json`, `max_retries`)
- **THEN** the output includes the C4 PlantUML rules (injected from the `c4:rules` skill tag) and all diagram variables substituted

#### Scenario: Skill tag injection
- **WHEN** the template contains the directive `{{! skill: c4:rules as c4_plantuml_rules }}`
- **THEN** `prompt_loader.py` resolves the tag via `skill_loader.py` and injects the content into the render context under key `c4_plantuml_rules`

### Requirement: Maintain code generation template
The system SHALL provide a `code_generation.md` mustache template that defines the user prompt for generating a single PlantUML diagram.

#### Scenario: Loading and rendering code generation prompt
- **WHEN** the template is rendered with variables (`diagram_type`, `focus_entity_id`, `focus_entity_label`, `focus_entity_description`, `elements_block`, `relationships_block`)
- **THEN** the output includes the C4 rules (injected from `c4:rules`) and all entity/relationship blocks substituted

### Requirement: Maintain error correction template
The system SHALL provide an `error_correction.md` mustache template for correcting PlantUML syntax errors returned by the PlantUML server.

#### Scenario: Loading and rendering error correction prompt
- **WHEN** the template is rendered with variables (`diagram_id`, `error_text`, `current_puml_code`, `retry_count`, `max_retries`)
- **THEN** the output includes the error text, current code, and retry count/max substituted, with instructions for minimal correction

