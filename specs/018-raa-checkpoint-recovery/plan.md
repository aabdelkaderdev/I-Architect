# Implementation Plan: SQLite Checkpointing and Crash Recovery

**Branch**: `018-raa-checkpoint-recovery` | **Date**: 2026-05-19 | **Spec**: [specs/018-raa-checkpoint-recovery/spec.md](spec.md)

**Input**: Feature specification from `specs/018-raa-checkpoint-recovery/spec.md`

## Summary

This plan covers SQLite checkpointing and crash recovery for the RAA pipeline. It integrates `SqliteSaver` from the `langgraph-checkpoint-sqlite` library into RAA's production compilation (`compile_for_production`). The checkpointer database path is passed dynamically by the orchestrator. The run uses a deterministic thread ID based on a SHA-256 hash of the ARLO output version. At startup, the state is queried using `graph.get_state(run_config)` and checked: if `batch_cursor` is non-zero, it resumes from the last checkpoint; otherwise, it starts fresh. After successful execution, the checkpoint DB is moved to the archive directory. It handles corrupt checkpoints by catching recovery exceptions, logging a warning, and falling back to a fresh start.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `langchain`, `langgraph`, `langgraph-checkpoint-sqlite`

**Storage**: SQLite database for checkpointing (`raa_graph.db`).

**Testing**: `pytest` tests to verify `SqliteSaver` compilation, deterministic thread ID generation, resume logic (skipping completed batches), and corrupt-checkpoint fallback.

**Target Platform**: Linux filesystem

**Project Type**: Runtime Python entrypoint and graph configuration code

**Performance Goals**: Fast state commits, minimal serialization overhead.

**Constraints**: The checkpointer DB path is a required parameter for RAA compilation. Thread ID must be deterministic and prefix-controlled (`raa-`).

**Scale/Scope**: Modify `raa/runner.py` to compile with checkpointer and implement fresh start/resume wrapper; write tests in `tests/test_runner.py`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Spec-Driven Architecture (C4 + SAAM Compliance)**: Passed. SQLite checkpointing handles structural state channels, allowing graph execution to save and resume correctly without impacting the output schema.
- **Principle II: Deterministic Data Pipeline**: Passed. State checkpointing is a structural mechanism; state variables (like `batch_cursor`, `best_batch_output`) are saved/restored deterministically.
- **Principle III: LLM Isolation & Context Injection**: Passed. LLM instances are not stored in the state channels or serialized into checkpoints; they are passed via context, matching Orchestrator Plan §3C.
- **Principle IV: Hierarchical Integrity (Orphan Prevention)**: Passed. In-progress hierarchy building is safely checkpointed.
- **Principle V: Incremental Coherence (Batch-Sequential Model)**: Passed. `batch_cursor` acts as the authoritative resume marker. Active checkpoints are archived only after output validation completes.

No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/018-raa-checkpoint-recovery/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── readme.md        # Phase 1 output
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
raa/
└── runner.py            # Compilation and run entrypoint (checkpointing, thread ID, fresh start/resume logic)
tests/
└── test_runner.py       # Checkpointer compilation and resume tests
```

**Structure Decision**: Single project layout matching the existing `raa/` and `tests/` conventions in the workspace.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
