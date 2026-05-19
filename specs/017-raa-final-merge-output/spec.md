# Feature Specification: RAA Final Merge and Output

**Feature Branch**: `017-raa-final-merge-output`

**Created**: 2026-05-19

**Status**: Draft

**Input**: User description: "Create a focused feature for final merge and RAA output. Scope strictly to RAA_Plan.md Section 16. Define the deliverable as global merge, scoped reconciliation, C4 JSON validation, diagram_manifest generation, and arch_model.json filesystem output."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Global Merge and Scoped Reconciliation (Priority: P1)

After all batches have finished execution, the pipeline must synthesize all individual batch outputs (`best_batch_output`) and the final `running_arch_model` into a single unified architecture model. The system applies the 4-step deterministic merge algorithm globally. Any remaining conflicts, ties, or coverage gaps recorded in `open_questions` are resolved via a single focused LLM reconciliation pass using `llm_judge` (avoiding a full re-analysis and strictly addressing the listed conflicts).

**Why this priority**: Without a global merge and reconciliation step, the final architecture output would remain fragmented across batches, with unresolved conflicts, and would not represent a unified system model.

**Independent Test**: Write a unit test that takes multiple mock batch outputs containing conflicting details (e.g. conflicting container parent assignments or relationship scopes) and some unresolved open questions. Verify that:
- The global merge executes successfully.
- The LLM reconciliation pass resolves the open questions.
- A single coherent `ArchModel` is returned.

**Acceptance Scenarios**:

1. **Given** multiple `best_batch_output` fragments, **When** the final merge node is invoked, **Then** a global deterministic merge combines all systems, containers, components, persons, external systems, and relationships.
2. **Given** outstanding conflicts in `open_questions` after the global merge, **When** the reconciliation pass runs, **Then** `llm_judge` is used to resolve them, updating the merged model and clearing resolved questions.

---

### User Story 2 - C4 JSON Validation and Diagram Manifest Generation (Priority: P2)

The system must validate the finalized architecture model to guarantee structural integrity before downstream consumption. It must ensure nested hierarchies (systems containing containers containing components), verify that relationship endpoints exist, check that relationship scopes correspond to endpoint types, and prevent duplicate IDs across hierarchical levels. It also deterministically generates a work queue for the Architecture Generation Agent (AGA) as `diagram_manifest`, containing exactly one context diagram per system, one container diagram per system, and one component diagram per container.

**Why this priority**: Ensuring that the JSON output is valid C4 prevents the downstream rendering stage (AGA) from crashing on malformed structures. The `diagram_manifest` decouples AGA from hierarchy parsing logic.

**Independent Test**: Provide a merged model with a custom structure. Verify that:
- Validation fails if there are orphan components, invalid relationship endpoints, or scope mismatches.
- For a valid structure, the generated `diagram_manifest` has exactly `(2 * num_systems) + num_containers` entries with correct type and focus entity IDs.

**Acceptance Scenarios**:

1. **Given** an invalid C4 hierarchy (e.g. an orphaned container with no parent system ID, or relationship endpoints referencing non-existent entities), **When** validation runs, **Then** a validation error is raised.
2. **Given** a valid hierarchical model, **When** generating the manifest, **Then** the `diagram_manifest` is constructed with correct `diagram_id`, `diagram_type`, `focus_entity_id`, and `label` for each entry.

---

### User Story 3 - Filesystem Output and Checkpoint Archiving (Priority: P3)

The finalized C4-compliant JSON model must be written to the project-scoped output directory. The output path is provided dynamically by the orchestrator at runtime. After the model is written and validated successfully, the SQLite checkpoint database is moved from its active path to an archive directory to prevent unbounded database growth while preserving the run history.

**Why this priority**: Writing the output to the correct filesystem path is the final deliverable. Archiving the checkpoint completes the execution lifecycle cleanly.

**Independent Test**: Execute the output writing node with a mocked output directory and checkpoint path. Verify that:
- `arch_model.json` is successfully written to `projects/{project_name}/output/raa/arch_model.json`.
- The active checkpoint DB is archived to the archive subdirectory `projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db` only after output validation succeeds.

**Acceptance Scenarios**:

1. **Given** a validated model, **When** output is written, **Then** the JSON file is saved to the orchestrator-provided path.
2. **Given** successful output writing, **When** the run completes, **Then** the checkpoint DB is moved to the archive folder.

---

### Edge Cases

- **Reconciliation Failures**: If the LLM reconciliation pass returns invalid JSON or violates the C4 schema, the system must reject the result, fall back to preserving the conflicts in `open_questions`, and log a warning.
- **Incoherent Batch Confidence**: Entities originating from incoherent batches (flagged with `reduced_confidence`) must have their `reduced_confidence` flag and metadata persisted in the final `confidence_metadata` dict.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST perform a global merge of all `best_batch_output` fragments and the final `running_arch_model`.
- **FR-002**: System MUST run a single, focused reconciliation pass using `llm_judge` to resolve outstanding `open_questions` before final schema validation.
- **FR-003**: System MUST validate the final merged model against the C4 schema, ensuring:
  - Strict system -> container -> component hierarchy nesting.
  - No orphan containers (must have a valid parent system) or components (must have a valid parent container).
  - No entity ID is shared across different levels of the hierarchy.
  - All relationship `source_id` and `target_id` resolve to existing entities.
  - Every relationship's `diagram_scope` matches endpoint types (`context` for system/person/external system, `container` for container/person/external system, `component` for component/container/external system).
- **FR-004**: System MUST deterministically generate a `diagram_manifest` work queue containing context, container, and component diagram entries.
- **FR-005**: System MUST serialize and write the final merged C4 model to `projects/{project_name}/output/raa/arch_model.json`.
- **FR-006**: System MUST receive the output directory path dynamically from the orchestrator and must not hardcode default paths.
- **FR-007**: System MUST move the SQLite checkpoint database to an archive subdirectory (`projects/{project_name}/checkpoints/archive/{thread_id}/raa_graph.db`) after successful validation and output writing.

### Key Entities *(include if feature involves data)*

- **ArchModel**: The hierarchical model containing `systems`, `persons`, `external_systems`, `patterns`, `diagram_manifest`, `confidence_metadata`, and `open_questions`.
- **DiagramManifestEntry**: Entry specifying `diagram_id`, `diagram_type` (`context`, `container`, or `component`), `focus_entity_id`, and `label`.
- **ConfidenceRecord**: Metadata for confidence, tracking `reduced_confidence`, `source_batch`, and `saam_score` per entity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The global deterministic merge succeeds in combining all batch fragments.
- **SC-002**: All outstanding conflicts in `open_questions` are either resolved by the reconciliation pass or retained with a warning, without blocking output generation.
- **SC-003**: Generated `diagram_manifest` length matches the expected count: `(2 * number of systems) + total number of containers`.
- **SC-004**: The file `arch_model.json` is successfully written to the output directory and matches the `C4JsonModel` schema.
- **SC-005**: Checkpoint databases are archived correctly.

## Assumptions

- The branch `017-raa-final-merge-output` is created for this feature.
- The output directory and active checkpointer database paths are provided by the orchestrator at runtime.
