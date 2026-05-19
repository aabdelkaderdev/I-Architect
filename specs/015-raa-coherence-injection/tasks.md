# Tasks: RAA Cross-Batch Coherence Injection

**Input**: Design documents from `/specs/015-raa-coherence-injection/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `RAA_Plan.md` Section 15

**Tests**: Required by the feature specification independent test and implementation plan. Write the listed pytest tests before implementation and ensure they fail for the current flat JSON prompt behavior.

**Organization**: Tasks are grouped by the single P1 user story so the feature can be implemented and verified as one independently testable MVP.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel after dependencies are satisfied because it touches different files
- **[Story]**: User story label from `spec.md`
- All task descriptions include exact repository file paths

## Phase 1: Setup

**Purpose**: Confirm Section 15 scope and current integration points before changing behavior.

- [X] T001 Review `RAA_Plan.md` Section 15 and the current injection points in `raa/graphs/subgraphs/routing.py` and `raa/graphs/subgraphs/common.py`

---

## Phase 2: Foundational

**Purpose**: Establish the payload contract that the user story implementation will use.

- [X] T002 Add `model_constraints: str` to `SubgraphPayload` in `raa/graphs/subgraphs/common.py` while preserving `running_arch_model` for parent-link and relationship validation

**Checkpoint**: Send payloads have an explicit field for serialized prompt constraints without removing raw model state used by validators.

---

## Phase 3: User Story 1 - Inject Serialized Running Architecture Constraints (Priority: P1) MVP

**Goal**: Before each batch's RAA subgraphs run, serialize the current `running_arch_model` as a deterministic hierarchical C4 tree and include the prefixed constraint block in every subgraph Send payload.

**Independent Test**: Run targeted pytest coverage that proves empty models serialize safely, populated hierarchical models render systems -> containers -> components with relationships and external entities, and all normal `fan_out_subgraphs` Sends include the exact prefixed constraint text before prompt assembly.

### Tests for User Story 1

- [X] T003 [US1] Add empty-model serializer tests for `None` and empty dict inputs in `tests/raa/test_model_serialiser.py`
- [X] T004 [US1] Add deterministic nested tree tests for unsorted dict inputs with `systems[*].containers[*].components[*]` in `tests/raa/test_model_serialiser.py`
- [X] T005 [US1] Add `ArchModel` dataclass serialization tests covering `ArchSystem.containers`, `ArchContainer.components`, and embedded relationship lists in `tests/raa/test_model_serialiser.py`
- [X] T006 [US1] Add external entity and relationship endpoint tests requiring an `External Entities` section for persons, external systems, and relationship endpoints missing from the nested tree in `tests/raa/test_model_serialiser.py`
- [X] T007 [P] [US1] Add routing tests asserting all three normal `fan_out_subgraphs` Send payloads contain identical prefixed `model_constraints` text in `tests/raa/test_parallel_subgraphs.py`
- [X] T008 [US1] Add prompt assembly tests asserting `build_subgraph_prompt` reads `payload["model_constraints"]` under `## Existing Architecture Model` instead of JSON dumping `running_arch_model` in `tests/raa/test_parallel_subgraphs.py`

### Implementation for User Story 1

- [X] T009 [US1] Implement `WARNING_PREFIX`, `serialize_arch_model(model)`, and `build_model_constraint_block(model)` in `raa/utils/model_serialiser.py`
- [X] T010 [US1] Implement deterministic model normalization helpers for dataclass, dict, hierarchical nested, and semi-flat parent-id model shapes in `raa/utils/model_serialiser.py`
- [X] T011 [US1] Render sorted systems, containers, and components as an indented C4 tree in `raa/utils/model_serialiser.py`
- [X] T012 [US1] Render sorted relationships and sorted `External Entities` sections, including referenced endpoint IDs missing from the nested tree, in `raa/utils/model_serialiser.py`
- [X] T013 [US1] Export `WARNING_PREFIX`, `serialize_arch_model`, and `build_model_constraint_block` from `raa/utils/__init__.py`
- [X] T014 [P] [US1] Import `build_model_constraint_block` and add `model_constraints` to `_common_send_payload` in `raa/graphs/subgraphs/routing.py`
- [X] T015 [P] [US1] Update `build_subgraph_prompt` in `raa/graphs/subgraphs/common.py` to inject `payload["model_constraints"]` under `## Existing Architecture Model`
- [X] T016 [US1] Replace the old flat `serialize_running_arch_model` prompt path in `raa/graphs/subgraphs/common.py` while preserving raw `running_arch_model` access for `validate_parent_links` and `validate_relationship_scopes`
- [X] T017 [US1] Run `pytest tests/raa/test_model_serialiser.py tests/raa/test_parallel_subgraphs.py` and fix failures in `raa/utils/model_serialiser.py`, `raa/graphs/subgraphs/routing.py`, and `raa/graphs/subgraphs/common.py`

**Checkpoint**: User Story 1 is complete when the current running architecture model is rendered once during fan-out and every normal RAA Send payload carries the same prefixed constraint block.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Verify the implementation does not regress existing RAA behavior.

- [X] T018 Run `pytest tests/raa` and fix feature-caused regressions in `raa/utils/model_serialiser.py`, `raa/graphs/subgraphs/routing.py`, `raa/graphs/subgraphs/common.py`, and `tests/raa/test_parallel_subgraphs.py`
- [X] T019 Confirm no implementation imports or task references use the draft `raa/utils/model_serializer.py` spelling instead of `raa/utils/model_serialiser.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on T001 and blocks the user story implementation
- **User Story 1 (Phase 3)**: Depends on T002
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational phase completion and is the MVP scope

### Within User Story 1

- Tests T003-T008 must be written before implementation tasks T009-T016
- Serializer implementation T009-T012 must complete before exports T013 and routing/prompt integration T014-T016
- T014 and T015 can run in parallel after T009-T013 because they touch different files
- T017 validates User Story 1 before broader regression testing in T018

### Parallel Opportunities

- T007 can run in parallel with T003-T006 because it touches `tests/raa/test_parallel_subgraphs.py` while serializer tests touch `tests/raa/test_model_serialiser.py`
- T014 and T015 can run in parallel after the utility API exists because they touch `raa/graphs/subgraphs/routing.py` and `raa/graphs/subgraphs/common.py`
- T018 can be run by a separate executor after T017 passes

---

## Parallel Example: User Story 1

```bash
# After T002, write independent test files in parallel:
Task: "Add serializer behavior tests in tests/raa/test_model_serialiser.py"
Task: "Add routing and prompt assembly tests in tests/raa/test_parallel_subgraphs.py"

# After T009-T013, integrate independent code paths in parallel:
Task: "Add model_constraints to _common_send_payload in raa/graphs/subgraphs/routing.py"
Task: "Read model_constraints in build_subgraph_prompt in raa/graphs/subgraphs/common.py"
```

---

## Implementation Strategy

### MVP First

1. Complete T001-T002 to lock the Section 15 integration contract.
2. Write failing tests T003-T008.
3. Implement the serializer and exports T009-T013.
4. Integrate fan-out and prompt assembly T014-T016.
5. Validate with T017.

### Incremental Delivery

1. Deliver deterministic serializer output first.
2. Add prefix block construction once serialization is stable.
3. Wire the block into Send payloads.
4. Replace prompt assembly's flat JSON model dump with the structured block.
5. Run focused and broader RAA regression tests.

### Suggested MVP Scope

Complete User Story 1 only. There are no lower-priority stories in this feature.
