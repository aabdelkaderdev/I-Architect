# Feature Specification: RAA LangGraph Skeleton

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Sections 3 and 4

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run the RAA LangGraph pipeline up to batch queue ordering (Priority: P1)

Downstream orchestrators require a single compiled graph interface to process requirements. The main LangGraph skeleton initializes the execution state, validates that `embeddings_ready` is true, and routes the payload sequentially through preparation, batch construction, overlap bridging, batch coherence gating, and batch queue ordering. The pipeline state is modified and tracked at each step using LangGraph state reducers.

**Why this priority**: Without the outer graph skeleton, individual analysis nodes cannot be executed sequentially or pass state.

**Independent Test**: Write a unit test that feeds raw input to the RAA graph skeleton, mocks the intermediate node executions, and asserts that the graph compiles, executes, reduces state keys correctly, and outputs a valid `batch_queue`.

**Acceptance Scenarios**:

1. **Given** `embeddings_ready` is false, **When** graph is executed, **Then** it halts or raises an error.
2. **Given** valid inputs, **When** executed, **Then** all nodes (preparation, batch construction, overlap bridging, coherence gate, batch queue ordering) are visited in sequence.
3. **Given** state updates, **When** nodes execute, **Then** state keys (such as `embeddings_ready`, `batch_queue`, `bridge_requirements`, `incoherent_batches`) are merged/reduced properly.

---

### Edge Cases

- **Missing Required Inputs**: If essential input keys (e.g. raw requirements list or condition groups mapping) are missing from the input state, the graph aborts immediately with a clear validation exception.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define the main LangGraph skeleton in `raa/graphs/main_graph.py`.
- **FR-002**: System MUST validate that `embeddings_ready` state is true before proceeding.
- **FR-003**: System MUST use the authoritative `RAAState` schema from `raa/state/channels.py` as the LangGraph state, including: `batch_queue`, `batch_cursor`, `running_arch_model`, `bridge_requirements`, `embeddings_ready`, `open_questions`, `incoherent_batches`, `batch_outputs`, `best_batch_output` plus reused ARLO channels.
- **FR-004**: System MUST use LangGraph state reducers to append/merge lists and update state properties.
- **FR-005**: System MUST wire the nodes sequentially: Preparation -> Batch Construction -> Overlap Bridging -> Coherence Gate -> Batch Queue Ordering. Section 3 steps 6 (execution loop) and 7 (final merge) remain future downstream graph phases and are not wired by this feature.

### Key Entities *(include if feature involves data)*

- **Main Graph**: The compiled LangGraph instance.
- **Graph State**: The shared dictionary/state object containing pipeline variables.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The LangGraph skeleton compiles successfully.
- **SC-002**: Running the compiled graph with mocked node outputs executes all steps in sequence and returns the correct sorted `batch_queue`.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
