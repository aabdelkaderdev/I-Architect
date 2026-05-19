# Feature Specification: RAA Overlap Bridging

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 9

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Identify and inject bridge requirements between adjacent groups (Priority: P1)

Downstream RAA nodes executing parallel analysis need shared base components to be discovered collectively. For each pair of adjacent condition groups (identified by centroid similarity above a threshold), the system calculates non-ASR relevance scores to both centroids, selects 1–3 top bridge requirements, injects them into both batches, and records them in a `bridge_requirements` registry mapping.

**Why this priority**: Without overlap bridging, subgraphs executing in parallel will produce isolated architecture designs, missing opportunities to reuse base utilities (e.g. database connections, middleware, or authorization layers).

**Independent Test**: Write a unit test that mock-calculates cosine similarities between non-ASRs and two centroids, verifies that adjacent groups are detected, asserts that between 1 and 3 requirements are chosen as bridges, injects them into both batches, and registers them in the `bridge_requirements` dictionary.

**Acceptance Scenarios**:

1. **Given** two condition groups, **When** centroids similarity is checked, **Then** they are adjacent if their similarity score exceeds the adjacency threshold.
2. **Given** adjacent groups, **When** scoring bridges, **Then** each non-ASR candidate receives a score based on its combined similarity to both centroids.
3. **Given** candidate bridges, **When** selected, **Then** 1 to 3 candidate IDs are selected as bridges, with a hard cap of 3.
4. **Given** selected bridges, **When** batches are finalized, **Then** those bridge requirements are added to both batch lists and recorded under `bridge_requirements` in the pipeline state.

---

### Edge Cases

- **No Adjacent Groups**: If no centroids exceed the adjacency similarity threshold, the overlap bridging step finishes without selecting any bridge requirements, leaving `bridge_requirements` empty without throwing errors.
- **Sparse Candidates**: If fewer than 3 candidates have high similarity to both centroids, the utility selects only the available qualifying candidates (including zero), and does not crash.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST identify adjacent or related condition groups by comparing their centroid similarity.
- **FR-002**: System MUST compute a bridging score for non-ASR requirements based on their similarity to both group centroids.
- **FR-003**: System MUST select between 1 and 3 bridge requirements per adjacent pair, enforcing a hard cap of 3.
- **FR-004**: System MUST inject the selected bridge requirement IDs into both corresponding batches.
- **FR-005**: System MUST record the bridging mappings in the pipeline state under the dictionary key `bridge_requirements` (keyed by the pair identifier string, e.g. `"groupA-groupB"`).

### Key Entities *(include if feature involves data)*

- **Adjacency Mapping**: Pair of condition groups whose centroids are close in vector space.
- **Bridge Requirements Registry**: State variable `bridge_requirements` tracking the list of shared requirement IDs per pair.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Adjacent groups are correctly identified and have bridge requirements selected.
- **SC-002**: Bridge requirements are successfully added to both batch lists.
- **SC-003**: The `bridge_requirements` dictionary contains the mapping of injected IDs.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
- Adjacency similarity threshold is set to a default value of 0.50 unless otherwise specified.
