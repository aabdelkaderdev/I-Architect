# Tasks: RAA State Contracts

**Input**: `RAA_Plan.md` Section 4, `spec.md`, `data-model.md`, `contracts/`
**Feature Directory**: `specs/002-raa-subgraph/`
**Scope**: Implement all dataclasses, TypedDict channels with correct reducers, and JsonPlusSerializer-compatible serialization in `raa/state/`

**Status**: All 30 tasks complete. US1/US2 (ARLO compatibility) done in prior run. US3/US4/US5 (RAA state contracts) done this run.

---

## Phase 1: Setup (RAA State Package)

**Purpose**: Create the `raa/state/` package directory and PEP 561 marker.

- [X] T001 Create `raa/state/` package directory with `raa/state/__init__.py`
- [X] T002 [P] Create `raa/py.typed` PEP 561 marker file (empty marker for type checkers)

---

## Phase 2: User Story 1 — RAA-Compatible ARLOOutput Payload (P1) ✓ COMPLETED

**Goal**: Downstream consumers receive `asrs`, `non_asr`, `condition_groups`, and `quality_weights` from ARLO with `non_asr` shaped as full requirement dictionaries.

**Status**: Implemented. Included for complete feature traceability.

- [X] T003 [US1] Update `ARLOOutput.non_asr` from `list[str]` to `list[dict]` in `arlo/state/schemas.py`
- [X] T004 [US1] Update `ARLOState.non_asr` from `list[str]` to `list[dict]` in `arlo/state/schemas.py`
- [X] T005 [US1] Change `parse_requirements` to return full non-ASR dictionaries in `arlo/nodes/parsing.py`
- [X] T006 [US1] Verify `create_arlo_wrapper` forwards `non_asr` and `condition_groups` directly in `arlo/pipeline_wrapper.py`

---

## Phase 3: User Story 2 — ASR Embedding SQLite Persistence (P1) ✓ COMPLETED

**Goal**: ARLO persists ASR condition embeddings to `embeddings/asr_embeddings.db` while preserving the existing `{"embeddings": embeddings}` state write for internal clustering.

**Status**: Implemented. Included for complete feature traceability.

- [X] T007 [US2] Add `json`, `sqlite3` imports and project-root path helpers in `arlo/nodes/embedding.py`
- [X] T008 [US2] Create `asr_embeddings` table keyed by `requirement_id TEXT PRIMARY KEY` in `embeddings/asr_embeddings.db` from `arlo/nodes/embedding.py`
- [X] T009 [US2] Upsert each ASR requirement ID + embedding vector as JSON blob after FastEmbed generation in `arlo/nodes/embedding.py`
- [X] T010 [US2] Preserve existing LangGraph state return `{"embeddings": embeddings}` after SQLite persistence in `arlo/nodes/embedding.py`

**Checkpoint**: ARLO output boundary and embedding persistence are RAA-ready.

---

## Phase 4: User Story 3 — Type-Safe Graph State Structure (Priority: P1)

**Goal**: Define all Python dataclasses and TypedDicts matching `RAA_Plan.md` Section 4 type definitions so graph state channels can be populated and inspected with full type safety.

**Independent Test**: Instantiate every dataclass with valid field values and assert no type errors. Inspect `RAAState` TypedDict keys and verify all 9 state channels from Section 4 are present with correct types.

### Implementation for User Story 3

- [X] T011 [US3] Define leaf/simple dataclasses in `raa/state/types.py`: `ArchPattern`, `OpenQuestion`, `IncoherentBatchRecord`, `ConfidenceRecord`. Use `@dataclass` with `from __future__ import annotations` for forward-reference support. All fields must be JSON-primitive types (`str`, `int`, `float`, `bool`, `list`, `dict`, `str | None`, `float | None`).
- [X] T012 [US3] Define actor dataclasses in `raa/state/types.py`: `ArchPerson`, `ArchExternalSystem`. Flat leaf entities — no nested children. Include field `source_fragment: str | None` and `confidence: float | None`.
- [X] T013 [US3] Define `ArchRelationship` dataclass in `raa/state/types.py` with fields: `source_id`, `target_id`, `interaction_type`, `technology`, `requirement_ids`, `source_fragment`, `diagram_scope`. `diagram_scope` accepts `"context"`, `"container"`, or `"component"`.
- [X] T014 [US3] Define C4 hierarchy dataclasses in `raa/state/types.py`: `ArchComponent` (with `parent_container_id`, `component_relationships`), `ArchContainer` (with `parent_system_id`, `container_relationships`, `components`), `ArchSystem` (with `context_relationships`, `containers`). Use forward references via `from __future__ import annotations`.
- [X] T015 [US3] Define aggregate dataclasses in `raa/state/types.py`: `ArchFragment` (semi-flat with `systems`, `containers`, `components`, `persons`, `external_systems`, `relationships`, `patterns`, `rationale`), `ArchModel` (hierarchical with `systems`, `persons`, `external_systems`, `patterns`, `open_questions`).
- [X] T016 [US3] Define `Batch` TypedDict and `DiagramManifestEntry` dataclass in `raa/state/types.py`. `Batch`: `batch_id: int`, `group_id: int`, `requirement_ids: list[str]`, `group_centroid: list[float] | None`, `reduced_confidence: bool`. `DiagramManifestEntry`: `diagram_id`, `diagram_type`, `focus_entity_id`, `label` (per `contracts/arch_model_schema.json`).
- [X] T017 [US3] Create `raa/state/__init__.py` with public API exports: all dataclass names, `Batch`, `DiagramManifestEntry`. Re-export `RAAState` from `.channels` once T019 is complete.
- [X] T018 [P] [US3] Create unit tests in `tests/raa/test_state_types.py`: instantiate every dataclass with valid field values, verify field types match, verify nested structures (system→containers→components), verify `from __future__ import annotations` resolves all forward references.

**Checkpoint**: All 14 type definitions from Section 4 + Batch + DiagramManifestEntry are importable and type-safe.

---

## Phase 5: User Story 4 — State Channel Reducers for Parallel Execution (Priority: P2)

**Goal**: Configure LangGraph `Annotated` reducers on multi-writer state channels so concurrent writes from parallel RAA subgraphs merge correctly instead of last-write-wins.

**Independent Test**: Write to `batch_outputs` and `open_questions` from simulated concurrent sources; verify data merges (not overwrites). Write to `batch_cursor` from two sources; verify overwrite behavior (single-writer channel).

### Implementation for User Story 4

- [X] T019 [US4] Define `RAAState` TypedDict in `raa/state/channels.py` with all 9 channels from `RAA_Plan.md` Section 4 New State Channels table plus reused ARLO channels (`asrs`, `non_asr`, `condition_groups`, `quality_weights`). Multi-writer channels use `Annotated[type, reducer]`:
  - `batch_outputs: Annotated[dict[int, list[ArchFragment]], merge_batch_outputs]`
  - `best_batch_output: Annotated[dict[int, ArchFragment], merge_best_batch_output]`
  - `open_questions: Annotated[list[OpenQuestion], add]`
  - `incoherent_batches: Annotated[list[IncoherentBatchRecord], add]`
  - Single-writer channels use plain types (default overwrite): `batch_queue`, `batch_cursor`, `running_arch_model`, `bridge_requirements`, `embeddings_ready`.
- [X] T020 [US4] Implement `merge_batch_outputs` reducer in `raa/state/channels.py`: dict-merge that appends list values per key. When key exists in both left and right dicts, concatenate their lists. When key exists in only one, copy it.
- [X] T021 [US4] Implement `merge_best_batch_output` reducer in `raa/state/channels.py`: dict-merge for `dict[int, ArchFragment]`. When same batch index key exists in both, prefer the one with higher SAAM confidence (keep the one with more entities/relationships). Log a warning on key collision.
- [X] T022 [US4] Update `raa/state/__init__.py` to re-export `RAAState`, `merge_batch_outputs`, and `merge_best_batch_output`.
- [X] T023 [P] [US4] Create unit tests in `tests/raa/test_state_reducers.py`:
  - Test `merge_batch_outputs`: two dicts with same key → lists concatenated.
  - Test `merge_batch_outputs`: disjoint keys → merged dict with both keys.
  - Test `merge_best_batch_output`: same key → higher-confidence fragment kept.
  - Test `operator.add` on `open_questions`: two lists → concatenated.
  - Test default overwrite on `batch_cursor`: two writes → last value retained.

**Checkpoint**: All multi-writer channels use correct reducers. Parallel subgraph outputs merge without data loss.

---

## Phase 6: User Story 5 — JsonPlusSerializer-Compatible Serialization (Priority: P3)

**Goal**: All custom dataclasses survive a full `JsonPlusSerializer` round-trip (serialize → deserialize) without data loss, enabling SQLite checkpointing without custom codecs.

**Independent Test**: Create an `ArchModel` with deeply nested systems, containers, components, and relationships. Serialize via `JsonPlusSerializer.dumps()`, deserialize via `JsonPlusSerializer.loads()`. Assert structural identity (same hierarchy, same field values).

### Implementation for User Story 5

- [X] T024 [US5] Create `raa/state/serialization.py` with helper functions:
  - `dataclass_to_dict(obj) -> dict`: recursively convert any dataclass to plain dict using `dataclasses.asdict()` with `dict_factory=dict`.
  - `dict_to_dataclass(data: dict, target_type: type)` : recursively reconstruct dataclass from dict, handling nested `list[SomeDataclass]` fields by inspecting `__annotations__`.
  - `to_json(obj) -> str`: `json.dumps(dataclass_to_dict(obj))`.
  - `from_json(json_str: str, target_type: type)`: `dict_to_dataclass(json.loads(json_str), target_type)`.
- [X] T025 [US5] Add a `__post_init__` or validation helper in `raa/state/serialization.py` that verifies no non-serializable types exist in any dataclass field (reject `Callable`, `ModuleType`, raw `object`). Raise `TypeError` with field path on failure.
- [X] T026 [P] [US5] Create unit tests in `tests/raa/test_state_serialization.py`:
  - Round-trip `ArchModel` with 2 systems, 3 containers, 4 components, 2 persons, 5 relationships → assert structural equality.
  - Round-trip `ArchFragment` with all fields populated including `rationale: dict[str, object]` with JSON-safe values.
  - Round-trip `OpenQuestion`, `IncoherentBatchRecord`, `ConfidenceRecord` individually.
  - Test `TypeError` raised when a non-serializable type (e.g. `object()` not dict-safe) appears in a field.
  - Verify serialized output is valid JSON parseable by `json.loads()`.

**Checkpoint**: All RAA state is checkpointable via LangGraph's default `JsonPlusSerializer`.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validate type correctness, contract compliance, and quickstart examples.

- [X] T027 [P] Run Python syntax validation on all `raa/state/` files: `python3 -m py_compile raa/state/types.py raa/state/channels.py raa/state/serialization.py`
- [X] T028 [P] Run mypy static type check on `raa/state/` (if mypy available): `mypy raa/state/ --strict` or equivalent. Fix all type errors.
- [X] T029 Verify `quickstart.md` examples execute correctly: import dataclasses, instantiate `ArchSystem`, create `RAAState` dict, invoke `merge_batch_outputs`.
- [X] T030 Verify JSON schema contract compliance: serialized `ArchModel` output validates against `contracts/arch_model_schema.json`. Every required field present, every `diagram_scope` value in `["context", "container", "component"]`, every `type` field in `OpenQuestion` matches the enum.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **US1 (Phase 2)**: Already complete. Marked for reference.
- **US2 (Phase 3)**: Already complete. Marked for reference.
- **US3 (Phase 4)**: Depends on Phase 1 (package exists). Core dataclasses in `types.py`.
- **US4 (Phase 5)**: Depends on US3 (needs dataclass types for TypedDict annotations and reducer signatures).
- **US5 (Phase 6)**: Depends on US3 (needs dataclasses for round-trip tests). Can run in parallel with US4.
- **Polish (Phase 7)**: Depends on US3, US4, US5.

### User Story Dependencies

- **US3 (P1)**: Can start after Setup. No dependency on US1/US2 (different files).
- **US4 (P2)**: Depends on US3. No dependency on US5.
- **US5 (P3)**: Depends on US3. No dependency on US4.

### Within Each User Story

- Dataclass tasks T011–T015 all write to same file (`raa/state/types.py`). Execute sequentially.
- T016 (Batch + DiagramManifestEntry) can run in parallel with T017 (__init__.py).
- T018 (tests) runs after all dataclasses are defined.
- T019–T021 all write to `raa/state/channels.py`. Execute sequentially.
- T022 (update __init__.py) depends on T019–T021.
- T023 (reducer tests) runs after T019–T022.
- T024–T025 both write to `raa/state/serialization.py`. Execute sequentially.
- T026 (serialization tests) runs after T024–T025.

### Parallel Opportunities

- T002 can run in parallel with T001.
- US5 (Phase 6) can run in parallel with US4 (Phase 5) — different files, no shared dependencies beyond US3 dataclasses.
- T027, T028, T029, T030 can run in parallel within Polish phase.
- T018 (US3 tests), T023 (US4 tests), T026 (US5 tests) can each run in parallel once their respective implementation is complete.

---

## Parallel Example: US4 + US5 Concurrent Implementation

```text
# After US3 dataclasses are complete, launch in parallel:
Task: "Define RAAState TypedDict and reducers in raa/state/channels.py"  (US4)
Task: "Create serialization helpers in raa/state/serialization.py"       (US5)
```

---

## Implementation Strategy

### MVP First (US3 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 4: US3 (all dataclasses in `types.py`).
3. Validate: instantiate all dataclasses, run T018 tests.
4. At this point, `raa/state/types.py` is consumable by downstream RAA node implementations.

### Incremental Delivery

1. Phase 1 → package exists.
2. US3 (dataclasses) → type-safe structures available.
3. US4 (reducers) → StateGraph channels configurable for parallel execution.
4. US5 (serialization) → Full checkpointing support via JsonPlusSerializer.
5. Polish → contracts validated, types clean, quickstart works.

### Notes

- All dataclasses use `@dataclass` (stdlib), not Pydantic. `JsonPlusSerializer` natively supports `@dataclass`.
- `from __future__ import annotations` at top of `types.py` enables forward references (e.g., `ArchContainer` references `ArchComponent` in `components` field, `ArchSystem` references `ArchContainer` in `containers` field).
- The `Batch` type is a TypedDict (not a dataclass) — it's a simple state container with no behavior.
- `bridge_requirements: dict[tuple, list[str]]` — tuple keys are JSON-serialized as strings by `JsonPlusSerializer`. This is acceptable because bridge requirement lookups are internal; the final JSON output to AGA does not include `bridge_requirements`.
- US1 and US2 are fully implemented in `arlo/`; no regression expected from `raa/state/` work.
- Tests directory `tests/raa/` must be created; add `__init__.py` so test discovery works.
