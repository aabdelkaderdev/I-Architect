# Tasks: ARLO RAA Compatibility Patch

**Input**: `RAA_Plan.md` Sections 1 and 1B only
**Feature Directory**: `specs/002-raa-subgraph/`
**Source Scope**: Patch ARLO output payloads, ASR embedding SQLite persistence, and shared `embeddings/` runtime storage only
**Tests**: Not generated; the request did not ask for TDD and the selected plan scope is limited to Sections 1 and 1B

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the shared runtime storage location used by ARLO and later RAA code.

- [X] T001 [P] Create the shared runtime directory at `embeddings/`
- [X] T002 [P] Ensure the repository ignore rule includes `embeddings/` in `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm the graph output boundary before changing the payload shape.

- [X] T003 Confirm all ARLO graph builders use `ARLOOutput` as the graph output schema in `arlo/graphs/core.py`, `arlo/graphs/influential.py`, and `arlo/graphs/varying.py`

**Checkpoint**: Output-schema boundary is understood; user story work can begin.

---

## Phase 3: User Story 1 - RAA-Compatible ARLOOutput Payload (Priority: P1) MVP

**Goal**: Downstream consumers receive `asrs`, `non_asr`, `condition_groups`, and `quality_weights` from ARLO with `non_asr` shaped as full requirement dictionaries.

**Independent Test**: Run ARLO through parsing and confirm `ARLOOutput["non_asr"]` is `list[dict]`, `ARLOOutput["condition_groups"]` remains `list[dict]`, and the wrapper forwards both keys unchanged.

### Implementation for User Story 1

- [X] T004 [US1] Update `ARLOOutput.non_asr` from `list[str]` to `list[dict]` in `arlo/state/schemas.py`
- [X] T005 [US1] Update `ARLOState.non_asr` from `list[str]` to `list[dict]` in `arlo/state/schemas.py`
- [X] T006 [US1] Change `parse_requirements` to return full non-ASR parsed requirement dictionaries instead of requirement IDs in `arlo/nodes/parsing.py`
- [X] T007 [US1] Verify `create_arlo_wrapper` forwards `arlo_output["non_asr"]` and `arlo_output["condition_groups"]` without payload conversion in `arlo/pipeline_wrapper.py`

**Checkpoint**: `ARLOOutput` exposes the RAA-required non-ASR and condition-group payloads.

---

## Phase 4: User Story 2 - ASR Embedding SQLite Persistence (Priority: P1)

**Goal**: ARLO persists ASR condition embeddings to `embeddings/asr_embeddings.db` while preserving the existing `{"embeddings": embeddings}` state write for internal clustering.

**Independent Test**: Run `generate_embeddings` with ASRs and confirm `embeddings/asr_embeddings.db` exists, has one SQLite row per ASR requirement ID, and the node still returns the in-memory `embeddings` list.

### Implementation for User Story 2

- [X] T008 [P] [US2] Add SQLite persistence imports and project-root path helpers in `arlo/nodes/embedding.py`
- [X] T009 [US2] Create the SQLite database and ASR embedding table keyed by requirement ID at `embeddings/asr_embeddings.db` from `arlo/nodes/embedding.py`
- [X] T010 [US2] Serialize and upsert each ASR requirement ID plus embedding vector after FastEmbed generation in `arlo/nodes/embedding.py`
- [X] T011 [US2] Preserve the existing LangGraph state return `{"embeddings": embeddings}` after SQLite persistence in `arlo/nodes/embedding.py`
- [X] T012 [US2] Log the ASR embedding SQLite write count and database path in `arlo/nodes/embedding.py`

**Checkpoint**: ARLO writes ASR embeddings for RAA without moving vectors through the downstream output state.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate the focused ARLO compatibility patch without expanding beyond Sections 1 and 1B.

- [X] T013 [P] Run Python syntax validation for the touched ARLO files in `arlo/state/schemas.py`, `arlo/nodes/parsing.py`, and `arlo/nodes/embedding.py`
- [X] T014 [P] Inspect `embeddings/asr_embeddings.db` after a local embedding run and confirm row count matches ASR count from `arlo/nodes/embedding.py`
- [X] T015 Confirm no embedding vectors were added to `ARLOOutput` or `arlo/pipeline_wrapper.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Story 1 (Phase 3)**: Depends on Foundational completion.
- **User Story 2 (Phase 4)**: Depends on Setup completion and can run after Foundational completion.
- **Polish (Final Phase)**: Depends on the implemented user stories.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2; no dependency on User Story 2.
- **User Story 2 (P1)**: Can start after Phase 1 and Phase 2; no dependency on User Story 1.

### Parallel Opportunities

- T001 and T002 can run in parallel.
- T008 can run in parallel with T004-T007 because it only touches `arlo/nodes/embedding.py`.
- US1 and US2 can be implemented in parallel after Phase 2 because they touch different ARLO files except for final validation.
- T013 and T014 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Update ARLOOutput.non_asr from list[str] to list[dict] in arlo/state/schemas.py"
Task: "Change parse_requirements to return full non-ASR parsed requirement dictionaries instead of requirement IDs in arlo/nodes/parsing.py"
```

## Parallel Example: User Story 2

```bash
Task: "Add SQLite persistence imports and project-root path helpers in arlo/nodes/embedding.py"
Task: "Ensure the repository ignore rule includes embeddings/ in .gitignore"
```

---

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete User Story 1 so downstream consumers receive `non_asr` and `condition_groups` in the required shape.
3. Validate the ARLO output payload before touching SQLite persistence.

### Incremental Delivery

1. Deliver User Story 1 and validate the output schema.
2. Deliver User Story 2 and validate SQLite persistence at `embeddings/asr_embeddings.db`.
3. Run final validation to confirm vectors remain out of `ARLOOutput`.

### Notes

- `ARLOOutput.condition_groups` is already present, but T003 and T007 keep the output boundary explicit.
- `non_asr` currently exists as requirement IDs; the required compatibility change is to expose full dictionaries.
- `embeddings/` is runtime storage and should remain ignored by Git.
