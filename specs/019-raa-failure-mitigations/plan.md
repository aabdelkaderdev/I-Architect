# Implementation Plan: RAA Failure Mode Mitigations

**Branch**: `019-raa-failure-mitigations` | **Date**: 2026-05-19 | **Spec**: [spec.md](file:///home/delatom/_Graduation/I-Architect%20%28Final%29/specs/019-raa-failure-mitigations/spec.md)

**Input**: Feature specification from `specs/019-raa-failure-mitigations/spec.md`

---

## Summary

This feature implements the remaining runtime failure mode mitigations, database concurrency enhancements, and desync recovery procedures for the Requirement Analysis Agent (RAA) pipeline. Specifically, the technical scope includes:
1. **Startup safety checks & diagnostics** in `prepare_embeddings` to verify the presence and integrity of `asr_embeddings.db` and rebuild `non_asr_embeddings.db` automatically in case of corruption.
2. **Hash-based cache integrity checks** to verify and recompute stale embeddings when requirement text changes.
3. **SQLite WAL mode & read-only connections** across the RAA subgraphs to prevent file lock contention.
4. **Desync verification & targeted batch reruns** in the `final_merge` node.
5. **Updating the Failure Modes Register** to document Section 18 and 22H mitigations.

---

## Technical Context

- **Language/Version**: Python 3.12
- **Primary Dependencies**: `langgraph` (v0.2.0+), `langgraph-checkpoint-sqlite` (v2.0.0+), `fastembed` (v0.2.0+), `sqlite3`
- **Storage**: SQLite database files (`asr_embeddings.db`, `non_asr_embeddings.db`, `raa_graph.db`)
- **Testing**: `pytest`
- **Target Platform**: Linux (Ubuntu 22.04 LTS)
- **Project Type**: Data Pipeline (LangGraph Agentic Workflow)
- **Performance Goals**: Startup validation runs in <2.0s; stale embedding check takes <1.0s overhead per requirement.
- **Constraints**: WAL mode connections must never throw SQLite "database is locked" errors during parallel reads.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Our design aligns fully with the I-Architect project constitution:
1. **Principle I (Spec-Driven Architecture)**: The final C4 model structural integrity and diagram manifests are validated against normative schemas before output files are committed.
2. **Principle II (Deterministic Data Pipeline)**: Embedding integrity is ensured via SHA-256 requirement hashes; all non-ASR databases are automatically rebuilt if corrupted.
3. **Principle III (LLM Isolation & Context Injection)**: Subgraph execution dynamically retrieves LLMs from runtime context (`llm_raa_a/b/c` and `llm_judge`), avoiding any serialization of LLM instances into the checkpointer database.
4. **Principle IV (Hierarchical Integrity)**: The judge and final merge nodes perform orphan checks to prevent orphan components and systems from leaking into the output.
5. **Principle V (Incremental Coherence)**: State recovery resumes from batch boundaries using `batch_cursor`, and incoherent batches fallback to single-RAA-A execution.

---

## Project Structure

### Documentation (this feature)

```text
specs/019-raa-failure-mitigations/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/
    └── readme.md        # Phase 1 output
```

### Source Code

```text
raa/
├── nodes/
│   ├── preparation.py    # Startup validation, corruption rebuild, hash check
│   └── final_merge.py    # Desync detection and batch rollback
└── runner.py             # SQLite WAL checkpointer initialization

tests/raa/
├── test_preparation.py   # Verify safety checks, rebuilds, and hash updates
├── test_final_merge.py   # Verify desync recovery and rollback
└── test_checkpoint_recovery.py # Checkpointer WAL settings and lifecycle tests
```

**Structure Decision**: Standard single-project layout extending the existing `raa/` runtime modules and `tests/raa/` validation suites.

---

## Complexity Tracking

*No constitution violations detected or recorded.*
