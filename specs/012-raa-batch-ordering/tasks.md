# Tasks: RAA Batch Queue Ordering

**Input**: Design documents from `specs/012-raa-batch-ordering/`
**Source Scope**: `RAA_Plan.md` Section 11 only
**Tests**: Included because the feature specification requires strategy ordering, metadata validation, deterministic tie-breaking, and state-channel output tests.

**Organization**: Tasks are grouped around one independently testable batch-queue ordering story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the RAA node, state, and test paths needed by batch queue ordering are present before implementation.

- [X] T001 [P] Confirm the RAA nodes package exists at `raa/nodes/`
- [X] T002 [P] Confirm the RAA state package exists at `raa/state/`
- [X] T003 [P] Confirm the RAA test package exists at `tests/raa/`
- [X] T004 [P] Confirm batch payloads expose `batch_id`, `group_id`, `requirement_ids`, `requirements`, and `quality_attributes` on requirement payloads in `raa/state/types.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature docs and state contract with Section 11 ordering metadata and the requested `batch_queue.py` node.

- [X] T005 [P] Update `specs/012-raa-batch-ordering/plan.md` to name the implementation module `raa/nodes/batch_queue.py` and test path `tests/raa/test_batch_queue.py`
- [X] T006 [P] Update `specs/012-raa-batch-ordering/quickstart.md` examples to import `order_batch_queue` from `raa.nodes.batch_queue` and use normalized `quality_attributes` lists
- [X] T007 [P] Update `specs/012-raa-batch-ordering/data-model.md` to document `sorting_metadata` on `Batch` and the `batch_ordering_strategy` pipeline parameter
- [X] T008 [P] Update `specs/012-raa-batch-ordering/contracts/readme.md` to require `risk_first`, `asr_count`, `quality_weight`, invalid-strategy fallback, sorting metadata, and `batch_queue` output
- [X] T009 Add `SortingMetadata` TypedDict and optional `sorting_metadata` field to the `Batch` TypedDict in `raa/state/types.py`
- [X] T010 Add optional `batch_ordering_strategy: str` to `RAAState` as the pipeline parameter read by queue ordering in `raa/state/channels.py`
- [X] T011 Export `SortingMetadata` from the public RAA state API in `raa/state/__init__.py`

**Checkpoint**: Feature docs and state contracts describe the Section 11 ordering input, output, and metadata before node implementation begins.

---

## Phase 3: User Story 1 - Order Batch Execution Queue By Risk Or Override Strategy (Priority: P1) MVP

**Goal**: Sort the batch execution queue using `risk_first` by default, support `asr_count` and `quality_weight` overrides, attach ordering metadata to every batch, and return the final ordered list through the `batch_queue` state channel.

**Independent Test**: Run `tests/raa/test_batch_queue.py` and confirm all three strategies order the same fixture queue correctly, every output batch has sorting metadata, invalid strategy falls back to `risk_first`, ties are deterministic, and `order_batch_queue(state)` returns `{"batch_queue": ordered_batches}`.

### Tests for User Story 1

- [X] T012 [US1] Create `tests/raa/test_batch_queue.py` with batch fixtures containing ASR and non-ASR requirement payloads, `quality_attributes`, `group_id`, `batch_id`, and a full RAA state fixture
- [X] T013 [US1] Add a unit test verifying default `risk_first` ordering puts Security and Reliability batches before Performance and Usability batches in `tests/raa/test_batch_queue.py`
- [X] T014 [US1] Add a unit test verifying `batch_ordering_strategy = "asr_count"` orders batches by descending ASR count without counting non-ASR bridge or candidate requirements in `tests/raa/test_batch_queue.py`
- [X] T015 [US1] Add a unit test verifying `batch_ordering_strategy = "quality_weight"` orders batches by descending summed `state["quality_weights"]` for ASR `quality_attributes` in `tests/raa/test_batch_queue.py`
- [X] T016 [US1] Add a unit test verifying every ordered batch contains `sorting_metadata.score`, `sorting_metadata.strategy`, and `sorting_metadata.tie_breaker` in `tests/raa/test_batch_queue.py`
- [X] T017 [US1] Add a unit test verifying tied ordering scores are resolved deterministically by lexicographical `group_id` or `batch_id` tie-breaker in `tests/raa/test_batch_queue.py`
- [X] T018 [US1] Add a unit test verifying an invalid `batch_ordering_strategy` logs a warning, uses `risk_first`, and records `strategy = "risk_first"` in metadata in `tests/raa/test_batch_queue.py`
- [X] T019 [US1] Add a node-level unit test verifying `order_batch_queue(state)` returns only `{"batch_queue": ordered_batches}` while preserving all existing batch payload fields in `tests/raa/test_batch_queue.py`
- [X] T020 [US1] Add a unit test verifying an empty input `batch_queue` returns an empty `batch_queue` without raising in `tests/raa/test_batch_queue.py`

### Implementation for User Story 1

- [X] T021 [US1] Create `raa/nodes/batch_queue.py` with constants `DEFAULT_BATCH_ORDERING_STRATEGY = "risk_first"`, `VALID_BATCH_ORDERING_STRATEGIES`, and `RISK_PRIORITY`
- [X] T022 [US1] Implement `_normalize_strategy(strategy: object) -> str` with default `risk_first`, invalid-strategy fallback, and warning logging in `raa/nodes/batch_queue.py`
- [X] T023 [US1] Implement `_requirement_id(requirement_or_id: object) -> str | None` to normalize integer IDs and string IDs like `R12` for ASR matching in `raa/nodes/batch_queue.py`
- [X] T024 [US1] Implement `_asr_id_set(asrs: list[dict]) -> set[str]` from `state["asrs"]` for distinguishing ASR payloads from non-ASR payloads in `raa/nodes/batch_queue.py`
- [X] T025 [US1] Implement `_is_asr_requirement(requirement: dict, asr_ids: set[str]) -> bool` using `is_asr`, `is_architecturally_significant`, and fallback ID membership in `raa/nodes/batch_queue.py`
- [X] T026 [US1] Implement `_quality_attributes(requirement: dict) -> list[str]` reading normalized `quality_attributes` first and singular `quality_attribute` as a compatibility fallback in `raa/nodes/batch_queue.py`
- [X] T027 [US1] Implement `_risk_first_score(batch: dict, asr_ids: set[str]) -> float` using max risk priority with Security=4, Reliability=3, Performance=2, Usability=1, and unknown attributes=0 in `raa/nodes/batch_queue.py`
- [X] T028 [US1] Implement `_asr_count_score(batch: dict, asr_ids: set[str]) -> float` counting only ASR requirements in the batch payload in `raa/nodes/batch_queue.py`
- [X] T029 [US1] Implement `_quality_weight_score(batch: dict, quality_weights: dict[str, int], asr_ids: set[str]) -> float` summing case-insensitive quality weights for ASR requirement attributes in `raa/nodes/batch_queue.py`
- [X] T030 [US1] Implement `_batch_tie_breaker(batch: dict) -> str` using `group_id` when present and falling back to `batch_id` in `raa/nodes/batch_queue.py`
- [X] T031 [US1] Implement `_calculate_ordering_score(batch: dict, strategy: str, quality_weights: dict[str, int], asr_ids: set[str]) -> float` dispatching to all three strategies in `raa/nodes/batch_queue.py`
- [X] T032 [US1] Implement `_annotate_batch(batch: dict, score: float, strategy: str, tie_breaker: str) -> dict` that returns a copied batch with `sorting_metadata` while preserving all original payload fields in `raa/nodes/batch_queue.py`
- [X] T033 [US1] Implement `_ordered_batches(batches: list[dict], strategy: str, quality_weights: dict[str, int], asr_ids: set[str]) -> list[dict]` sorting by descending score and ascending tie-breaker in `raa/nodes/batch_queue.py`
- [X] T034 [US1] Implement `order_batch_queue(state: RAAState) -> dict` reading `batch_queue`, `batch_ordering_strategy`, `quality_weights`, and `asrs`, then returning `{"batch_queue": ordered_batches}` in `raa/nodes/batch_queue.py`
- [X] T035 [US1] Export `order_batch_queue` from `raa/nodes/__init__.py`

**Checkpoint**: Batch queue ordering is independently callable after coherence gating and writes the final ordered batch list to `batch_queue`.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate Section 11 behavior and keep implementation limited to batch queue ordering.

- [X] T036 [P] Run `pytest tests/raa/test_batch_queue.py`
- [X] T037 [P] Run Python syntax validation for `raa/nodes/batch_queue.py`, `raa/nodes/__init__.py`, `raa/state/types.py`, `raa/state/channels.py`, and `raa/state/__init__.py`
- [X] T038 Confirm `raa/nodes/batch_queue.py` writes only the `batch_queue` state channel and does not create additional runtime state channels
- [X] T039 Confirm `raa/nodes/batch_queue.py` implements only Section 11 ordering and does not implement batch construction, overlap bridging, coherence gating, RAA subgraphs, judge behavior, or final merge behavior
- [X] T040 Confirm `raa/nodes/batch_queue.py` uses the exact allowed strategies `risk_first`, `asr_count`, and `quality_weight` with `risk_first` as the default
- [X] T041 Confirm the implementation uses `raa/nodes/batch_queue.py` and does not create or depend on `raa/nodes/queue_orderer.py`

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

- Write tests T012-T020 before implementation tasks T021-T035.
- Implement strategy normalization and ID helpers before score helpers.
- Implement score helpers before metadata annotation and sorting.
- Implement `order_batch_queue` after `_ordered_batches` exists.
- Export `order_batch_queue` only after implementation exists.

### Parallel Opportunities

- T001 through T004 can run in parallel.
- T005 through T008 can run in parallel because they edit different feature documents.
- T012 through T020 should run sequentially or with coordination because they edit the same test file.
- T021 through T034 should run mostly sequentially because they build one module.
- T036 and T037 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a unit test verifying default risk_first ordering puts Security and Reliability batches before Performance and Usability batches in tests/raa/test_batch_queue.py"
Task: "Add a unit test verifying batch_ordering_strategy = \"asr_count\" orders batches by descending ASR count without counting non-ASR bridge or candidate requirements in tests/raa/test_batch_queue.py"
Task: "Add a unit test verifying batch_ordering_strategy = \"quality_weight\" orders batches by descending summed state[\"quality_weights\"] for ASR quality_attributes in tests/raa/test_batch_queue.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write tests for risk-first ordering, both override strategies, sorting metadata, invalid strategy fallback, deterministic tie-breaking, and empty queues.
3. Implement `raa/nodes/batch_queue.py`.
4. Run the batch queue unit tests.

### Incremental Delivery

1. Align feature docs and state metadata with Section 11 and the requested `batch_queue.py` module.
2. Implement strategy normalization, ASR detection, and quality-attribute extraction.
3. Implement the three score strategies.
4. Annotate batches with ordering metadata and sort deterministically.
5. Return the final ordered list through the `batch_queue` state channel.

### Notes

- This feature assumes batch construction, overlap bridging, and coherence gating have already produced the input queue.
- `risk_first` is the default and must be used when the strategy parameter is missing or invalid.
- `asr_count` counts architecturally significant requirements only; it must not count non-ASR candidates or bridge payloads.
- `quality_weight` uses ARLO `quality_weights` from state and should handle quality attribute key casing deterministically.
