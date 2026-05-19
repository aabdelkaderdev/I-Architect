# Implementation Plan: RAA Parallel Subgraphs

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/014-raa-parallel-subgraphs/spec.md`

**Input**: Feature specification from `specs/014-raa-parallel-subgraphs/spec.md`

## Summary

This plan details the implementation of the three parallel strategy subgraphs under `raa/graphs/subgraphs/` (package: `raa_a.py`, `raa_b.py`, `raa_c.py`) and their Send routing in `raa/graphs/subgraphs/routing.py`. The routing helper creates the list of Send targets using the active LLM references from the configuration context. Each strategy node builds its prompt context, invokes its designated LLM, validates container/component parent relations to prevent orphan structures, and outputs the result as a partial `ArchFragment` structure.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `langgraph`, `langchain`

**Storage**: State channels in LangGraph.

**Testing**: Pytest unit tests under `tests/` checking conditional routing, context LLM loading, prompt injection, and parent validation rules.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Concurrent execution of LLM subgraph threads.

**Constraints**: LLM objects must only be passed in `context` parameter (to prevent serialization issues). All components and containers must resolve to a valid system parent.

**Scale/Scope**: Strategy nodes under `raa/nodes/strategies.py`, subgraph send routing helper under `raa/graphs/subgraphs.py`, and test module.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Validation checks on output entities keep graph schemas structured and valid.
- **Principle III: LLM Isolation & Context Injection**: Passed. Heterogeneous LLM instances are retrieved purely from runtime context keys (`llm_raa_a`, `llm_raa_b`, `llm_raa_c`).

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/014-raa-parallel-subgraphs/
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
    └── subgraphs/
        ├── common.py     # Shared payload types, reference loading, validation
        ├── routing.py    # Send fan-out routing helper
        ├── raa_a.py      # SAAM-first strategy subgraph
        ├── raa_b.py      # Pattern-driven strategy subgraph
        └── raa_c.py      # Entity-driven strategy subgraph
tests/
└── raa/
    └── test_parallel_subgraphs.py  # Unit tests for routing and strategies
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
