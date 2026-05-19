# Implementation Plan: RAA Per-Batch Judge Node

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/016-raa-judge-node/spec.md`

**Input**: Feature specification from `specs/016-raa-judge-node/spec.md`

## Summary

This plan covers the implementation of the judge node under `raa/nodes/judge.py`. It includes logic to score parallel fragments using SAAM scenarios via the `llm_judge` context parameter. It defines the 4-step deterministic merge algorithm (Entity Deduplication, Relationship Deduplication, Coverage Union with Orphan Prevention, and Tree Assembly). It handles recording of `hierarchy_conflict`, `scope_conflict`, and `coverage_gap` in the `open_questions` state. It correctly applies the `reduced_confidence` scoring multiplier and advances `batch_cursor`.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `langchain`, `langgraph`

**Storage**: State channels in LangGraph.

**Testing**: Pytest unit tests under `tests/` to verify mock SAAM scoring, deterministic merging, conflict logging, and hierarchical tree generation.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Constraints**: Must strictly prevent orphaned entities. Must not overwrite existing hierarchical entities incorrectly.

**Scale/Scope**: A single node module (`raa/nodes/judge.py`) and unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. C4 hierarchy is assembled and verified natively in code.
- **Principle II: Deterministic Data Pipeline**: Passed. The 4-step merge algorithm is strictly deterministic code, not LLM reasoning.
- **Principle III: LLM Isolation & Context Injection**: Passed. `llm_judge` is retrieved from context.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/016-raa-judge-node/
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
    └── judge.py         # Judge and merge logic
tests/
└── test_judge.py        # Unit tests for merge steps
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
