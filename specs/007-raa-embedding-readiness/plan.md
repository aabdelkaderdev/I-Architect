# Implementation Plan: RAA Preparation & Embedding Readiness

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/007-raa-embedding-readiness/spec.md`

**Input**: Feature specification from `specs/007-raa-embedding-readiness/spec.md`

## Summary

This plan outlines the design for the RAA preparation and embedding readiness node. This node connects to the SQLite databases under `embeddings/`, verifies ASR embedding compliance, and generates embeddings for all non-ASR requirements utilizing the FastEmbed library with `mixedbread-ai/mxbai-embed-large-v1`. Connections will explicitly enable Write-Ahead Logging (WAL) mode to handle concurrent access.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `sqlite3`, `fastembed` (v0.2.0+)

**Storage**: SQLite databases (`embeddings/asr_embeddings.db` and `embeddings/non_asr_embeddings.db`).

**Testing**: Pytest unit tests under `tests/` to verify table existence, WAL mode setup, ASR verification errors, and non-ASR embedding persistence.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python node code

**Performance Goals**: Avoid redundant embedding generations via database caching.

**Constraints**: FastEmbed CPU execution. Both SQLite databases must run in WAL mode.

**Scale/Scope**: A single preparation node module (`raa/nodes/preparation.py`) and associated unit test file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed.
- **Principle II: Deterministic Data Pipeline**: Passed. Standardizes embedding lookups and models across ARLO and RAA.
- **Principle III: LLM Isolation & Context Injection**: Passed. Uses CPU-based FastEmbed model rather than cloud LLMs for embeddings.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/007-raa-embedding-readiness/
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
    └── preparation.py   # RAA preparation node
tests/
└── test_preparation.py  # Unit tests for preparation node
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
