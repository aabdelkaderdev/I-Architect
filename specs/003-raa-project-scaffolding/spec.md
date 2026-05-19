# Feature Specification: RAA Project Scaffolding

**Feature Branch**: `002-raa-subgraph`

**Created**: 2026-05-19

**Status**: Draft

**Input**: `RAA_Plan.md` Section 21

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAA Project Scaffolding Structure (Priority: P1)

Developers need a standardized, empty directory scaffolding for `raa/`, `Skills/RAA/`, and `embeddings/` so that code, skills, prompts, references, and placeholders are correctly organized and separated before implementing any runtime logic.

**Why this priority**: Setup is a P1 prerequisite to avoid placement issues and directory conflicts when implementing functional RAA stages.

**Independent Test**: Run a directory scan script verifying all folders, empty `__init__.py` files, prompt templates, and references exist in the exact paths specified in RAA_Plan Section 21.

**Acceptance Scenarios**:

1. **Given** a workspace, **When** the scaffolding feature is completed, **Then** all directories and placeholder files specified in the requirements exist.

---

### User Story 2 - Tag-Based Prompt Resource Access (Priority: P1)

Agents need the runtime prompt resource bundle files under `raa/prompts/` to have correct tag associations for lookup.

**Why this priority**: Without the tag structure in the prompt files, prompt retrieval code cannot locate the correct excerpt blocks.

**Independent Test**: Inspect prompt excerpt files and verify they match the exact tag expectations (`c4:levels`, `c4:notation`, `c4:technology`, etc.) as defined in RAA_Plan Section 21C.

**Acceptance Scenarios**:

1. **Given** the runtime prompts folder `raa/prompts/`, **When** the node tag mapping is checked, **Then** all required tags map to corresponding excerpt text files.

---

### Edge Cases

- **Pre-existing Directories**: If directories already exist, the scaffolding must preserve any existing files and create missing directories/placeholders.
- **Git Ignoring Local Databases**: The `embeddings/` directory contains local databases and must remain untracked by Git to keep the repository clean.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create the following directory structure:
  - `raa/`
  - `raa/graphs/`
  - `raa/models/`
  - `raa/nodes/`
  - `raa/state/`
  - `raa/utils/`
  - `raa/prompts/`
  - `raa/prompts/excerpts/`
  - `Skills/RAA/`
  - `Skills/RAA/references/`
  - `embeddings/`
- **FR-002**: System MUST place placeholder reference documents in `Skills/RAA/references/` for: `C4.md`, `Quality_Attributes.md`, `Entity_Extraction.md`, `Relationship_Extraction.md`, `Pattern_Selection.md`, `Technology_Inference.md`, and `C4_Level_Mapping.md`. Existing reference files (e.g. `SAAM.md`) MUST NOT be overwritten.
- **FR-003**: System MUST place the following placeholder runtime prompt templates in `raa/prompts/`: `source_register.md`, `c4_constraints.md`, `saam_constraints.md`.
- **FR-004**: System MUST place the following placeholder excerpt files in `raa/prompts/excerpts/`: `c4_levels.txt`, `c4_notation.txt`, `c4_technology.txt`, `saam_steps.txt`, `saam_scenarios.txt`.
- **FR-005**: All files MUST contain placeholder headings or template outlines matching the RAA plan.
- **FR-006**: System MUST ensure `embeddings/` is listed in `.gitignore`.

### Key Entities *(include if feature involves data)*

- **Skill Resource Bundle**: Documentation files under `Skills/RAA/`.
- **Prompt Resource Bundle**: Runtime prompts and excerpts under `raa/prompts/`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the specified directories and placeholder files exist in the file system.
- **SC-002**: The `embeddings/` directory is successfully ignored by Git.

## Assumptions

- No business logic or functional code is written in Python files during this scaffolding phase.
- The branch `002-raa-subgraph` is reused for this feature.
