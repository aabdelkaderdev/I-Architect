# Feature Specification: RAA Requirement Normalization

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 5

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Normalization of ARLO output dicts into unified requirement schema (Priority: P1)

Developers and nodes require every input requirement (both ASR and non-ASR) to be normalized into a unified, consistent schema structure before performing embeddings, searches, or batch construction.

**Why this priority**: ARLO produces ASR and non-ASR dictionaries with different field conventions and uses raw positional integers for requirement IDs. If the field conventions are not unified or keys remain integer-based, downstream RAA nodes will fail to resolve text descriptions or lookup dependencies.

**Independent Test**: Write a unit test that feeds the normalization node sample lists of ARLO ASR and non-ASR dictionaries along with a parent requirement lookup mapping. The test verifies that all outputs conform exactly to the normalized schema fields (`id`, `text`, `is_asr`, `quality_attributes`, `condition_text`).

**Acceptance Scenarios**:

1. **Given** ARLO dictionary outputs and parent requirements mapping, **When** normalized, **Then** `id` is converted from integer to string (e.g., `1` → `"R1"`).
2. **Given** an ASR requirement, **When** normalized, **Then** `is_architecturally_significant` is renamed to `is_asr`.
3. **Given** a non-ASR requirement without a condition or quality attribute classifications, **When** normalized, **Then** `condition_text` defaults to `None`/`null` and `quality_attributes` defaults to an empty list `[]`.

---

### Edge Cases

- **Missing ID in Parent Requirements**: What happens if an ID from ARLO is not present in the parent pipeline's `requirements` dictionary? The normalizer must raise a clear `KeyError` or custom validation error to avoid inserting empty text.
- **Unexpected Fields**: The normalizer must discard any auxiliary fields present in the ARLO dictionaries to keep the unified schema clean and memory-efficient.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a normalization function/node taking ARLO's list of `asrs` and `non_asr` dictionaries, along with the parent pipeline's `requirements` lookup dictionary.
- **FR-002**: System MUST convert the `id` field from integer to the mapped string key (e.g. `id=1` -> `f"R{id}"`).
- **FR-003**: System MUST resolve the `text` field by looking up the string key in the parent pipeline's `requirements` dictionary.
- **FR-004**: System MUST rename `is_architecturally_significant` to `is_asr`.
- **FR-005**: System MUST ensure `condition_text` is present and defaults to `None`/`null` if not provided.
- **FR-006**: System MUST ensure `quality_attributes` is present and defaults to `[]` if not provided.

### Key Entities *(include if feature involves data)*

- **Unified Requirement**: The standardized dictionary schema:
  - `id`: string
  - `text`: string
  - `is_asr`: boolean
  - `quality_attributes`: list of strings
  - `condition_text`: string or null

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of input ARLO dictionary items are successfully normalized into the unified schema without field naming mismatches.
- **SC-002**: Unit tests cover successful conversions, default fallback assignments, and error cases (e.g., missing keys).

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
