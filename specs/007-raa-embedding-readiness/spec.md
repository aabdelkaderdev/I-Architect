# Feature Specification: RAA Preparation & Embedding Readiness

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 6

## User Scenarios & Testing *(mandatory)*

### User Story 1 - ASR embedding verification and non-ASR embedding persistence (Priority: P1)

Downstream RAA nodes (batch construction, overlap bridging, coherence gate) require that all requirement vector embeddings are generated and available in the vector space before executing search operations.

**Why this priority**: If vector embeddings are missing, incomplete, or created using mismatching models, similarity search results will be random, resulting in incoherent requirements batches.

**Independent Test**: Write a unit test that verifies that ASR requirements exist in `embeddings/asr_embeddings.db`, embeds non-ASR requirements to `embeddings/non_asr_embeddings.db` using FastEmbed's `mixedbread-ai/mxbai-embed-large-v1` model, and asserts that the `embeddings_ready` state flag is set to `True`.

**Acceptance Scenarios**:

1. **Given** ASR requirements, **When** checked, **Then** the system throws an error if any ASR does not have a corresponding vector row in the database.
2. **Given** non-ASR requirements, **When** processed, **Then** the system embeds their description text and writes them to the SQLite database.
3. **Given** both checks pass, **When** finished, **Then** `embeddings_ready` is set to `True`.

---

### Edge Cases

- **Missing ASR in Database**: If an ASR from the state channel does not have a matching database entry, the preparation node must abort execution and raise an exception advising the operator to re-run the ARLO pipeline.
- **Database Locks**: If multiple reads/writes occur concurrently on the SQLite files, the connection must be opened with Write-Ahead Logging (WAL) enabled to prevent lock timeouts.
- **Redundant Generation**: To prevent unnecessary CPU/GPU usage, existing non-ASR embeddings must be cached and re-used based on the requirement text hash or ID.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify that `embeddings/asr_embeddings.db` contains a row for every input ASR requirement (checking by original string ID).
- **FR-002**: System MUST throw an operational error if any input ASR has no corresponding vector row in the database.
- **FR-003**: System MUST embed all input non-ASR requirements using the `mixedbread-ai/mxbai-embed-large-v1` model.
- **FR-004**: System MUST write the non-ASR embeddings into `embeddings/non_asr_embeddings.db`.
- **FR-005**: Both SQLite databases (`asr_embeddings.db` and `non_asr_embeddings.db`) MUST be configured to run in Write-Ahead Logging (WAL) mode.
- **FR-006**: System MUST check if non-ASR embeddings already exist in the database (cache hit) before calling the embedding model to avoid redundant embedding generations.
- **FR-007**: System MUST set `embeddings_ready = True` in the LangGraph state channels upon successful completion of verification and embedding.

### Key Entities *(include if feature involves data)*

- **ASR Database**: SQLite table mapping ASR IDs to float arrays representing vectors.
- **Non-ASR Database**: SQLite table mapping non-ASR IDs to float arrays representing vectors.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All requirements in the input lists have their vectors populated in their respective SQLite database files.
- **SC-002**: Verification raises a prompt error if a required ASR vector is missing.
- **SC-003**: `embeddings_ready` flag is set to `True` after verification and generation.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
- SQLite files are stored under the `embeddings/` directory at the project root.
