# Phase 3 — Skills & Prompt Templates

> **Goal:** Create the AGA skills bundle (SKILL.md manifest + C4 PlantUML reference) and all three mustache prompt templates, plus the utility loaders (`prompt_loader.py`, `skill_loader.py`) that resolve skill tags and render templates at runtime.
>
> **Depends on:** Phase 1 (folder scaffold exists)
> **Produces:** `aga/Skills/SKILL.md`, `aga/Skills/references/c4.md`, `aga/prompts/agent_instruction.md`, `aga/prompts/code_generation.md`, `aga/prompts/error_correction.md`, `aga/utils/prompt_loader.py`, `aga/utils/skill_loader.py`, `aga/utils/__init__.py`
> **Test fixture:** `arch_model_test_result-1.json`

---

## 8) Mustache Prompt Templates

### 8A — Template Loading Pattern

Following the RAA pattern (`raa/utils/prompt_loader.py`), AGA uses **chevron** for mustache rendering with skill tag injection:

- Templates live in `aga/prompts/*.md`
- Skill declarations use the `{{! skill: <tag> as <key> }}` directive
- Context variables use `{{variable}}` (escaped) and `{{{variable}}}` (unescaped/triple-stache for injected skill content)
- The `prompt_loader.py` resolves skill tags → loads reference content → injects into template → renders

### 8B — Agent Instruction Template (`agent_instruction.md`)

```mustache
{{! skill: c4:rules as c4_plantuml_rules }}

You are the Architecture Generation Agent (AGA). Your task is to generate
C4-compliant PlantUML diagrams from an architecture model.

## C4 PlantUML Rules (STRICT)
{{{c4_plantuml_rules}}}

## Diagram Specification
- Diagram ID: {{diagram_id}}
- Diagram Type: {{diagram_type}}
- Focus Entity: {{focus_entity_id}}
- Focus Entity Label: {{focus_entity_label}}

## Entities in Scope
{{entities_json}}

## Relationships in Scope
{{relationships_json}}

## Retry Policy
- Maximum {{max_retries}} correction attempts per diagram
- On syntax error: read the error, identify the faulty construct, fix minimally
- Do not restructure the entire diagram on a single error

## Constraints
- Do NOT invent entities or relationships not listed above
- Every PlantUML alias MUST exactly match a canonical entity ID
- Do NOT modify the architecture model — only translate it to diagram code
```

### 8C — Code Generation Template (`code_generation.md`)

```mustache
{{! skill: c4:rules as c4_rules }}

Generate PlantUML code for a {{diagram_type}} diagram.

## Focus Entity
- ID: {{focus_entity_id}}
- Label: {{focus_entity_label}}
- Description: {{focus_entity_description}}

## Elements
{{{elements_block}}}

## Relationships
{{{relationships_block}}}

## Generation Rules
{{{c4_rules}}}

Produce valid PlantUML wrapped in @startuml / @enduml.
Include LAYOUT_WITH_LEGEND() at the end.
```

### 8D — Error Correction Template (`error_correction.md`)

```mustache
The PlantUML server returned a syntax error for diagram {{diagram_id}}.

## Error Text
{{{error_text}}}

## Current PlantUML Code
{{{current_puml_code}}}

## Instructions
1. Quote the error text verbatim
2. Locate the offending construct in the code
3. Apply the minimal fix to resolve the error
4. Return the corrected PlantUML code

Attempt {{retry_count}} of {{max_retries}}.
```

---

## 9) Skills Bundle

### 9A — SKILL.md Manifest

The AGA skill manifest follows the same frontmatter-based pattern as RAA:

```yaml
---
name: c4-plantuml-syntax
description: Authoritative reference for generating C4 architecture diagrams
  using PlantUML. Covers element types, relationship syntax, and diagram layout.
metadata:
  version: "2.0"
  target: aga
---
```

### 9B — Skill Tag Registry

| Tag | Reference File | Content |
|-----|---------------|---------|
| `c4:rules` | `references/c4.md` | C4 PlantUML syntax rules, element macros, relationship arrows |
| `c4:context_example` | `references/c4.md` | Context diagram example |
| `c4:container_example` | `references/c4.md` | Container diagram example |
| `c4:component_example` | `references/c4.md` | Component diagram example |

### 9C — Skill Injection at Runtime

The `prompt_loader.py` resolves skill declarations in templates:

```
{{! skill: c4:rules as c4_plantuml_rules }}
```

This loads the tagged section from `aga/Skills/references/c4.md`, validates statement word limits, and injects the content into the render context under key `c4_plantuml_rules`.
