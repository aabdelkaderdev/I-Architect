# Implementation Plan: RAA Overlap Bridging

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/010-raa-overlap-bridging/spec.md`

**Input**: Feature specification from `specs/010-raa-overlap-bridging/spec.md`

## Summary

This plan details the implementation of the overlap bridging node under `raa/nodes/overlap_bridging.py`. The node compares centroid vectors of the condition groups, identifies adjacent pairs, computes bridging relevance scores for non-ASR requirement candidates, selects 1–3 bridge requirements (enforcing a hard cap of 3), injects them into both corresponding batches, and registers them in the `bridge_requirements` state dictionary.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `sqlite3`, `numpy`

**Storage**: State channels in LangGraph.

**Testing**: Pytest unit tests under `tests/` verifying correct adjacency filters, combined scoring calculations, selection bounds, batch modifications, and registration maps.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Negligible execution overhead using NumPy vector operations.

**Constraints**: Cap of 3 bridge requirements per adjacent pair.

**Scale/Scope**: A single node module (`raa/nodes/overlap_bridging.py`) and unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Adjacency and bridging computations are deterministic.
- **Principle III: LLM Isolation & Context Injection**: Passed. No LLM calls occur in this node.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/010-raa-overlap-bridging/
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
    └── overlap_bridging.py # RAA overlap bridging node
tests/
└── test_overlap_bridging.py # Unit tests for overlap bridging
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
