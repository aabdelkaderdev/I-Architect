# Tasks: RAA SQLite Checkpointing and Crash Recovery

**Input**: Design documents from `/specs/018-raa-checkpoint-recovery/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `RAA_Plan.md` Section 22, LangGraph persistence/checkpointer docs

**Tests**: Required by the feature specification independent tests. Write the listed pytest coverage before implementation and confirm current code fails because `compile_for_production()` and the runner recovery helpers are not implemented.

**Organization**: Tasks are grouped by user story so checkpoint compilation, deterministic resume, and archive/corruption handling can be implemented and verified independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel after dependencies are satisfied because it touches different files
- **[Story]**: User story label from `spec.md`
- All task descriptions include exact repository file paths

## Phase 1: Setup

**Purpose**: Confirm Section 22 behavior, existing graph compilation boundaries, and dependency availability.

- [X] T001 Review `RAA_Plan.md` Section 22A-22G and record the required `SqliteSaver`, `thread_id`, resume, archive, and failure-mode behavior in `specs/018-raa-checkpoint-recovery/tasks.md`
- [X] T002 Review current graph compilation in `raa/graphs/main_graph.py` and current runner placeholder in `raa/runner.py`
- [X] T003 Verify `langgraph-checkpoint-sqlite` remains listed in `pyproject.toml` and note that `compile_for_production()` must import `SqliteSaver` from `langgraph.checkpoint.sqlite`

---

## Phase 2: Foundational

**Purpose**: Establish checkpoint helper contracts shared by all user stories.

- [X] T004 Create shared checkpointing test fixtures for temporary SQLite paths, mock compiled graph objects, mock state snapshots, and minimal RAA initial state in `tests/raa/test_checkpoint_recovery.py`
- [X] T005 [P] Define runner helper signatures in `raa/runner.py` for `derive_thread_id(arlo_output_version_hash, run_label="default")`, `build_run_config(thread_id, context=None)`, `should_resume_from_snapshot(snapshot)`, `run_with_recovery(...)`, and `archive_checkpoint(...)`
- [X] T006 [P] Define production compilation helper signatures in `raa/graphs/main_graph.py` for `compile_for_production(db_path, node_overrides=None, durability="sync")` and `_open_sqlite_checkpointer(db_path)`
- [X] T007 Add tests that no RAA state channel stores `llm_raa_a`, `llm_raa_b`, `llm_raa_c`, `llm_judge`, SQLite connections, `SqliteSaver`, or embedding vectors in `tests/raa/test_checkpoint_recovery.py`

**Checkpoint**: The test suite has fixture scaffolding and the implementation has clear helper boundaries for production compilation, run configuration, resume checks, and archive handling.

---

## Phase 3: User Story 1 - SQLite Checkpointing and Graph Compilation (Priority: P1) MVP

**Goal**: Compile the production RAA graph with a `SqliteSaver` checkpointer backed by the orchestrator-provided SQLite `db_path`, preserving every LangGraph super-step snapshot and pending writes.

**Independent Test**: Run `pytest tests/raa/test_checkpoint_recovery.py -k "compile or sqlite or persisted"` with a temporary database path and a simple graph update; verify the compiled graph uses a checkpointer and persists state for a configured `thread_id`.

### Tests for User Story 1

- [X] T008 [US1] Add tests that `compile_for_production(db_path=...)` in `raa/graphs/main_graph.py` requires `db_path` with no default and rejects missing or empty paths in `tests/raa/test_checkpoint_recovery.py`
- [X] T009 [US1] Add tests that `compile_for_production(...)` raises a clear configuration error when `Path(db_path).parent` does not exist, because Section 22A assigns directory creation to the orchestrator, in `tests/raa/test_checkpoint_recovery.py`
- [X] T010 [US1] Add tests that `_open_sqlite_checkpointer(db_path)` opens `sqlite3.connect(str(db_path), check_same_thread=False)` and executes `PRAGMA journal_mode=WAL` in `tests/raa/test_checkpoint_recovery.py`
- [X] T011 [US1] Add tests that `_open_sqlite_checkpointer(db_path)` calls `SqliteSaver(conn)` and `setup()` before graph compilation in `tests/raa/test_checkpoint_recovery.py`
- [X] T012 [US1] Add tests that `compile_for_production(...)` passes the checkpointer to `StateGraph.compile(checkpointer=...)` while preserving `node_overrides` support in `raa/graphs/main_graph.py` in `tests/raa/test_checkpoint_recovery.py`
- [X] T013 [US1] Add tests that an invoked production graph persists `batch_cursor`, `batch_queue`, `running_arch_model`, `best_batch_output`, `open_questions`, `bridge_requirements`, `incoherent_batches`, and `embeddings_ready` for a configured `thread_id` in `tests/raa/test_checkpoint_recovery.py`
- [X] T014 [US1] Add tests that production checkpointing preserves completed pending writes in a failed super-step where possible using LangGraph checkpoint inspection APIs in `tests/raa/test_checkpoint_recovery.py`

### Implementation for User Story 1

- [X] T015 [US1] Implement `_validate_db_path(db_path)` in `raa/graphs/main_graph.py` to require an orchestrator-provided path and reject missing parent directories with a clear error
- [X] T016 [US1] Implement `_open_sqlite_checkpointer(db_path)` in `raa/graphs/main_graph.py` using `sqlite3.connect(str(db_path), check_same_thread=False)`, WAL mode, `SqliteSaver(conn)`, and `checkpointer.setup()`
- [X] T017 [US1] Implement `compile_for_production(db_path, node_overrides=None, durability="sync")` in `raa/graphs/main_graph.py` to build the RAA graph and compile it with the SQLite checkpointer
- [X] T018 [US1] Preserve `compile_raa_graph(...)` as the non-production/test compilation path in `raa/graphs/main_graph.py`
- [X] T019 [US1] Add `compile_for_production` to imports and `__all__` in `raa/graphs/__init__.py`
- [X] T020 [US1] Run `pytest tests/raa/test_checkpoint_recovery.py -k "compile or sqlite or persisted"` and fix failures in `raa/graphs/main_graph.py`, `raa/graphs/__init__.py`, and `tests/raa/test_checkpoint_recovery.py`

**Checkpoint**: User Story 1 is complete when the production graph compiles with `SqliteSaver` using the orchestrator-provided database path and LangGraph can persist state under a configured `thread_id`.

---

## Phase 4: User Story 2 - Deterministic Thread IDs and Resume/Fresh Start (Priority: P2)

**Goal**: Derive stable `raa-{sha256[:16]}` thread IDs from the ARLO output version hash and run label, query `graph.get_state(run_config)` at process startup, resume when `batch_cursor > 0`, and start fresh otherwise.

**Independent Test**: Run `pytest tests/raa/test_checkpoint_recovery.py -k "thread_id or resume or fresh"` with mock graph snapshots; verify identical inputs derive identical thread IDs and that resume invokes the graph with `None` input while fresh start invokes it with initial state.

### Tests for User Story 2

- [X] T021 [US2] Add tests that `derive_thread_id("arlo-hash", "default")` in `raa/runner.py` returns `raa-` plus exactly 16 lowercase SHA-256 hex characters in `tests/raa/test_checkpoint_recovery.py`
- [X] T022 [US2] Add tests that identical ARLO output version hash and run label produce identical `thread_id` values across calls in `tests/raa/test_checkpoint_recovery.py`
- [X] T023 [US2] Add tests that changing the ARLO output version hash or run label changes the derived `thread_id` in `tests/raa/test_checkpoint_recovery.py`
- [X] T024 [US2] Add tests that `build_run_config(thread_id, context)` in `raa/runner.py` returns `{"configurable": {"thread_id": thread_id}, "context": context}` without placing LLMs in state in `tests/raa/test_checkpoint_recovery.py`
- [X] T025 [US2] Add tests that `should_resume_from_snapshot(snapshot)` returns true only when `snapshot.values["batch_cursor"] > 0` in `tests/raa/test_checkpoint_recovery.py`
- [X] T026 [US2] Add tests that `run_with_recovery(...)` calls `graph.get_state(run_config)` before `graph.invoke(...)` in `tests/raa/test_checkpoint_recovery.py`
- [X] T027 [US2] Add tests that an existing checkpoint with `batch_cursor > 0` resumes with `graph.invoke(None, run_config)` and skips fresh initial state in `tests/raa/test_checkpoint_recovery.py`
- [X] T028 [US2] Add tests that no checkpoint, a checkpoint with no values, or a checkpoint with `batch_cursor == 0` starts fresh with `graph.invoke(initial_state, run_config)` in `tests/raa/test_checkpoint_recovery.py`
- [X] T029 [US2] Add tests that resume logging includes the resumed `thread_id` and `batch_cursor` in `tests/raa/test_checkpoint_recovery.py`

### Implementation for User Story 2

- [X] T030 [US2] Implement `derive_thread_id(arlo_output_version_hash, run_label="default")` in `raa/runner.py` using SHA-256 over the version hash and run label, truncated to 16 hex characters and prefixed with `raa-`
- [X] T031 [US2] Implement `build_run_config(thread_id, context=None)` in `raa/runner.py` with `thread_id` under `configurable` and runtime LLM/output context under `context`
- [X] T032 [US2] Implement `should_resume_from_snapshot(snapshot)` in `raa/runner.py` to inspect `snapshot.values.get("batch_cursor", 0)` safely
- [X] T033 [US2] Implement `run_with_recovery(graph, initial_state, run_config, *, db_path, compile_graph_factory=None)` in `raa/runner.py` to call `graph.get_state(run_config)` before invocation
- [X] T034 [US2] Implement the resume branch in `run_with_recovery(...)` in `raa/runner.py` using `graph.invoke(None, run_config)` when `batch_cursor > 0`
- [X] T035 [US2] Implement the fresh-start branch in `run_with_recovery(...)` in `raa/runner.py` using `graph.invoke(initial_state, run_config)` when no resumable snapshot exists
- [X] T036 [US2] Implement a public runner entrypoint in `raa/runner.py` that accepts `initial_state`, `arlo_output_version_hash`, `db_path`, `run_label`, and runtime `context`, compiles via `compile_for_production(db_path=...)`, derives `thread_id`, builds the run config, and delegates to `run_with_recovery(...)`
- [X] T037 [US2] Run `pytest tests/raa/test_checkpoint_recovery.py -k "thread_id or resume or fresh"` and fix failures in `raa/runner.py` and `tests/raa/test_checkpoint_recovery.py`

**Checkpoint**: User Story 2 is complete when process startup can deterministically target a checkpoint thread and choose resume versus fresh start solely from `batch_cursor`.

---

## Phase 5: User Story 3 - Archive Policy and Corrupt Checkpoint Fallback (Priority: P3)

**Goal**: Preserve checkpoint safety during failures, fall back to a fresh run when `get_state` detects corruption, and archive the active checkpoint database only after successful final merge output validation.

**Independent Test**: Run `pytest tests/raa/test_checkpoint_recovery.py -k "corrupt or archive or failure_mode"` with corrupt database fixtures and successful final-output markers; verify warnings, fallback behavior, and archive movement.

### Tests for User Story 3

- [X] T038 [US3] Add tests that `run_with_recovery(...)` catches `sqlite3.DatabaseError` raised by `graph.get_state(run_config)`, logs a warning, and does not crash in `tests/raa/test_checkpoint_recovery.py`
- [X] T039 [US3] Add tests that corrupt-checkpoint fallback renames the active database to a `.corrupted` path before starting fresh in `tests/raa/test_checkpoint_recovery.py`
- [X] T040 [US3] Add tests that corrupt-checkpoint fallback recompiles or receives a fresh compiled graph and invokes it with `initial_state` in `tests/raa/test_checkpoint_recovery.py`
- [X] T041 [US3] Add tests that corrupt-checkpoint fallback never silently deletes the corrupt database file in `tests/raa/test_checkpoint_recovery.py`
- [X] T042 [US3] Add tests that `archive_checkpoint(db_path, project_name, thread_id)` moves `projects/{project_name}/checkpoints/raa_graph.db` to `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db` in `tests/raa/test_checkpoint_recovery.py`
- [X] T043 [US3] Add tests that archive is skipped when final merge did not validate or `arch_model.json` was not written in `tests/raa/test_checkpoint_recovery.py`
- [X] T044 [US3] Add tests that archive occurs after a successful final merge result reports validated output, and that the active checkpoint path no longer exists afterward, in `tests/raa/test_checkpoint_recovery.py`
- [X] T045 [US3] Add tests covering Section 22G failure modes: mid-embedding resumes with `embeddings_ready` false, after-judge resumes with advanced `batch_cursor`, and during-final-merge reruns final merge from `best_batch_output` in `tests/raa/test_checkpoint_recovery.py`

### Implementation for User Story 3

- [X] T046 [US3] Implement corrupt checkpoint exception handling in `run_with_recovery(...)` in `raa/runner.py` for `sqlite3.DatabaseError` and checkpoint deserialization failures during `graph.get_state(run_config)`
- [X] T047 [US3] Implement `_preserve_corrupt_checkpoint(db_path)` in `raa/runner.py` to rename the corrupt database file with a `.corrupted` suffix without deleting it
- [X] T048 [US3] Implement the corrupt fallback path in `raa/runner.py` to log a warning, preserve the corrupt DB, recompile or accept a fresh graph via `compile_graph_factory`, and start fresh with `initial_state`
- [X] T049 [US3] Implement `archive_checkpoint(db_path, project_name, thread_id)` in `raa/runner.py` using `shutil.move` into `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db`
- [X] T050 [US3] Implement `archive_after_success(result, db_path, project_name, thread_id)` in `raa/runner.py` so archiving runs only after the final merge result indicates successful C4 validation and `arch_model.json` output
- [X] T051 [US3] Integrate archive triggering into the public runner entrypoint in `raa/runner.py` after graph invocation returns a validated final output result
- [X] T052 [US3] Run `pytest tests/raa/test_checkpoint_recovery.py -k "corrupt or archive or failure_mode"` and fix failures in `raa/runner.py` and `tests/raa/test_checkpoint_recovery.py`

**Checkpoint**: User Story 3 is complete when corrupt checkpoints are preserved and fresh-start fallback works, while successful completed runs archive the active checkpoint database only after validated final output exists.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify checkpoint recovery does not regress existing graph behavior or violate Section 22 boundaries.

- [X] T053 Run `pytest tests/raa/test_checkpoint_recovery.py tests/raa/test_main_graph.py tests/raa/test_final_merge.py` and fix feature-caused regressions in `raa/graphs/main_graph.py`, `raa/runner.py`, and related tests
- [X] T054 Confirm `raa/graphs/main_graph.py` production compilation requires `db_path` and does not hardcode `projects/{project_name}/checkpoints/raa_graph.db`
- [X] T055 Confirm `raa/runner.py` derives thread IDs only from ARLO output version hash plus run label and never from timestamps, random UUIDs, process IDs, or machine-specific paths
- [X] T056 Confirm checkpoint state snapshots exclude LLM instances, SQLite connection objects, `SqliteSaver`, and embedding vectors
- [X] T057 Confirm archive code in `raa/runner.py` runs only after final merge validation/output success and never before C4 validation or `arch_model.json` write completion

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on User Story 1 because resume requires a production-compiled checkpointer graph
- **User Story 3 (Phase 5)**: Depends on User Story 2 because corruption fallback and archive lifecycle wrap startup/invocation behavior
- **Polish (Phase 6)**: Depends on all selected user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational phase completion and is the MVP scope
- **User Story 2 (P2)**: Depends on User Story 1 production checkpointer compilation
- **User Story 3 (P3)**: Depends on User Story 2 runner entrypoint and run configuration

### Within User Story 1

- Tests T008-T014 must be written before implementation tasks T015-T020
- `db_path` validation T015 must complete before checkpointer creation T016
- Checkpointer creation T016 must complete before production compilation T017
- T020 validates User Story 1 before resume work begins

### Within User Story 2

- Tests T021-T029 must be written before implementation tasks T030-T037
- Thread ID derivation T030 and run config T031 must complete before startup orchestration T033-T036
- Resume/fresh decision T032 must complete before branch implementations T034-T035

### Within User Story 3

- Tests T038-T045 must be written before implementation tasks T046-T052
- Corrupt DB preservation T047 must complete before corrupt fallback T048
- Archive helper T049 must complete before post-success archive trigger T050-T051

### Parallel Opportunities

- T005 and T006 can run in parallel after T004 because runner and graph helper signatures are in separate files
- T008-T014 can be split across compilation, SQLite connection, and persistence behavior tests in `tests/raa/test_checkpoint_recovery.py`
- T030-T032 can run in parallel after T021-T025 because thread ID, config construction, and snapshot inspection are independent helpers
- T046-T048 can proceed separately from T049-T051 after User Story 2 because corrupt fallback and archive policy touch distinct helper paths

---

## Parallel Example: User Story 1

```bash
# After T004-T006:
Task: "Add compile_for_production db_path validation and SqliteSaver tests in tests/raa/test_checkpoint_recovery.py"
Task: "Implement _open_sqlite_checkpointer in raa/graphs/main_graph.py"
```

## Parallel Example: User Story 2

```bash
# After User Story 1:
Task: "Implement derive_thread_id in raa/runner.py"
Task: "Implement should_resume_from_snapshot in raa/runner.py"
```

## Parallel Example: User Story 3

```bash
# After User Story 2:
Task: "Implement corrupt checkpoint fallback in raa/runner.py"
Task: "Implement archive_checkpoint and archive_after_success in raa/runner.py"
```

---

## Implementation Strategy

### MVP First

1. Complete T001-T007 to establish test fixtures and helper boundaries.
2. Complete User Story 1 T008-T020 to compile the graph with SQLite checkpointing.
3. Stop and validate checkpoint persistence independently.

### Incremental Delivery

1. Add User Story 2 T021-T037 to derive deterministic thread IDs and resume from `batch_cursor`.
2. Add User Story 3 T038-T052 to handle corrupt checkpoints and archive after validated final output.
3. Run polish checks T053-T057 to confirm Section 22 guarantees and regression safety.

### Suggested MVP Scope

User Story 1 is the MVP. User Stories 2 and 3 are required for complete crash recovery and checkpoint lifecycle behavior.
