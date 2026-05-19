# Implementation Plan: RAA Cross-Batch Coherence Injection

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/015-raa-coherence-injection/spec.md`

**Input**: Feature specification from `specs/015-raa-coherence-injection/spec.md`

## Summary

This plan details the implementation of the model serialization utility under `raa/utils/model_serializer.py`. The utility traverses the consolidated nested fields of `running_arch_model` (systems, containers, components) and generates a structured, indent-nested text representation. It prefixes this representation with the required hard constraint message and merges it into the prompt variables context of the parallel subgraph strategy nodes.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: None (Standard Library only)

**Storage**: State channels in LangGraph.

**Testing**: Pytest unit tests under `tests/` verifying correct tree serialization formats, prefix preservation, empty model cases, and prompt context payload inclusion.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Instantaneous serialization rendering.

**Constraints**: Serialization must sort keys/entities to ensure deterministic, reproducible text inputs. Injected warning prefix must match the specification exactly.

**Scale/Scope**: A single utility module (`raa/utils/model_serializer.py`) and unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Sorted traversal maintains consistent input texts for downstream LLM prompts.
- **Principle III: LLM Isolation & Context Injection**: Passed. No direct LLM interactions occur inside this serialization/context builder.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/015-raa-coherence-injection/
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
    └── model_serializer.py # Hierarchical tree serializer
tests/
└── test_model_serializer.py # Unit tests for model serializer
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
