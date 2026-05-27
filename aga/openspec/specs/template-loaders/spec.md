# template-loaders Specification

## Purpose
TBD - created by archiving change phase-3-skills-prompts. Update Purpose after archive.
## Requirements
### Requirement: Skill tag resolution
The `skill_loader.py` utility SHALL parse YAML-frontmatter skill manifests and resolve skill tags (e.g. `c4:rules`) to the corresponding section content from reference files.

#### Scenario: Resolving a known skill tag
- **WHEN** provided a skill tag `c4:rules`
- **THEN** the loader reads `aga/Skills/SKILL.md`, locates the `c4:rules` entry in the tag registry, opens the mapped reference file (`references/c4.md`), extracts the matching section, and returns its content as a string

#### Scenario: Resolving an unknown skill tag
- **WHEN** provided a skill tag `c4:nonexistent`
- **THEN** the loader raises a `KeyError` with a message indicating the unresolved tag name

### Requirement: Mustache template rendering with skill injection
The `prompt_loader.py` utility SHALL read mustache templates from `aga/prompts/`, scan for `{{! skill: <tag> as <key> }}` directives, resolve each tag via `skill_loader.py`, inject the resolved content into the render context, and render the template using `chevron`.

#### Scenario: Rendering a template with skill directives and context variables
- **WHEN** rendering `agent_instruction.md` with context `{"diagram_id": "ctx-1", "diagram_type": "SystemContext", ...}`
- **THEN** the loader extracts the `{{! skill: c4:rules as c4_plantuml_rules }}` directive, resolves `c4:rules` via `skill_loader`, adds the content to the context under key `c4_plantuml_rules`, and renders the complete template via `chevron.render()`

#### Scenario: Missing required context variable
- **WHEN** rendering a template that expects `{{diagram_id}}` but the caller omits `diagram_id` from the context
- **THEN** the loader raises a `ValueError` listing the missing variable names

### Requirement: Template variable documentation
Each mustache template in `aga/prompts/` SHALL include a YAML frontmatter block listing its expected context variables (name and type), enabling the loader to validate inputs at render time.

#### Scenario: Template with frontmatter variable list
- **WHEN** `prompt_loader.py` reads `agent_instruction.md`
- **THEN** it parses the YAML frontmatter `variables` list and uses it for validation before rendering

