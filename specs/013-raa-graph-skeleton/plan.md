# Implementation Plan: RAA LangGraph Skeleton

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/013-raa-graph-skeleton/spec.md`

**Input**: Feature specification from `specs/013-raa-graph-skeleton/spec.md`

## Summary

This plan details the implementation of the main LangGraph skeleton under `raa/graphs/main_graph.py`. The skeleton uses the authoritative `RAAState` from `raa/state/channels.py`, registers appropriate reducers for list variables, gates execution on the boolean state `embeddings_ready`, and sequentializes nodes: Preparation -> Batch Construction -> Overlap Bridging -> Coherence Gate -> Batch Queue Ordering.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `langgraph`

**Storage**: State channels in LangGraph memory saver checkpointing.

**Testing**: Pytest unit tests under `tests/` verifying graph compiling, sequential traversal, state reductions, and gating exceptions.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Instantaneous routing transition.

**Constraints**: Aborts if `embeddings_ready` is False.

**Scale/Scope**: A single graph module (`raa/graphs/main_graph.py`) and unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Standard Graph structures execute sequential nodes deterministically.
- **Principle III: LLM Isolation & Context Injection**: Passed. No direct LLM calls occur in this orchestration skeleton.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/013-raa-graph-skeleton/
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
└── graphs/
    └── main_graph.py    # Main LangGraph skeleton wiring
tests/
└── raa/
    └── test_main_graph.py   # Unit tests for LangGraph skeleton
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
