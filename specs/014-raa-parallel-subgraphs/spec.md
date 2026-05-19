# Feature Specification: RAA Parallel Subgraphs

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 12

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Invoke three parallel RAA subgraphs with dedicated LLM instances (Priority: P1)

Downstream pipeline execution requires analyzing batches from multiple architectural perspectives. The main graph triggers three parallel RAA subgraph executions using LangGraph's `Send` API: RAA-A (SAAM-first), RAA-B (Pattern-driven), and RAA-C (Entity-driven). The conditional routing edge extracts dedicated `ChatModel` instances from the invocation `context` and constructs three `Send` objects containing the respective LLM configurations. Each subgraph executes its reasoning and returns a partial architecture fragment (`ArchFragment`).

**Why this priority**: Running diverse strategy subgraphs in parallel is the core mechanism to generate robust, multi-perspective architectural proposals for the merge phase.

**Independent Test**: Write a unit test that mocks the three subgraphs, sets up the config/context containing simulated LLMs, executes the fan-out edge, and verifies that three separate `Send` payloads are successfully generated with correct assigned LLMs and batch data.

**Acceptance Scenarios**:

1. **Given** a normal batch, **When** evaluated at the conditional edge, **Then** three parallel `Send` payloads (for RAA-A, RAA-B, and RAA-C) are emitted.
2. **Given** an incoherent batch (`reduced_confidence = true`), **When** evaluated, **Then** only a single `Send` payload (defaulting to RAA-A) is emitted.
3. **Given** LLM configs in the invocation context, **When** a subgraph executes, **Then** it retrieves and uses its designated `ChatModel` instance from context.
4. **Given** subgraph completions, **When** outputs are returned, **Then** each subgraph returns a schema-compliant `ArchFragment` with resolved parent links.

---

### Edge Cases

- **Missing Subgraph LLM**: If a specific LLM instance is not defined in the context (e.g. `llm_raa_b` is missing), the pipeline falls back to using the default system LLM or raises a detailed configuration exception.
- **Orphan Entity Prevention**: If a subgraph proposes a component, it must also specify its parent container ID. If the container is new, it must specify its parent system ID. Subgraphs must never return components or containers without valid parent links.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement the three parallel subgraphs under `raa/graphs/subgraphs/raa_a.py`, `raa/graphs/subgraphs/raa_b.py`, `raa/graphs/subgraphs/raa_c.py`, and the Send routing helper in `raa/graphs/subgraphs/routing.py`.
- **FR-002**: System MUST wire the conditional fan-out edge to parallelize RAA-A, RAA-B, and RAA-C using the `Send` API.
- **FR-003**: System MUST route incoherent batches (`reduced_confidence = true`) to a single RAA-A subgraph run.
- **FR-004**: System MUST inject LLM instances from the invocation `context` dictionary and never store them in serialization checkpoints.
- **FR-005**: System MUST define the output of each subgraph as a partial `ArchFragment` containing systems, containers, components, persons, relationships, patterns, and rationale.
- **FR-006**: System MUST enforce container parent assignment (`parent_system_id`) and component parent assignment (`parent_container_id`) in the generated `ArchFragment` to prevent orphaned entities.

### Key Entities *(include if feature involves data)*

- **Send Payload**: LangGraph execution wrapper containing the batch data and the designated subgraph LLM context.
- **ArchFragment**: A data dictionary representing partial systems, containers, components, relationships, patterns, and rationale.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The parallel subgraphs execute concurrently via the `Send` API.
- **SC-002**: Every subgraph successfully returns a valid, parent-resolved `ArchFragment`.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
