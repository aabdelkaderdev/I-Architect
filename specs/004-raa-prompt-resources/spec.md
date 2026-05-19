# Feature Specification: RAA Prompt Resource Bundle & Source Register

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 2

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Prompt Reference Validity & Excerpt Alignment (Priority: P1)

Agents require the prompt constraint templates and tagged excerpt files under `raa/prompts/` to have clear content that strictly complies with C4 model definitions and the 5-step SAAM process.

**Why this priority**: If the prompt resource bundle contains incorrect or vague rules, downstream LLM subgraphs will generate invalid architectural elements, relationships, or SAAM tradeoff analysis ratings.

**Independent Test**: Write a unit test that loads all prompt template files and excerpt text files, checking that each excerpt block is under the 25-word cap and that the constraints contain all mandatory architectural rules.

**Acceptance Scenarios**:

1. **Given** the prompt constraints files, **When** parsed, **Then** C4 constraints contain rules for the three C4 levels (Context, Container, Component), element attributes, and relationship scopes.
2. **Given** the SAAM constraints file, **When** parsed, **Then** it details the 5-step evaluation process in order.
3. **Given** the prompt excerpt files, **When** checked, **Then** each text file is under the 25-word limit.

---

### Edge Cases

- **Retrieval Tag Mismatch**: What happens if a node requests a tag that doesn't correspond to an excerpt file? The retrieval policy must map tags to specific filenames and raise a clear error if an invalid tag is requested.
- **Word-Limit Violations**: What happens if an excerpt file grows beyond 25 words? Excerpts must be strictly validated during test runs to ensure they remain concise.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `raa/prompts/source_register.md` MUST define a markdown table with columns: `Source`, `URL`, `Retrieval Date`, and `Governs`, listing:
  - C4 Model — Diagrams
  - C4 Model — Notation
  - SAAM — SEI Technical Report
- **FR-002**: `raa/prompts/c4_constraints.md` MUST define constraints for C4 levels (Context, Container, Component), elements (label, description, relationships, parent ID), and technologies.
- **FR-003**: `raa/prompts/saam_constraints.md` MUST define constraints for the 5-step SAAM process: partition, map, choose quality attributes, define scenarios, and evaluate.
- **FR-004**: System MUST define tagged excerpt files under `raa/prompts/excerpts/`:
  - `c4_levels.txt` (defines levels)
  - `c4_notation.txt` (defines notation)
  - `c4_technology.txt` (defines technology annotation requirement)
  - `saam_steps.txt` (defines SAAM steps)
  - `saam_scenarios.txt` (defines scenario selection)
- **FR-005**: All excerpt text files MUST contain 25 words or fewer.

### Key Entities *(include if feature involves data)*

- **Prompt Resource Bundle**: The collection of constraints and excerpts stored under `raa/prompts/`.
- **Source Register**: The table listing the authoritative URLs and governance rules.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Excerpts and constraints files are present and match their exact file names.
- **SC-002**: Every file in `raa/prompts/excerpts/` contains 25 words or fewer.
- **SC-003**: 100% of defined prompt files parse correctly as text assets.

## Assumptions

- No business logic or Python execution code is written in this phase.
- The branch `002-raa-subgraph` is reused for this feature.
