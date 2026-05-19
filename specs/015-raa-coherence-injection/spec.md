# Feature Specification: RAA Cross-Batch Coherence Injection

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 15

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Inject serialized running architecture model as hard constraints into subgraph prompt payloads (Priority: P1)

Downstream subgraphs must avoid contradicting or duplicating architectural elements created in earlier execution steps. Before invoking subgraphs for a batch, the system serializes the current `running_arch_model` state into a nested C4 hierarchical tree (Software Systems with their Containers, and Containers with their Components) along with existing relationships. This tree is injected into each subgraph prompt payload with the following prefix:

`The following components and relationships are already part of the architecture model. You must be consistent with them. Do not rename, restructure, or contradict any listed entity or relationship.`

**Why this priority**: Preventing naming collisions and contradictory architectural structures is required to ensure successive merge cycles remain clean and consistent.

**Independent Test**: Write a unit test that verifies that for a given hierarchical `running_arch_model` state, the serialization function outputs a readable tree representation, and the injection helper integrates it into the prompt payload of the parallel subgraphs.

**Acceptance Scenarios**:

1. **Given** an empty `running_arch_model` state, **When** serialized, **Then** it produces an empty or minimal notification string.
2. **Given** a populated hierarchical `running_arch_model` state (systems, containers, components, relationships), **When** serialized, **Then** it produces a structured C4 tree showing nesting structure and relationships.
3. **Given** the serialized string, **When** injected, **Then** it is prefixed with the mandated constraint warning.

---

### Edge Cases

- **Missing Entities**: If relationships reference entities that are not nested in the systems tree (e.g. human actors or external systems), they must still be serialized in a separate "External Entities" section.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement the hierarchical serialization of `running_arch_model` in `raa/utils/model_serializer.py`.
- **FR-002**: System MUST structure the serialization as a nested tree: Software Systems -> Containers -> Components, along with their relationships.
- **FR-003**: System MUST prefix the injected constraints with the exact string:
  `The following components and relationships are already part of the architecture model. You must be consistent with them. Do not rename, restructure, or contradict any listed entity or relationship.`
- **FR-004**: System MUST inject the serialized constraints text into each strategy's prompt context.

### Key Entities *(include if feature involves data)*

- **Running Architecture Model**: The current consolidated architecture state representing merged system elements.
- **Serialized Model Constraints**: The text string containing the nested C4 tree and prefix constraint statement.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The running architecture model is correctly formatted into a nested C4 text tree.
- **SC-002**: All strategy prompts for subgraphs include the serialized model constraints.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
