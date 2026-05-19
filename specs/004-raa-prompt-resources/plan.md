# Implementation Plan: RAA Prompt Resource Bundle & Source Register

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/004-raa-prompt-resources/spec.md`

**Input**: Feature specification from `specs/004-raa-prompt-resources/spec.md`

## Summary

This plan outlines the design and files for the RAA Prompt Resource Bundle. It covers the creation of the source register, C4 and SAAM prompt constraint files, and tagged excerpt files under `raa/prompts/`. All excerpt blocks are constrained to a strict ≤25-word limit for LLM context optimization.

## Technical Context

**Language/Version**: Markdown, Plain Text (.txt)

**Primary Dependencies**: None

**Storage**: Local filesystem

**Testing**: Python-based test script to verify that all files exist and all files under `raa/prompts/excerpts/` have a word count of 25 or less.

**Target Platform**: Linux filesystem

**Project Type**: Prompt Engineering Assets

**Performance Goals**: Minimum context token usage (achieved via strict word-count limits on excerpts).

**Constraints**: Excerpt files must not exceed 25 words.

**Scale/Scope**: 1 markdown source register, 2 markdown prompt constraint files, 5 plain-text excerpt files.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. Incorporates C4 levels and SAAM's 5-step process into structured prompt files.
- **Principle II: Deterministic Data Pipeline**: Passed.
- **Principle III: LLM Isolation & Context Injection**: Passed. Excerpts are formatted to be dynamically loaded and injected at execution time based on node tags.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/004-raa-prompt-resources/
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
raa/prompts/
├── source_register.md
├── c4_constraints.md
├── saam_constraints.md
└── excerpts/
    ├── c4_levels.txt
    ├── c4_notation.txt
    ├── c4_technology.txt
    ├── saam_steps.txt
    └── saam_scenarios.txt
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
