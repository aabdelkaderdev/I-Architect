# Tasks: RAA Overlap Bridging

**Input**: Design documents from `specs/010-raa-overlap-bridging/`
**Source Scope**: `RAA_Plan.md` Section 9 only
**Tests**: Included because the user request explicitly requires a hard-cap unit test and the feature spec requires adjacency, bridge scoring, injection, and registry validation.

**Organization**: Tasks are grouped around one independently testable overlap-bridging story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the batch-construction outputs and RAA state paths exist before implementing overlap bridging.

- [X] T001 [P] Confirm the RAA nodes package exists at `raa/nodes/`
- [X] T002 [P] Confirm the RAA state package exists at `raa/state/`
- [X] T003 [P] Confirm the RAA test package exists at `tests/raa/`
- [X] T004 [P] Confirm batch construction output fields `group_id`, `group_centroid`, `requirements`, and `similarity_scores` are available in `raa/nodes/batch_construction.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature docs and state contract with the requested `overlap_bridging.py` node and Section 9 state-channel behavior.

- [X] T005 Update `specs/010-raa-overlap-bridging/plan.md` to name the implementation module `raa/nodes/overlap_bridging.py` instead of `raa/nodes/overlap_bridger.py`
- [X] T006 Update `specs/010-raa-overlap-bridging/quickstart.md` examples to import from `raa.nodes.overlap_bridging`
- [X] T007 Update `specs/010-raa-overlap-bridging/data-model.md` to document `bridge_requirements` as the RAA state channel written by overlap bridging
- [X] T008 Update `specs/010-raa-overlap-bridging/data-model.md` to document pair keys consistently with implementation, including group IDs and selected bridge requirement IDs
- [X] T009 Confirm `RAAState.bridge_requirements` exists as an overwrite channel in `raa/state/channels.py`
- [X] T010 Confirm `Batch` payloads in `raa/state/types.py` can hold injected bridge requirements in `requirements`, `requirement_ids`, and `similarity_scores`

**Checkpoint**: Feature docs and state contracts are aligned before node implementation.

---

## Phase 3: User Story 1 - Bridge Adjacent Batches With Shared Requirements (Priority: P1) MVP

**Goal**: Detect adjacent or related batches, select 1-3 shared bridge requirements, inject them into both batches, and record the selected IDs in `bridge_requirements`.

**Independent Test**: Run `tests/raa/test_overlap_bridging.py` and confirm adjacent detection, dual-centroid scoring, hard cap, batch injection, and `bridge_requirements` recording all pass.

### Tests for User Story 1

- [X] T011 [P] [US1] Create `tests/raa/test_overlap_bridging.py` with batch fixtures containing `group_id`, `cluster`, `group_centroid`, `requirements`, `requirement_ids`, and `similarity_scores`
- [X] T012 [P] [US1] Add a unit test verifying batches are adjacent when their cluster IDs match in `tests/raa/test_overlap_bridging.py`
- [X] T013 [P] [US1] Add a unit test verifying batches are adjacent when centroid cosine similarity is greater than or equal to the configured threshold in `tests/raa/test_overlap_bridging.py`
- [X] T014 [P] [US1] Add a unit test verifying non-adjacent batches produce no bridge requirements and leave batches unchanged in `tests/raa/test_overlap_bridging.py`
- [X] T015 [P] [US1] Add a unit test verifying dual-centroid bridge scoring ranks candidates by similarity to both batch centroids in `tests/raa/test_overlap_bridging.py`
- [X] T016 [P] [US1] Add a unit test verifying selected bridge requirements are limited to a hard cap of 3 per adjacent pair in `tests/raa/test_overlap_bridging.py`
- [X] T017 [P] [US1] Add a unit test verifying fewer than 3 qualifying bridge candidates are selected without padding or errors in `tests/raa/test_overlap_bridging.py`
- [X] T018 [P] [US1] Add a unit test verifying selected bridge requirement payloads are injected into both adjacent batches in `tests/raa/test_overlap_bridging.py`
- [X] T019 [P] [US1] Add a unit test verifying injected bridge IDs are present in both batches' `requirement_ids` and `similarity_scores` in `tests/raa/test_overlap_bridging.py`
- [X] T020 [P] [US1] Add a node-level unit test verifying `apply_overlap_bridging(state)` returns updated `batch_queue` and `bridge_requirements` in `tests/raa/test_overlap_bridging.py`

### Implementation for User Story 1

- [X] T021 [US1] Create `raa/nodes/overlap_bridging.py` with constants `ADJACENCY_THRESHOLD = 0.50`, `BRIDGE_SIMILARITY_THRESHOLD = 0.0`, and `MAX_BRIDGE_REQUIREMENTS = 3`
- [X] T022 [US1] Implement `_cosine_similarity(a: list[float], b: list[float]) -> float` for centroid and candidate scoring in `raa/nodes/overlap_bridging.py`
- [X] T023 [US1] Implement `_batch_cluster(batch: dict) -> object | None` reading cluster metadata from a batch payload in `raa/nodes/overlap_bridging.py`
- [X] T024 [US1] Implement `_are_adjacent(left: dict, right: dict, threshold: float = ADJACENCY_THRESHOLD) -> bool` using cluster ID match or centroid cosine similarity in `raa/nodes/overlap_bridging.py`
- [X] T025 [US1] Implement `_adjacent_pairs(batches: list[dict]) -> list[tuple[int, int]]` that detects adjacent batch pairs without duplicate or self pairs in `raa/nodes/overlap_bridging.py`
- [X] T026 [US1] Implement `_candidate_pool(left: dict, right: dict) -> list[dict]` collecting unique non-ASR requirement payloads from both batches in `raa/nodes/overlap_bridging.py`
- [X] T027 [US1] Implement `_candidate_embedding(candidate: dict) -> list[float] | None` reading candidate embedding/vector data from candidate payloads when available in `raa/nodes/overlap_bridging.py`
- [X] T028 [US1] Implement `_bridge_score(candidate: dict, left_centroid: list[float], right_centroid: list[float]) -> float` using dual-centroid multiplicative similarity in `raa/nodes/overlap_bridging.py`
- [X] T029 [US1] Implement `_select_bridge_requirements(left: dict, right: dict) -> list[dict]` sorting candidates by bridge score and enforcing `MAX_BRIDGE_REQUIREMENTS = 3` in `raa/nodes/overlap_bridging.py`
- [X] T030 [US1] Implement `_requirement_id(requirement: dict) -> str` normalizing bridge requirement IDs to strings in `raa/nodes/overlap_bridging.py`
- [X] T031 [US1] Implement `_inject_bridge_requirements(batch: dict, bridges: list[dict], pair_scores: dict[str, float]) -> dict` that appends missing bridge payloads to `requirements`, `requirement_ids`, and `similarity_scores` in `raa/nodes/overlap_bridging.py`
- [X] T032 [US1] Implement `_bridge_pair_key(left: dict, right: dict) -> tuple` using the adjacent batch group IDs in stable sorted order in `raa/nodes/overlap_bridging.py`
- [X] T033 [US1] Implement `apply_overlap_bridging(state: RAAState) -> dict` that updates both batches in `batch_queue` and writes `bridge_requirements[pair] = [req_ids]` in `raa/nodes/overlap_bridging.py`
- [X] T034 [US1] Ensure `apply_overlap_bridging` returns `{"batch_queue": updated_batches, "bridge_requirements": bridge_requirements}` even when no adjacent pairs are found in `raa/nodes/overlap_bridging.py`
- [X] T035 [US1] Export `apply_overlap_bridging` from `raa/nodes/__init__.py`

**Checkpoint**: Overlap bridging is independently callable after batch construction and writes updated batches plus bridge mappings.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate Section 9 behavior and keep implementation limited to overlap bridging.

- [X] T036 [P] Run `pytest tests/raa/test_overlap_bridging.py`
- [X] T037 [P] Run Python syntax validation for `raa/nodes/overlap_bridging.py` and `raa/nodes/__init__.py`
- [X] T038 Confirm `raa/nodes/overlap_bridging.py` enforces the hard cap of 3 bridge requirements per adjacent pair
- [X] T039 Confirm `raa/nodes/overlap_bridging.py` records bridge mappings in the `bridge_requirements` state channel and does not create a new state channel
- [X] T040 Confirm `raa/nodes/overlap_bridging.py` injects selected bridge payloads into both adjacent batches rather than only recording IDs
- [X] T041 Confirm `raa/nodes/overlap_bridging.py` does not implement coherence gating, batch queue ordering, RAA subgraphs, judge behavior, or final merge behavior

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

- Write tests T011-T020 before implementation tasks T021-T035.
- Implement similarity and adjacency helpers before bridge selection.
- Implement bridge selection before batch injection and state-channel output.
- Export `apply_overlap_bridging` only after implementation exists.

### Parallel Opportunities

- T001 through T004 can run in parallel.
- T011 through T020 can be drafted in parallel only if edits to `tests/raa/test_overlap_bridging.py` are coordinated.
- T021 through T035 should run mostly sequentially because they build one module.
- T036 and T037 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a unit test verifying batches are adjacent when their cluster IDs match in tests/raa/test_overlap_bridging.py"
Task: "Add a unit test verifying selected bridge requirements are limited to a hard cap of 3 per adjacent pair in tests/raa/test_overlap_bridging.py"
Task: "Add a unit test verifying selected bridge requirement payloads are injected into both adjacent batches in tests/raa/test_overlap_bridging.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write tests for adjacency detection, dual-centroid scoring, hard cap, injection, and bridge registry output.
3. Implement `raa/nodes/overlap_bridging.py`.
4. Run the overlap bridging unit tests.

### Incremental Delivery

1. Align docs and state contract with Section 9 and requested module name.
2. Implement adjacency detection by cluster or centroid similarity.
3. Implement dual-centroid bridge scoring and hard-capped selection.
4. Inject bridges into both batches and record `bridge_requirements`.
5. Validate no downstream phases were introduced.

### Notes

- This feature assumes batch construction already produced batch payloads with centroids and full normalized requirement payloads.
- Select zero bridges when no candidates qualify; the 1-3 range applies only when qualifying candidates exist.
- Do not implement coherence scoring or queue ordering in this feature.
