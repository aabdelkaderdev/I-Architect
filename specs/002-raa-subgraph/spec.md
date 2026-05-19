# Feature Specification: ARLO RAA Compatibility & State Contracts

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Sections 1, 1B, and 4

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAA-Compatible ARLOOutput Payload (Priority: P1)

RAA can consume ARLO output directly because ARLO exposes `asrs`, `non_asr`, `condition_groups`, and `quality_weights` with the payload shapes defined in `RAA_Plan.md` Section 1.

**Why this priority**: RAA batch construction depends on full non-ASR dictionaries and condition groups; without this boundary contract, downstream RAA work cannot start reliably.

**Independent Test**: Run ARLO through parsing and confirm `ARLOOutput["non_asr"]` is a list of requirement dictionaries and `ARLOOutput["condition_groups"]` is a list of condition-group dictionaries.

**Acceptance Scenarios**:

1. **Given** parsed ARLO requirements with at least one non-ASR, **When** ARLO returns its output schema, **Then** `non_asr` contains full parsed requirement dictionaries rather than only IDs.
2. **Given** ARLO has built condition groups, **When** the parent wrapper forwards ARLO results, **Then** `condition_groups` is available unchanged to downstream consumers.

---

### User Story 2 - ASR Embedding SQLite Persistence (Priority: P1)

RAA can load ASR condition embeddings from shared SQLite storage without embedding vectors being passed through LangGraph output state.

**Why this priority**: RAA needs ASR embeddings for batch construction, while Section 1 requires vectors to remain out of downstream LangGraph state for checkpoint efficiency.

**Independent Test**: Run `generate_embeddings` with ASR inputs and confirm `embeddings/asr_embeddings.db` contains one persisted row per ASR requirement ID while the node still returns `{"embeddings": embeddings}` for ARLO clustering.

**Acceptance Scenarios**:

1. **Given** ASRs with condition text, **When** `generate_embeddings` completes, **Then** ARLO writes `embeddings/asr_embeddings.db` keyed by requirement ID.
2. **Given** embedding persistence succeeds, **When** the node returns to LangGraph, **Then** the existing `embeddings` state channel remains available for clustering.

---

### User Story 3 - Type-Safe Graph State Structure (Priority: P1)

Developers require clearly defined type annotations and Python dataclasses representing the RAA state structures so they can populate and inspect graph state safely, ensuring no typo or type mismatches.

**Why this priority**: Type-safe structures are the fundamental block of the LangGraph state. Without them, we cannot configure state channels, reducers, or compile the graph.

**Independent Test**: Write a unit test that instantiates all defined dataclasses and the State schema TypedDict, checking field names and types.

**Acceptance Scenarios**:

1. **Given** a set of RAA dataclass definitions, **When** they are instantiated with matching types, **Then** no type errors occur.
2. **Given** the TypedDict representation of the RAA graph state, **When** we inspect the keys and types, **Then** all channels specified in `RAA_Plan.md` Section 4 are present and match their spec-defined types.

---

### User Story 4 - State Channel Reducers for Parallel Execution (Priority: P2)

Developers require State channels that receive writes from multiple nodes in the same super-step (such as `batch_outputs` and `open_questions`) to correctly merge outputs instead of overwriting.

**Why this priority**: Without correct reducers, LangGraph will apply last-write-wins semantics, which would silently discard outputs from parallel subgraphs.

**Independent Test**: Write unit tests verifying that writing to `batch_outputs` and `open_questions` from multiple concurrent sources merges the data as expected rather than overwriting.

**Acceptance Scenarios**:

1. **Given** a state with an empty `open_questions` list, **When** two nodes write lists of `OpenQuestion`s, **Then** they are concatenated together.
2. **Given** a state with empty `batch_outputs` dict, **When** parallel subgraphs write to `batch_outputs` for the same batch, **Then** their fragments are accumulated in a list under the batch key.

---

### User Story 5 - JsonPlusSerializer-Compatible Serialization (Priority: P3)

Operators require that the full state (including deeply nested custom dataclasses like `ArchModel` and `ArchFragment`) is fully serializable by LangGraph's `JsonPlusSerializer` so that checkpointers can write them to SQLite.

**Why this priority**: Enables checkpointing and crash recovery without requiring manual custom serializer registrations or custom codecs.

**Independent Test**: Write a unit test that serializes the state to a JSON-like representation using `JsonPlusSerializer` and deserializes it back to identical dataclass instances.

**Acceptance Scenarios**:

1. **Given** an `ArchModel` instance with deeply nested systems, containers, components, and relationships, **When** serialized via `JsonPlusSerializer`, **Then** it can be serialized and deserialized back to identical dataclass objects without loss of hierarchy or data.

---

### Edge Cases

- **No ASRs**: If there are no ASRs, `generate_embeddings` returns an empty embeddings list and does not create misleading embedding rows.
- **Shared Directory Missing**: If the shared `embeddings/` directory does not exist, ARLO creates it before writing SQLite data.
- **Duplicate Embedded ID**: If a requirement ID is embedded more than once, the SQLite row for that requirement ID is replaced or updated rather than duplicated.
- **Container/Component Parent Conflict**: What happens if two subgraphs propose the same container/component ID but associate it with different parent systems or containers? The system must detect these hierarchy conflicts during merging and log them as `hierarchy_conflict` open questions.
- **Orphan Entities**: What happens if a subgraph proposes a component whose parent container is not in the fragment and not in the running architecture model? The system must prevent orphan entities from entering the merged output and flag them as `coverage_gap` in open questions.
- **Stale or Invalid Serialization Types**: What happens if Python dataclasses contain fields that cannot be serialized by `JsonPlusSerializer`? The dataclass field types must be strictly limited to primitives, lists, dicts, and other serializable dataclasses.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `ARLOOutput` MUST expose `non_asr` as `list[dict]`.
- **FR-002**: `ARLOOutput` MUST expose `condition_groups` as `list[dict]`.
- **FR-003**: `parse_requirements` MUST populate `non_asr` with full parsed non-ASR requirement dictionaries.
- **FR-004**: `generate_embeddings` MUST persist ASR embeddings to `embeddings/asr_embeddings.db` via SQLite after computing them.
- **FR-005**: `generate_embeddings` MUST continue returning `{"embeddings": embeddings}` for internal ARLO clustering.
- **FR-006**: The shared `embeddings/` directory MUST exist at the project root and remain ignored by Git.
- **FR-007**: Embedding vectors MUST NOT be added to `ARLOOutput`.
- **FR-008**: System MUST define the dataclass schemas for `ArchModel`, `ArchFragment`, `ArchSystem`, `ArchContainer`, `ArchComponent`, `ArchPerson`, `ArchExternalSystem`, `ArchRelationship`, `ArchPattern`, `OpenQuestion`, `IncoherentBatchRecord`, and `ConfidenceRecord` exactly as defined in `RAA_Plan.md` §4.
- **FR-009**: System MUST define the LangGraph state channels using a TypedDict containing:
  - `batch_queue`: `list[Batch]`
  - `batch_cursor`: `int`
  - `batch_outputs`: `dict[int, list[ArchFragment]]`
  - `best_batch_output`: `dict[int, ArchFragment]`
  - `running_arch_model`: `ArchModel`
  - `open_questions`: `list[OpenQuestion]`
  - `bridge_requirements`: `dict[tuple, list[str]]`
  - `incoherent_batches`: `list[IncoherentBatchRecord]`
  - `embeddings_ready`: `bool`
- **FR-010**: System MUST define and configure appropriate reducer functions for multi-writer channels (`batch_outputs` appending/merging per key, `open_questions` list addition, `incoherent_batches` list addition).
- **FR-011**: All dataclass definitions MUST be compatible with LangGraph's default `JsonPlusSerializer` to support seamless serialization/deserialization for SQLite checkpoints.
- **FR-012**: All dataclasses MUST support serialization/deserialization to standard dictionaries/JSON to facilitate C4-compliant JSON conversion for the final output.

### Key Entities *(include if feature involves data)*

- **ARLOOutput**: LangGraph output schema returned to the parent pipeline.
- **Non-ASR Requirement**: Parsed requirement dictionary not marked architecturally significant.
- **Condition Group**: ASR grouping payload with `nominal_condition`, `conditions`, `requirements`, and `cluster`.
- **ASR Embedding Record**: SQLite row keyed by requirement ID containing an embedding vector and metadata.
- **ArchModel**: The accumulated architecture model in hierarchical form. Contains lists of `systems`, `persons`, `external_systems`, `patterns`, and `open_questions`.
- **ArchFragment**: A partial architecture model representing a single strategy subgraph's output, using a semi-flat structure with explicit parent ID fields for easier merging.
- **ArchSystem**: A software system under design. Contains its `containers` and `context_relationships`.
- **ArchContainer**: A deployable unit within a system. Contains its `components` and `container_relationships`.
- **ArchComponent**: An internal building block within a container. Contains its `component_relationships`.
- **ArchRelationship**: A directed relationship between C4 elements, with a `diagram_scope` value indicating where it is visible (`context`, `container`, or `component`).
- **OpenQuestion**: Unresolved or conflicting item flagged during graph runs (e.g. `change_risk`, `hierarchy_conflict`, `coverage_gap`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The implementation prerequisite script succeeds for `specs/002-raa-subgraph`.
- **SC-002**: ARLO output contains `non_asr` and `condition_groups` in the shapes required by `RAA_Plan.md` Section 1.
- **SC-003**: A local embedding run creates `embeddings/asr_embeddings.db` with row count equal to the ASR count.
- **SC-004**: No embedding vectors are present in `ARLOOutput`.
- **SC-005**: 100% of defined dataclasses can be successfully serialized and deserialized via `JsonPlusSerializer` without data loss.
- **SC-006**: Replaced/merged state channel updates from concurrent subgraphs complete in under 10ms of processing time.
- **SC-007**: Zero static analysis (e.g., mypy) type check errors across all state definitions.
- **SC-008**: Merged state channels and dataclasses preserve hierarchical C4 structure without orphan elements or mismatched IDs.

## Assumptions

- Scope is limited to `RAA_Plan.md` Sections 1, 1B, and 4.
- RAA runtime nodes are not implemented by this patch.
- The project remains a Python LangGraph codebase using FastEmbed for embeddings.
- SQLite persistence is local project runtime storage, not a tracked source artifact.
- Standard LangGraph `JsonPlusSerializer` is used for checkpointers without custom extensions.
- All IDs are string-typed.
