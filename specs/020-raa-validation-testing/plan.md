# Implementation Plan: RAA Validation and Testing

**Branch**: `020-raa-validation-testing` | **Date**: 2026-05-19 | **Spec**: [specs/020-raa-validation-testing/spec.md](file:///home/delatom/_Graduation/I-Architect%20%28Final%29/specs/020-raa-validation-testing/spec.md)

**Input**: Feature specification from `/specs/020-raa-validation-testing/spec.md`

## Summary

Deliver the full unit, integration, and functional test suite for the Requirement Analysis Agent (RAA) scoped strictly to Section 19 of `RAA_Plan.md`. The test suite will validate pipeline integrity, coherence gates, entity deduplication, deterministic output ordering, and SAAM scoring correctness using pytest and isolated mock structures.

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: `pytest`, `langgraph`, `langchain_core`
**Storage**: SQLite (temp directories via `pytest` fixtures)
**Testing**: `pytest`
**Target Platform**: Local development and CI/CD pipelines
**Project Type**: Test Suite / Library Testing
**Performance Goals**: Test suite completes in < 2 minutes sequentially
**Constraints**: Fully offline testing (100% LLM mocking or stubbing required)
**Scale/Scope**: ~30-50 localized tests spanning unit, integration, and functional validations.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (Spec-Driven Architecture)**: Functional tests will validate that outputs strictly adhere to C4 schema compliance and hierarchical integrity.
- **Principle II (Deterministic Data Pipeline)**: Unit tests will enforce stable cross-batch canonical ID deduplication, sorting behavior, and cache hashing matching.
- **Principle III (LLM Isolation)**: Test framework will strictly mock LLMs injected through the LangGraph context parameter, enforcing offline-first testing.
- **Principle IV (Hierarchical Integrity)**: Tests specifically cover orphan component rejection and parent existence checks in the merge processes.
- **Principle V (Incremental Coherence)**: Integration tests will exercise the 0.5x SAAM multiplier for incoherent batches and confirm the 3-item hard cap on bridge requirements.

## Project Structure

### Documentation (this feature)

```text
specs/020-raa-validation-testing/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
└── quickstart.md        # Phase 1 output
```

### Source Code (repository root)

```text
tests/raa/
├── __init__.py
├── conftest.py          # Shared fixtures (mock LLMs, state payloads, db helpers)
├── test_preparation.py  # Unit tests for ASR db verification and non-ASR embeddings
├── test_batching.py     # Unit tests for batch assembly, bridging, coherence gate
├── test_judge.py        # Unit tests for entity deduplication and merge logic
├── test_integration.py  # Integration tests for end-to-end multi-batch runs
└── test_final_merge.py  # Functional tests for structural integrity and JSON correctness
```

**Structure Decision**: A flat organizational layout within `tests/raa/` separated by logical pipeline stage or test boundary, leveraging a shared `conftest.py` for mocking.

## Complexity Tracking

No violations. Standard testing patterns using `pytest` without architectural complexity overhead.
