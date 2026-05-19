# Implementation Plan: RAA Batch Coherence Gate

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/011-raa-batch-coherence/spec.md`

**Input**: Feature specification from `specs/011-raa-batch-coherence/spec.md`

## Summary

This plan details the implementation of the coherence gate node under `raa/nodes/coherence_gate.py`. The node calculates the average cosine similarity of a batch's requirement embeddings to its centroid. If it falls below 0.55, the node splits the batch into two sub-batches using a deterministic 2-way clustering algorithm, re-evaluates both, and routes them appropriately (replacing the batch if both pass, or flagging the original batch with `reduced_confidence = true` if either fails).

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `numpy`

**Storage**: State channels in LangGraph.

**Testing**: Pytest unit tests under `tests/` verifying correct coherence calculations, deterministic splitting behavior, queue mutation, and state flag updates.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Deterministic, fast clustering with NumPy to ensure zero runtime delays.

**Constraints**: Coherence threshold is strictly 0.55. Clustering must be 100% deterministic (seeded centroids or static split logic).

**Scale/Scope**: A single node module (`raa/nodes/coherence_gate.py`) and unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Seeded clustering ensures matching inputs produce identical batches and splits.
- **Principle III: LLM Isolation & Context Injection**: Passed. No LLM calls occur in this node.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/011-raa-batch-coherence/
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
    └── coherence_gate.py # RAA coherence gate node
tests/raa/
└── test_coherence_gate.py # Unit tests for coherence gate
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
