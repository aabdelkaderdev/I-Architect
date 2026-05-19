# Feature Specification: RAA Skill Resource Bundle References

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 14

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Compliance of Skill References with 7-Section Template & Stated Hard Rules (Priority: P1)

Developers and agents need the skill-specific reference files in `Skills/RAA/references/` to follow the exact seven-section template (Purpose, Input, Normative Rules, Decision Guidelines, Output Schema, Error Cases, Examples) and enforce the hard rules (such as no component without container, no container without system, and explicit `diagram_scope` assignments).

**Why this priority**: These reference documents serve as the source of truth for both developers and LLM runtime parser agents. If they are incomplete, vague, or fail to enforce the hard constraints of the RAA pipeline, it will cause design-time misalignment and merge failures.

**Independent Test**: Write a markdown parser validation script to check each of the 5 skill-specific reference markdown files for the presence of the seven-section headers, and verify that the hard rules are explicitly stated and documented.

**Acceptance Scenarios**:

1. **Given** the 7 skill-specific/authoritative reference files, **When** checked, **Then** each file exists and is populated with non-trivial text contents.
2. **Given** the 5 skill-specific references, **When** parsed, **Then** they contain all 7 sections defined in the template.
3. **Given** the authoritative references, **When** parsed, **Then** they define the domain without requiring the Input/Output sections.

---

### Edge Cases

- **Preservation of Existing Assets**: `Skills/RAA/references/SAAM.md` already exists and is fully fleshed out; it must remain completely untouched.
- **Header Parsing Deviations**: If sections are named slightly differently (e.g. "Purpose of Node" instead of "Purpose"), validation might fail. The template headers must be matched exactly.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create `Skills/RAA/references/C4.md` defining the C4 model levels, element types, notation rules, and relationship syntax.
- **FR-002**: System MUST create `Skills/RAA/references/Quality_Attributes.md` defining the ISO/IEC 25010 quality attributes.
- **FR-003**: System MUST create `Skills/RAA/references/Entity_Extraction.md` adhering to the seven-section template and enforcing the **Hard rule**: a subgraph must never propose a component without ensuring a container is present, and never propose a container without ensuring a system is present (orphan prevention).
- **FR-004**: System MUST create `Skills/RAA/references/Relationship_Extraction.md` adhering to the seven-section template and enforcing the **Hard rule**: every proposed relationship must carry an explicit `diagram_scope` value (context, container, or component).
- **FR-005**: System MUST create `Skills/RAA/references/Pattern_Selection.md` adhering to the seven-section template.
- **FR-006**: System MUST create `Skills/RAA/references/Technology_Inference.md` adhering to the seven-section template.
- **FR-007**: System MUST create `Skills/RAA/references/C4_Level_Mapping.md` adhering to the seven-section template and mapping how to assign `parent_system_id`, `parent_container_id`, and `diagram_scope`.

### Key Entities *(include if feature involves data)*

- **Skill Resource Bundle Reference Files**: Markdown documents containing guidelines and constraints for each extraction skill.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 7 reference files exist in `Skills/RAA/references/`.
- **SC-002**: All 5 skill-specific reference files contain all seven sections required by the template.
- **SC-003**: No existing reference files (like `SAAM.md`) are modified or deleted.

## Assumptions

- The branch `002-raa-subgraph` is reused for this feature.
