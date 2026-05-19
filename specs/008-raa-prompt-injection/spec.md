# Feature Specification: RAA Prompt Constraint Injection Policy

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 7 and 21C

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retrieval of node-specific C4 and SAAM prompt excerpts by tags (Priority: P1)

Downstream RAA subgraph execution nodes require a prompt injection mechanism to retrieve only the specific prompt excerpt text files associated with their execution tags (e.g. Entity extraction node requests `c4:levels` and `c4:notation`), rather than injecting the entire prompt resource bundle.

**Why this priority**: Bloating prompt contexts degrades LLM compliance with C4 and SAAM guidelines and increases token overhead. Focused excerpt injection keeps context windows minimal and guides subgraphs efficiently.

**Independent Test**: Write a unit test that verifies that mapping tags (such as `c4:levels`) returns the correct content of the corresponding excerpt file (`c4_levels.txt`), and that calling the injection helper for specific nodes retrieves the exact subset of tags defined in the mapping matrix.

**Acceptance Scenarios**:

1. **Given** a tag name, **When** queried, **Then** the retrieval utility returns the exact text contents of the corresponding file under `raa/prompts/excerpts/`.
2. **Given** a node name, **When** queried, **Then** the system retrieves only the specific list of tags configured for that node in Section 21C.
3. **Given** a non-existent tag, **When** queried, **Then** the retrieval utility raises a clear exception (e.g. `FileNotFoundError`).

---

### Edge Cases

- **Missing Tag Mapping**: If a node requests a tag that doesn't exist in the file system, the utility must raise a clear exception.
- **Whitespace formatting in files**: The utility must strip leading and trailing whitespace from the loaded excerpt text before injecting it into the prompt.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define a prompt retrieval helper function/module taking a tag string (e.g., `"c4:levels"`) and returning the string content of the corresponding excerpt file (`raa/prompts/excerpts/c4_levels.txt`).
- **FR-002**: System MUST map tag colons to file name underscores (e.g. `c4:levels` -> `c4_levels.txt`).
- **FR-003**: System MUST define a node-to-tag mapping configuration matching the matrix in Section 21C:
  - Entity extraction -> `c4:levels`, `c4:notation`
  - Relationship extraction -> `c4:notation`, `c4:technology`
  - Pattern selection -> `c4:levels`
  - SAAM tradeoff (judge) -> `saam:steps`, `saam:scenarios`
  - Final merge / reconciliation -> `c4:levels`, `c4:notation`, `c4:technology`
- **FR-004**: System MUST expose a helper to construct system/user prompt snippets containing the C4 and SAAM constraints retrieved for a given node.
- **FR-005**: All prompt constraint lookups MUST be read-only and raise standard python errors on missing assets.

### Key Entities *(include if feature involves data)*

- **Prompt Excerpt**: The individual plain text file stored under `raa/prompts/excerpts/`.
- **Node Tag Mapping**: The configuration matrix linking RAA pipeline nodes to specific tags.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Retrieval utility successfully retrieves excerpts for all tags in the mapping matrix.
- **SC-002**: Unit tests verify 100% code coverage for valid lookups, node-specific tags retrieval, and missing tag exceptions.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
- Excerpt files exist under `raa/prompts/excerpts/`.
