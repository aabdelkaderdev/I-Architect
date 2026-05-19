# Implementation Plan: ARLO RAA Compatibility & State Contracts

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/002-raa-subgraph/spec.md`

**Input**: Feature specification from `specs/002-raa-subgraph/spec.md`

## Summary

This feature delivers two major segments of the RAA (Requirement Analysis Agent) integration:
1. **ARLO Compatibility Patch**: Modify ARLO's output boundary to expose `non_asr` requirements (with full dictionary payloads) and `condition_groups` in the `ARLOOutput` schema, and persist computed ASR embeddings in a local SQLite database (`embeddings/asr_embeddings.db`) rather than passing them through downstream graph state.
2. **RAA State Contracts**: Define Python dataclasses for all C4-compliant architectural entities, relationships, patterns, and tracking metadata. Define the central `RAAState` TypedDict schema for state channels, configure specific list and dict-merge reducers to support parallel multi-model execution, and ensure full compatibility with LangGraph's default `JsonPlusSerializer` for robust SQLite checkpointing.

No runtime nodes or execution logic are implemented within this scope.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: LangGraph >= 0.1.0, LangChain >= 0.1.0, FastEmbed >= 0.3.0, Pydantic >= 2.0, scikit-learn >= 1.0

**Storage**: SQLite database for ASR embeddings (`embeddings/asr_embeddings.db`) and checkpointers.

**Testing**: Python syntax validation and unit testing via unittest/pytest.

**Target Platform**: Local Python runtime on Linux

**Project Type**: Python LangGraph package

**Performance Goals**: State updates for parallel subgraphs must resolve in under 10ms. No embedding vectors in checkpoint state.

**Constraints**: Dataclasses must be natively serializable by `JsonPlusSerializer` without custom codecs. Reducers must prevent last-write-wins data loss during parallel super-steps.

**Scale/Scope**: Dozens to hundreds of requirements; C4 nested hierarchy with up to 3 levels (System, Container, Component) and global leaf actors (Persons, External Systems).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. Dataclasses strictly model the three-level C4 hierarchy (System → Container → Component) and relationships carry explicit `diagram_scope` values. No diagrams or code are generated.
- **Principle II: Deterministic Data Pipeline**: Passed. Deduplication and merging algorithms are designed deterministically. Embedding databases use `text_hash` validation and WAL mode.
- **Principle III: LLM Isolation & Context Injection**: Passed. State channels do not store LLM instances or ChatModel config; these are passed strictly via LangGraph context at runtime.
- **Principle IV: Hierarchical Integrity (Orphan Prevention)**: Passed. Dataclasses carry explicit parent associations (`parent_system_id`, `parent_container_id`) and state validation rules prevent orphan entities.
- **Principle V: Incremental Coherence (Batch-Sequential Model)**: Passed. State channels include `batch_queue`, `batch_cursor`, `best_batch_output`, and `running_arch_model` to track sequential batch state.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/002-raa-subgraph/
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
arlo/
├── state/
│   └── schemas.py       # Exposes updated ARLOOutput and ARLOState
├── nodes/
│   ├── parsing.py       # Exposes parsed non-ASR requirement dicts
│   └── embedding.py     # Writes ASR embeddings to SQLite
└── pipeline_wrapper.py  # Passes ARLO output downstream

raa/
├── __init__.py
├── state/
│   ├── __init__.py
│   ├── types.py         # Dataclasses and type definitions (§4)
│   ├── channels.py      # TypedDict channels and custom reducers (§4)
│   └── serialization.py # Helper routines for JsonPlusSerializer and JSON serialization
└── py.typed             # PEP 561 marker for typing

embeddings/
├── asr_embeddings.db    # SQLite database (ASR embeddings)
└── .gitignore           # Git ignore rule for embeddings/
```

**Structure Decision**: Expose ARLO modifications within the existing `arlo/` package. Create a new `raa/` folder at the root with a `state/` submodule to host RAA dataclasses, state channels, and serialization wrappers, ensuring type-safe access and decoupling from future graph nodes.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
