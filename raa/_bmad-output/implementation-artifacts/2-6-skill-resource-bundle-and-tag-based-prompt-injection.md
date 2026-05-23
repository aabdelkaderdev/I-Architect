# Story 2.6: Skill Resource Bundle and Tag-Based Prompt Injection

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want to define design-time reference guidelines under a Skills resource bundle matching the structure of developer reference skills,
so that strategy-parallel subgraphs and final reconciliation nodes execute with structured, concise, and context-targeted instructions.

## Acceptance Criteria

1. **Skill resource bundle exists**: Given the RAA package, when this story is complete, then a package-local `raa/Skills/` directory must exist with `SKILL.md` plus reference markdown files for C4 Level Mapping, Entity Extraction, Relationship Extraction, Pattern Selection, and Technology Inference.

2. **Skill files follow Agent Skills structure**: Given a skill reference file, when authored, then it must include YAML frontmatter containing `name`, `description`, and `metadata` such as `target_node` and `version`, followed by sections for Product Summary / Definition, When to Use, Quick Reference / Rules, Decision Guidance, Workflow, Common Gotchas, and Verification Checklist.

3. **LangChain-style progressive disclosure is preserved**: Given the LangChain Agent Skills pattern, when RAA skill resources are loaded, then startup/runtime prompts must not ingest the full skill bundle; only explicitly requested reference sections are injected into prompt context.

4. **Prompt loader supports skill tag placeholders**: Given a prompt template containing skill placeholders, when `load_prompt(...)` renders it, then the loader must resolve each requested skill tag to a reference file and tagged section, inject the extracted text into the Mustache context, and render through `chevron.render()`.

5. **Tag extraction is deterministic**: Given a requested tag such as `entity_extraction:rules` or `entity_extraction:checklist`, when the loader resolves it, then it must find the matching tagged markdown section and extract only that section, not the whole file.

6. **Concise injection is enforced**: Given extracted reference content, when a section is injected into a prompt, then each injected bullet, checklist item, table row, or standalone rule statement must be `<= 25` words after markdown syntax is stripped.

7. **Missing resources fail clearly**: Given a requested skill file, section, or tag is absent, when rendering the prompt, then the loader must raise `FileNotFoundError`, `KeyError`, or a project-specific clear exception naming the missing resource and prompt template.

8. **Existing prompt system remains the single runtime path**: Given Story 2.2 introduced `raa/utils/prompt_loader.py` and `raa/prompts/*.md`, when this story is implemented, then developers must extend that loader and those templates instead of adding a second prompt-rendering system.

## Tasks / Subtasks

- [x] Task 1: Create the RAA Agent Skills resource bundle (AC: #1, #2, #3)
  - [x] 1.1 Create `raa/Skills/SKILL.md`.
  - [x] 1.2 Create `raa/Skills/references/` with the required files:
    - `c4_level_mapping.md`
    - `entity_extraction.md`
    - `relationship_extraction.md`
    - `pattern_selection.md`
    - `technology_inference.md`
  - [x] 1.3 Also create architecture-listed core references unless deliberately deferred in a comment in the story implementation notes:
    - `saam.md`
    - `c4.md`
    - `quality_attributes.md`
  - [x] 1.4 `SKILL.md` must follow LangChain Agent Skills expectations: frontmatter first, concise description for routing/progressive disclosure, and references listed with when-to-use guidance.
  - [x] 1.5 Each reference file must have frontmatter with `name`, `description`, and `metadata.target_node` plus `metadata.version`.
  - [x] 1.6 Each reference file must include the required sections: Product Summary / Definition, When to Use, Quick Reference / Rules, Decision Guidance, Workflow, Common Gotchas, Verification Checklist.
  - [x] 1.7 Do not copy full source documents into runtime prompts. The references are design-time resources; runtime prompt injection stays tag-scoped.

- [x] Task 2: Define the exact tag convention for reference sections (AC: #4, #5, #6, #7)
  - [x] 2.1 Use markdown heading tags, for example:
    - `## Quick Reference / Rules <!-- tag: entity_extraction:rules -->`
    - `## Verification Checklist <!-- tag: entity_extraction:checklist -->`
  - [x] 2.2 Extract content from the tagged heading until the next heading of the same or higher level.
  - [x] 2.3 Tags must be unique across the bundle. Duplicate tags must raise a clear exception.
  - [x] 2.4 Required tags at minimum:
    - `c4_level_mapping:rules`
    - `c4_level_mapping:checklist`
    - `entity_extraction:rules`
    - `entity_extraction:checklist`
    - `relationship_extraction:rules`
    - `relationship_extraction:checklist`
    - `pattern_selection:rules`
    - `pattern_selection:checklist`
    - `technology_inference:rules`
    - `technology_inference:checklist`
  - [x] 2.5 Add any strategy-specific tags needed by the existing prompts, such as `saam:steps` or `c4:relationships`, only if the implementation uses those snippets.

- [x] Task 3: Implement skill reference loading utilities (AC: #2, #4, #5, #6, #7)
  - [x] 3.1 Add `raa/utils/skill_loader.py`.
  - [x] 3.2 Implement package-local path constants using `Path(__file__).resolve().parent.parent / "Skills"`; do not use process current working directory.
  - [x] 3.3 Implement frontmatter parsing for the narrow supported subset needed here (`name`, `description`, `metadata`). Do not add a new YAML dependency unless the project already includes one.
  - [x] 3.4 Implement `load_skill_section(tag: str) -> str` or equivalent.
  - [x] 3.5 Implement section extraction by `<!-- tag: ... -->`, not by fuzzy matching display headings.
  - [x] 3.6 Implement concise-statement validation. Strip markdown markers, table pipes, checkbox markers, and inline code delimiters before counting words.
  - [x] 3.7 Raise clear exceptions with file path, tag, and line context for missing tags, duplicate tags, malformed frontmatter, or excerpt statements over 25 words.
  - [x] 3.8 Keep utility functions pure and unit-testable; no LLM calls, no LangGraph runtime, no network.

- [x] Task 4: Extend the existing prompt loader for tag injection (AC: #4, #5, #6, #7, #8)
  - [x] 4.1 Modify `raa/utils/prompt_loader.py`; do not create a parallel runtime prompt loader.
  - [x] 4.2 Preserve the existing public behavior: `load_prompt(template_name: str, context: dict) -> str` still renders plain Mustache prompts.
  - [x] 4.3 Add support for skill placeholder declarations in Mustache comments, for example:
    - `{{! skill: entity_extraction:rules as entity_extraction_rules }}`
    - `{{{entity_extraction_rules}}}`
  - [x] 4.4 Before calling `chevron.render()`, scan the template for skill declarations, resolve each tag through `skill_loader`, and add the extracted content to a copy of the render context.
  - [x] 4.5 Explicit caller-provided context keys must not be silently overwritten by injected skill keys. Raise a clear exception on collision.
  - [x] 4.6 Preserve `FileNotFoundError` for missing prompt templates and add similarly clear errors for missing skill references.
  - [x] 4.7 Keep prompt rendering deterministic and side-effect-free.

- [x] Task 5: Refactor existing prompts to use skill snippets (AC: #3, #4, #6, #8)
  - [x] 5.1 Update `raa/prompts/saam_analysis.md`.
  - [x] 5.2 Update `raa/prompts/pattern_matching.md`.
  - [x] 5.3 Update `raa/prompts/entity_extraction.md`.
  - [x] 5.4 Replace the current hard-coded C4 hierarchy rules with skill snippet placeholders where appropriate.
  - [x] 5.5 Keep all prompts Mustache `.md` files rendered by `load_prompt(...)`.
  - [x] 5.6 Do not inject full reference files. Prompts should contain only the specific rules/checklists needed by that node.
  - [x] 5.7 Keep the current structured-output instruction: output shape is enforced by `ArchFragment` Pydantic parsing, not raw JSON examples.

- [x] Task 6: Add tests for skills and prompt injection (AC: #1, #2, #4, #5, #6, #7, #8)
  - [x] 6.1 Add `tests/raa/unit/test_skill_loader.py`.
  - [x] 6.2 Test required `raa/Skills/SKILL.md` and reference files exist.
  - [x] 6.3 Test every reference file has required frontmatter keys and required sections.
  - [x] 6.4 Test `load_skill_section("entity_extraction:rules")` returns only the tagged section.
  - [x] 6.5 Test duplicate tags raise an explicit error.
  - [x] 6.6 Test missing tags raise an explicit error.
  - [x] 6.7 Test a line or table row above 25 words fails validation with file/tag context.
  - [x] 6.8 Add `tests/raa/unit/test_prompt_loader.py` or extend an existing prompt-loader test file.
  - [x] 6.9 Test `load_prompt(...)` still renders normal Mustache variables.
  - [x] 6.10 Test skill placeholder comments inject expected content into `{{{...}}}` variables.
  - [x] 6.11 Test context key collision raises a clear exception.
  - [x] 6.12 Regression-test current strategy prompts render successfully with representative batch context.

- [x] Task 7: Regression check Story 2.2 prompt/subgraph behavior (AC: #8)
  - [x] 7.1 Run Story 2.2 subgraph tests after prompt injection changes.
  - [x] 7.2 Verify `build_raa_a_subgraph`, `build_raa_b_subgraph`, and `build_raa_c_subgraph` still call `load_prompt(...)` and do not gain separate skill-loading logic.
  - [x] 7.3 Verify structured extraction still uses `with_structured_output(ArchFragment, include_raw=True)`.

### Review Findings

- [x] [Review][Patch] Duplicate tag check is not executed for found tags [raa/utils/skill_loader.py:228-248]
- [x] [Review][Patch] HTML comments and heading hashes are not stripped from validated headings [raa/utils/skill_loader.py:96-101]
- [x] [Review][Patch] Nested bullet points are not split correctly in validation [raa/utils/skill_loader.py:109-120]
- [x] [Review][Patch] Path traversal vulnerability in tag resolving [raa/utils/skill_loader.py:179-185]
- [x] [Review][Patch] Disk I/O overhead from missing skill cache [raa/utils/skill_loader.py:208-252]
- [x] [Review][Patch] Descriptions in reference files use labels instead of "Use when..." triggers [raa/Skills/references/*.md]
- [x] [Review][Patch] Skill loader does not truncate/limit description length to 1024 characters [raa/utils/skill_loader.py:55-93]
- [x] [Review][Patch] Skill loader does not enforce the 10 MB file size limit constraint [raa/utils/skill_loader.py:208-252]

## Dev Notes

### Current Implementation Baseline

Story 2.2 is in `review` and introduced the first runtime prompt infrastructure. Treat these files as active implementation state and extend them carefully:

| File | Current State | Story 2.6 Change |
| --- | --- | --- |
| `raa/utils/prompt_loader.py` | Simple `load_prompt(template_name, context)` that reads `raa/prompts/` and calls `chevron.render()`. | Extend this file to resolve skill-tag placeholders before rendering. Preserve existing behavior. |
| `raa/prompts/saam_analysis.md` | Contains inline C4 hierarchy rules and basic context variables. | Replace relevant inline rule blocks with targeted skill snippet placeholders. |
| `raa/prompts/pattern_matching.md` | Contains inline C4 hierarchy rules and basic context variables. | Inject pattern-selection plus C4/entity/relationship snippets as needed. |
| `raa/prompts/entity_extraction.md` | Contains inline C4 hierarchy rules and basic context variables. | Inject entity extraction, relationship extraction, C4 level mapping, and technology inference snippets as needed. |
| `raa/subgraphs/raa_a.py` | Calls `load_prompt("saam_analysis.md", context)` then `llm.with_structured_output(ArchFragment, include_raw=True)`. | Should continue to call `load_prompt(...)`; do not add skill loading inside the subgraph node. |
| `raa/subgraphs/raa_b.py` | Same pattern for `pattern_matching.md`. | Same preservation requirement. |
| `raa/subgraphs/raa_c.py` | Same pattern for `entity_extraction.md`. | Same preservation requirement. |

There is currently no `raa/Skills/` directory and no skill-loader utility.

### Epic And Architecture Context

Epic 2 Story 2.6 adds a design-time Skills resource bundle and tag-based prompt injection for strategy-parallel subgraphs and final reconciliation nodes. The acceptance criteria require skill reference files, a standard skill template, tag extraction, `<=25` word injected statements, dynamic Mustache context injection, and clear failures for missing files/sections/tags. [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.6: Skill Resource Bundle and Tag-Based Prompt Injection`]

Architecture requires runtime prompts to be Mustache `.md` files in `prompts/`, rendered via `chevron.render()`. It also states that LLM nodes receive only relevant excerpts, full source documents are never copied into prompts, and excerpts must be `<=25` words each. [Source: `_bmad-output/planning-artifacts/architecture.md#Prompt Template Standard (Mustache via Chevron)`]

The architecture describes `Skills/references/` as design-time authoritative references and `prompts/` as the runtime counterpart containing short injected excerpts. [Source: `_bmad-output/planning-artifacts/architecture.md#Skills Bundle Pattern (Agent Skills Spec)`]

Concrete repository path: use `raa/Skills/` inside the Python package. The epics text says `./Skills/`, but the architecture tree places `Skills/` under the `raa/` package next to `prompts/`, and the existing prompt loader is package-local.

### LangChain Docs MCP Context

Use the LangChain docs MCP as the reference for how skills are implemented:

- `/oss/python/deepagents/skills`: skills are directories containing `SKILL.md`; `SKILL.md` starts with frontmatter and then instructions; optional scripts, docs, templates, and other resources must be referenced from the skill file.
- `/oss/python/deepagents/skills`: agents read frontmatter first and load full skill content only when useful; this is progressive disclosure.
- `/oss/python/deepagents/harness`: each skill directory contains `SKILL.md`; skills can include scripts, reference docs, templates, and resources; frontmatter is read at startup and full content is reviewed when needed.
- `/oss/python/langchain/multi-agent/skills`: skills are prompt-driven specializations; reference awareness means a skill can point to additional assets and load them only when relevant.

Implementation inference from these docs: RAA should make `raa/Skills/SKILL.md` the routing/discovery file and put larger domain guidance in referenced files under `raa/Skills/references/`. RAA runtime prompts should not import all of that guidance; they should request specific tagged sections.

### Required Skill File Shape

Use this shape for `raa/Skills/SKILL.md`:

```markdown
---
name: raa
description: Requirements Analysis Agent references for C4 extraction, relationship mapping, pattern selection, technology inference, and SAAM-informed reconciliation.
metadata:
  version: "1.0"
  target: raa
---

# RAA Skill

## Overview
...

## References
- `references/entity_extraction.md` — use for entity extraction rules.
...
```

Use this shape for reference files:

```markdown
---
name: entity_extraction
description: Rules for extracting C4 entities from requirement batches.
metadata:
  target_node: raa_c
  version: "1.0"
---

# Entity Extraction

## Product Summary / Definition
...

## When to Use
...

## Quick Reference / Rules <!-- tag: entity_extraction:rules -->
- Prefer existing running-model entities when requirement intent matches.

## Decision Guidance
...

## Workflow
...

## Common Gotchas
...

## Verification Checklist <!-- tag: entity_extraction:checklist -->
- [ ] Every entity has requirement traceability.
```

Do not rely on heading text alone to resolve tags. The HTML comment marker is the tag source of truth.

### Prompt Placeholder Convention

Use this convention unless implementation discovers a better local fit:

```markdown
{{! skill: entity_extraction:rules as entity_extraction_rules }}

## Entity Extraction Rules
{{{entity_extraction_rules}}}
```

Rules:

- The comment declares `skill: <tag> as <context_key>`.
- The triple-mustache variable renders the injected markdown without escaping.
- The loader injects into a copy of `context`.
- If `context` already contains `<context_key>`, raise an exception instead of overwriting it.

### Previous Story Intelligence

Story 2.2 established these behaviors that must not regress:

- Runtime prompts already render through `raa/utils/prompt_loader.py`; this story should extend that loader.
- Subgraph nodes do not instantiate LLMs. They read configured LLMs from `config["configurable"]`.
- Subgraph extraction uses `llm.with_structured_output(ArchFragment, include_raw=True)`.
- Prompt rendering happens before structured output extraction.
- Recoverable model-structure issues become open questions through C4 validation, not prompt-loader exceptions.
- Prompt-loader exceptions are appropriate for programmer/configuration problems such as missing prompt files, missing skill tags, malformed reference files, or invalid overlong injected snippets.

[Source: `_bmad-output/implementation-artifacts/2-2-c4-metamodel-hierarchy-enforcement-in-private-subgraphs.md#Completion Notes List`]

### File Structure Requirements

Create:

| File | Purpose |
| --- | --- |
| `raa/Skills/SKILL.md` | Agent Skills discovery/routing file for RAA domain references. |
| `raa/Skills/references/c4_level_mapping.md` | C4 level assignment rules and checklist. |
| `raa/Skills/references/entity_extraction.md` | Entity extraction rules and checklist. |
| `raa/Skills/references/relationship_extraction.md` | Relationship derivation rules and checklist. |
| `raa/Skills/references/pattern_selection.md` | Architectural pattern decision guidance. |
| `raa/Skills/references/technology_inference.md` | Technology annotation inference rules. |
| `raa/Skills/references/saam.md` | SAAM scenario/evaluation reference if used by RAA-A or Judge prompts. |
| `raa/Skills/references/c4.md` | General C4 model reference if used by shared snippets. |
| `raa/Skills/references/quality_attributes.md` | Quality attribute reference if used by RAA-A/Judge prompts. |
| `raa/utils/skill_loader.py` | Skill frontmatter, tag extraction, word-limit validation. |
| `tests/raa/unit/test_skill_loader.py` | Skill-loader and reference-file tests. |
| `tests/raa/unit/test_prompt_loader.py` | Prompt-loader skill injection tests. |

Modify:

| File | Required Change |
| --- | --- |
| `raa/utils/prompt_loader.py` | Resolve skill declarations and inject snippets into Mustache context. |
| `raa/prompts/saam_analysis.md` | Replace inline rules with targeted snippet placeholders. |
| `raa/prompts/pattern_matching.md` | Replace inline rules with targeted snippet placeholders. |
| `raa/prompts/entity_extraction.md` | Replace inline rules with targeted snippet placeholders. |
| `tests/raa/unit/test_strategy_subgraphs.py` | Adjust only if prompt text expectations need the new injected snippets. |

### Testing Requirements

Run at minimum:

```bash
python3 -m pytest \
  tests/raa/unit/test_skill_loader.py \
  tests/raa/unit/test_prompt_loader.py \
  tests/raa/unit/test_strategy_subgraphs.py -q
```

Then run broader regression if prompt-loader changes affect existing tests:

```bash
python3 -m pytest tests/raa/unit -q
```

Expected test style:

- Skill-loader tests are pure filesystem/string tests.
- Prompt-loader tests render temporary or package prompt templates without LLM calls.
- Subgraph tests continue using fake structured-output wrappers; no live LLM/API calls.

### Implementation Pitfalls To Avoid

- Do not create top-level `Skills/` outside the package unless architecture is explicitly changed. Use `raa/Skills/`.
- Do not add a second prompt loader or bypass `load_prompt(...)`.
- Do not inject whole reference files into prompts.
- Do not allow overlong injected lines to pass because the whole section is short. Validate each bullet/table row/rule statement.
- Do not use fuzzy heading matching for tags. Use explicit `<!-- tag: ... -->` markers.
- Do not silently ignore missing tags or context key collisions.
- Do not put runtime prompt snippets in `SKILL.md`; keep `SKILL.md` for discovery and reference inventory.
- Do not add live LLM calls to tests.
- Do not rework Story 2.2 C4 validation as part of this story.

### References

- `_bmad-output/planning-artifacts/epics.md#Story 2.6: Skill Resource Bundle and Tag-Based Prompt Injection`
- `_bmad-output/planning-artifacts/architecture.md#Prompt Template Standard (Mustache via Chevron)`
- `_bmad-output/planning-artifacts/architecture.md#Skills Bundle Pattern (Agent Skills Spec)`
- `raa_module_specification.md#7. Reference Document Architecture`
- `_bmad-output/implementation-artifacts/2-2-c4-metamodel-hierarchy-enforcement-in-private-subgraphs.md#Completion Notes List`
- LangChain docs MCP: `/oss/python/deepagents/skills`
- LangChain docs MCP: `/oss/python/deepagents/harness`
- LangChain docs MCP: `/oss/python/langchain/multi-agent/skills`

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

- 74/74 skill_loader + prompt_loader tests pass
- 17/17 Story 2.2 subgraph regression tests pass
- 263/263 full unit suite passes

### Completion Notes List

- Story context created by BMad create-story workflow on 2026-05-23.
- LangChain docs MCP used to verify Agent Skills structure, progressive disclosure, referenced resources, and prompt-driven skill specialization.
- **Task 1:** Created `raa/Skills/SKILL.md` and 8 reference files under `raa/Skills/references/` with full frontmatter and all required sections.
- **Task 2:** Defined tag convention using `<!-- tag: file_prefix:section -->` HTML comments on markdown headings. Tags are extracted by regex, not fuzzy heading matching.
- **Task 3:** Implemented `raa/utils/skill_loader.py` with `load_skill_section(tag)`, frontmatter parsing (via pyyaml), section extraction by heading level, and ≤25 word statement validation.
- **Task 4:** Extended `raa/utils/prompt_loader.py` to scan for `{{! skill: <tag> as <key> }}` Mustache comments, resolve via skill_loader, inject into a copy of context (collision detection included), and render via chevron.
- **Task 5:** Refactored all three prompt templates (`saam_analysis.md`, `pattern_matching.md`, `entity_extraction.md`) to use skill snippet placeholders instead of hardcoded C4 hierarchy rules.
- **Task 6:** Created `tests/raa/unit/test_skill_loader.py` (55 tests) and `tests/raa/unit/test_prompt_loader.py` (19 tests) with comprehensive coverage.
- **Task 7:** Ran full unit suite — 263 tests pass, zero regressions. Subgraphs still use `load_prompt(...)` + `with_structured_output(ArchFragment, include_raw=True)`.

### File List

**New files:**
- `raa/Skills/SKILL.md`
- `raa/Skills/references/c4_level_mapping.md`
- `raa/Skills/references/entity_extraction.md`
- `raa/Skills/references/relationship_extraction.md`
- `raa/Skills/references/pattern_selection.md`
- `raa/Skills/references/technology_inference.md`
- `raa/Skills/references/saam.md`
- `raa/Skills/references/c4.md`
- `raa/Skills/references/quality_attributes.md`
- `raa/utils/skill_loader.py`
- `tests/raa/unit/test_skill_loader.py`
- `tests/raa/unit/test_prompt_loader.py`

**Modified files:**
- `raa/utils/prompt_loader.py`
- `raa/prompts/saam_analysis.md`
- `raa/prompts/pattern_matching.md`
- `raa/prompts/entity_extraction.md`

### Change Log

- 2026-05-23: Story 2.6 implementation complete — Skill resource bundle, tag-based prompt injection, prompt refactor, and full test coverage.
