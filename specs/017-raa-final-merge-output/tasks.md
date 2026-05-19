# Tasks: RAA Final Merge and Output

**Input**: Design documents from `/specs/017-raa-final-merge-output/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `RAA_Plan.md` Sections 16 and 19

**Tests**: Required by the feature specification independent tests. Write the listed pytest coverage before implementation and confirm the current code fails because `raa/nodes/final_merge.py` is not implemented.

**Organization**: Tasks are grouped by user story so global merge, schema/manifest validation, and filesystem output can be implemented and tested independently. Checkpoint archiving is intentionally out of scope for this Section 16 task list.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel after dependencies are satisfied because it touches different files
- **[Story]**: User story label from `spec.md`
- All task descriptions include exact repository file paths

## Phase 1: Setup

**Purpose**: Confirm the Section 16 final merge contract and existing reusable merge/state utilities.

- [X] T001 Review `RAA_Plan.md` Sections 16 and 19 for the final merge, output schema, diagram manifest, downstream handoff, filesystem output, and validation requirements
- [X] T002 Review the Section 13 deterministic merge helpers in `raa/nodes/judge.py` and decide which helpers can be reused by `raa/nodes/final_merge.py`
- [X] T003 Review JSON serialization helpers and dataclass fields in `raa/state/serialization.py` and `raa/state/types.py`

---

## Phase 2: Foundational

**Purpose**: Establish the final output data shape and node entry point before implementing story behavior.

- [X] T004 Add `diagram_manifest: list[DiagramManifestEntry]` and `confidence_metadata: dict[str, ConfidenceRecord]` default fields to `ArchModel` in `raa/state/types.py`
- [X] T005 Create `raa/nodes/final_merge.py` with a public `final_merge(state, config=None)` node stub, `LLM_JUDGE_KEY = "llm_judge"`, and helper placeholders for global merge, reconciliation, validation, manifest generation, output serialization, and file writing
- [X] T006 [P] Create shared final-merge fixtures for multi-batch `ArchFragment`, `ArchModel`, `OpenQuestion`, fake `llm_judge`, and temporary output directory contexts in `tests/raa/test_final_merge.py`
- [X] T007 [P] Add import/export coverage expectations for `final_merge` in `tests/raa/test_final_merge.py` and prepare to export it from `raa/nodes/__init__.py`

**Checkpoint**: The final merge module exists, output schema fields are available on `ArchModel`, and tests can construct the required global merge and output fixtures.

---

## Phase 3: User Story 1 - Global Merge and Scoped Reconciliation (Priority: P1) MVP

**Goal**: Combine all `best_batch_output` fragments and the final `running_arch_model` into one unified model using the deterministic Section 13 merge algorithm globally, then run one focused `llm_judge` reconciliation pass over outstanding `open_questions`.

**Independent Test**: Run `pytest tests/raa/test_final_merge.py -k "global_merge or reconciliation"` with multiple batch fragments containing duplicate entities, conflicting hierarchy/scope details, and unresolved open questions; verify the merged model is coherent and unresolved questions are either resolved or retained safely.

### Tests for User Story 1

- [X] T008 [US1] Add tests that `final_merge` reads all `best_batch_output` entries in deterministic batch-index order and includes the current `running_arch_model` baseline in `tests/raa/test_final_merge.py`
- [X] T009 [US1] Add tests that global entity deduplication in `raa/nodes/final_merge.py` operates per type, keeps longest descriptions, preserves available technology annotations, and produces deterministic canonical ID ordering in `tests/raa/test_final_merge.py`
- [X] T010 [US1] Add tests that global relationship deduplication in `raa/nodes/final_merge.py` uses `(source_id, target_id, interaction_type)` and preserves endpoint-consistent `diagram_scope` in `tests/raa/test_final_merge.py`
- [X] T011 [US1] Add tests that unresolved hierarchy and scope conflicts from the global merge are represented as `OpenQuestion` records in the final model in `tests/raa/test_final_merge.py`
- [X] T012 [US1] Add tests that a single focused reconciliation pass invokes fake `llm_judge.invoke(...)` only with current `open_questions` and a compact merged-model summary in `tests/raa/test_final_merge.py`
- [X] T013 [US1] Add tests that valid reconciliation output can update the merged model and remove only resolved `open_questions` in `tests/raa/test_final_merge.py`
- [X] T014 [US1] Add tests that malformed reconciliation JSON or schema-invalid reconciliation output logs a warning, preserves unresolved `open_questions`, and does not corrupt the merged model in `tests/raa/test_final_merge.py`
- [X] T015 [US1] Add tests that final merge output excludes `llm_judge`, `llm`, and any object with an `.invoke` attribute from returned state updates in `tests/raa/test_final_merge.py`

### Implementation for User Story 1

- [X] T016 [US1] Implement `_context_dict(config)`, `_require_llm_judge(context)`, `_invoke_llm(llm, prompt)`, and `_response_to_dict(raw_response)` in `raa/nodes/final_merge.py`
- [X] T017 [US1] Implement `_collect_global_fragments(best_batch_output, running_arch_model)` in `raa/nodes/final_merge.py` to collect fragments in sorted batch-index order and include the running model baseline deterministically
- [X] T018 [US1] Implement `_global_merge_fragments(...)` in `raa/nodes/final_merge.py` by applying the Section 13 entity deduplication, relationship deduplication, coverage union, orphan prevention, and tree assembly rules globally across all collected fragments
- [X] T019 [US1] Reuse or extract deterministic helpers from `raa/nodes/judge.py` in `raa/nodes/final_merge.py` without introducing any LLM calls into entity merge, relationship merge, coverage union, orphan prevention, or tree assembly
- [X] T020 [US1] Implement `_build_confidence_metadata(model, best_batch_output, incoherent_batches)` in `raa/nodes/final_merge.py` keyed by entity ID with `ConfidenceRecord(reduced_confidence, source_batch, saam_score)` values
- [X] T021 [US1] Implement `_build_reconciliation_prompt(open_questions, merged_model)` in `raa/nodes/final_merge.py` so the prompt is strictly scoped to listed questions and forbids full re-analysis
- [X] T022 [US1] Implement `_apply_reconciliation_response(merged_model, open_questions, response)` in `raa/nodes/final_merge.py` to accept only structured, validated operations that resolve listed `OpenQuestion` items
- [X] T023 [US1] Implement reconciliation failure handling in `raa/nodes/final_merge.py` that logs a warning, keeps unresolved questions, and returns the pre-reconciliation deterministic model
- [X] T024 [US1] Implement the global merge and reconciliation portion of `final_merge(state, config=None)` in `raa/nodes/final_merge.py`

**Checkpoint**: User Story 1 is complete when the node can produce a single reconciled `ArchModel` from all batch outputs without returning LLM objects or using LLMs for deterministic merge decisions.

---

## Phase 4: User Story 2 - C4 JSON Validation and Diagram Manifest Generation (Priority: P2)

**Goal**: Validate the final merged model against the Section 19 C4 structural criteria and generate a deterministic `diagram_manifest` work queue for AGA.

**Independent Test**: Run `pytest tests/raa/test_final_merge.py -k "validation or manifest or handoff"` with valid and invalid hierarchical models; verify validation errors for invalid structures and exact manifest counts and fields for valid structures.

### Tests for User Story 2

- [X] T025 [US2] Add tests that C4 validation accepts a valid nested `ArchModel` with systems, containers, components, persons, external systems, and scoped relationships in `tests/raa/test_final_merge.py`
- [X] T026 [US2] Add tests that C4 validation rejects duplicate IDs reused across systems, containers, components, persons, and external systems in `tests/raa/test_final_merge.py`
- [X] T027 [US2] Add tests that C4 validation rejects orphan containers, orphan components, and parent ID mismatches inside the hierarchy in `tests/raa/test_final_merge.py`
- [X] T028 [US2] Add tests that C4 validation rejects relationships whose `source_id` or `target_id` does not resolve to any final model entity in `tests/raa/test_final_merge.py`
- [X] T029 [US2] Add tests that C4 validation rejects relationship `diagram_scope` values inconsistent with endpoint types using the Section 12 scope rules in `tests/raa/test_final_merge.py`
- [X] T030 [US2] Add tests that `diagram_manifest` contains exactly one `ctx-{system_id}` context entry and one `cnt-{system_id}` container entry per system plus one `cmp-{container_id}` component entry per container in `tests/raa/test_final_merge.py`
- [X] T031 [US2] Add tests that every `DiagramManifestEntry` has `diagram_id`, `diagram_type`, `focus_entity_id`, and `label` populated with deterministic values in `tests/raa/test_final_merge.py`
- [X] T032 [US2] Add tests that the downstream handoff JSON contains `systems`, `persons`, `external_systems`, `patterns`, `diagram_manifest`, `confidence_metadata`, and `open_questions`, and contains no generated diagrams, code, PlantUML, or AGA filtering hints in `tests/raa/test_final_merge.py`

### Implementation for User Story 2

- [X] T033 [US2] Implement `_index_c4_entities(model)` in `raa/nodes/final_merge.py` to traverse nested systems, containers, components, persons, and external systems and return deterministic ID/type indexes
- [X] T034 [US2] Implement `_collect_model_relationships(model)` in `raa/nodes/final_merge.py` to gather `context_relationships`, `container_relationships`, and `component_relationships` from the hierarchy
- [X] T035 [US2] Implement `validate_c4_model(model)` in `raa/nodes/final_merge.py` to enforce strict system -> container -> component nesting, no duplicate IDs across entity types, no orphan parent links, valid relationship endpoints, and scope alignment from Section 19
- [X] T036 [US2] Implement `_expected_relationship_scope(source_type, target_type)` in `raa/nodes/final_merge.py` using the Section 12 C4 scope rules
- [X] T037 [US2] Implement `generate_diagram_manifest(model)` in `raa/nodes/final_merge.py` with deterministic traversal and entry IDs `ctx-{system_id}`, `cnt-{system_id}`, and `cmp-{container_id}`
- [X] T038 [US2] Implement `_build_c4_handoff_dict(model)` in `raa/nodes/final_merge.py` using `raa/state/serialization.py` helpers to serialize the final C4 JSON fields exactly as the Section 16 output schema table requires
- [X] T039 [US2] Integrate validation, manifest generation, and handoff JSON construction into `final_merge(state, config=None)` in `raa/nodes/final_merge.py`

**Checkpoint**: User Story 2 is complete when the final model fails fast on invalid C4 structures and valid models produce an AGA-ready `diagram_manifest` with exact count `(2 * len(systems)) + total_containers`.

---

## Phase 5: User Story 3 - Filesystem Output (Priority: P3)

**Goal**: Write the validated C4-compliant handoff JSON to the orchestrator-provided output path `projects/{project_name}/output/raa/arch_model.json` without hardcoding project defaults.

**Independent Test**: Run `pytest tests/raa/test_final_merge.py -k "filesystem or output"` with a temporary orchestrator-provided `output_dir`; verify `arch_model.json` is written only after validation and contains the final serialized handoff JSON.

### Tests for User Story 3

- [X] T040 [US3] Add tests that `final_merge` requires an orchestrator-provided `config["context"]["output_dir"]` and does not fall back to a hardcoded `projects/{project_name}` path in `tests/raa/test_final_merge.py`
- [X] T041 [US3] Add tests that a valid final model writes indented JSON to `Path(output_dir) / "arch_model.json"` in `tests/raa/test_final_merge.py`
- [X] T042 [US3] Add tests that invalid C4 validation prevents any `arch_model.json` write in `tests/raa/test_final_merge.py`
- [X] T043 [US3] Add tests that the written JSON file matches the downstream handoff schema and includes `diagram_manifest` and `confidence_metadata` in `tests/raa/test_final_merge.py`
- [X] T044 [US3] Add tests that `final_merge` returns a state update with the final `running_arch_model` and unresolved `open_questions` but no filesystem-only or LLM objects in `tests/raa/test_final_merge.py`

### Implementation for User Story 3

- [X] T045 [US3] Implement `_require_output_dir(context)` in `raa/nodes/final_merge.py` to read only the orchestrator-provided output directory from runtime context
- [X] T046 [US3] Implement `_write_arch_model_json(output_dir, handoff_dict)` in `raa/nodes/final_merge.py` to write `arch_model.json` with deterministic key ordering and indentation
- [X] T047 [US3] Ensure `final_merge(state, config=None)` in `raa/nodes/final_merge.py` calls validation before `_write_arch_model_json(...)` and does not write a file if validation raises
- [X] T048 [US3] Export `final_merge` from `raa/nodes/__init__.py`
- [X] T049 [US3] Run `pytest tests/raa/test_final_merge.py` and fix failures in `raa/nodes/final_merge.py`, `raa/state/types.py`, `raa/nodes/__init__.py`, and `tests/raa/test_final_merge.py`

**Checkpoint**: User Story 3 is complete when valid final output is written to the orchestrator-provided `output/raa` directory and invalid models leave the filesystem untouched.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify Section 16 remains deterministic and bounded to the requested final merge/output behavior.

- [X] T050 Run `pytest tests/raa/test_final_merge.py tests/raa/test_judge.py tests/raa/test_main_graph.py` and fix feature-caused regressions in `raa/nodes/final_merge.py`, `raa/nodes/judge.py`, `raa/state/types.py`, and `raa/nodes/__init__.py`
- [X] T051 Confirm `raa/nodes/final_merge.py` contains no LLM calls inside global merge, C4 validation, diagram manifest generation, output serialization, or filesystem writing helpers
- [X] T052 Confirm `raa/nodes/final_merge.py` does not implement checkpoint archive movement or reference `checkpoints/archive`, because checkpoint archiving is outside the strict Section 16 task scope
- [X] T053 Confirm `raa/nodes/final_merge.py` writes only `arch_model.json` and does not generate PlantUML, diagrams, code, or AGA-side filtering artifacts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on User Story 1 because validation and manifest operate on the merged final model
- **User Story 3 (Phase 5)**: Depends on User Story 2 because filesystem output must only write validated C4 JSON
- **Polish (Phase 6)**: Depends on all selected user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational phase completion and is the MVP scope
- **User Story 2 (P2)**: Depends on User Story 1 merged model output
- **User Story 3 (P3)**: Depends on User Story 2 validation and handoff JSON construction

### Within User Story 1

- Tests T008-T015 must be written before implementation tasks T016-T024
- Context helpers T016 must complete before reconciliation tasks T021-T023
- Fragment collection T017 and global merge T018-T019 must complete before confidence metadata T020 and final orchestration T024

### Within User Story 2

- Tests T025-T032 must be written before implementation tasks T033-T039
- Entity indexing T033 and relationship collection T034 must complete before validation T035-T036
- Validation T035-T036 and manifest generation T037 must complete before handoff JSON construction T038-T039

### Within User Story 3

- Tests T040-T044 must be written before implementation tasks T045-T049
- Output directory resolution T045 and handoff JSON construction from User Story 2 must complete before file writing T046-T047
- Export T048 can run in parallel with final test cleanup after `final_merge` exists

### Parallel Opportunities

- T006 and T007 can run in parallel with T005 because they touch tests while the module skeleton is created
- T021 and T022 can run in parallel with deterministic merge helpers after T016-T020 because reconciliation logic is isolated from merge logic
- T033 and T034 can run in parallel after User Story 1 because entity indexing and relationship collection touch separate helpers
- T048 can run in parallel with T046-T047 once the public `final_merge` callable exists

---

## Parallel Example: User Story 1

```bash
# After T004-T005:
Task: "Create multi-batch final merge fixtures in tests/raa/test_final_merge.py"
Task: "Implement _collect_global_fragments and deterministic merge integration in raa/nodes/final_merge.py"

# After T016-T020:
Task: "Implement strictly-scoped reconciliation prompt and response parser in raa/nodes/final_merge.py"
Task: "Add reconciliation failure fallback tests in tests/raa/test_final_merge.py"
```

## Parallel Example: User Story 2

```bash
# After User Story 1:
Task: "Implement _index_c4_entities in raa/nodes/final_merge.py"
Task: "Implement _collect_model_relationships in raa/nodes/final_merge.py"
```

## Parallel Example: User Story 3

```bash
# After User Story 2:
Task: "Implement _write_arch_model_json in raa/nodes/final_merge.py"
Task: "Export final_merge from raa/nodes/__init__.py"
```

---

## Implementation Strategy

### MVP First

1. Complete T001-T007 to establish the schema and node entry point.
2. Complete User Story 1 T008-T024 to produce a reconciled global model.
3. Stop and validate User Story 1 independently with the global merge/reconciliation tests.

### Incremental Delivery

1. Add User Story 2 T025-T039 to validate C4 structure and generate the AGA manifest.
2. Validate manifest count and downstream handoff JSON shape independently.
3. Add User Story 3 T040-T049 to write `arch_model.json` at the orchestrator-provided path.
4. Run polish checks T050-T053 to confirm strict Section 16 scope.

### Suggested MVP Scope

User Story 1 is the MVP. User Stories 2 and 3 are required before the final RAA deliverable is usable by AGA.
