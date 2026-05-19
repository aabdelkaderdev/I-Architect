# Feature Specification: RAA Validation and Testing

**Feature Branch**: `020-raa-validation-testing`

**Created**: 2026-05-19

**Status**: Draft

**Input**: User description: "Create a focused feature for RAA validation and testing. Scope strictly to RAA_Plan.md Section 19. Define the deliverable as the full unit, integration, and functional test suite covering embeddings, batches, bridges, coherence, judge, structure, and manifest completeness."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Unit Test Coverage for RAA Core Nodes (Priority: P1)

Developers must be able to run unit tests that validate the isolated behavior of the RAA nodes (preparation, batch assembly, coherence gate, entity deduplication) to ensure they correctly implement the specification and handle edge cases locally.

**Why this priority**: Catching logic errors at the unit level prevents difficult-to-debug failures in the complex downstream LangGraph coordination.

**Independent Test**: Can be fully tested by running a unit test suite targeting individual modules without invoking the full orchestration engine.

**Acceptance Scenarios**:

1. **Given** a preparation node check, **When** the `asr_embeddings.db` is missing ASR IDs, **Then** it rejects startup.
2. **Given** stale `text_hash` entries in the SQLite DB, **When** the preparation node runs, **Then** it triggers recomputation instead of silent reuse.
3. **Given** batch assembly, **When** a condition group is processed, **Then** all ASRs from that condition group are included in the batch.
4. **Given** a heterogeneous synthetic batch, **When** the coherence gate evaluates it, **Then** the batch is correctly split into sub-clusters.
5. **Given** multiple fragments with hierarchy conflicts (same ID, different parent), **When** entity deduplication operates, **Then** conflicts are detected and recorded in `open_questions`.

---

### User Story 2 - Integration Test Coverage for Cross-Batch Operations (Priority: P1)

Developers must be able to run integration tests that validate the data flow and state consistency across multiple batch runs, including bridge overlap logic and the judge's merge process.

**Why this priority**: Validates that the parallel batching mechanism and the judge's state accumulation (`running_arch_model`) work correctly end-to-end.

**Independent Test**: Can be tested by running the orchestration engine over a controlled set of 3 batches with synthetic data.

**Acceptance Scenarios**:

1. **Given** 3 batches with known overlaps, **When** processed end-to-end, **Then** bridge requirements appear in both adjacent batches.
2. **Given** sequential batches N and N+1, **When** the judge merges them, **Then** `running_arch_model` is updated and entities from N+1 do not contradict entities from N.
3. **Given** an incoherent batch, **When** the integration pipeline runs, **Then** it produces a `reduced_confidence = true` flag in the final model metadata.

---

### User Story 3 - Functional Test Coverage for Output Validation (Priority: P1)

Stakeholders must be guaranteed that the final `C4JsonModel` output strictly adheres to C4 constraints (structural integrity, scoping rules) and that the SAAM judge ranks fragments accurately.

**Why this priority**: RAA's primary deliverable is the C4-compliant JSON model. If the output structure is invalid or the SAAM scoring is flawed, the downstream Architecture Generation Agent will fail.

**Independent Test**: Can be fully tested by validating the pipeline's final JSON output against a golden fixture and a rigid schema validator.

**Acceptance Scenarios**:

1. **Given** a synthetic fragment with an orphaned component, **When** the judge processes it, **Then** a `coverage_gap` is recorded and the component is not added to the output.
2. **Given** two synthetic RAA fragments with known quality-attribute coverage profiles, **When** the SAAM judge scores them, **Then** the fragment with greater weighted coverage is ranked higher against the ground-truth expected ranking.
3. **Given** the final merged output, **When** structural integrity is verified, **Then** every container is nested inside a system, every component inside a container, and all relationship scopes are consistent with their endpoint types.
4. **Given** the final merged output, **When** manifest completeness is verified, **Then** the `diagram_manifest` length strictly equals `(2 × systems) + containers`.

### Edge Cases

- What happens when a test fixture is outdated or missing?
- How does the test suite handle locked SQLite databases during parallel unit tests?
- How do we handle floating point discrepancies when evaluating cosine similarity thresholds in tests?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The test suite MUST validate that non-ASR embeddings in `non_asr_embeddings.db` use the identical FastEmbed model version as ASR embeddings.
- **FR-002**: The test suite MUST validate that bridge requirement overlaps never exceed the hard cap of 3 per adjacent pair.
- **FR-003**: The test suite MUST validate that canonical IDs are produced in a deterministic order regardless of the input fragment order.
- **FR-004**: The test suite MUST enforce that no entity ID appears at more than one level in the final hierarchy.
- **FR-005**: The test suite MUST verify that cross-batch entities remain perfectly consistent (same ID, no contradictory directions).
- **FR-006**: The test suite MUST run without requiring external network calls to LLMs (must use synthetic/mocked LLM responses or golden fixtures for deterministic testing).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Test suite execution completes without manual intervention.
- **SC-002**: 100% of the criteria listed in RAA_Plan.md Section 19 are covered by at least one passing test case.
- **SC-003**: Test suite execution time is under 2 minutes when running sequentially (using mock LLMs and in-memory/isolated SQLite DBs).
- **SC-004**: The test suite runs automatically in CI/CD environments.

## Assumptions

- We assume a standard testing framework is used.
- We assume all tests utilize mocked LLMs or deterministic stubs (golden fixtures) to avoid relying on actual LLM inference cost and latency.
- We assume an isolated testing environment where test databases are created and dropped per run.
