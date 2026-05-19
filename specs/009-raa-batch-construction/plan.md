# Implementation Plan: RAA Batch Construction

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/009-raa-batch-construction/spec.md`

**Input**: Feature specification from `specs/009-raa-batch-construction/spec.md`

## Summary

This plan details the implementation of the batch construction node under `raa/nodes/batch_construction.py`. The node calculates centroids for condition groups, runs a cosine similarity query against non-ASR requirement vectors using `numpy` and `sqlite3`, filters out candidates below a similarity score of 0.65, and caps candidates at 10. A fallback re-embeds the nominal condition on the fly if a condition group contains zero ASRs.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `sqlite3`, `numpy`, `fastembed` (for fallback embedding)

**Storage**: In-memory math matrices and SQLite reads.

**Testing**: Pytest unit tests under `tests/` verifying correct centroid math, fallback re-embedding, cosine similarity metrics, and candidate caps.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Element-wise array math using Numpy to prevent performance bottlenecks.

**Constraints**: Cap of 10 candidates per batch, similarity threshold >= 0.65.

**Scale/Scope**: A single node module (`raa/nodes/batch_construction.py`) and unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Batch calculations and vector math are fully deterministic.
- **Principle III: LLM Isolation & Context Injection**: Passed. No LLM calls are executed in this node.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/009-raa-batch-construction/
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
└── nodes/
    └── batch_construction.py # RAA batch builder node
tests/
└── test_batch_construction.py # Unit tests for batch builder
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
