# Feature Specification: RAA Batch Coherence Gate

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 10

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evaluate batch coherence, split if incoherent, or flag with reduced confidence (Priority: P1)

Downstream parallel analysis subgraphs require requirement batches to be semantically cohesive. For each requirement batch, the system computes the average cosine similarity of all its requirements to its centroid. If this score is >= 0.55, the batch is considered coherent. If it is < 0.55, we split it into 2 sub-clusters and re-evaluate each. If both pass, we replace the batch with the two sub-batches. If any sub-cluster still fails, the batch is flagged with `reduced_confidence = true` and routed to run as a single-RAA batch instead of three-parallel.

**Why this priority**: Semantic drift in batches leads to low-quality LLM prompts containing unrelated requirements, which causes poor architecture suggestions and contradictory decisions.

**Independent Test**: Write a unit test that verifies that a cohesive batch passes, a slightly incoherent batch splits into two passing sub-batches, and a highly incoherent batch that fails split re-evaluation is marked with `reduced_confidence = true`.

**Acceptance Scenarios**:

1. **Given** a batch with average intra-batch similarity >= 0.55, **When** checked, **Then** it passes the gate as coherent.
2. **Given** a batch with similarity < 0.55, **When** evaluated, **Then** it is split into 2 sub-batches.
3. **Given** a split where both sub-batches have similarity >= 0.55, **When** evaluated, **Then** they replace the original batch.
4. **Given** a split where either sub-batch has similarity < 0.55, **When** evaluated, **Then** the original batch is routed to the incoherent list with `reduced_confidence = true`.

---

### Edge Cases

- **Small Batches**: If a batch contains 2 or fewer requirements, it cannot be meaningfully split or may trivially show high similarity. In this case, the batch automatically passes the coherence gate.
- **Failed Sub-clusters**: If the sub-clusters still do not meet the 0.55 similarity threshold, the original batch must not split further and is flagged as incoherent.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST compute the intra-batch coherence score as the average cosine similarity between all requirement embeddings in the batch and its centroid.
- **FR-002**: System MUST pass the batch as coherent if the coherence score is >= 0.55.
- **FR-003**: System MUST split the batch into two sub-batches if the coherence score is < 0.55.
- **FR-004**: System MUST replace the original batch with the two sub-batches if both sub-batches have a coherence score >= 0.55.
- **FR-005**: System MUST flag the original batch with `reduced_confidence = true` if either split sub-batch has a coherence score < 0.55.
- **FR-006**: System MUST record incoherent batches in the pipeline state under the dictionary key `incoherent_batches`.

### Key Entities *(include if feature involves data)*

- **Coherence Score**: The average intra-batch cosine similarity of all requirement embeddings in the batch to the batch centroid.
- **Incoherent Batch Entry**: Object containing the original batch ID/metadata, the calculated coherence score, and the `reduced_confidence` flag.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every batch is evaluated for coherence.
- **SC-002**: Splitting and reduced-confidence flagging are correctly applied according to thresholds.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
