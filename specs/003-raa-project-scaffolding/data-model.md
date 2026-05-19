# Filesystem Layout: RAA Project Scaffolding

This document details the directories and files to be created as part of the project scaffolding.

## 1. Directory Tree Structure

The scaffolding creates the following paths at the repository root:

- `Skills/RAA/references/` — For design-time agent reference documents.
- `raa/` — The main package folder.
  - `graphs/` — Runtime graph nodes/routes.
  - `models/` — Data model structures.
  - `nodes/` — Agent nodes.
  - `state/` — State channels and custom reducers.
  - `utils/` — Utility modules.
  - `prompts/` — Runtime prompt resources.
    - `excerpts/` — Excerpt files for context injection.
- `embeddings/` — The shared embedding persistent databases (ignored by git).

---

## 2. Target Placeholder Files

### Reference Documents (`Skills/RAA/references/`)
- `C4.md`
- `Quality_Attributes.md`
- `Entity_Extraction.md`
- `Relationship_Extraction.md`
- `Pattern_Selection.md`
- `Technology_Inference.md`
- `C4_Level_Mapping.md`

### Runtime Prompts (`raa/prompts/`)
- `source_register.md`
- `c4_constraints.md`
- `saam_constraints.md`

### Prompt Excerpts (`raa/prompts/excerpts/`)
- `c4_levels.txt`
- `c4_notation.txt`
- `c4_technology.txt`
- `saam_steps.txt`
- `saam_scenarios.txt`

### Code Package Init and Module Files
- `raa/__init__.py`
- `raa/llm.py`
- `raa/runner.py`
