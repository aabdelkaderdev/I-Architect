# Tasks: RAA Batch Coherence Gate

**Input**: Design documents from `specs/011-raa-batch-coherence/`
**Source Scope**: `RAA_Plan.md` Section 10 only
**Tests**: Included because the user request explicitly requires unit tests for homogeneous-pass and heterogeneous-split behavior, and the feature spec requires reduced-confidence failure handling.

**Organization**: Tasks are grouped around one independently testable coherence-gate story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the RAA node, state, and test paths needed by the coherence gate are present before implementation.

- [X] T001 [P] Confirm the RAA nodes package exists at `raa/nodes/`
- [X] T002 [P] Confirm the RAA state package exists at `raa/state/`
- [X] T003 [P] Confirm the RAA test package exists at `tests/raa/`
- [X] T004 [P] Confirm batch payloads expose `batch_id`, `group_id`, `requirement_ids`, `requirements`, `group_centroid`, and `reduced_confidence` in `raa/state/types.py`
- [X] T005 [P] Confirm `RAAState.incoherent_batches` exists as an append channel in `raa/state/channels.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature docs and state contract with the Section 10 coherence metadata before implementing the node.

- [X] T006 Update `specs/011-raa-batch-coherence/plan.md` to use the repository test path `tests/raa/test_coherence_gate.py`
- [X] T007 Update `specs/011-raa-batch-coherence/data-model.md` to align the incoherent record with `IncoherentBatchRecord(batch_id, coherence_score, reduced_confidence)` from `raa/state/types.py`
- [X] T008 Extend the `Batch` TypedDict in `raa/state/types.py` with optional `coherence_score`, `is_split`, and `source_batch_id` fields for Section 10 metadata
- [X] T009 Confirm every requirement payload used by `raa/nodes/coherence_gate.py` contains an embedding vector under `embedding` or `vector`, and document the error path in `tests/raa/test_coherence_gate.py`

**Checkpoint**: Feature docs and state contracts describe the coherence gate inputs, outputs, and metadata before node implementation begins.

---

## Phase 3: User Story 1 - Evaluate Batch Coherence, Split Incoherent Batches, Or Flag Reduced Confidence (Priority: P1) MVP

**Goal**: Compute average intra-batch cosine similarity for every batch, split low-coherence batches once into two sub-batches, and record reduced-confidence batches when splitting does not produce two coherent sub-batches.

**Independent Test**: Run `tests/raa/test_coherence_gate.py` and confirm cohesive batches pass unchanged, heterogeneous batches split into two passing sub-batches, and still-incoherent batches are recorded with `reduced_confidence = true`.

### Tests for User Story 1

- [X] T010 [P] [US1] Create `tests/raa/test_coherence_gate.py` with deterministic vector helpers, batch fixtures, and a full RAA state fixture containing `batch_queue` and `incoherent_batches`
- [X] T011 [P] [US1] Add a unit test verifying `_compute_centroid` averages requirement embeddings and returns a normalized centroid in `tests/raa/test_coherence_gate.py`
- [X] T012 [P] [US1] Add a unit test verifying `_compute_coherence_score` returns the average cosine similarity from each requirement embedding to the computed batch centroid in `tests/raa/test_coherence_gate.py`
- [X] T013 [P] [US1] Add a unit test verifying the coherence threshold is `0.55` and does not reuse the Section 8 non-ASR candidate threshold `0.65` in `tests/raa/test_coherence_gate.py`
- [X] T014 [P] [US1] Add a unit test verifying batches with 2 or fewer requirements pass automatically and are not split in `tests/raa/test_coherence_gate.py`
- [X] T015 [P] [US1] Add a homogeneous-pass unit test verifying a batch with coherence score `>= 0.55` remains in `batch_queue` unchanged except for `coherence_score` metadata in `tests/raa/test_coherence_gate.py`
- [X] T016 [P] [US1] Add a unit test verifying a batch with coherence score `< 0.55` is split into exactly two sub-batches when both sub-clusters re-score at `>= 0.55` in `tests/raa/test_coherence_gate.py`
- [X] T017 [P] [US1] Add a heterogeneous-split unit test verifying split sub-batches preserve the original requirement payloads, requirement IDs, similarity scores, group metadata, and source batch ID in `tests/raa/test_coherence_gate.py`
- [X] T018 [P] [US1] Add a unit test verifying deterministic split assignment is stable across repeated runs with the same embeddings in `tests/raa/test_coherence_gate.py`
- [X] T019 [P] [US1] Add a unit test verifying a split failure keeps the original batch, sets `reduced_confidence = true`, and appends an `IncoherentBatchRecord` with `reduced_confidence = true` in `tests/raa/test_coherence_gate.py`
- [X] T020 [P] [US1] Add a node-level unit test verifying `apply_coherence_gate(state)` evaluates every batch in `state["batch_queue"]` and returns an updated `batch_queue` plus `incoherent_batches` in `tests/raa/test_coherence_gate.py`
- [X] T021 [P] [US1] Add a unit test verifying missing requirement embeddings raise a clear blocking error instead of silently passing or using `group_centroid` in `tests/raa/test_coherence_gate.py`

### Implementation for User Story 1

- [X] T022 [US1] Create `raa/nodes/coherence_gate.py` with constants `COHERENCE_THRESHOLD = 0.55`, `MAX_SPLIT_CLUSTERS = 2`, and `MAX_KMEANS_ITERATIONS = 10`
- [X] T023 [US1] Implement `_as_float_array(vector: list[float]) -> numpy.ndarray` with empty-vector and zero-vector handling in `raa/nodes/coherence_gate.py`
- [X] T024 [US1] Implement `_normalize(vector: numpy.ndarray) -> numpy.ndarray` returning zero vectors unchanged in `raa/nodes/coherence_gate.py`
- [X] T025 [US1] Implement `_cosine_similarity(a: list[float] | numpy.ndarray, b: list[float] | numpy.ndarray) -> float` for Section 10 scoring in `raa/nodes/coherence_gate.py`
- [X] T026 [US1] Implement `_requirement_embedding(requirement: dict) -> list[float]` reading `embedding` first, then `vector`, and raising `ValueError` when neither is present in `raa/nodes/coherence_gate.py`
- [X] T027 [US1] Implement `_batch_embeddings(batch: dict) -> list[list[float]]` extracting embeddings from every requirement payload in `raa/nodes/coherence_gate.py`
- [X] T028 [US1] Implement `_compute_centroid(vectors: list[list[float]]) -> list[float]` using element-wise averaging followed by L2 normalization in `raa/nodes/coherence_gate.py`
- [X] T029 [US1] Implement `_compute_coherence_score(vectors: list[list[float]]) -> float` as average cosine similarity between each vector and the computed batch centroid in `raa/nodes/coherence_gate.py`
- [X] T030 [US1] Implement `_should_pass_without_split(batch: dict) -> bool` so batches with 2 or fewer requirements pass automatically in `raa/nodes/coherence_gate.py`
- [X] T031 [US1] Implement `_furthest_pair_indices(vectors: list[list[float]]) -> tuple[int, int]` to seed deterministic two-way splitting from the least-similar pair in `raa/nodes/coherence_gate.py`
- [X] T032 [US1] Implement `_split_vectors_k2(vectors: list[list[float]]) -> tuple[list[int], list[int]]` using deterministic two-centroid assignment and at most 10 iterations in `raa/nodes/coherence_gate.py`
- [X] T033 [US1] Implement `_build_sub_batch(batch: dict, selected_indices: list[int], sub_index: int) -> dict` preserving payloads, requirement IDs, similarity scores, group metadata, and `source_batch_id` in `raa/nodes/coherence_gate.py`
- [X] T034 [US1] Implement `_evaluate_batch(batch: dict) -> tuple[list[dict], IncoherentBatchRecord | None]` that returns one passing batch, two passing sub-batches, or one reduced-confidence original batch plus an incoherent record in `raa/nodes/coherence_gate.py`
- [X] T035 [US1] Implement `_renumber_batch_queue(batches: list[dict]) -> list[dict]` so split output batches have unique queue-order `batch_id` values while preserving `source_batch_id` in `raa/nodes/coherence_gate.py`
- [X] T036 [US1] Implement `apply_coherence_gate(state: RAAState) -> dict` reading `batch_queue`, evaluating each batch, and returning `{"batch_queue": updated_batches, "incoherent_batches": records}` in `raa/nodes/coherence_gate.py`
- [X] T037 [US1] Export `apply_coherence_gate` from `raa/nodes/__init__.py`

**Checkpoint**: Coherence gate is independently callable after overlap bridging and writes an updated batch queue plus incoherent-batch records.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate Section 10 behavior and keep implementation limited to the coherence gate.

- [X] T038 [P] Run `pytest tests/raa/test_coherence_gate.py`
- [X] T039 [P] Run Python syntax validation for `raa/nodes/coherence_gate.py`, `raa/nodes/__init__.py`, and `raa/state/types.py`
- [X] T040 Confirm `raa/nodes/coherence_gate.py` uses `COHERENCE_THRESHOLD = 0.55` and never imports or reuses the Section 8 `SIMILARITY_THRESHOLD = 0.65`
- [X] T041 Confirm `raa/nodes/coherence_gate.py` computes the centroid from all requirement embeddings in the batch rather than using `group_centroid` as the coherence centroid
- [X] T042 Confirm `raa/nodes/coherence_gate.py` performs only one split attempt and does not recursively split failed sub-clusters
- [X] T043 Confirm `raa/nodes/coherence_gate.py` appends only `IncoherentBatchRecord` entries to `incoherent_batches` and does not create a new state channel
- [X] T044 Confirm `raa/nodes/coherence_gate.py` does not implement batch construction, overlap bridging, queue ordering, RAA subgraphs, judge behavior, or final merge behavior

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational state and doc alignment.
- **Polish (Final Phase)**: Depends on User Story 1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 and has no dependency on other stories.

### Within User Story 1

- Write tests T010-T021 before implementation tasks T022-T037.
- Implement vector helpers before centroid and coherence scoring.
- Implement deterministic split helpers before sub-batch assembly.
- Implement `apply_coherence_gate` after `_evaluate_batch` and queue renumbering exist.
- Export `apply_coherence_gate` only after implementation exists.

### Parallel Opportunities

- T001 through T005 can run in parallel.
- T010 through T021 can be drafted in parallel only if edits to `tests/raa/test_coherence_gate.py` are coordinated.
- T022 through T037 should run mostly sequentially because they build one module.
- T038 and T039 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a homogeneous-pass unit test verifying a batch with coherence score >= 0.55 remains in batch_queue unchanged except for coherence_score metadata in tests/raa/test_coherence_gate.py"
Task: "Add a unit test verifying a batch with coherence score < 0.55 is split into exactly two sub-batches when both sub-clusters re-score at >= 0.55 in tests/raa/test_coherence_gate.py"
Task: "Add a unit test verifying a split failure keeps the original batch, sets reduced_confidence = true, and appends an IncoherentBatchRecord with reduced_confidence = true in tests/raa/test_coherence_gate.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write tests for centroid scoring, homogeneous pass, heterogeneous split, deterministic split stability, and reduced-confidence failure.
3. Implement `raa/nodes/coherence_gate.py`.
4. Run the coherence gate unit tests.

### Incremental Delivery

1. Align feature docs and state metadata with Section 10.
2. Implement vector extraction, centroid calculation, and coherence scoring.
3. Implement deterministic one-pass split and sub-batch assembly.
4. Implement reduced-confidence fallback and incoherent-batch recording.
5. Validate no downstream phases were introduced.

### Notes

- This feature assumes batch construction and overlap bridging have already assembled full requirement payloads before the coherence gate runs.
- The coherence score is the Section 10 average intra-batch cosine similarity, not the Section 8 per-requirement candidate-selection similarity.
- Do not persist embeddings or load embedding SQLite databases in this node; use requirement embeddings already present in the batch payload.
