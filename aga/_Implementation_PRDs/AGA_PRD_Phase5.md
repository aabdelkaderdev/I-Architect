# Product Requirements Document
## Architecture Generation Agent (AGA) — Phase 5: Prompt Template Revision
**Version:** 1.0
**Status:** Draft
**Scope:** Full revision of the three Mustache prompt templates in `aga/prompts/` to match the actual RAA output schema. Covers the variable contract for each template, the serialisation rules that the prompt-rendering utility must follow, and the mapping from `DiagramSpec` source fields to template variables.

---

## 1. Overview

The existing prompts (`agent_instruction.md`, `code_generation.md`, `error_correction.md`) reference variables (`entities_json`, `relationships_json`, `boundary_groups_json`, `assumption_flags_json`) that were designed for an earlier, flat RAA schema. These variables have no correspondence to the actual RAA output, which uses an `l1/l2/l3` structure (see Phase 2 §3).

This phase revises all three templates in-place. No new files are created. The templates use standard [Mustache](https://mustache.github.io/) syntax extended with the custom `{{! skill: <tag> as <variable> }}` directive already supported by the AGA's prompt loader (as seen in the existing templates).

---

## 2. Files Revised in This Phase

| File | Change |
|------|--------|
| `aga/prompts/agent_instruction.md` | Full rewrite — variable contract aligned to RAA l1/l2/l3 schema |
| `aga/prompts/code_generation.md` | Full rewrite — source data variables updated, skill tag preserved |
| `aga/prompts/error_correction.md` | Minor revision — variables unchanged, clarifying wording updated |

---

## 3. Mustache Template Conventions

### 3.1 Syntax Rules

| Syntax | Meaning |
|--------|---------|
| `{{variable}}` | HTML-escaped variable interpolation |
| `{{{variable}}}` | Unescaped variable interpolation — used for JSON blocks and multiline code |
| `{{#flag}}...{{/flag}}` | Section — renders the block if `flag` is truthy |
| `{{^flag}}...{{/flag}}` | Inverted section — renders the block if `flag` is falsy |
| `{{! skill: <tag> as <var> }}` | Custom skill injection — loads tagged content from `Skills/references/c4.md` into `<var>` |

### 3.2 Variable Naming Rules

- All variable names are `snake_case`.
- JSON payload variables use a `_json` suffix and are always rendered with triple-braces `{{{...}}}` to prevent double-escaping of JSON quotes.
- Boolean flag variables use an `is_` prefix.

### 3.3 Diagram-Type Sections

All three diagram types (context, container, component) are served by a single template instance per prompt file, using boolean flag sections to control which blocks are rendered. The calling code sets exactly one of `is_context`, `is_container`, `is_component` to `true` and the others to `false`.

---

## 4. `aga/prompts/agent_instruction.md` — Revised

### 4.1 Variable Contract

| Variable | Type | Set by | Description |
|----------|------|--------|-------------|
| `diagram_id` | `str` | queue builder output | Stable diagram ID (e.g. `ctx`, `cnt-concern_batch_2`) |
| `diagram_type` | `str` | `DiagramSpec.diagram_type` | One of `context`, `container`, `component` |
| `diagram_label` | `str` | `DiagramSpec.label` | Human-readable diagram label |
| `plantuml_base_url` | `str` | `AGAConfig.plantuml_base_url` | PlantUML server URL to pass to the render tool |
| `output_path` | `str` | derived from `DiagramSpec.output_filename` + `AGAConfig.output_dir` | Absolute path for the output PNG |
| `max_retries` | `int` | `AGAConfig.max_retries` | Maximum render tool calls for this diagram, including the first render attempt |
| `is_context` | `bool` | renderer | `true` if `diagram_type == "context"` |
| `is_container` | `bool` | renderer | `true` if `diagram_type == "container"` |
| `is_component` | `bool` | renderer | `true` if `diagram_type == "component"` |
| `system_name` | `str` | `DiagramSpec.source_l1.system_name` | Context diagrams only |
| `system_description` | `str` | `DiagramSpec.source_l1.system_description` | Context diagrams only |
| `actors_json` | `str` | serialised `source_l1.actors` | Context diagrams only |
| `external_systems_json` | `str` | serialised `source_l1.external_systems` | Context diagrams only |
| `concern_id` | `str` | `DiagramSpec.source_l2.concern_id` | Container diagrams only |
| `condition` | `str` | `DiagramSpec.source_l2.condition` | Container diagrams only |
| `containers_json` | `str` | serialised `source_l2.containers` | Container diagrams only |
| `parent_container_id` | `str` | `DiagramSpec.source_l3.parent_container_id` | Component diagrams only |
| `components_json` | `str` | serialised `source_l3.components` | Component diagrams only |
| `relationships_json` | `str` | serialised relationships from the active source level | All diagram types |
| `c4_plantuml_rules` | `str` | skill injection | Loaded from `c4:rules` tag in `Skills/references/c4.md` |

### 4.2 Revised Template

```markdown
---
variables:
  - {name: diagram_id, type: string}
  - {name: diagram_type, type: string}
  - {name: diagram_label, type: string}
  - {name: plantuml_base_url, type: string}
  - {name: output_path, type: string}
  - {name: max_retries, type: number}
  - {name: is_context, type: boolean}
  - {name: is_container, type: boolean}
  - {name: is_component, type: boolean}
  - {name: system_name, type: string}
  - {name: system_description, type: string}
  - {name: actors_json, type: string}
  - {name: external_systems_json, type: string}
  - {name: concern_id, type: string}
  - {name: condition, type: string}
  - {name: containers_json, type: string}
  - {name: parent_container_id, type: string}
  - {name: components_json, type: string}
  - {name: relationships_json, type: string}
---
{{! skill: c4:rules as c4_plantuml_rules }}

You are the Architecture Generation Agent (AGA). Your task is to generate
a single C4-compliant PlantUML diagram from a structured architecture
description, render it using the `render_plantuml_tool`, and report success
or failure.

## C4 PlantUML Rules (STRICT)
{{{c4_plantuml_rules}}}

---

## Current Diagram
- **ID:** {{diagram_id}}
- **Type:** {{diagram_type}}
- **Label:** {{diagram_label}}
- **Output path:** {{output_path}}

---

{{#is_context}}
## Diagram Scope — System Context
Render a C4 Context diagram for the following system. Include all actors,
external systems, and their relationships to the system boundary.

**System name:** {{system_name}}
**System description:** {{system_description}}

### Actors (Persons)
{{{actors_json}}}

### External Systems
{{{external_systems_json}}}

### Relationships
{{{relationships_json}}}
{{/is_context}}

{{#is_container}}
## Diagram Scope — Container
Render a C4 Container diagram for the operational concern described below.
Group all containers inside a `System_Boundary`. Include any actors or
external systems referenced in the relationships.

**Concern ID:** {{concern_id}}
**Condition:** {{condition}}

### Containers
{{{containers_json}}}

### Relationships
{{{relationships_json}}}
{{/is_container}}

{{#is_component}}
## Diagram Scope — Component
Render a C4 Component diagram for the container identified below.
Group all components inside a `Container_Boundary`. Include any external
containers referenced in the relationships.

**Parent container ID:** {{parent_container_id}}

### Components
{{{components_json}}}

### Relationships
{{{relationships_json}}}
{{/is_component}}

---

## Tool Instructions
1. Generate valid PlantUML code for the diagram scope above.
2. Call `render_plantuml_tool` with:
   - `puml_code` = your generated PlantUML string
   - `output_path` = "{{output_path}}"
   - `output_type` = "png"
   - `base_url` = "{{plantuml_base_url}}"
3. If the tool returns a string starting with `"OK:"` → you are done.
4. If the tool returns a string starting with `"ERROR:"` → read the error,
   correct the PlantUML code minimally, and retry only if you have not already
   called the tool {{max_retries}} times for this diagram.

## Hard Constraints
- Do NOT invent entities or relationships not listed in the scope above.
- Use each entity's `canonical_id` as the PlantUML alias (no abbreviation).
- Do NOT modify this diagram's scope or mix C4 levels.
```

---

## 5. `aga/prompts/code_generation.md` — Revised

### 5.1 Purpose

This template provides the targeted code generation sub-prompt used when the agent needs a clean generation pass (first attempt) rather than a correction. It is shorter and more focused than `agent_instruction.md`.

### 5.2 Variable Contract

| Variable | Type | Description |
|----------|------|-------------|
| `diagram_type` | `str` | One of `context`, `container`, `component` |
| `is_context` | `bool` | Section flag |
| `is_container` | `bool` | Section flag |
| `is_component` | `bool` | Section flag |
| `system_name` | `str` | Context only — system display name |
| `system_description` | `str` | Context only — system description |
| `actors_json` | `str` | Context only |
| `external_systems_json` | `str` | Context only |
| `concern_id` | `str` | Container only |
| `condition` | `str` | Container only |
| `containers_json` | `str` | Container only |
| `parent_container_id` | `str` | Component only |
| `components_json` | `str` | Component only |
| `relationships_json` | `str` | All types |
| `c4_rules` | `str` | Skill-injected C4 rules |

### 5.3 Revised Template

```markdown
---
variables:
  - {name: diagram_type, type: string}
  - {name: is_context, type: boolean}
  - {name: is_container, type: boolean}
  - {name: is_component, type: boolean}
  - {name: system_name, type: string}
  - {name: system_description, type: string}
  - {name: actors_json, type: string}
  - {name: external_systems_json, type: string}
  - {name: concern_id, type: string}
  - {name: condition, type: string}
  - {name: containers_json, type: string}
  - {name: parent_container_id, type: string}
  - {name: components_json, type: string}
  - {name: relationships_json, type: string}
---
{{! skill: c4:rules as c4_rules }}

Generate PlantUML code for a **{{diagram_type}}** C4 diagram.

{{#is_context}}
- Include `@startuml`, then `!include` for `C4_Context.puml`.
- Declare a `System(...)` for "{{system_name}}" with description "{{system_description}}".
- Declare each actor below as `Person(canonical_id, name, description)`.
- Declare each external system as `System_Ext(canonical_id, name, description)`.
- Emit one `Rel(...)` per relationship below.
- Actors and external systems are from:
{{{actors_json}}}
{{{external_systems_json}}}
{{/is_context}}

{{#is_container}}
- Include `@startuml`, then `!include` for `C4_Container.puml`.
- Wrap all containers in `System_Boundary({{concern_id}}, "{{condition}}")`.
- Declare each container as `Container(canonical_id, name, "", description)`.
  Use an empty technology string unless a technology field is explicitly present
  in the serialized container data.
- Containers are from:
{{{containers_json}}}
{{/is_container}}

{{#is_component}}
- Include `@startuml`, then `!include` for `C4_Component.puml`.
- Wrap all components in `Container_Boundary({{parent_container_id}}, "{{parent_container_id}}")`.
- Declare each component as `Component(canonical_id, name, "", description)`.
  Use an empty technology string unless a technology field is explicitly present
  in the serialized component data.
- Components are from:
{{{components_json}}}
{{/is_component}}

## Relationships
{{{relationships_json}}}

## C4 Syntax Reference
{{{c4_rules}}}

Produce valid PlantUML wrapped in `@startuml` / `@enduml`.
Include `LAYOUT_WITH_LEGEND()` before `@enduml`.
Use each entity's `canonical_id` exactly as the PlantUML alias — no changes.
```

---

## 6. `aga/prompts/error_correction.md` — Revised

### 6.1 Changes

The variable set is unchanged from the original (`diagram_id`, `error_text`, `current_puml_code`, `retry_count`, `max_retries`). The only revision is:

- Add a reference to `c4:rules` via skill injection so the agent can cross-check the violated rule during correction.
- Sharpen the instruction to restate the tool error before applying a minimal fix.

### 6.2 Revised Template

```markdown
---
variables:
  - {name: diagram_id, type: string}
  - {name: error_text, type: string}
  - {name: current_puml_code, type: string}
  - {name: retry_count, type: number}
  - {name: max_retries, type: number}
---
{{! skill: c4:rules as c4_rules }}

The `render_plantuml_tool` returned an error for diagram **{{diagram_id}}**.
This is render attempt **{{retry_count}}** of **{{max_retries}}**.

## Error Text
{{{error_text}}}

## Current PlantUML Code
```plantuml
{{{current_puml_code}}}
```

## Correction Instructions
1. Briefly restate the exact tool error before changing the code.
2. Locate the specific line or construct in the code that caused the error.
3. Cross-reference the C4 rules below to identify the violated constraint.
4. Apply the **minimal fix** — do not restructure the entire diagram.
5. Return the corrected PlantUML code and call `render_plantuml_tool` again.

## C4 Rules (for cross-reference)
{{{c4_rules}}}
```

---

## 7. Template Rendering Utility

### 7.1 Purpose

A helper function serialises a `DiagramSpec` into the flat `dict` of Mustache variables expected by the templates. This function is called by the agent node (Phase 6) immediately before rendering a prompt.

### 7.2 Location

`aga/prompt_renderer.py` — new file created in this phase.

### 7.3 Signature

```python
def build_template_vars(
    spec: DiagramSpec,
    config: AGAConfig,
    retry_count: int = 0,
    error_text: str = "",
    current_puml_code: str = "",
) -> dict:
    """
    Build the flat variable dict for Mustache template rendering.

    Parameters
    ----------
    spec : DiagramSpec
        The diagram being processed.
    config : AGAConfig
        Runtime config (supplies plantuml_base_url, max_retries, output_dir).
    retry_count : int
        Current render attempt count for error_correction template.
    error_text : str
        Error message for error_correction template.
    current_puml_code : str
        Current PUML code for error_correction template.

    Returns
    -------
    dict
        Flat key→value dict ready to pass to the Mustache renderer.
    """
```

### 7.4 Serialisation Rules

- All Pydantic model lists (actors, containers, components, relationships) are serialised with `json.dumps([item.model_dump() for item in list_], indent=2, ensure_ascii=False)`.
- `output_path` is constructed as `str(Path(config.output_dir) / spec.output_filename)`.
- Boolean flags: `is_context = spec.diagram_type == "context"`, etc.
- Fields not applicable to the current diagram type are set to `""` or `[]` — never omitted — to avoid Mustache rendering errors on undefined variables.

### 7.5 Files Created

| File | Purpose |
|------|---------|
| `aga/prompt_renderer.py` | `build_template_vars(...)` helper |

---

## 8. Design Constraints Summary

| Constraint | Rule |
|------------|------|
| One template per purpose | Three prompt files — not one per diagram type |
| Sections for type branching | `{{#is_context}}`, `{{#is_container}}`, `{{#is_component}}` |
| JSON variables | Always triple-braces `{{{...}}}` to avoid quote escaping |
| Skill injection | `c4:rules` injected in all three templates |
| `canonical_id` as alias | Explicitly enforced in all templates |
| Undefined variables | Always set to `""` or `[]` — never omitted |
| `plantuml_base_url` in prompt | Explicitly passed to the agent so it always knows which URL to use |

---

## 9. What This Phase Defers

| Concern | Phase |
|---------|-------|
| Mustache rendering library selection and integration | Phase 6 |
| Agent node that calls `build_template_vars` and renders templates | Phase 6 |
| Full graph wiring | Phase 6 |
