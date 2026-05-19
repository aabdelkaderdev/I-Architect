# Research Notes: RAA SQLite Checkpointing and Crash Recovery

## Summary

This document researches and defines the core technical decisions for the SQLite checkpointing and crash recovery mechanisms of the RAA pipeline, specifically focusing on `SqliteSaver` integration, deterministic thread ID generation, fresh-start vs resume wrappers, the archive policy, and crash/corruption fallbacks.

---

## 1. SqliteSaver Production Compilation

### Decision
Compile the RAA StateGraph with `SqliteSaver` from the `langgraph-checkpoint-sqlite` package.
- **Connection**: `sqlite3.connect(str(db_path), check_same_thread=False)`.
- **Durability**: Configurable with default `"sync"`.
- **Directory**: The orchestrator is responsible for directory creation, but the runner will ensure the parent directory exists dynamically via `Path.parent.mkdir(parents=True, exist_ok=True)`.

### Rationale
This aligns exactly with ARLO's checkpoint compilation pattern (`compile_for_production` in `arlo/runner.py`), providing consistent storage lifecycle management across the whole I-Architect pipeline.

---

## 2. Deterministic Thread IDs

### Decision
Generate thread IDs prefixed with `raa-` followed by the hex digest of the SHA-256 hash of the normalized inputs.
- **Inputs**: ARLO output structure (`asrs`, `condition_groups`) and a run label (defaulting to `"default"` if not provided).
- **Calculation**: Serialize the normalized inputs to a deterministic JSON string, concatenate with the run label, calculate SHA-256, and truncate to 16 hex characters.
- **Format**: `raa-{hash}`.

### Rationale
This prevents naming collisions, ensures identical runs map to the same thread ID across restarts, and supports manual retry/resumption scenarios.

---

## 3. Fresh-Start vs. Resume Wrapper

### Decision
The RAA entrypoint query the checkpointer using `graph.get_state(config)` before execution:
- If a state snapshot is found and its `batch_cursor` is greater than 0, the runner logs a resume message and calls `graph.invoke(None, config, ...)` to resume from the last committed step.
- If no snapshot is found or `batch_cursor` is 0, the runner starts a fresh run by passing the initial state payload.

### Rationale
Ensures the graph doesn't repeat already completed batches, keeping pipeline runs efficient.

---

## 4. Archive Policy

### Decision
Active checkpoints in `raa_graph.db` are moved to `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db` using Python's standard `shutil.move`.
- **Condition**: Must execute *only after* the final merged JSON (`arch_model.json`) is successfully written and verified against the C4 schema.
- **Safety**: If the final merge or validation fails, the checkpoint database is left untouched so the operator can resume or troubleshoot.

### Rationale
Protects run history, prevents checkpoint DB size inflation, and prevents dataloss on failures.

---

## 5. Corrupt-Checkpoint Fallback

### Decision
Wrap checkpointer initialization and graph compilation in try-except blocks:
- **Error Types**: `sqlite3.DatabaseError` or serialization issues during `get_state` or `compile`.
- **Handling**: Log a prominent `WARNING` indicating checkpoint corruption, reinitialize the SQLite database file as a clean/fresh database, and execute a fresh start. Do not crash.

### Rationale
Ensures pipeline progress is never completely blocked by a corrupted state file, allowing the system to fall back automatically.
