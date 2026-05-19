# Tasks: RAA Per-Batch Judge Node

**Input**: Design documents from `/specs/016-raa-judge-node/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `RAA_Plan.md` Section 13

**Tests**: Required by the feature specification independent test and implementation plan. Write the listed pytest coverage before implementation and confirm the current code fails because `raa/nodes/judge.py` is not implemented.

**Organization**: Tasks are grouped by the single P1 user story so the Judge node can be implemented and verified as one independently testable MVP.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel after dependencies are satisfied because it touches different files
- **[Story]**: User story label from `spec.md`
- All task descriptions include exact repository file paths

## Phase 1: Setup

**Purpose**: Confirm the Section 13 behavior and the existing state/type contracts before adding the Judge node.

- [x] T001 Review `RAA_Plan.md` Section 13 and the existing state contracts in `raa/state/types.py` and `raa/state/channels.py`
- [x] T002 Review runtime context access in `raa/graphs/subgraphs/routing.py` and relationship scope rules in `raa/graphs/subgraphs/common.py`

---

## Phase 2: Foundational

**Purpose**: Establish the Judge node API, test fixtures, and internal score contract used by the user story.

- [x] T003 Create `raa/nodes/judge.py` with a public `judge_batch(state, config=None)` node stub, `LLM_JUDGE_KEY = "llm_judge"`, and module-level helper placeholders for scoring, merge, residual scan, tree assembly, and state output
- [x] T004 [P] Create shared `ArchFragment`, `ArchModel`, fake batch, fake score response, and fake `llm_judge` fixtures in `tests/raa/test_judge.py`
- [x] T005 Define a module-local `JudgeScore` typed structure in `raa/nodes/judge.py` containing `source_fragment`, `base_score`, `weighted_score`, `covered_entity_ids`, `covered_relationship_keys`, and `reduced_confidence`

**Checkpoint**: The implementation has one public node callable, test fixtures can construct three strategy fragments, and score metadata is explicit without adding new state channels.

---

## Phase 3: User Story 1 - Evaluate Parallel Subgraphs and Merge Architectural Outputs (Priority: P1) MVP

**Goal**: Use `llm_judge` from runtime context for SAAM scoring and LLM-only conflict/gap analysis, then deterministically select, deduplicate, residual-scan, assemble, and commit the merged batch output.

**Independent Test**: Run `pytest tests/raa/test_judge.py` with three mock `ArchFragment` outputs that include duplicates, hierarchy conflicts, scope conflicts, residual coverage, orphan entities, and a reduced-confidence batch; verify `best_batch_output`, `running_arch_model`, `open_questions`, and `batch_cursor` updates.

### Tests for User Story 1

- [x] T006 [US1] Add tests that `judge_batch` in `raa/nodes/judge.py` reads `llm_judge` from `config["context"]`, raises a clear error when missing, and never reads an LLM object from state in `tests/raa/test_judge.py`
- [x] T007 [US1] Add tests that SAAM scenario scoring invokes fake `llm_judge.invoke(...)` with batch requirements, quality weights, and all candidate fragment summaries in `tests/raa/test_judge.py`
- [x] T008 [US1] Add tests that a batch with `reduced_confidence = True` applies a `0.5` multiplier to every `JudgeScore.weighted_score` in `tests/raa/test_judge.py`
- [x] T009 [US1] Add tests that primary selection chooses the fragment with the highest weighted SAAM score and records deterministic tie behavior in `tests/raa/test_judge.py`
- [x] T010 [US1] Add tests that entity deduplication merges identical IDs per entity type, keeps the longest description, retains available technology, and keeps canonical IDs normalized in `tests/raa/test_judge.py`
- [x] T011 [US1] Add tests that duplicate containers with conflicting `parent_system_id` values and duplicate components with conflicting `parent_container_id` values append `OpenQuestion(type="hierarchy_conflict", ...)` in `tests/raa/test_judge.py`
- [x] T012 [US1] Add tests that relationship deduplication uses key `(source_id, target_id, interaction_type)`, prefers the higher-scored fragment for conflicting descriptions, and appends `OpenQuestion(type="scope_conflict", ...)` for diagram-scope mismatches in `tests/raa/test_judge.py`
- [x] T013 [US1] Add tests that scope-conflict resolution chooses the endpoint-consistent `diagram_scope` using the Section 12 scope rules in `tests/raa/test_judge.py`
- [x] T014 [US1] Add tests that the residual scan carries forward non-selected entities and relationships only when their ID/key appears in positive SAAM coverage metadata in `tests/raa/test_judge.py`
- [x] T015 [US1] Add tests that residual orphan containers and components are rejected and append `OpenQuestion(type="coverage_gap", ...)` with the missing parent ID in `tests/raa/test_judge.py`
- [x] T016 [US1] Add tests that tree assembly nests containers under systems, components under containers, and distributes context/container/component relationships onto the correct dataclass relationship lists in `tests/raa/test_judge.py`
- [x] T017 [US1] Add tests that consistency checking against an existing `running_arch_model` records `hierarchy_conflict` or `scope_conflict` without corrupting the existing tree in `tests/raa/test_judge.py`
- [x] T018 [US1] Add tests that the node output writes `best_batch_output[batch_index]`, updates `running_arch_model`, appends `open_questions`, and returns `batch_cursor = batch_index + 1` in `tests/raa/test_judge.py`
- [x] T019 [US1] Add tests that `judge_batch` output excludes `llm_judge`, `llm`, and any object with an `.invoke` attribute from returned state updates in `tests/raa/test_judge.py`

### Implementation for User Story 1

- [x] T020 [US1] Implement `_context_dict(config)`, `_require_llm_judge(context)`, `_invoke_llm(llm, prompt)`, and `_response_to_dict(raw_response)` in `raa/nodes/judge.py`
- [x] T021 [US1] Implement SAAM scoring prompt assembly and response parsing in `raa/nodes/judge.py`, requiring scores plus positive coverage metadata for entity IDs and relationship keys
- [x] T022 [US1] Implement reduced-confidence score weighting in `raa/nodes/judge.py` so `weighted_score = base_score * 0.5` for reduced-confidence batches and `base_score` otherwise
- [x] T023 [US1] Implement deterministic canonical ID and relationship-key normalization helpers in `raa/nodes/judge.py`
- [x] T024 [US1] Implement deterministic primary-fragment selection by `weighted_score` with a stable source-fragment tie break in `raa/nodes/judge.py`
- [x] T025 [US1] Implement entity deduplication per type in `raa/nodes/judge.py` for systems, containers, components, persons, and external systems
- [x] T026 [US1] Implement hierarchy conflict detection in `raa/nodes/judge.py` for mismatched `parent_system_id` and `parent_container_id` values and create `OpenQuestion(type="hierarchy_conflict", ...)` records using the existing dataclass fields
- [x] T027 [US1] Implement relationship deduplication in `raa/nodes/judge.py` using `(source_id, target_id, interaction_type)` and higher `weighted_score` for conflicting descriptions
- [x] T028 [US1] Implement endpoint type indexing and expected-scope resolution in `raa/nodes/judge.py`, reusing the Section 12 scope constants from `raa/graphs/subgraphs/common.py` where practical
- [x] T029 [US1] Implement scope conflict recording in `raa/nodes/judge.py` as `OpenQuestion(type="scope_conflict", ...)` while selecting the endpoint-consistent relationship `diagram_scope`
- [x] T030 [US1] Implement residual scan and coverage union in `raa/nodes/judge.py` so losing-fragment entities and relationships are considered only when present in positive SAAM coverage metadata
- [x] T031 [US1] Implement orphan prevention in `raa/nodes/judge.py` so residual containers require a resolvable parent system and residual components require a resolvable parent container in the merged output, same union pass, or existing `running_arch_model`
- [x] T032 [US1] Implement coverage gap recording in `raa/nodes/judge.py` as `OpenQuestion(type="coverage_gap", ...)` for every rejected orphan container, orphan component, or unresolved covered relationship endpoint
- [x] T033 [US1] Implement LLM-backed conflict reconciliation and gap-analysis description helpers in `raa/nodes/judge.py` that call `llm_judge` only to phrase descriptions, never to choose merged entities or tree structure
- [x] T034 [US1] Implement deterministic tree assembly in `raa/nodes/judge.py` that builds an `ArchFragment` contribution with nested `ArchSystem.containers`, nested `ArchContainer.components`, and relationships assigned to `context_relationships`, `container_relationships`, or `component_relationships`
- [x] T035 [US1] Implement deterministic update of `running_arch_model` in `raa/nodes/judge.py` by merging the assembled batch contribution into the existing `ArchModel` without duplicating entities or overwriting unrelated existing branches
- [x] T036 [US1] Implement `judge_batch(state, config=None)` orchestration in `raa/nodes/judge.py` to read `batch_outputs[batch_cursor]`, score fragments, select primary, merge residuals, assemble tree, update `best_batch_output`, update `running_arch_model`, append `open_questions`, and advance `batch_cursor`
- [x] T037 [P] [US1] Export `judge_batch` from `raa/nodes/__init__.py`
- [x] T038 [US1] Run `pytest tests/raa/test_judge.py` and fix failures in `raa/nodes/judge.py`, `raa/nodes/__init__.py`, and `tests/raa/test_judge.py`

**Checkpoint**: User Story 1 is complete when `judge_batch` deterministically merges the current batch, records all required open question types, updates the running architecture tree, and advances the cursor without returning any LLM object.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Verify the Judge node does not regress existing RAA state behavior or graph constraints.

- [x] T039 Run `pytest tests/raa/test_judge.py tests/raa/test_main_graph.py tests/raa/test_parallel_subgraphs.py` and fix feature-caused regressions in `raa/nodes/judge.py`, `raa/state/channels.py`, and `raa/graphs/subgraphs/common.py`
- [x] T040 Confirm `raa/nodes/judge.py` contains no LLM calls inside entity deduplication, relationship deduplication, residual union, orphan prevention, or tree assembly helpers
- [x] T041 Confirm `raa/nodes/judge.py` records only `OpenQuestion(type="hierarchy_conflict")`, `OpenQuestion(type="scope_conflict")`, and `OpenQuestion(type="coverage_gap")` for Section 13 merge issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on T001-T002 and blocks User Story 1 implementation
- **User Story 1 (Phase 3)**: Depends on T003-T005
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational phase completion and is the MVP scope

### Within User Story 1

- Tests T006-T019 must be written before implementation tasks T020-T037
- LLM context and scoring helpers T020-T022 must complete before primary selection T024 and residual coverage filtering T030
- Canonical helpers T023 must complete before deduplication T025, relationship merging T027, and tree assembly T034
- Conflict and gap constructors T026, T029, T032, and T033 must complete before `judge_batch` orchestration T036
- Tree assembly T034 and running model update T035 must complete before decision output T036
- T038 validates User Story 1 before broader regression checks T039-T041

### Parallel Opportunities

- T003 and T004 can be done in parallel after T001-T002 because they touch `raa/nodes/judge.py` and `tests/raa/test_judge.py`
- T037 can be done in parallel with final test cleanup after T036 because it only touches `raa/nodes/__init__.py`
- T040 and T041 can be reviewed in parallel after T039 because they inspect different Section 13 constraints

---

## Parallel Example: User Story 1

```bash
# After T001-T002:
Task: "Create raa/nodes/judge.py skeleton with judge_batch and helper placeholders"
Task: "Create tests/raa/test_judge.py fixtures for candidate fragments and fake llm_judge"

# After T036:
Task: "Export judge_batch from raa/nodes/__init__.py"
Task: "Run focused pytest tests/raa/test_judge.py and fix failures"
```

---

## Implementation Strategy

### MVP First

1. Complete T001-T005 to lock the Section 13 API and fixture contract.
2. Write failing tests T006-T019.
3. Implement LLM-scoped scoring and description helpers T020-T022 and T033.
4. Implement deterministic merge helpers T023-T032 and tree updates T034-T035.
5. Implement orchestration and export T036-T037.
6. Validate with T038.

### Incremental Delivery

1. Make scoring and primary selection work with mocked `llm_judge`.
2. Add deterministic entity and relationship deduplication.
3. Add residual scan with orphan prevention and coverage gaps.
4. Add tree assembly and running model merge.
5. Add final state output and cursor advancement.

### Suggested MVP Scope

Complete User Story 1 only. There are no lower-priority stories in this feature.
