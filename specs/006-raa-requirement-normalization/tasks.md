# Tasks: RAA Requirement Normalization

**Input**: Design documents from `specs/006-raa-requirement-normalization/`
**Source Scope**: `RAA_Plan.md` Section 5 only
**Tests**: Included because the user request and feature specification explicitly require unit tests for ASR and non-ASR output schemas.

**Organization**: Tasks are grouped around the single independently testable normalization story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the runtime package and test paths exist before adding the first RAA runtime node.

- [ ] T001 [P] Confirm the RAA nodes package exists at `raa/nodes/`
- [ ] T002 [P] Confirm the RAA state package exists at `raa/state/`
- [ ] T003 [P] Confirm the RAA test package exists at `tests/raa/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define the data contract and state inputs needed by the normalization node.

- [ ] T004 Add `UnifiedRequirement` TypedDict with fields `id`, `text`, `is_asr`, `quality_attributes`, and `condition_text` in `raa/state/types.py`
- [ ] T005 Export `UnifiedRequirement` from `raa/state/__init__.py`
- [ ] T006 Add or confirm the parent `requirements: dict[str, str]` channel exists in `RAAState` in `raa/state/channels.py`
- [ ] T007 Confirm `RAAState.asrs` and `RAAState.non_asr` can hold normalized `list[UnifiedRequirement]` payloads after the normalization node in `raa/state/channels.py`

**Checkpoint**: The normalized requirement schema and required state channels are defined before node implementation.

---

## Phase 3: User Story 1 - Normalize ARLO Output Into Unified Requirement Schema (Priority: P1) MVP

**Goal**: Convert ARLO ASR and non-ASR dictionaries into the unified schema used by downstream RAA nodes.

**Independent Test**: Run the normalization unit tests and confirm ASR and non-ASR inputs both produce dictionaries with exactly `id`, `text`, `is_asr`, `quality_attributes`, and `condition_text`.

### Tests for User Story 1

- [ ] T008 [P] [US1] Create `tests/raa/test_requirement_normalization.py` with a passing ASR fixture containing integer `id`, `is_architecturally_significant`, `quality_attributes`, and `condition_text`
- [ ] T009 [P] [US1] Add a unit test in `tests/raa/test_requirement_normalization.py` verifying ASR `id=1` maps to `"R1"` and resolves `text` from the parent `requirements` dict
- [ ] T010 [P] [US1] Add a unit test in `tests/raa/test_requirement_normalization.py` verifying `is_architecturally_significant` is renamed to `is_asr` for ASR inputs
- [ ] T011 [P] [US1] Add a unit test in `tests/raa/test_requirement_normalization.py` verifying non-ASR input without `condition_text` defaults `condition_text` to `None`
- [ ] T012 [P] [US1] Add a unit test in `tests/raa/test_requirement_normalization.py` verifying non-ASR input without `quality_attributes` defaults `quality_attributes` to `[]`
- [ ] T013 [P] [US1] Add a unit test in `tests/raa/test_requirement_normalization.py` verifying auxiliary ARLO fields are discarded from normalized output
- [ ] T014 [P] [US1] Add a unit test in `tests/raa/test_requirement_normalization.py` verifying missing parent requirement key raises `KeyError`
- [ ] T015 [P] [US1] Add a node-level unit test in `tests/raa/test_requirement_normalization.py` verifying the normalization node returns normalized `asrs` and `non_asr` lists in the state update

### Implementation for User Story 1

- [ ] T016 [US1] Implement `_requirement_key(raw_id: int) -> str` mapping integer ARLO IDs to string keys like `"R1"` in `raa/nodes/normalization.py`
- [ ] T017 [US1] Implement `_resolve_text(requirement_key: str, requirements: dict[str, str]) -> str` that raises a descriptive `KeyError` for missing keys in `raa/nodes/normalization.py`
- [ ] T018 [US1] Implement `normalize_requirement(raw: dict, requirements: dict[str, str]) -> UnifiedRequirement` with exact output keys in `raa/nodes/normalization.py`
- [ ] T019 [US1] Implement the `is_architecturally_significant` to `is_asr` rename in `normalize_requirement` in `raa/nodes/normalization.py`
- [ ] T020 [US1] Implement `condition_text` defaulting to `None` for raw non-ASR dictionaries without conditions in `raa/nodes/normalization.py`
- [ ] T021 [US1] Implement `quality_attributes` defaulting to `[]` for raw dictionaries without QA classifications in `raa/nodes/normalization.py`
- [ ] T022 [US1] Ensure `normalize_requirement` discards auxiliary fields and returns only `id`, `text`, `is_asr`, `quality_attributes`, and `condition_text` in `raa/nodes/normalization.py`
- [ ] T023 [US1] Implement `normalize_requirements(items: list[dict], requirements: dict[str, str]) -> list[UnifiedRequirement]` in `raa/nodes/normalization.py`
- [ ] T024 [US1] Implement the LangGraph node function `normalize_requirement_state(state: RAAState) -> dict` returning normalized `asrs` and `non_asr` lists in `raa/nodes/normalization.py`
- [ ] T025 [US1] Export normalization helpers from `raa/nodes/__init__.py`

**Checkpoint**: The normalization node can be called independently and produces the exact unified schema for ASR and non-ASR inputs.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate the node and keep the implementation scoped to Section 5.

- [ ] T026 [P] Run `pytest tests/raa/test_requirement_normalization.py`
- [ ] T027 [P] Run Python syntax validation for `raa/nodes/normalization.py`, `raa/state/types.py`, `raa/state/channels.py`, and `raa/state/__init__.py`
- [ ] T028 Confirm the normalization implementation does not perform embeddings, SQLite access, batch construction, or prompt loading in `raa/nodes/normalization.py`
- [ ] T029 Confirm normalized requirement dictionaries use string IDs from the parent `requirements` dict key format and never retain raw integer IDs in `tests/raa/test_requirement_normalization.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks node implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational schema and state-channel tasks.
- **Polish (Final Phase)**: Depends on User Story 1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 and has no dependency on other stories.

### Within User Story 1

- Write tests T008-T015 before implementation tasks T016-T025.
- Implement helper functions before the LangGraph node function.
- Export node helpers only after implementation exists.

### Parallel Opportunities

- T001 through T003 can run in parallel.
- T008 through T015 can be drafted in parallel because they all target the same test file only if coordinated carefully; otherwise write them sequentially to avoid merge conflicts.
- T016 through T023 should run sequentially because they build on one another in `raa/nodes/normalization.py`.
- T026 and T027 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a unit test verifying non-ASR input without condition_text defaults condition_text to None in tests/raa/test_requirement_normalization.py"
Task: "Add a unit test verifying non-ASR input without quality_attributes defaults quality_attributes to [] in tests/raa/test_requirement_normalization.py"
Task: "Add a unit test verifying missing parent requirement key raises KeyError in tests/raa/test_requirement_normalization.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write the normalization tests for ASR and non-ASR inputs.
3. Implement `raa/nodes/normalization.py`.
4. Run the normalization unit tests and syntax validation.

### Incremental Delivery

1. Establish the unified requirement type and state input channel.
2. Add unit tests for all Section 5 transform rules.
3. Implement helpers and the LangGraph node.
4. Validate no out-of-scope behavior was introduced.

### Notes

- Keep this feature limited to normalization only.
- Do not implement preparation, embedding, SQLite persistence, batch construction, or graph wiring here.
- Missing requirement text must fail fast with `KeyError`; never default to empty text.
