# Tasks: RAA Failure Mode Mitigations

**Input**: Design documents from `specs/019-raa-failure-mitigations/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Required by the feature specification independent tests. Write the listed pytest coverage before implementation and confirm current code fails because the mitigation logic is not yet present.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Scope

Strictly §18 (Failure Modes & Mitigations) and §22H (Integration with §18 Failure Modes Register) of RAA_Plan.md. The following mitigations are in scope:

1. **Empty non-ASR passthrough** (§18 row "No good non-ASR matches for a group") — batch proceeds with ASRs only
2. **Reconciliation output C4 validation gate** (§18 row "Reconciliation LLM introduces new conflicts") — validate reconciliation output against C4 schema before acceptance
3. **Stale embedding hash warning** (§18 row "Embedding text hash mismatch") — emit WARNING log for each stale entry
4. **Corrupt embedding DB fallback** (§18 row "Embedding DB corrupted or locked") — fall back to full recomputation with WARNING
5. **ASR DB blocking error** (§18 + §22H) — blocking error with instructions to re-run ARLO
6. **Embedding DB WAL mode** (§22H row "Embedding SQLite DB locked") — WAL mode on ALL connections including read-only
7. **`batch_cursor` desync targeted re-run** (§22H row) — final merge validates keys before running
8. **Failure register rows** (§22H) — add all five §22H rows to the §18 register in code

---

## Phase 1: Setup

**Purpose**: Verify existing infrastructure and confirm gap coverage

- [x] T001 Verify that `langgraph-checkpoint-sqlite` is listed in `pyproject.toml` and note current `fastembed` version constraint
- [x] T002 [P] Confirm the 308 existing RAA tests still pass by running `.venv/bin/pytest tests/raa/` — this is the regression baseline

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared helper and schema infrastructure that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Extract a shared `open_embedding_db(db_path, read_only=False)` helper into `raa/utils/db.py` that opens SQLite in WAL mode (via `PRAGMA journal_mode=WAL;`) and supports read-only URI (`mode=ro`). Both `raa/nodes/preparation.py` (`_connect_embedding_db`) and `raa/nodes/batch_construction.py` (`_connect_readonly`) must delegate to this helper
- [x] T004 Add the `FailureRegisterEntry` dataclass to `raa/state/types.py` with fields: `risk_id: str`, `description: str`, `mitigation_strategy: str`, `section_ref: str`, `verified_node: str`
- [x] T005 [P] Create the failure register constant list `FAILURE_REGISTER` in `raa/utils/failure_register.py` containing all eight §18 rows and all five §22H rows (13 entries total) as `FailureRegisterEntry` instances. Include an `__all__` export

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Resilient Recovery from Pipeline Interruptions (Priority: P1) 🎯 MVP

**Goal**: Ensure interrupted pipelines resume from the last completed batch and that the checkpoint DB corruption fallback works correctly.

**Independent Test**: Kill the process during batch 2, restart with the same thread_id → pipeline resumes at batch 2 using existing checkpoint and embeddings.

### Tests for User Story 1

- [x] T006 [P] [US1] Add test `test_corrupt_asr_db_raises_blocking_error` in `tests/raa/test_preparation.py` that creates a corrupt `asr_embeddings.db` (write garbage bytes to the file), calls `prepare_embeddings`, and asserts `RuntimeError` is raised with a message containing "re-run ARLO"
- [x] T007 [P] [US1] Add test `test_corrupt_non_asr_db_rebuilds_automatically` in `tests/raa/test_preparation.py` that creates a corrupt `non_asr_embeddings.db` (garbage bytes), calls `prepare_embeddings`, and asserts: (a) the function succeeds returning `{"embeddings_ready": True}`, (b) the DB file now has a valid `embeddings` table, (c) a WARNING log was emitted containing "corrupt" or "Rebuilding"
- [x] T008 [P] [US1] Add test `test_embeddings_ready_true_bypasses_all_checks` in `tests/raa/test_preparation.py` that passes `{"embeddings_ready": True}` in state and asserts prepare_embeddings returns `{}` without touching any database files

### Implementation for User Story 1

- [x] T009 [US1] Wrap the `_verify_asr_embeddings` call in `prepare_embeddings` in `raa/nodes/preparation.py` with a `try/except sqlite3.DatabaseError` that catches corrupt DB errors and re-raises as `RuntimeError("ASR embedding database is corrupt: {e}. Please re-run ARLO.")` per §18 row "ASR embedding DB missing or incomplete"
- [x] T010 [US1] Add fast-path bypass at the top of `prepare_embeddings` in `raa/nodes/preparation.py`: if `state.get("embeddings_ready", False)` is `True`, return `{}` immediately. This preserves idempotency on checkpoint resume per §22G
- [x] T011 [US1] Wrap the `_persist_non_asr_embeddings` call in `prepare_embeddings` in `raa/nodes/preparation.py` with a `try/except (sqlite3.DatabaseError, sqlite3.OperationalError)` that: (a) logs `WARNING "Non-ASR embedding DB is corrupt or missing: %s. Rebuilding from scratch."`, (b) calls `Path(non_asr_db).unlink(missing_ok=True)`, (c) retries `_persist_non_asr_embeddings` on a fresh file per §18 row "Embedding DB corrupted or locked"

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 — Startup Safety Checks and Diagnostics (Priority: P1)

**Goal**: Validate embedding environment integrity before any LLM calls. Detect and log stale embeddings with explicit warnings.

**Independent Test**: Start pipeline with missing `asr_embeddings.db` → immediate blocking error. Start with corrupt `non_asr_embeddings.db` → automatic rebuild with WARNING log.

### Tests for User Story 2

- [x] T012 [P] [US2] Add test `test_stale_hash_emits_warning_log` in `tests/raa/test_preparation.py` that pre-populates a non-ASR DB with a known-stale hash, calls `_persist_non_asr_embeddings`, and asserts a WARNING-level log is emitted containing "Stale embedding" and the requirement ID
- [x] T013 [P] [US2] Add test `test_empty_non_asr_list_produces_zero_batches_gracefully` in `tests/raa/test_batch_construction.py` that passes empty `non_asr=[]` with valid ASRs and condition groups, calls `construct_batches`, and asserts batches are created with empty `non_asr_candidates` lists without error per §18 row "No good non-ASR matches for a group"

### Implementation for User Story 2

- [x] T014 [US2] Add explicit `logger.warning("Stale embedding detected for requirement ID %d. Recomputing.", req_id)` inside the `if req_id not in cached or cached[req_id] != current_hash:` branch of `_persist_non_asr_embeddings` in `raa/nodes/preparation.py`, only when the requirement DID exist in cache but the hash differs (distinguishing stale from new). This fulfils §18 row "Embedding text hash mismatch (stale embedding)"
- [x] T015 [US2] Add explicit `logger.info("Group %s: no matching non-ASR candidates above threshold %.2f; batch will proceed with ASRs only.", gid, SIMILARITY_THRESHOLD)` after the `_search_non_asr_candidates` call in `construct_batches` in `raa/nodes/batch_construction.py` when `candidates` is empty. This fulfils §18 row "No good non-ASR matches for a group"

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 — Automatic Database Concurrency & File Lock Mitigation (Priority: P2)

**Goal**: Ensure WAL mode is consistently enabled on ALL SQLite connections — including read-only batch construction connections — to prevent deadlocks during parallel subgraph execution.

**Independent Test**: Open two concurrent read-only connections to an embedding DB that is in WAL mode → zero "database is locked" errors.

### Tests for User Story 3

- [x] T016 [P] [US3] Add test `test_connect_readonly_enables_wal` in `tests/raa/test_batch_construction.py` that creates a temporary embedding DB, calls the new `open_embedding_db(db_path, read_only=True)` from `raa/utils/db.py`, and asserts `PRAGMA journal_mode` returns `WAL`
- [x] T017 [P] [US3] Add test `test_concurrent_readonly_no_lock_errors` in `tests/raa/test_batch_construction.py` that opens three concurrent read-only connections to the same embedding DB (all via `open_embedding_db`), executes parallel SELECT queries, and asserts zero `sqlite3.OperationalError` exceptions

### Implementation for User Story 3

- [x] T018 [US3] Refactor `_connect_readonly` in `raa/nodes/batch_construction.py` to call `open_embedding_db(db_path, read_only=True)` from `raa/utils/db.py` instead of raw `sqlite3.connect`. The new helper must set `PRAGMA journal_mode=WAL;` on every connection, ensuring concurrent reads in parallel subgraphs never hit file lock contention per §22H row "Embedding SQLite DB locked"
- [x] T019 [US3] Refactor `_connect_embedding_db` in `raa/nodes/preparation.py` to call `open_embedding_db(db_path, read_only=False)` from `raa/utils/db.py`. Delete the duplicated `_connect_embedding_db` function and update all internal callers

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 — Desync Recovery during Final Merge (Priority: P2)

**Goal**: Validate `best_batch_output` completeness before final merge. If keys are missing (desync), roll back `batch_cursor` to trigger a targeted re-run instead of producing an incomplete C4 model.

**Independent Test**: Construct state with `batch_queue` of length 3 but `best_batch_output` missing index 1 → final merge raises a desync error and returns `batch_cursor=1`.

### Tests for User Story 4

- [x] T020 [P] [US4] Add test `test_desync_detection_missing_batch_key` in `tests/raa/test_final_merge.py` that constructs a state with `batch_queue` of length 3, `best_batch_output` with keys `{0, 2}` (missing 1), calls `final_merge`, and asserts: (a) a WARNING log is emitted containing "Desync detected", (b) the returned state update sets `batch_cursor` to 1, (c) the function does NOT write `arch_model.json`
- [x] T021 [P] [US4] Add test `test_desync_detection_corrupt_fragment` in `tests/raa/test_final_merge.py` that constructs a state with all batch keys present but one value is `None`, calls `final_merge`, and asserts desync recovery triggers for that index
- [x] T022 [P] [US4] Add test `test_reconciliation_output_validated_against_c4` in `tests/raa/test_final_merge.py` that mocks the LLM reconciliation to return an output that would break C4 hierarchy rules (e.g. assign a component to a non-existent container), calls `final_merge`, and asserts the broken reconciliation is rejected and the pre-reconciliation model is preserved. This fulfils §18 row "Reconciliation LLM introduces new conflicts"

### Implementation for User Story 4

- [x] T023 [US4] Add a `_validate_batch_completeness` private function in `raa/nodes/final_merge.py` that accepts `batch_queue` and `best_batch_output`, computes `expected_indices = set(range(len(batch_queue)))`, `actual_indices = set(best_batch_output.keys())`, and `missing_indices = expected_indices - actual_indices`. Also iterate `best_batch_output` values to detect `None` or empty fragments. Return the set of missing/corrupt indices
- [x] T024 [US4] Insert a call to `_validate_batch_completeness` at the top of `final_merge()` in `raa/nodes/final_merge.py`, before step 3 (global merge). If missing indices are non-empty: log `WARNING "Desync detected: missing batch outputs for indices %s. Rolling back batch_cursor to %d for targeted re-run."`, and return `{"batch_cursor": min(missing_indices)}` immediately — do NOT proceed to merge or write files. This fulfils §22H row "`batch_cursor` desync"
- [x] T025 [US4] Add post-reconciliation C4 validation in `final_merge()` in `raa/nodes/final_merge.py`: after `_apply_reconciliation_response` (step 5, line ~947), run `validate_c4_model` on the reconciled model. If the reconciled model has MORE validation errors than the pre-reconciliation model, log `WARNING "Reconciliation introduced new C4 violations; reverting to pre-reconciliation model."` and discard the reconciliation result, falling back to the pre-reconciliation `merged_model` with all `open_questions` preserved. This fulfils §18 row "Reconciliation LLM introduces new conflicts"

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Failure register integration, documentation, and final regression

- [x] T026 [P] Add a `get_failure_register()` public function in `raa/utils/failure_register.py` that returns a deep copy of the `FAILURE_REGISTER` list. Add `failure_register` to `raa/utils/__init__.py` `__all__` exports
- [x] T027 [P] Add test `test_failure_register_has_13_entries` in `tests/raa/test_failure_register.py` that imports `FAILURE_REGISTER` from `raa/utils/failure_register.py` and asserts `len(FAILURE_REGISTER) == 13`, covering all 8 §18 rows + 5 §22H rows
- [x] T028 [P] Add test `test_failure_register_entries_have_required_fields` in `tests/raa/test_failure_register.py` that iterates every entry and asserts all fields (`risk_id`, `description`, `mitigation_strategy`, `section_ref`, `verified_node`) are non-empty strings
- [x] T029 [P] Add test `test_failure_register_risk_ids_unique` in `tests/raa/test_failure_register.py` that asserts all `risk_id` values across the register are unique
- [x] T030 Run the full test suite `.venv/bin/pytest tests/raa/` and confirm all existing 308 tests plus all new tests pass — zero regressions
- [x] T031 Update `specs/019-raa-failure-mitigations/data-model.md` to document the final `FailureRegisterEntry` dataclass and the complete 13-row register table

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **User Stories (Phase 3–6)**: All depend on Phase 2 completion
  - US1 and US2 can proceed in parallel (different files)
  - US3 depends on T003 (shared helper) but can proceed concurrently with US1/US2
  - US4 depends on T003 indirectly but operates on a different file (`final_merge.py`)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phase 2 only — no other story dependencies
- **User Story 2 (P1)**: Depends on Phase 2 only — independent of US1
- **User Story 3 (P2)**: Depends on T003 (shared `open_embedding_db`) — independent of US1/US2
- **User Story 4 (P2)**: Depends on Phase 2 only — operates on `final_merge.py` (no conflict with US1–US3 files)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation tasks are ordered: helpers first, then node integration
- Story complete before moving to next priority

### Parallel Opportunities

- T006/T007/T008 can run in parallel (different test functions, same file)
- T012/T013 can run in parallel (different test files)
- T016/T017 can run in parallel (same test file, different functions)
- T020/T021/T022 can run in parallel (same test file, different functions)
- T026/T027/T028/T029 can run in parallel (different files)
- US1 and US2 can execute in parallel (preparation.py vs batch_construction.py)
- US4 can execute in parallel with US3 (final_merge.py vs batch_construction.py + preparation.py)

---

## Parallel Example: User Story 4

```bash
# Launch all tests for User Story 4 together:
Task: "Add test_desync_detection_missing_batch_key in tests/raa/test_final_merge.py"
Task: "Add test_desync_detection_corrupt_fragment in tests/raa/test_final_merge.py"
Task: "Add test_reconciliation_output_validated_against_c4 in tests/raa/test_final_merge.py"

# Then implement sequentially:
Task: "Add _validate_batch_completeness in raa/nodes/final_merge.py"
Task: "Insert desync check at top of final_merge() in raa/nodes/final_merge.py"
Task: "Add post-reconciliation C4 validation in final_merge() in raa/nodes/final_merge.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (Resilient Recovery)
4. **STOP and VALIDATE**: Run `.venv/bin/pytest tests/raa/test_preparation.py tests/raa/test_checkpoint_recovery.py` — confirm all pass
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently (MVP!)
3. Add User Story 2 → Test independently
4. Add User Story 3 → Test independently
5. Add User Story 4 → Test independently
6. Polish phase: failure register, data-model update, full regression

### File Impact Summary

| File | Stories | Changes |
|------|---------|---------|
| `raa/utils/db.py` | US3 (new file) | Shared `open_embedding_db` helper |
| `raa/utils/failure_register.py` | Polish (new file) | `FAILURE_REGISTER` constant + `get_failure_register()` |
| `raa/state/types.py` | Foundation | `FailureRegisterEntry` dataclass |
| `raa/nodes/preparation.py` | US1, US2 | Corrupt DB handling, stale hash warnings, fast-path bypass |
| `raa/nodes/batch_construction.py` | US2, US3 | Empty non-ASR log, WAL on readonly connections |
| `raa/nodes/final_merge.py` | US4 | Desync detection, reconciliation C4 validation gate |
| `raa/utils/__init__.py` | Polish | Export additions |
| `tests/raa/test_preparation.py` | US1, US2 | 4 new test functions |
| `tests/raa/test_batch_construction.py` | US2, US3 | 3 new test functions |
| `tests/raa/test_final_merge.py` | US4 | 3 new test functions |
| `tests/raa/test_failure_register.py` | Polish (new file) | 3 test functions |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
