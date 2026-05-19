# Feature Specification: RAA Batch Construction

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 8 and Section 3 steps 1-2

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Assemble requirement batches per condition group (Priority: P1)

Downstream RAA nodes require requirements to be grouped into focused batches to perform parallel strategy analysis. For each ARLO condition group, we compute a centroid vector (the average of its ASR requirements' vectors), search the non-ASR database for similar requirements, filter by a cosine similarity threshold of >= 0.65, cap at max 10 candidates, and output the final batch payload.

**Why this priority**: Correct batching ensures that LLMs process cohesive requirement clusters. Incorrect grouping results in fragmented architecture suggestions and missing context.

**Independent Test**: Write a unit test that verifies that for a given condition group, the centroid is correctly calculated, ANN returns matching requirements with similarity scores >= 0.65, candidates are capped at 10, and the final payload contains the correct group ID and requirement IDs.

**Acceptance Scenarios**:

1. **Given** a condition group with multiple ASRs, **When** centroid is computed, **Then** the centroid is the element-wise mathematical average of their ASR vectors.
2. **Given** a centroid vector, **When** searching non-ASRs, **Then** only non-ASRs with a cosine similarity >= 0.65 are kept as candidates.
3. **Given** more than 10 matching candidates, **When** selected, **Then** the candidates list is capped at the top 10 most similar.
4. **Given** a condition group with no ASRs, **When** processed, **Then** the system falls back to re-embedding the group's `nominal_condition` on the fly to use as the centroid.

---

### Edge Cases

- **Zero ASRs in Condition Group**: The batch generator must resolve the group centroid by re-embedding the group's `nominal_condition` using the FastEmbed model.
- **Empty Candidate Pool**: If no non-ASR requirements match the similarity threshold of 0.65, the batch payload is constructed with only ASR requirements, without raising errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST compute the centroid vector for each condition group by averaging the vectors of its ASR requirements.
- **FR-002**: System MUST fall back to re-embedding the group's `nominal_condition` on the fly using FastEmbed if the group contains no ASR requirements.
- **FR-003**: System MUST search `embeddings/non_asr_embeddings.db` using the centroid vector.
- **FR-004**: System MUST filter search results keeping only non-ASR requirements with cosine similarity >= 0.65.
- **FR-005**: System MUST cap the selected non-ASR candidates at a maximum of 10 per condition group.
- **FR-006**: System MUST output a list of batch payload dictionaries, each containing: `group_id`, `centroid`, `asr_ids`, `non_asr_candidates` (with their similarity scores).

### Key Entities *(include if feature involves data)*

- **Condition Group**: The ARLO output cluster definition containing ASR condition IDs and text.
- **Batch Payload**: The assembled object containing the target group ID, centroid, ASR requirements, and selected non-ASR requirements.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Batch assembly correctly generates a batch payload for every input condition group.
- **SC-002**: Verification matches that similarity filters and candidate caps are strictly enforced.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
- SQLite files `embeddings/asr_embeddings.db` and `embeddings/non_asr_embeddings.db` exist and contain vectors.
