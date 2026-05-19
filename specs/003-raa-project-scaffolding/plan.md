# Implementation Plan: RAA Project Scaffolding

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/003-raa-project-scaffolding/spec.md`

**Input**: Feature specification from `specs/003-raa-project-scaffolding/spec.md`

## Summary

This plan sets up the directory layout and file scaffolding for the RAA (Requirement Analysis Agent) module. It establishes the design-time documentation bundle under `Skills/RAA/`, the runtime code and prompt templates folder under `raa/`, and ensures the shared `embeddings/` runtime folder is ignored by git. No functional business logic or runtime node code is implemented in this feature.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: None (Standard OS/Python filesystem libraries)

**Storage**: Local file system; local SQLite files under `embeddings/` are git-ignored.

**Testing**: Structural directories/files verification script.

**Target Platform**: Linux filesystem

**Project Type**: Project Scaffolding

**Performance Goals**: N/A

**Constraints**: Folder structure and names must strictly match the conventions defined in `RAA_Plan.md` Section 21. `raa/` is lowercase; `Skills/RAA/` matches the skill bundle directory naming style.

**Scale/Scope**: 3 root-level directories (`raa/`, `Skills/RAA/`, `embeddings/`), 5 subdirectories under `raa/`, 1 subdirectory under `Skills/`, and ~15 placeholder files/documents.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. Prompt resource bundles (`raa/prompts/`) and skill references (`Skills/RAA/references/`) are established with the correct authority layout.
- **Principle II: Deterministic Data Pipeline**: Passed. The shared embedding directory (`embeddings/`) is defined and the repository ignore rules are verified.
- **Principle III: LLM Isolation & Context Injection**: Passed. No LLM instances or configs are stored or defined.
- **Principle IV: Hierarchical Integrity (Orphan Prevention)**: Passed. Reference files define hierarchical constraints for C4 levels.
- **Principle V: Incremental Coherence (Batch-Sequential Model)**: Passed. Scaffold defines directories but no node triggers.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/003-raa-project-scaffolding/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
Skills/RAA/
├── SKILL.MD
└── references/
    ├── C4.md
    ├── Quality_Attributes.md
    ├── Entity_Extraction.md
    ├── Relationship_Extraction.md
    ├── Pattern_Selection.md
    ├── Technology_Inference.md
    └── C4_Level_Mapping.md

raa/
├── __init__.py
├── llm.py
├── runner.py
├── graphs/
├── models/
├── nodes/
├── state/
├── utils/
└── prompts/
    ├── source_register.md
    ├── c4_constraints.md
    ├── saam_constraints.md
    └── excerpts/
        ├── c4_levels.txt
        ├── c4_notation.txt
        ├── c4_technology.txt
        ├── saam_steps.txt
        └── saam_scenarios.txt

embeddings/
└── .gitignore
```

**Structure Decision**: Create directories using POSIX command-line calls or Python standard library scripts. Write placeholders as clean markdown/text files. Ensure Git ignore rules exist.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
