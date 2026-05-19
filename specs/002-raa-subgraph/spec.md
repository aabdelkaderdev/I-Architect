# Feature Specification: ARLO RAA Compatibility Patch

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Sections 1 and 1B only

## User Scenarios & Testing

### User Story 1 - RAA-Compatible ARLOOutput Payload (Priority: P1)

RAA can consume ARLO output directly because ARLO exposes `asrs`, `non_asr`, `condition_groups`, and `quality_weights` with the payload shapes defined in `RAA_Plan.md` Section 1.

**Why this priority**: RAA batch construction depends on full non-ASR dictionaries and condition groups; without this boundary contract, downstream RAA work cannot start reliably.

**Independent Test**: Run ARLO through parsing and graph output filtering, then confirm `ARLOOutput["non_asr"]` is a list of requirement dictionaries and `ARLOOutput["condition_groups"]` is a list of condition-group dictionaries.

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

### Edge Cases

- If there are no ASRs, `generate_embeddings` returns an empty embeddings list and does not create misleading embedding rows.
- If the shared `embeddings/` directory does not exist, ARLO creates it before writing SQLite data.
- If a requirement ID is embedded more than once, the SQLite row for that requirement ID is replaced or updated rather than duplicated.

## Requirements

### Functional Requirements

- **FR-001**: `ARLOOutput` MUST expose `non_asr` as `list[dict]`.
- **FR-002**: `ARLOOutput` MUST expose `condition_groups` as `list[dict]`.
- **FR-003**: `parse_requirements` MUST populate `non_asr` with full parsed non-ASR requirement dictionaries.
- **FR-004**: `generate_embeddings` MUST persist ASR embeddings to `embeddings/asr_embeddings.db` via SQLite after computing them.
- **FR-005**: `generate_embeddings` MUST continue returning `{"embeddings": embeddings}` for internal ARLO clustering.
- **FR-006**: The shared `embeddings/` directory MUST exist at the project root and remain ignored by Git.
- **FR-007**: Embedding vectors MUST NOT be added to `ARLOOutput`.

### Key Entities

- **ARLOOutput**: LangGraph output schema returned to the parent pipeline.
- **Non-ASR Requirement**: Parsed requirement dictionary not marked architecturally significant.
- **Condition Group**: ASR grouping payload with `nominal_condition`, `conditions`, `requirements`, and `cluster`.
- **ASR Embedding Record**: SQLite row keyed by requirement ID containing an embedding vector and metadata.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The implementation prerequisite script succeeds for `specs/002-raa-subgraph`.
- **SC-002**: ARLO output contains `non_asr` and `condition_groups` in the shapes required by `RAA_Plan.md` Section 1.
- **SC-003**: A local embedding run creates `embeddings/asr_embeddings.db` with row count equal to the ASR count.
- **SC-004**: No embedding vectors are present in `ARLOOutput`.

## Assumptions

- Scope is limited to `RAA_Plan.md` Sections 1 and 1B.
- RAA itself is not implemented by this patch.
- The project remains a Python LangGraph codebase using FastEmbed for embeddings.
- SQLite persistence is local project runtime storage, not a tracked source artifact.
