# Tasks: RAA Parallel Subgraphs Per Batch

**Input**: Design documents from `specs/014-raa-parallel-subgraphs/`
**Source Scope**: `RAA_Plan.md` Section 12 only, including LLM Instance Configuration, `fan_out_subgraphs` Send routing, Subgraph Strategies, Hierarchy Placement Responsibilities, and Relationship Scoping Rules
**Tests**: Included because the feature specification requires Send routing, context LLM assignment, reduced-confidence fallback, typed `ArchFragment` output, parent-link validation, and `batch_outputs` reducer behavior.

**Organization**: Tasks are grouped around one independently testable parallel-subgraph story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the graph package, state contracts, reference bundle, and tests package exist before implementing Section 12.

- [x] T001 [P] Confirm the RAA graphs package exists at `raa/graphs/`
- [x] T002 [P] Confirm the RAA state contracts define `ArchFragment`, `ArchSystem`, `ArchContainer`, `ArchComponent`, `ArchPerson`, `ArchExternalSystem`, `ArchRelationship`, and `ArchPattern` in `raa/state/types.py`
- [x] T003 [P] Confirm `RAAState.batch_outputs` uses `merge_batch_outputs` as a dict-merge append reducer in `raa/state/channels.py`
- [x] T004 [P] Confirm the RAA test package exists at `tests/raa/`
- [x] T005 [P] Confirm `Skills/RAA/references/C4.md`, `Skills/RAA/references/C4_Level_Mapping.md`, `Skills/RAA/references/Entity_Extraction.md`, `Skills/RAA/references/Relationship_Extraction.md`, `Skills/RAA/references/Technology_Inference.md`, `Skills/RAA/references/Quality_Attributes.md`, `Skills/RAA/references/SAAM.md`, and `Skills/RAA/references/Pattern_Selection.md` exist

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature docs and shared contracts with the requested `raa/graphs/subgraphs/` package and Section 12 Send payload behavior.

- [x] T006 [P] Update `specs/014-raa-parallel-subgraphs/spec.md` so FR-001 names `raa/graphs/subgraphs/raa_a.py`, `raa/graphs/subgraphs/raa_b.py`, `raa/graphs/subgraphs/raa_c.py`, and `raa/graphs/subgraphs/routing.py` instead of `raa/graphs/subgraphs.py` or `raa/nodes/strategies.py`
- [x] T007 [P] Update `specs/014-raa-parallel-subgraphs/plan.md` to use the package path `raa/graphs/subgraphs/` and test path `tests/raa/test_parallel_subgraphs.py`
- [x] T008 [P] Update `specs/014-raa-parallel-subgraphs/data-model.md` to reference the dataclass `ArchFragment` from `raa/state/types.py` and valid `diagram_scope` values `context`, `container`, and `component`
- [x] T009 [P] Update `specs/014-raa-parallel-subgraphs/contracts/readme.md` to require Send payload keys `batch`, `batch_index`, `quality_weights`, `running_arch_model`, `bridge_requirements`, `strategy`, and `llm`
- [x] T010 [P] Update `specs/014-raa-parallel-subgraphs/quickstart.md` to import `Send` from `langgraph.types` and import `fan_out_subgraphs` from `raa.graphs.subgraphs.routing`
- [x] T011 Define `SubgraphPayload` and `SubgraphStrategy` TypedDict or Literal contracts for the Send payload and strategy names in `raa/graphs/subgraphs/common.py`
- [x] T012 Define constants for LLM context keys `llm_raa_a`, `llm_raa_b`, and `llm_raa_c` plus Send target node names `raa_a`, `raa_b`, and `raa_c` in `raa/graphs/subgraphs/common.py`
- [x] T013 Define the per-strategy reference manifest in `raa/graphs/subgraphs/common.py`: RAA-A uses `SAAM.md`, `Quality_Attributes.md`, `Entity_Extraction.md`, `Relationship_Extraction.md`, `Technology_Inference.md`, `C4.md`, and `C4_Level_Mapping.md`; RAA-B uses `Pattern_Selection.md`, `Quality_Attributes.md`, `Entity_Extraction.md`, `Relationship_Extraction.md`, `Technology_Inference.md`, `C4.md`, and `C4_Level_Mapping.md`; RAA-C uses `Entity_Extraction.md`, `Relationship_Extraction.md`, `Technology_Inference.md`, `C4.md`, and `C4_Level_Mapping.md`
- [x] T014 Define the Section 12 relationship scope table in `raa/graphs/subgraphs/common.py` mapping system/person/external-system endpoint combinations to `context`, container endpoint combinations to `container`, and component endpoint combinations to `component`

**Checkpoint**: Docs and shared constants define the exact Section 12 payload, strategy, reference, hierarchy, and scope contracts.

---

## Phase 3: User Story 1 - Fan Out Each Batch To Parallel RAA Strategy Subgraphs (Priority: P1) MVP

**Goal**: Emit Send payloads for RAA-A, RAA-B, and RAA-C using LLM instances from runtime context, run each strategy with the correct reference bundle, validate parent links and relationship scopes, and write typed `ArchFragment` results to `batch_outputs`.

**Independent Test**: Run `tests/raa/test_parallel_subgraphs.py` and confirm normal batches emit three Send objects, reduced-confidence batches emit only RAA-A, each Send payload contains the correct LLM and batch context, each strategy consumes `payload["llm"]`, each strategy returns `{"batch_outputs": {batch_index: [ArchFragment]}}`, parent-link and `diagram_scope` hard rules are enforced, and `merge_batch_outputs` combines all three fragments under the same batch index.

### Tests for User Story 1

- [x] T015 [US1] Create `tests/raa/test_parallel_subgraphs.py` with fake batches, fake `running_arch_model`, fake bridge requirements, fake LLMs, and JSON/dict ArchFragment response fixtures
- [x] T016 [US1] Add a unit test verifying `fan_out_subgraphs(state, config)` returns three `Send` objects targeting `raa_a`, `raa_b`, and `raa_c` for a normal batch in `tests/raa/test_parallel_subgraphs.py`
- [x] T017 [US1] Add a unit test verifying `fan_out_subgraphs(state, config)` returns one `Send` object targeting `raa_a` when the current batch has `reduced_confidence = True` in `tests/raa/test_parallel_subgraphs.py`
- [x] T018 [US1] Add a unit test verifying every Send payload contains `batch`, `batch_index`, `quality_weights`, `running_arch_model`, `bridge_requirements`, `strategy`, and the correct role-specific `llm` from context in `tests/raa/test_parallel_subgraphs.py`
- [x] T019 [US1] Add a unit test verifying `fan_out_subgraphs` raises a clear configuration error when a required `llm_raa_a`, `llm_raa_b`, or `llm_raa_c` context key is missing for the selected route in `tests/raa/test_parallel_subgraphs.py`
- [x] T020 [US1] Add a unit test verifying `run_raa_a(payload)` consumes `payload["llm"]`, not graph state or module globals, and returns `batch_outputs[batch_index] = [ArchFragment(...)]` in `tests/raa/test_parallel_subgraphs.py`
- [x] T021 [US1] Add a unit test verifying `run_raa_b(payload)` consumes `payload["llm"]`, includes Pattern Selection reference content, and returns `batch_outputs[batch_index] = [ArchFragment(...)]` in `tests/raa/test_parallel_subgraphs.py`
- [x] T022 [US1] Add a unit test verifying `run_raa_c(payload)` consumes `payload["llm"]`, uses entity/relationship-driven reference content, and returns `batch_outputs[batch_index] = [ArchFragment(...)]` in `tests/raa/test_parallel_subgraphs.py`
- [x] T023 [US1] Add a unit test verifying RAA-A prompt assembly includes `SAAM.md`, `Quality_Attributes.md`, `Entity_Extraction.md`, `Relationship_Extraction.md`, `Technology_Inference.md`, `C4.md`, and `C4_Level_Mapping.md` in `tests/raa/test_parallel_subgraphs.py`
- [x] T024 [US1] Add a unit test verifying RAA-B prompt assembly includes `Pattern_Selection.md`, `Quality_Attributes.md`, `Entity_Extraction.md`, `Relationship_Extraction.md`, `Technology_Inference.md`, `C4.md`, and `C4_Level_Mapping.md` in `tests/raa/test_parallel_subgraphs.py`
- [x] T025 [US1] Add a unit test verifying RAA-C prompt assembly includes `Entity_Extraction.md`, `Relationship_Extraction.md`, `Technology_Inference.md`, `C4.md`, and `C4_Level_Mapping.md` and excludes `SAAM.md` and `Pattern_Selection.md` in `tests/raa/test_parallel_subgraphs.py`
- [x] T026 [US1] Add a unit test verifying `validate_parent_links(fragment, running_arch_model)` accepts containers whose `parent_system_id` resolves to a same-fragment system or existing running-model system in `tests/raa/test_parallel_subgraphs.py`
- [x] T027 [US1] Add a unit test verifying `validate_parent_links(fragment, running_arch_model)` rejects a container with an unresolved `parent_system_id` in `tests/raa/test_parallel_subgraphs.py`
- [x] T028 [US1] Add a unit test verifying `validate_parent_links(fragment, running_arch_model)` accepts components whose `parent_container_id` resolves to a same-fragment container or existing running-model container in `tests/raa/test_parallel_subgraphs.py`
- [x] T029 [US1] Add a unit test verifying `validate_parent_links(fragment, running_arch_model)` rejects a component with an unresolved `parent_container_id` in `tests/raa/test_parallel_subgraphs.py`
- [x] T030 [US1] Add a unit test verifying `validate_relationship_scopes(fragment, running_arch_model)` accepts `context`, `container`, and `component` scopes that match the Section 12 endpoint-type table in `tests/raa/test_parallel_subgraphs.py`
- [x] T031 [US1] Add a unit test verifying `validate_relationship_scopes(fragment, running_arch_model)` rejects missing or mismatched `diagram_scope` values in `tests/raa/test_parallel_subgraphs.py`
- [x] T032 [US1] Add a unit test verifying the subgraph output parser creates real `ArchFragment`, `ArchSystem`, `ArchContainer`, `ArchComponent`, `ArchPerson`, `ArchExternalSystem`, `ArchRelationship`, and `ArchPattern` dataclass instances from an LLM dict/JSON response in `tests/raa/test_parallel_subgraphs.py`
- [x] T033 [US1] Add a unit test verifying `merge_batch_outputs({idx: [fragment_a]}, {idx: [fragment_b]})` appends both strategy fragments under the same batch index in `tests/raa/test_parallel_subgraphs.py`
- [x] T034 [US1] Add a unit test verifying subgraph Send payloads and returned updates do not include `llm_raa_a`, `llm_raa_b`, `llm_raa_c`, `llm_judge`, or any ChatModel object in `RAAState` channels in `tests/raa/test_parallel_subgraphs.py`

### Implementation for User Story 1

- [x] T035 [US1] Create package directory files `raa/graphs/subgraphs/__init__.py`, `raa/graphs/subgraphs/common.py`, `raa/graphs/subgraphs/routing.py`, `raa/graphs/subgraphs/raa_a.py`, `raa/graphs/subgraphs/raa_b.py`, and `raa/graphs/subgraphs/raa_c.py`
- [x] T036 [US1] Implement `_current_batch(state: RAAState) -> tuple[int, dict]` in `raa/graphs/subgraphs/routing.py` reading `batch_cursor` and `batch_queue` with clear index errors
- [x] T037 [US1] Implement `_context_dict(config: dict | None) -> dict` in `raa/graphs/subgraphs/routing.py` extracting runtime context without reading or mutating graph state
- [x] T038 [US1] Implement `_require_llm(context: dict, key: str) -> object` in `raa/graphs/subgraphs/routing.py` raising a detailed configuration exception for missing Section 12 LLM keys
- [x] T039 [US1] Implement `_common_send_payload(state: RAAState, batch_index: int, batch: dict) -> dict` in `raa/graphs/subgraphs/routing.py` including `batch`, `batch_index`, `quality_weights`, `running_arch_model`, and `bridge_requirements`
- [x] T040 [US1] Implement `fan_out_subgraphs(state: RAAState, config: dict | None = None) -> list[Send]` in `raa/graphs/subgraphs/routing.py` returning three Send objects for normal batches and one RAA-A Send object for `reduced_confidence` batches
- [x] T041 [US1] Implement `load_reference_file(filename: str) -> str` in `raa/graphs/subgraphs/common.py` reading only from `Skills/RAA/references/` and raising `FileNotFoundError` for missing references
- [x] T042 [US1] Implement `load_strategy_references(strategy: SubgraphStrategy) -> dict[str, str]` in `raa/graphs/subgraphs/common.py` using the per-strategy reference manifest
- [x] T043 [US1] Implement `serialize_running_arch_model(running_arch_model: ArchModel | dict | None) -> dict` in `raa/graphs/subgraphs/common.py` exposing existing system IDs, container IDs, component IDs, actors, and relationships for prompt constraints
- [x] T044 [US1] Implement `build_subgraph_prompt(payload: SubgraphPayload, strategy: SubgraphStrategy, references: dict[str, str]) -> str` in `raa/graphs/subgraphs/common.py` injecting batch requirements, quality weights, bridge requirements, running model constraints, strategy focus, orphan-prevention rules, and relationship scoping rules
- [x] T045 [US1] Implement `_invoke_llm(llm: object, prompt: str) -> object` in `raa/graphs/subgraphs/common.py` supporting LLMs with `.invoke(prompt)` and returning the raw message or dict response without storing the LLM in state
- [x] T046 [US1] Implement `_response_to_dict(raw_response: object) -> dict` in `raa/graphs/subgraphs/common.py` accepting dict responses and JSON string or `.content` message responses in `raa/graphs/subgraphs/common.py`
- [x] T047 [US1] Implement `arch_fragment_from_dict(data: dict, source_fragment: str) -> ArchFragment` in `raa/graphs/subgraphs/common.py` constructing typed dataclass instances for systems, containers, components, persons, external systems, relationships, patterns, and rationale
- [x] T048 [US1] Implement `_running_system_ids(running_arch_model: ArchModel | dict | None) -> set[str]` and `_running_container_ids(running_arch_model: ArchModel | dict | None) -> set[str]` in `raa/graphs/subgraphs/common.py`
- [x] T049 [US1] Implement `validate_parent_links(fragment: ArchFragment, running_arch_model: ArchModel | dict | None) -> None` in `raa/graphs/subgraphs/common.py` enforcing no container without resolvable system parent and no component without resolvable container parent
- [x] T050 [US1] Implement `_entity_type_index(fragment: ArchFragment, running_arch_model: ArchModel | dict | None) -> dict[str, str]` in `raa/graphs/subgraphs/common.py` indexing systems, containers, components, persons, and external systems by ID
- [x] T051 [US1] Implement `_expected_diagram_scope(source_type: str, target_type: str) -> str` in `raa/graphs/subgraphs/common.py` from the Section 12 Relationship Scoping Rules table
- [x] T052 [US1] Implement `validate_relationship_scopes(fragment: ArchFragment, running_arch_model: ArchModel | dict | None) -> None` in `raa/graphs/subgraphs/common.py` requiring every relationship to have `diagram_scope` and match endpoint types
- [x] T053 [US1] Implement `execute_strategy_subgraph(payload: SubgraphPayload, strategy: SubgraphStrategy, source_fragment: str) -> dict` in `raa/graphs/subgraphs/common.py` loading references, building the prompt, invoking `payload["llm"]`, parsing a typed `ArchFragment`, validating parent links and scopes, and returning `{"batch_outputs": {payload["batch_index"]: [fragment]}}`
- [x] T054 [US1] Implement `run_raa_a(payload: SubgraphPayload) -> dict` in `raa/graphs/subgraphs/raa_a.py` using strategy `saam_first`, source fragment `raa_a`, and the conservative SAAM-first prompt focus
- [x] T055 [US1] Implement `run_raa_b(payload: SubgraphPayload) -> dict` in `raa/graphs/subgraphs/raa_b.py` using strategy `pattern_driven`, source fragment `raa_b`, and the pattern-driven prompt focus
- [x] T056 [US1] Implement `run_raa_c(payload: SubgraphPayload) -> dict` in `raa/graphs/subgraphs/raa_c.py` using strategy `entity_driven`, source fragment `raa_c`, and the entity/relationship-driven prompt focus
- [x] T057 [US1] Export `fan_out_subgraphs`, `run_raa_a`, `run_raa_b`, `run_raa_c`, strategy constants, validation helpers, and node-name constants from `raa/graphs/subgraphs/__init__.py`
- [x] T058 [US1] Export the `subgraphs` package symbols from `raa/graphs/__init__.py` without changing existing main graph exports

**Checkpoint**: Section 12 Send routing and all three strategy subgraph nodes are independently callable and write typed fragments to `batch_outputs`.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate Section 12 behavior and keep this feature scoped to fan-out and subgraph execution only.

- [x] T059 [P] Run `pytest tests/raa/test_parallel_subgraphs.py`
- [x] T060 [P] Run Python syntax validation for `raa/graphs/subgraphs/__init__.py`, `raa/graphs/subgraphs/common.py`, `raa/graphs/subgraphs/routing.py`, `raa/graphs/subgraphs/raa_a.py`, `raa/graphs/subgraphs/raa_b.py`, `raa/graphs/subgraphs/raa_c.py`, and `raa/graphs/__init__.py`
- [x] T061 Confirm `raa/graphs/subgraphs/routing.py` uses `langgraph.types.Send` and does not use normal edges for Section 12 dynamic fan-out
- [x] T062 Confirm `raa/graphs/subgraphs/raa_a.py`, `raa/graphs/subgraphs/raa_b.py`, and `raa/graphs/subgraphs/raa_c.py` consume LLM instances only from their Send payloads and never from `RAAState`
- [x] T063 Confirm subgraph outputs contain no diagrams, no PlantUML, and no generated code in `tests/raa/test_parallel_subgraphs.py`
- [x] T064 Confirm `raa/graphs/subgraphs/` does not implement judge selection, SAAM merge reconciliation, `running_arch_model` mutation, `best_batch_output`, `open_questions`, batch cursor advancement, or final merge behavior
- [x] T065 Confirm every returned `ArchRelationship.diagram_scope` is one of `context`, `container`, or `component` and is validated against endpoint types before writing `batch_outputs` in `raa/graphs/subgraphs/common.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational docs, payload contracts, reference manifests, and scope-table constants.
- **Polish (Final Phase)**: Depends on User Story 1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 and has no dependency on other stories.

### Within User Story 1

- Write tests T015-T034 before implementation tasks T035-T058.
- Implement routing helpers before `fan_out_subgraphs`.
- Implement reference loading and prompt assembly before strategy wrappers.
- Implement parsing before parent-link and relationship-scope validation.
- Implement validation before the three strategy wrappers return `batch_outputs`.
- Export package symbols only after the routing and strategy modules exist.

### Parallel Opportunities

- T001 through T005 can run in parallel.
- T006 through T010 can run in parallel because they edit different feature documents.
- T011 through T014 should run before strategy implementation because later tasks depend on the payload and reference constants.
- T020 through T022 can be drafted in parallel only if edits to `tests/raa/test_parallel_subgraphs.py` are coordinated.
- T023 through T025 can be drafted in parallel because they validate different strategy reference manifests in the same test file with coordination.
- T054, T055, and T056 can be implemented in parallel after T053 because they touch separate files.
- T059 and T060 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Implement run_raa_a(payload: SubgraphPayload) in raa/graphs/subgraphs/raa_a.py using strategy saam_first, source fragment raa_a, and the conservative SAAM-first prompt focus"
Task: "Implement run_raa_b(payload: SubgraphPayload) in raa/graphs/subgraphs/raa_b.py using strategy pattern_driven, source fragment raa_b, and the pattern-driven prompt focus"
Task: "Implement run_raa_c(payload: SubgraphPayload) in raa/graphs/subgraphs/raa_c.py using strategy entity_driven, source fragment raa_c, and the entity/relationship-driven prompt focus"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write Send routing tests, strategy reference tests, validation tests, and `batch_outputs` reducer tests.
3. Implement `raa/graphs/subgraphs/common.py` and `raa/graphs/subgraphs/routing.py`.
4. Implement the three strategy wrappers in `raa_a.py`, `raa_b.py`, and `raa_c.py`.
5. Export the package and run the parallel subgraph tests.

### Incremental Delivery

1. Establish payload, LLM key, reference, and relationship-scope constants.
2. Implement Send fan-out with reduced-confidence fallback.
3. Implement prompt/reference assembly and LLM invocation from Send payload only.
4. Parse typed `ArchFragment` dataclasses and validate hierarchy/scoping hard rules.
5. Write each strategy output to `batch_outputs` using the existing dict-merge reducer contract.

### Notes

- This feature implements Section 12 only; judge behavior and final merge remain out of scope.
- LLM instances must never be added to `RAAState` or returned in node updates.
- Every subgraph must prevent orphan containers/components before writing `batch_outputs`.
- Every relationship must carry a `diagram_scope` that matches the Section 12 endpoint-type table.
