# Implementation Plan: RAA Batch Queue Ordering

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/012-raa-batch-ordering/spec.md`

**Input**: Feature specification from `specs/012-raa-batch-ordering/spec.md`

## Summary

This plan details the implementation of the batch queue ordering node under `raa/nodes/batch_queue.py`. The node reads the active ordering strategy, assigns scores to requirement batches according to risk rankings, counts, or summed weights, inserts sorting metadata into each batch, and outputs the sorted list to the `batch_queue` state channel.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: None (Standard Library only)

**Storage**: State channels in LangGraph.

**Testing**: Pytest unit tests under `tests/` verifying risk priority sorting, count/weight overrides, metadata appending, and tie-breaking behavior.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Sub-millisecond execution using Python's standard `list.sort`.

**Constraints**: Fallback to `risk_first` on invalid configurations. Tie-breaking must be lexicographical on batch/group IDs to preserve determinism.

**Scale/Scope**: A single node module (`raa/nodes/batch_queue.py`) and unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Standard tie-breaking guarantees deterministic batch processing sequences across runs.
- **Principle III: LLM Isolation & Context Injection**: Passed. No LLM calls occur in this node.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/012-raa-batch-ordering/
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
    └── batch_queue.py         # RAA queue ordering node
tests/raa/
└── test_batch_queue.py       # Unit tests for queue ordering
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
