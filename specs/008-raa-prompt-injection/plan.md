# Implementation Plan: RAA Prompt Constraint Injection Policy

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/008-raa-prompt-injection/spec.md`

**Input**: Feature specification from `specs/008-raa-prompt-injection/spec.md`

## Summary

This plan outlines the design and files for the RAA prompt constraint injection helpers. We will implement tag-based excerpt retrieval under `raa/utils/prompt_loader.py`. The utility will load raw text files from `raa/prompts/excerpts/`, map colons in tag names to underscores (e.g. `c4:levels` -> `c4_levels.txt`), and provide a structured registry of node-to-tag configurations according to `RAA_Plan.md` §21C.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: None (Standard Library only)

**Storage**: Read-only local filesystem

**Testing**: Pytest unit tests under `tests/` verifying correct mappings, file reading logic, whitespace stripping, and exceptions.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python utility code

**Performance Goals**: Extremely low overhead (cached dictionary registry mapping nodes to tags).

**Constraints**: Excerpts must be retrieved dynamically per node. Only the requested excerpts should be injected to preserve LLM context.

**Scale/Scope**: A single utility module (`raa/utils/prompt_loader.py`) and associated unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. Excerpt lookups inject the exact C4 and SAAM compliance definitions required by the node.
- **Principle II: Deterministic Data Pipeline**: Passed.
- **Principle III: LLM Isolation & Context Injection**: Passed. Restricts LLM prompt context size by injecting only matching excerpts.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/008-raa-prompt-injection/
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
raa/
└── utils/
    └── prompt_loader.py   # Prompt excerpt loader and registry
tests/
└── test_prompt_loader.py  # Unit tests for prompt injection
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
