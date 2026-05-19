# Tasks: RAA Batch Construction

**Input**: Design documents from `specs/009-raa-batch-construction/`
**Source Scope**: `RAA_Plan.md` Section 8 and Section 3 steps 1-2 only
**Tests**: Included because the feature specification requires validation for centroid math, fallback re-embedding, similarity filtering, candidate cap, and final batch payloads.

**Organization**: Tasks are grouped around one independently testable batch-construction story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the runtime package, embedding persistence inputs, and test paths exist before implementing batch construction.

- [X] T001 [P] Confirm the RAA nodes package exists at `raa/nodes/`
- [X] T002 [P] Confirm the RAA state package exists at `raa/state/`
- [X] T003 [P] Confirm the RAA test package exists at `tests/raa/`
- [X] T004 [P] Confirm shared embedding runtime directory exists at `embeddings/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature docs and state payload contract with the requested `batch_construction.py` node and full normalized requirement payloads.

- [X] T005 Update `specs/009-raa-batch-construction/plan.md` to name the implementation module `raa/nodes/batch_construction.py` instead of `raa/nodes/batch_builder.py`
- [X] T006 Update `specs/009-raa-batch-construction/quickstart.md` examples to import from `raa.nodes.batch_construction`
- [X] T007 Update `specs/009-raa-batch-construction/data-model.md` so `BatchPayload` includes `group_id`, `cluster`, `centroid`, `requirements`, and `similarity_scores`
- [X] T008 Update `specs/009-raa-batch-construction/data-model.md` so `requirements` stores full normalized ASR and non-ASR requirement payloads, not only IDs
- [X] T009 Update `specs/009-raa-batch-construction/contracts/readme.md` to require threshold `similarity >= 0.65`, max 10 selected non-ASRs, full normalized payloads, and per-requirement similarity scores
- [X] T010 Extend the `Batch` TypedDict in `raa/state/types.py` with `cluster`, `requirements`, `similarity_scores`, and `non_asr_candidates` fields needed by Section 8 batch payloads
- [X] T011 Export any new batch helper TypedDicts from `raa/state/__init__.py`

**Checkpoint**: Documentation and state contracts describe the intended Section 8 batch payload before implementation begins.

---

## Phase 3: User Story 1 - Construct Condition-Group Anchored Requirement Batches (Priority: P1) MVP

**Goal**: For each ARLO condition group, compute an ASR-derived centroid or fallback nominal-condition embedding, retrieve similar non-ASR requirements, apply threshold and cap rules, and assemble full batch payloads.

**Independent Test**: Run `tests/raa/test_batch_construction.py` and confirm centroid math, fallback embedding, similarity filtering, top-10 capping, and full payload assembly all pass.

### Tests for User Story 1

- [X] T012 [P] [US1] Create `tests/raa/test_batch_construction.py` with temporary SQLite fixtures for `asr_embeddings.db` and `non_asr_embeddings.db` using the shared schema `requirement_id`, `embedding`, `text_hash`, and `model_name`
- [X] T013 [P] [US1] Add vector serialization/deserialization fixtures in `tests/raa/test_batch_construction.py` for deterministic 1024-dimensional test vectors
- [X] T014 [P] [US1] Add a unit test verifying group centroid is the element-wise average of ASR embeddings loaded from `asr_embeddings.db` in `tests/raa/test_batch_construction.py`
- [X] T015 [P] [US1] Add a unit test verifying fallback re-embeds `nominal_condition` when no ASR embeddings can be loaded for a condition group in `tests/raa/test_batch_construction.py`
- [X] T016 [P] [US1] Add a unit test verifying cosine similarity filter keeps only non-ASR candidates with score `>= 0.65` in `tests/raa/test_batch_construction.py`
- [X] T017 [P] [US1] Add a unit test verifying non-ASR candidate selection is capped at the top 10 highest similarity scores in `tests/raa/test_batch_construction.py`
- [X] T018 [P] [US1] Add a unit test verifying empty matching non-ASR pool still assembles an ASR-only batch without error in `tests/raa/test_batch_construction.py`
- [X] T019 [P] [US1] Add a unit test verifying assembled batch stores `group_id`, `centroid`, `similarity_scores`, and full normalized requirement payloads in `tests/raa/test_batch_construction.py`
- [X] T020 [P] [US1] Add a node-level unit test verifying `construct_batches(state)` returns `batch_queue` with one batch per `condition_groups` entry in `tests/raa/test_batch_construction.py`

### Implementation for User Story 1

- [X] T021 [US1] Create `raa/nodes/batch_construction.py` with constants for `ASR_DB_PATH`, `NON_ASR_DB_PATH`, `_MODEL_NAME`, `SIMILARITY_THRESHOLD = 0.65`, and `MAX_NON_ASR_CANDIDATES = 10`
- [X] T022 [US1] Implement project-root and embedding database path helpers in `raa/nodes/batch_construction.py`
- [X] T023 [US1] Implement SQLite connection helpers for read-only embedding lookups from `embeddings/asr_embeddings.db` and `embeddings/non_asr_embeddings.db` in `raa/nodes/batch_construction.py`
- [X] T024 [US1] Implement `_requirement_id_int(requirement_id: str | int) -> int` to map normalized IDs like `"R12"` and raw integers to SQLite `requirement_id` values in `raa/nodes/batch_construction.py`
- [X] T025 [US1] Implement `_deserialize_embedding(blob: bytes) -> list[float]` for the shared embedding BLOB format in `raa/nodes/batch_construction.py`
- [X] T026 [US1] Implement `_load_asr_embeddings(requirement_ids: list[str | int], db_path: Path) -> dict[int, list[float]]` reading ASR vectors from `asr_embeddings.db` in `raa/nodes/batch_construction.py`
- [X] T027 [US1] Implement `_compute_centroid(vectors: list[list[float]]) -> list[float]` using element-wise averaging in `raa/nodes/batch_construction.py`
- [X] T028 [US1] Implement `_get_embedding_model()` and `_embed_nominal_condition(nominal_condition: str) -> list[float]` using FastEmbed model `mixedbread-ai/mxbai-embed-large-v1` in `raa/nodes/batch_construction.py`
- [X] T029 [US1] Implement `_group_requirement_ids(condition_group: dict) -> list[str | int]` that extracts ASR IDs from `condition_group["requirements"]` first and falls back to indexed entries from `condition_group["conditions"]` in `raa/nodes/batch_construction.py`
- [X] T030 [US1] Implement `_centroid_for_group(condition_group: dict, asr_db_path: Path) -> list[float]` that prefers averaged ASR embeddings and falls back to nominal-condition re-embedding in `raa/nodes/batch_construction.py`
- [X] T031 [US1] Implement `_load_non_asr_embedding_rows(db_path: Path) -> list[dict]` reading `requirement_id`, `embedding`, `text_hash`, and `model_name` rows from `non_asr_embeddings.db` in `raa/nodes/batch_construction.py`
- [X] T032 [US1] Implement `_cosine_similarity(a: list[float], b: list[float]) -> float` without building a full all-requirements cosine similarity matrix in `raa/nodes/batch_construction.py`
- [X] T033 [US1] Implement `_search_non_asr_candidates(centroid: list[float], non_asr_rows: list[dict], non_asr_payloads: list[dict]) -> list[dict]` applying threshold `>= 0.65`, sorting descending, and capping at 10 in `raa/nodes/batch_construction.py`
- [X] T034 [US1] Implement `_payload_by_requirement_id(requirements: list[dict]) -> dict[int, dict]` mapping normalized ASR and non-ASR payloads to SQLite integer IDs in `raa/nodes/batch_construction.py`
- [X] T035 [US1] Implement `_assemble_batch(group_id: int, condition_group: dict, centroid: list[float], asr_payloads: list[dict], non_asr_candidates: list[dict]) -> Batch` storing group ID, cluster, centroid, full requirement payloads, and per-requirement similarity scores in `raa/nodes/batch_construction.py`
- [X] T036 [US1] Implement `construct_batches(state: RAAState) -> dict` that reads normalized `asrs`, `non_asr`, and `condition_groups`, constructs one batch per condition group, and returns `{"batch_queue": batches}` in `raa/nodes/batch_construction.py`
- [X] T037 [US1] Export `construct_batches` from `raa/nodes/__init__.py`

**Checkpoint**: Batch construction is independently callable after preparation and produces Section 8 batch payloads.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate Section 8 behavior and prevent out-of-scope pipeline work.

- [X] T038 [P] Run `pytest tests/raa/test_batch_construction.py`
- [X] T039 [P] Run Python syntax validation for `raa/nodes/batch_construction.py`, `raa/nodes/__init__.py`, `raa/state/types.py`, and `raa/state/__init__.py`
- [X] T040 Confirm `raa/nodes/batch_construction.py` performs one centroid-to-non-ASR search per condition group and does not compute a full all-requirements cosine similarity matrix
- [X] T041 Confirm `raa/nodes/batch_construction.py` only reads embedding SQLite databases and does not write to `asr_embeddings.db` or `non_asr_embeddings.db`
- [X] T042 Confirm `raa/nodes/batch_construction.py` does not implement overlap bridging, coherence gating, queue ordering, RAA subgraphs, or judge behavior
- [X] T043 Confirm every batch in `batch_queue` includes full normalized requirement payloads and per-requirement similarity scores

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational schema/doc alignment.
- **Polish (Final Phase)**: Depends on User Story 1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 and has no dependency on other stories.

### Within User Story 1

- Write tests T012-T020 before implementation tasks T021-T037.
- Implement SQLite and vector helpers before centroid and candidate-search helpers.
- Implement batch assembly after centroid and candidate-search helpers.
- Export `construct_batches` only after implementation exists.

### Parallel Opportunities

- T001 through T004 can run in parallel.
- T012 through T020 can be drafted in parallel only if edits to `tests/raa/test_batch_construction.py` are coordinated.
- T021 through T037 should run mostly sequentially because they build one module.
- T038 and T039 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a unit test verifying group centroid is the element-wise average of ASR embeddings loaded from asr_embeddings.db in tests/raa/test_batch_construction.py"
Task: "Add a unit test verifying cosine similarity filter keeps only non-ASR candidates with score >= 0.65 in tests/raa/test_batch_construction.py"
Task: "Add a unit test verifying non-ASR candidate selection is capped at the top 10 highest similarity scores in tests/raa/test_batch_construction.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write tests for centroid, fallback embedding, threshold, cap, and payload assembly.
3. Implement `raa/nodes/batch_construction.py` helper functions and `construct_batches`.
4. Run the batch construction unit tests.

### Incremental Delivery

1. Align docs and state payload contract to Section 8 and the requested module name.
2. Implement deterministic embedding loading and centroid computation.
3. Add non-ASR similarity search with threshold and cap.
4. Assemble full batch payloads and validate no downstream phases were introduced.

### Notes

- This feature assumes preparation has already normalized requirements and persisted ASR/non-ASR embeddings.
- Fallback nominal-condition re-embedding is only for condition groups with no loadable ASR embeddings.
- Do not implement overlap bridging or coherence scoring in this feature.
