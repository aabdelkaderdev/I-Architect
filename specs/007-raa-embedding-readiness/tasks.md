# Tasks: RAA Preparation and Embedding Readiness

**Input**: Design documents from `specs/007-raa-embedding-readiness/`
**Source Scope**: `RAA_Plan.md` Section 6 only
**Tests**: Included because the user request explicitly requires missing-ASR, stale-hash recomputation, and idempotent rerun unit tests.

**Organization**: Tasks are grouped around one independently testable preparation-node story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm embedding runtime paths, package paths, and test paths exist before implementation.

- [X] T001 [P] Confirm the RAA nodes package exists at `raa/nodes/`
- [X] T002 [P] Confirm the RAA test package exists at `tests/raa/`
- [X] T003 [P] Confirm shared embedding runtime directory exists at `embeddings/`
- [X] T004 [P] Confirm `fastembed==0.8.0` is available in `pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature contract and tests with the Section 6 shared SQLite schema before code is written.

- [X] T005 Update `specs/007-raa-embedding-readiness/data-model.md` to use shared SQLite columns `requirement_id`, `embedding`, `text_hash`, and `model_name`
- [X] T006 Update `specs/007-raa-embedding-readiness/contracts/readme.md` to require shared SQLite columns `requirement_id`, `embedding`, `text_hash`, and `model_name`
- [X] T007 Create `tests/raa/test_preparation.py` with temporary SQLite database fixtures for `asr_embeddings.db` and `non_asr_embeddings.db`
- [X] T008 Add a fake embedding model fixture in `tests/raa/test_preparation.py` so tests do not download or instantiate FastEmbed
- [X] T009 Add SQLite fixture helpers in `tests/raa/test_preparation.py` that create the shared `embeddings` table with `requirement_id`, `embedding`, `text_hash`, and `model_name`

**Checkpoint**: Feature docs and test fixtures use the Section 6 shared schema.

---

## Phase 3: User Story 1 - Verify ASR Embeddings and Persist Non-ASR Embeddings (Priority: P1) MVP

**Goal**: The preparation node verifies all ASR embeddings exist, generates only missing or stale non-ASR embeddings, persists them to SQLite, and returns `embeddings_ready = True`.

**Independent Test**: Run `tests/raa/test_preparation.py` and confirm missing ASR rows raise a blocking error, stale non-ASR rows are recomputed, idempotent reruns skip model calls, and success returns `{"embeddings_ready": True}`.

### Tests for User Story 1

- [X] T010 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying missing `embeddings/asr_embeddings.db` raises a blocking error instructing the operator to re-run ARLO
- [X] T011 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying an ASR ID missing from `asr_embeddings.db` raises a blocking error listing the missing ID
- [X] T012 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying ASR verification passes when every ASR requirement ID has a row in `asr_embeddings.db`
- [X] T013 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying non-ASR embeddings are written to `non_asr_embeddings.db` with `requirement_id`, `embedding`, `text_hash`, and `model_name`
- [X] T014 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying stale `text_hash` rows trigger recomputation and update the stored embedding row
- [X] T015 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying idempotent rerun behavior skips the fake embedding model when hashes already match
- [X] T016 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying the preparation node returns `{"embeddings_ready": True}` after successful ASR verification and non-ASR persistence
- [X] T017 [P] [US1] Add a unit test in `tests/raa/test_preparation.py` verifying SQLite connections use WAL mode for `asr_embeddings.db` and `non_asr_embeddings.db`

### Implementation for User Story 1

- [X] T018 [US1] Create `raa/nodes/preparation.py` with constants for `_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"`, `embeddings/asr_embeddings.db`, and `embeddings/non_asr_embeddings.db`
- [X] T019 [US1] Implement `_project_root()` and embedding database path helpers in `raa/nodes/preparation.py`
- [X] T020 [US1] Implement `_connect_embedding_db(db_path: Path) -> sqlite3.Connection` that enables `PRAGMA journal_mode=WAL` in `raa/nodes/preparation.py`
- [X] T021 [US1] Implement `_ensure_embeddings_schema(conn: sqlite3.Connection)` creating the shared `embeddings(requirement_id INTEGER PRIMARY KEY, embedding BLOB NOT NULL, text_hash TEXT NOT NULL, model_name TEXT NOT NULL)` table in `raa/nodes/preparation.py`
- [X] T022 [US1] Implement `_requirement_id_int(requirement: dict) -> int` that maps normalized IDs like `"R12"` or raw integer IDs to SQLite `requirement_id` values in `raa/nodes/preparation.py`
- [X] T023 [US1] Implement `_hash_text(text: str) -> str` using SHA-256 for cache integrity in `raa/nodes/preparation.py`
- [X] T024 [US1] Implement `_serialize_embedding(vector: list[float]) -> bytes` storing 1024 float values as a binary blob in `raa/nodes/preparation.py`
- [X] T025 [US1] Implement `_get_embedding_model()` using FastEmbed `TextEmbedding` with model `mixedbread-ai/mxbai-embed-large-v1` in `raa/nodes/preparation.py`
- [X] T026 [US1] Implement `_verify_asr_embeddings(asrs: list[dict], asr_db_path: Path)` that errors if `asr_embeddings.db` is missing in `raa/nodes/preparation.py`
- [X] T027 [US1] Implement `_verify_asr_embeddings` row lookup by `requirement_id` and raise a blocking error instructing operators to re-run ARLO when any ASR row is missing in `raa/nodes/preparation.py`
- [X] T028 [US1] Implement `_non_asr_text(requirement: dict, requirements: dict[str, str] | None = None) -> str` using normalized `text` first and parent `requirements` lookup only as fallback in `raa/nodes/preparation.py`
- [X] T029 [US1] Implement `_load_cached_hashes(conn: sqlite3.Connection) -> dict[int, str]` for `non_asr_embeddings.db` in `raa/nodes/preparation.py`
- [X] T030 [US1] Implement cache filtering that selects only missing or stale non-ASR requirements by comparing current `_hash_text(text)` to stored `text_hash` in `raa/nodes/preparation.py`
- [X] T031 [US1] Implement `_embed_texts(texts: list[str], model: TextEmbedding | None = None) -> list[list[float]]` to allow fake model injection in tests in `raa/nodes/preparation.py`
- [X] T032 [US1] Implement transactional upsert of non-ASR rows into `non_asr_embeddings.db` with `requirement_id`, serialized `embedding`, `text_hash`, and `_MODEL_NAME` in `raa/nodes/preparation.py`
- [X] T033 [US1] Implement `prepare_embeddings(state: RAAState) -> dict` that verifies ASR embeddings, persists non-ASR embeddings, and returns `{"embeddings_ready": True}` in `raa/nodes/preparation.py`
- [X] T034 [US1] Export `prepare_embeddings` from `raa/nodes/__init__.py`

**Checkpoint**: Preparation node is independently callable and marks embedding readiness only after ASR verification and non-ASR persistence succeed.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate Section 6 behavior and keep implementation scoped to embedding readiness.

- [X] T035 [P] Run `pytest tests/raa/test_preparation.py`
- [X] T036 [P] Run Python syntax validation for `raa/nodes/preparation.py` and `raa/nodes/__init__.py`
- [X] T037 Confirm `raa/nodes/preparation.py` does not load embeddings into LangGraph state channels and only returns `embeddings_ready`
- [X] T038 Confirm `raa/nodes/preparation.py` uses the same FastEmbed model name as ARLO, `mixedbread-ai/mxbai-embed-large-v1`
- [X] T039 Confirm `raa/nodes/preparation.py` uses `text_hash` cache checks and skips already-persisted non-ASR rows on rerun
- [X] T040 Confirm `raa/nodes/preparation.py` treats missing ASR embeddings as blocking errors and missing non-ASR DB as rebuildable state

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational schema/test fixtures.
- **Polish (Final Phase)**: Depends on User Story 1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 and has no dependency on other stories.

### Within User Story 1

- Write tests T010-T017 before implementation tasks T018-T034.
- Implement database helpers before ASR verification and non-ASR upsert logic.
- Implement cache filtering before transactional upsert.
- Export `prepare_embeddings` only after the node implementation exists.

### Parallel Opportunities

- T001 through T004 can run in parallel.
- T010 through T017 can be drafted in parallel only if edits to `tests/raa/test_preparation.py` are coordinated.
- T018 through T034 should run mostly sequentially because they build one module.
- T035 and T036 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a unit test verifying missing asr_embeddings.db raises a blocking error in tests/raa/test_preparation.py"
Task: "Add a unit test verifying stale text_hash rows trigger recomputation in tests/raa/test_preparation.py"
Task: "Add a unit test verifying idempotent rerun behavior skips the fake embedding model in tests/raa/test_preparation.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write tests for missing ASR rows, stale hashes, idempotent reruns, and readiness output.
3. Implement `raa/nodes/preparation.py` helpers and node function.
4. Run the preparation unit tests.

### Incremental Delivery

1. Align feature docs/contracts to the Section 6 shared schema.
2. Add failing tests with fake embedding model injection.
3. Implement SQLite helpers, ASR verification, cache filtering, and non-ASR upsert.
4. Validate that embedding vectors stay in SQLite and out of LangGraph state.

### Notes

- Follow `RAA_Plan.md` Section 6 and shared persistence schema over the stale `id/text/vector` draft in the feature docs.
- Do not implement batch construction, overlap bridging, coherence gate, or graph wiring in this feature.
- Tests should avoid real FastEmbed downloads by injecting or monkeypatching the embedding model.
