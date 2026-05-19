# Tasks: RAA Main LangGraph Skeleton

**Input**: Design documents from `specs/013-raa-graph-skeleton/`
**Source Scope**: `RAA_Plan.md` Section 3 full seven-step pipeline overview and Section 4 state-channel ownership and reducer rules
**Tests**: Included because the feature specification requires graph compilation, gated execution, sequential traversal, and reducer verification.

**Organization**: Tasks are grouped around one independently testable graph-skeleton story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the runtime graph package, state schema, node modules, and tests package exist before implementing the main graph.

- [x] T001 [P] Confirm the RAA graphs package exists at `raa/graphs/`
- [x] T002 [P] Confirm the RAA nodes package exports `prepare_embeddings`, `construct_batches`, `apply_overlap_bridging`, `apply_coherence_gate`, and `order_batch_queue` in `raa/nodes/__init__.py`
- [x] T003 [P] Confirm `RAAState` and reducer helpers are exported from `raa/state/__init__.py`
- [x] T004 [P] Confirm the RAA test package exists at `tests/raa/`
- [x] T005 [P] Confirm `langgraph` is declared as a project dependency in `pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature docs and state contract with the Section 3/4 graph scope before implementation.

- [x] T006 [P] Update `specs/013-raa-graph-skeleton/spec.md` so the implemented node sequence is Preparation -> Batch Construction -> Overlap Bridging -> Coherence Gate -> Batch Queue Ordering, with Section 3 steps 6 and 7 documented as future downstream graph phases
- [x] T007 [P] Update `specs/013-raa-graph-skeleton/plan.md` to use `RAAState`, `raa/graphs/main_graph.py`, and `tests/raa/test_main_graph.py`
- [x] T008 [P] Update `specs/013-raa-graph-skeleton/data-model.md` to remove duplicate `RaaState` fields and reference the authoritative `RAAState` channels from `raa/state/channels.py`
- [x] T009 [P] Update `specs/013-raa-graph-skeleton/contracts/readme.md` with the channel ownership table for Section 3 steps 1-5: `prepare_embeddings` owns `embeddings_ready`, `construct_batches` owns initial `batch_queue`, `apply_overlap_bridging` owns `batch_queue` and `bridge_requirements`, `apply_coherence_gate` owns `batch_queue` and `incoherent_batches`, and `order_batch_queue` owns final `batch_queue`
- [x] T010 [P] Update `specs/013-raa-graph-skeleton/quickstart.md` to import `build_raa_graph` and `compile_raa_graph` from `raa.graphs.main_graph`
- [x] T011 Confirm `RAAState` uses overwrite channels for `batch_queue`, `batch_cursor`, `running_arch_model`, `bridge_requirements`, and `embeddings_ready` in `raa/state/channels.py`
- [x] T012 Confirm `RAAState` uses append reducers for `open_questions` and `incoherent_batches` in `raa/state/channels.py`
- [x] T013 Confirm `RAAState` uses dict-merge reducers for `batch_outputs` and `best_batch_output` in `raa/state/channels.py`

**Checkpoint**: Documentation and state contracts align with Section 3/4 before graph implementation begins.

---

## Phase 3: User Story 1 - Compile And Run The RAA Graph Through Batch Queue Ordering (Priority: P1) MVP

**Goal**: Define the main LangGraph `StateGraph` with `RAAState`, gate batch construction on `embeddings_ready`, execute the Section 3 steps 1-5 nodes in order, and expose a compiled graph interface.

**Independent Test**: Run `tests/raa/test_main_graph.py` and confirm the graph compiles, invokes mocked nodes in the expected order, halts with a clear error when `embeddings_ready` is false after preparation, outputs final `batch_queue`, and exposes compiled channel reducers matching the Section 4 New State Channels table.

### Tests for User Story 1

- [x] T014 [US1] Create `tests/raa/test_main_graph.py` with mock node functions that append visited node names to a `visited_nodes` list outside graph state and return valid partial `RAAState` updates
- [x] T015 [US1] Add a unit test verifying `build_raa_graph()` returns a LangGraph `StateGraph` built with `RAAState` in `tests/raa/test_main_graph.py`
- [x] T016 [US1] Add a unit test verifying `compile_raa_graph()` returns an invokable compiled graph without requiring LLM objects or checkpointer configuration in `tests/raa/test_main_graph.py`
- [x] T017 [US1] Add a unit test verifying the graph edges run `prepare_embeddings`, `embeddings_ready_gate`, `construct_batches`, `apply_overlap_bridging`, `apply_coherence_gate`, and `order_batch_queue` in that exact order before `END` in `tests/raa/test_main_graph.py`
- [x] T018 [US1] Add a unit test invoking the graph with mocked nodes and asserting the final output includes the ordered `batch_queue` from the queue ordering mock in `tests/raa/test_main_graph.py`
- [x] T019 [US1] Add a unit test verifying `embeddings_ready_gate` raises `ValueError` with a clear message when preparation returns `{"embeddings_ready": False}` or omits the flag in `tests/raa/test_main_graph.py`
- [x] T020 [US1] Add a unit test verifying the graph does not continue to `construct_batches` when `embeddings_ready_gate` raises in `tests/raa/test_main_graph.py`
- [x] T021 [US1] Add a unit test verifying `build_raa_graph(node_overrides=...)` can inject mock node callables for all Section 3 step 1-5 nodes without patching module globals in `tests/raa/test_main_graph.py`
- [x] T022 [US1] Add a reducer introspection test verifying compiled `batch_queue`, `batch_cursor`, `running_arch_model`, `bridge_requirements`, and `embeddings_ready` channels are LangGraph overwrite channels in `tests/raa/test_main_graph.py`
- [x] T023 [US1] Add a reducer introspection test verifying compiled `open_questions` and `incoherent_batches` channels use the `operator.add` append reducer in `tests/raa/test_main_graph.py`
- [x] T024 [US1] Add a reducer introspection test verifying compiled `batch_outputs` uses `merge_batch_outputs` and compiled `best_batch_output` uses `merge_best_batch_output` in `tests/raa/test_main_graph.py`
- [x] T025 [US1] Add a unit test verifying the graph does not add LLM instances, embedding vectors, `normalized_requirements`, or `batches` as LangGraph state channels in `tests/raa/test_main_graph.py`

### Implementation for User Story 1

- [x] T026 [US1] Create `raa/graphs/main_graph.py` importing `StateGraph`, `START`, `END`, `RAAState`, and the five Section 3 step 1-5 node callables
- [x] T027 [US1] Define node-name constants for `prepare_embeddings`, `embeddings_ready_gate`, `construct_batches`, `apply_overlap_bridging`, `apply_coherence_gate`, and `order_batch_queue` in `raa/graphs/main_graph.py`
- [x] T028 [US1] Define `SECTION_3_PIPELINE_STEPS` in `raa/graphs/main_graph.py` listing all seven Section 3 steps, with steps 6 and 7 marked as not wired by this graph skeleton feature
- [x] T029 [US1] Implement `embeddings_ready_gate(state: RAAState) -> dict` that returns `{}` only when `state["embeddings_ready"] is True` and otherwise raises `ValueError` in `raa/graphs/main_graph.py`
- [x] T030 [US1] Implement `_default_node_map() -> dict[str, callable]` mapping graph node names to `prepare_embeddings`, `construct_batches`, `apply_overlap_bridging`, `apply_coherence_gate`, and `order_batch_queue` in `raa/graphs/main_graph.py`
- [x] T031 [US1] Implement `_resolve_node_map(node_overrides: dict[str, callable] | None) -> dict[str, callable]` so tests can inject mock nodes while defaults remain production nodes in `raa/graphs/main_graph.py`
- [x] T032 [US1] Implement `build_raa_graph(node_overrides: dict[str, callable] | None = None) -> StateGraph` using `StateGraph(RAAState)` in `raa/graphs/main_graph.py`
- [x] T033 [US1] Add the six graph nodes in `build_raa_graph`: preparation node, `embeddings_ready_gate`, batch construction node, overlap bridging node, coherence gate node, and batch queue ordering node in `raa/graphs/main_graph.py`
- [x] T034 [US1] Add fixed edges in `build_raa_graph`: `START` -> preparation -> `embeddings_ready_gate` -> batch construction -> overlap bridging -> coherence gate -> batch queue ordering -> `END` in `raa/graphs/main_graph.py`
- [x] T035 [US1] Implement `compile_raa_graph(node_overrides: dict[str, callable] | None = None, checkpointer: object | None = None)` that builds the graph and calls `.compile(checkpointer=checkpointer)` only when a checkpointer is provided in `raa/graphs/main_graph.py`
- [x] T036 [US1] Export `build_raa_graph`, `compile_raa_graph`, and `embeddings_ready_gate` from `raa/graphs/__init__.py`

**Checkpoint**: The main graph compiles and invokes through queue ordering with Section 4 reducer semantics preserved by `RAAState`.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate graph behavior and keep this feature scoped to Section 3/4 graph wiring only.

- [x] T037 [P] Run `pytest tests/raa/test_main_graph.py`
- [x] T038 [P] Run Python syntax validation for `raa/graphs/main_graph.py`, `raa/graphs/__init__.py`, and `tests/raa/test_main_graph.py`
- [x] T039 Confirm `raa/graphs/main_graph.py` uses `RAAState` directly and does not define a second graph-only state schema
- [x] T040 Confirm `raa/graphs/main_graph.py` does not implement Section 3 step 6 execution-loop subgraphs, judge behavior, or Section 3 step 7 final merge behavior
- [x] T041 Confirm `raa/graphs/main_graph.py` does not serialize LLM instances or embedding vectors into graph state channels
- [x] T042 Confirm the compiled graph's channel set matches the keys defined in `RAAState` plus LangGraph internal channels only in `tests/raa/test_main_graph.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks graph implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational state and doc alignment.
- **Polish (Final Phase)**: Depends on User Story 1 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 and has no dependency on other stories.

### Within User Story 1

- Write tests T014-T025 before implementation tasks T026-T036.
- Implement the embeddings-ready gate before building graph edges through batch construction.
- Implement node override support before tests invoke the graph with mock nodes.
- Build the `StateGraph(RAAState)` before compiling it.
- Export graph helpers only after `raa/graphs/main_graph.py` exists.

### Parallel Opportunities

- T001 through T005 can run in parallel.
- T006 through T010 can run in parallel because they edit different feature documents.
- T011 through T013 can run in parallel with document updates because they inspect existing state schema files.
- T014 through T025 should run sequentially or with coordination because they edit the same test file.
- T026 through T036 should run mostly sequentially because they build one graph module and package export.
- T037 and T038 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a unit test verifying compile_raa_graph() returns an invokable compiled graph without requiring LLM objects or checkpointer configuration in tests/raa/test_main_graph.py"
Task: "Add a reducer introspection test verifying compiled open_questions and incoherent_batches channels use the operator.add append reducer in tests/raa/test_main_graph.py"
Task: "Add a reducer introspection test verifying compiled batch_outputs uses merge_batch_outputs and compiled best_batch_output uses merge_best_batch_output in tests/raa/test_main_graph.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write graph compilation, execution-order, gate, and reducer introspection tests.
3. Implement `raa/graphs/main_graph.py` with injectable node callables.
4. Export graph helpers from `raa/graphs/__init__.py`.
5. Run the graph skeleton tests.

### Incremental Delivery

1. Align the feature docs with RAA Section 3/4 and existing `RAAState`.
2. Add tests for graph structure and mocked execution.
3. Add tests for compiled reducer channels.
4. Implement the graph builder, readiness gate, and compiler helper.
5. Validate no out-of-scope execution loop, judge, final merge, LLM storage, or embedding-vector state storage was introduced.

### Notes

- This feature wires Section 3 steps 1-5 only: preparation, batch construction, overlap bridging, coherence gate, and batch queue ordering.
- Section 3 step 6 execution loop and step 7 final merge remain future graph phases and must not be implemented here.
- Reducer behavior comes from `RAAState` annotations in `raa/state/channels.py`; `main_graph.py` should not duplicate those reducer definitions.
