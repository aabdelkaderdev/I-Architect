# Feature Specification: RAA SQLite Checkpointing and Crash Recovery

**Feature Branch**: `018-raa-checkpoint-recovery`

**Created**: 2026-05-19

**Status**: Draft

**Input**: User description: "Create a focused feature for SQLite checkpointing and crash recovery. Scope strictly to RAA_Plan.md Section 22. Define the deliverable as SqliteSaver production compilation, deterministic thread IDs, resume/fresh-start logic, archive policy, and corrupt-checkpoint fallback."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - SQLite Checkpointing & Graph Compilation (Priority: P1)

To protect long-running pipelines from system crashes, operator errors, or compute timeouts, the system must persist the graph state after every super-step. The graph must compile with `SqliteSaver` as its checkpointer, pointing to a database path provided dynamically by the orchestrator.

**Why this priority**: Checkpointing is the foundation of crash recovery. Without active checkpoint saving, no resume logic is possible.

**Independent Test**: Write a unit test that configures the graph compilation with a mock `SqliteSaver` connection. Run the graph for one batch step, terminate it, and verify that the graph state has been written to the SQLite database.

**Acceptance Scenarios**:

1. **Given** a compiled RAA graph, **When** execution runs, **Then** state changes (like `batch_cursor` increment or `best_batch_output` updates) are committed to the SQLite checkpoint database.
2. **Given** parallel subgraph executions in a super-step, **When** one subgraph completes and the process is interrupted, **Then** the pending writes for the completed subgraph are retained.

---

### User Story 2 - Deterministic Thread IDs and Resume/Fresh-Start (Priority: P2)

When restarting the pipeline, the system must determine whether to resume from a previous run or start a fresh execution. It computes a stable, deterministic `thread_id` (prefixed with `raa-`) derived from the input version hash. It queries the database using this ID, resuming from the checkpoint if `batch_cursor` is non-zero, or starting fresh if no state exists or `batch_cursor` is zero.

**Why this priority**: Enables recovery of specific executions without repeating successfully completed batch steps, saving compute cost and time.

**Independent Test**: Execute the graph with a specific input set up to batch index 2, stop it, then restart with the same input. Verify that:
- The generated `thread_id` is identical.
- The resume path is taken, skipping batches 0 and 1.

**Acceptance Scenarios**:

1. **Given** a previous checkpoint with `batch_cursor > 0`, **When** the pipeline starts, **Then** execution resumes from the checkpoint, skipping completed batches.
2. **Given** no previous checkpoint, **When** the pipeline starts, **Then** a fresh run is initialized.

---

### User Story 3 - Archive Policy and Corrupt Checkpoint Fallback (Priority: P3)

To prevent unbounded database growth and handle errors, the system must clean up active checkpoints on successful completion and fallback to a safe state on corruption. Once the run completes successfully and is validated, the database is moved to the archive directory. If a checkpoint database is corrupt or fails to load, the pipeline must log a warning and fall back to a fresh start.

**Why this priority**: Keeps disk usage low and prevents pipeline failures due to corrupt or invalid checkpoint state.

**Independent Test**: Simulate database corruption (e.g. write random bytes to the DB file). Verify that:
- Loading the checkpoint raises a handled warning.
- The pipeline falls back to a fresh execution.

**Acceptance Scenarios**:

1. **Given** a corrupt checkpoint database, **When** the graph attempts to load the state, **Then** a warning is logged and a fresh start is executed.
2. **Given** a successfully finalized execution, **When** validation completes, **Then** the active checkpoint DB is moved to `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db`.

---

### Edge Cases

- **WAL Mode locks**: Checkpoint DBs must be opened with WAL mode enabled to support concurrent read-only queries from monitoring tools without causing write lock delays.
- **Missing Directory**: If the checkpoint database parent directory does not exist, the checkpointer should raise a clear configuration error (as it is the orchestrator's responsibility to create it).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST configure `SqliteSaver` checkpointer for production compilation of the RAA graph.
- **FR-002**: System MUST receive the database path dynamically from the orchestrator and must not hardcode default paths.
- **FR-003**: System MUST compute a stable, deterministic `thread_id` prefixed with `raa-` based on a SHA-256 hash of the ARLO output version.
- **FR-004**: System MUST check for existing checkpoints before graph execution. If `batch_cursor` is non-zero, it MUST resume from the checkpoint; otherwise it MUST start fresh.
- **FR-005**: System MUST move the active checkpoint database to the archive path `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db` after successful execution.
- **FR-006**: System MUST handle checkpoint DB corruption gracefully, logging a warning and falling back to a fresh run without blocking pipeline start.

### Key Entities *(include if feature involves data)*

- **SqliteSaver**: The LangGraph checkpointer class.
- **Thread ID**: Stable thread identifier for checkpoint state configuration.
- **Batch Cursor**: State variable tracking batch processing progression.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: SQLite checkpointer successfully persists graph state after each super-step.
- **SC-002**: Verification of resume shows that execution skips previously completed batches.
- **SC-003**: Corrupted database files do not crash the pipeline, fallback triggers correctly.
- **SC-004**: Archiving successfully cleans up active checkpoints on completion.

## Assumptions

- The branch `018-raa-checkpoint-recovery` is created for this feature.
- The output directory and active checkpointer database paths are provided by the orchestrator at runtime.
