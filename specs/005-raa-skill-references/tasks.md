# Tasks: RAA Skill Resource Bundle References

**Input**: Design documents from `specs/005-raa-skill-references/`
**Source Scope**: `RAA_Plan.md` Section 14 only
**Tests**: Included because `specs/005-raa-skill-references/spec.md` requires validation for reference existence, seven-section structure, and hard-rule coverage.

**Organization**: Tasks are grouped by independently testable reference-document slices.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the Skill Resource Bundle exists and create the validation test location.

- [X] T001 [P] Confirm the skill bundle directory exists at `Skills/RAA/`
- [X] T002 [P] Confirm the reference directory exists at `Skills/RAA/references/`
- [X] T003 [P] Create skill reference test directory `tests/raa/` if missing

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish validation for all reference files before authoring or refactoring content.

- [X] T004 Create `tests/raa/test_skill_references.py` with the required reference file list from `RAA_Plan.md` Section 14
- [X] T005 Add existence and non-empty content assertions for `Skills/RAA/references/C4.md`, `Skills/RAA/references/Quality_Attributes.md`, `Skills/RAA/references/Entity_Extraction.md`, `Skills/RAA/references/Relationship_Extraction.md`, `Skills/RAA/references/Pattern_Selection.md`, `Skills/RAA/references/Technology_Inference.md`, `Skills/RAA/references/C4_Level_Mapping.md`, and `Skills/RAA/references/SAAM.md` in `tests/raa/test_skill_references.py`
- [X] T006 Add seven-section header validation for skill references in `tests/raa/test_skill_references.py`
- [X] T007 Add authoritative-reference validation that `Skills/RAA/references/C4.md` and `Skills/RAA/references/Quality_Attributes.md` define domain content without requiring Input or Output schema sections in `tests/raa/test_skill_references.py`
- [X] T008 Add hard-rule assertions for orphan prevention text in `Skills/RAA/references/Entity_Extraction.md` in `tests/raa/test_skill_references.py`
- [X] T009 Add hard-rule assertions for explicit `diagram_scope` assignment in `Skills/RAA/references/Relationship_Extraction.md` in `tests/raa/test_skill_references.py`
- [X] T010 Add parent-assignment assertions for `parent_system_id`, `parent_container_id`, and relationship scope mapping in `Skills/RAA/references/C4_Level_Mapping.md` in `tests/raa/test_skill_references.py`
- [X] T011 Add SAAM preservation assertions covering five-step process, scoring, merge algorithm, tie-breaking, hotspot detection, and error cases in `tests/raa/test_skill_references.py`

**Checkpoint**: Reference validation exists and should fail until all reference files are authored.

---

## Phase 3: User Story 1 - Authoritative References (Priority: P1) MVP

**Goal**: Author the two authoritative references that define C4 and quality-attribute domain rules used by all later skill references.

**Independent Test**: Run `tests/raa/test_skill_references.py` and confirm `C4.md` and `Quality_Attributes.md` exist, are non-empty, and contain the required domain coverage without requiring skill Input or Output schema sections.

### Tests for User Story 1

- [X] T012 [P] [US1] Verify authoritative reference validation fails before `Skills/RAA/references/C4.md` and `Skills/RAA/references/Quality_Attributes.md` are fully authored

### Implementation for User Story 1

- [X] T013 [US1] Author `Skills/RAA/references/C4.md` with Purpose and RAA adaptation sections covering Context, Container, and Component levels
- [X] T014 [US1] Add C4 element type definitions for `system`, `container`, `component`, `person`, and `external_system` to `Skills/RAA/references/C4.md`
- [X] T015 [US1] Add C4 notation rules for labels, descriptions, technology annotations, relationship direction, interaction descriptions, boundary grouping, and level-mixing prohibition to `Skills/RAA/references/C4.md`
- [X] T016 [US1] Author `Skills/RAA/references/Quality_Attributes.md` with Purpose and RAA adaptation sections covering Performance Efficiency, Compatibility, Usability, Reliability, Security, Maintainability, Portability, and Cost Efficiency
- [X] T017 [US1] Add representative ASR condition examples and SAAM scenario-evaluation prompts for every quality attribute in `Skills/RAA/references/Quality_Attributes.md`

**Checkpoint**: Authoritative domain references are available for all skill-specific references.

---

## Phase 4: User Story 2 - Entity, Relationship, and C4 Level Mapping References (Priority: P1)

**Goal**: Author the hierarchy-critical skill references that prevent orphan entities, enforce parent assignment, and require correct relationship scopes.

**Independent Test**: Run `tests/raa/test_skill_references.py` and confirm each file follows the seven-section template and contains the required hard rules.

### Tests for User Story 2

- [X] T018 [P] [US2] Verify seven-section validation fails before `Skills/RAA/references/Entity_Extraction.md`, `Skills/RAA/references/Relationship_Extraction.md`, and `Skills/RAA/references/C4_Level_Mapping.md` are authored
- [X] T019 [P] [US2] Verify hard-rule validation fails before orphan prevention, `diagram_scope`, and parent-assignment rules are added to the hierarchy-critical reference files

### Implementation for User Story 2

- [X] T020 [US2] Author `Skills/RAA/references/Entity_Extraction.md` with exact sections `Purpose`, `Input`, `Normative rules`, `Decision guidelines`, `Output schema`, `Error cases`, and `Examples`
- [X] T021 [US2] Add entity extraction rules for System vs Container vs Component introduction, canonical ID derivation, parent-child assignment, technology confidence, and ambiguous requirements to `Skills/RAA/references/Entity_Extraction.md`
- [X] T022 [US2] Add the orphan-prevention hard rule that components require a resolvable container and containers require a resolvable system to `Skills/RAA/references/Entity_Extraction.md`
- [X] T023 [US2] Add output schema references to `ArchSystem`, `ArchContainer`, `ArchComponent`, `ArchPerson`, and `ArchExternalSystem` in `Skills/RAA/references/Entity_Extraction.md`
- [X] T024 [US2] Author `Skills/RAA/references/Relationship_Extraction.md` with exact sections `Purpose`, `Input`, `Normative rules`, `Decision guidelines`, `Output schema`, `Error cases`, and `Examples`
- [X] T025 [US2] Add relationship extraction rules for directed relationships, interaction verb phrases, protocol or technology inference, cardinality, implicit relationships, and contradictions to `Skills/RAA/references/Relationship_Extraction.md`
- [X] T026 [US2] Add the hard rule that every relationship must carry explicit `diagram_scope` assigned as `context`, `container`, or `component` according to endpoint types in `Skills/RAA/references/Relationship_Extraction.md`
- [X] T027 [US2] Add output schema references to `ArchRelationship` and endpoint resolution requirements in `Skills/RAA/references/Relationship_Extraction.md`
- [X] T028 [US2] Author `Skills/RAA/references/C4_Level_Mapping.md` with exact sections `Purpose`, `Input`, `Normative rules`, `Decision guidelines`, `Output schema`, `Error cases`, and `Examples`
- [X] T029 [US2] Add rules for promoting or demoting entities between Context, Container, and Component levels in `Skills/RAA/references/C4_Level_Mapping.md`
- [X] T030 [US2] Add parent-assignment rules for implicit `parent_system_id`, inferred `parent_container_id`, and component-without-container handling in `Skills/RAA/references/C4_Level_Mapping.md`
- [X] T031 [US2] Add relationship endpoint combination rules that assign `diagram_scope` for context, container, and component relationships in `Skills/RAA/references/C4_Level_Mapping.md`

**Checkpoint**: Hierarchy and relationship skill references enforce orphan-prevention, parent-assignment, and scope rules.

---

## Phase 5: User Story 3 - Pattern, Technology, and SAAM References (Priority: P1)

**Goal**: Author the remaining skill references and adapt the existing SAAM reference into the requested template without losing its current scoring and merge guidance.

**Independent Test**: Run `tests/raa/test_skill_references.py` and confirm pattern, technology, and SAAM references satisfy required sections and preserve SAAM-specific content.

### Tests for User Story 3

- [X] T032 [P] [US3] Verify seven-section validation fails before `Skills/RAA/references/Pattern_Selection.md` and `Skills/RAA/references/Technology_Inference.md` are authored
- [X] T033 [P] [US3] Verify SAAM validation fails unless `Skills/RAA/references/SAAM.md` preserves five-step process, scoring, merge algorithm, tie-breaking, hotspot detection, and error cases

### Implementation for User Story 3

- [X] T034 [US3] Author `Skills/RAA/references/Pattern_Selection.md` with exact sections `Purpose`, `Input`, `Normative rules`, `Decision guidelines`, `Output schema`, `Error cases`, and `Examples`
- [X] T035 [US3] Add pattern selection rules for quality-architecture matrix use, ILP constraints, greedy fallback, quality-attribute mapping rationale, and pattern compatibility to `Skills/RAA/references/Pattern_Selection.md`
- [X] T036 [US3] Add output schema references to `ArchPattern` and selected-pattern rationale requirements in `Skills/RAA/references/Pattern_Selection.md`
- [X] T037 [US3] Author `Skills/RAA/references/Technology_Inference.md` with exact sections `Purpose`, `Input`, `Normative rules`, `Decision guidelines`, `Output schema`, `Error cases`, and `Examples`
- [X] T038 [US3] Add technology inference rules for databases, message brokers, API protocols, deployment targets, confidence levels, null handling, and conflicting signals to `Skills/RAA/references/Technology_Inference.md`
- [X] T039 [US3] Add output schema guidance for technology fields on `ArchContainer`, `ArchComponent`, `ArchExternalSystem`, and `ArchRelationship` to `Skills/RAA/references/Technology_Inference.md`
- [X] T040 [US3] Refactor `Skills/RAA/references/SAAM.md` into the requested seven-section skill reference structure while preserving all existing SAAM scoring, scenario classification, merge algorithm, tie-breaking, hotspot detection, and error-case content
- [X] T041 [US3] Add explicit judge input channels and output schema references to `ArchFragment`, `ArchModel`, `OpenQuestion`, and `ConfidenceRecord` in `Skills/RAA/references/SAAM.md`
- [X] T042 [US3] Add a worked example from the custom requirements dataset to `Skills/RAA/references/SAAM.md` without removing current adapted SAAM rules

**Checkpoint**: All Section 14 reference files are authored and structurally validated.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate completeness, rule coverage, and separation of design-time references from runtime prompts.

- [X] T043 [P] Run the skill reference validation tests in `tests/raa/test_skill_references.py`
- [X] T044 Confirm all five skill-specific files and `Skills/RAA/references/SAAM.md` use the exact seven-section headers from `specs/005-raa-skill-references/data-model.md`
- [X] T045 Confirm authoritative references `Skills/RAA/references/C4.md` and `Skills/RAA/references/Quality_Attributes.md` omit skill Input and Output schema sections
- [X] T046 Confirm `Skills/RAA/references/Entity_Extraction.md` contains the orphan-prevention hard rules and references C4 type definitions
- [X] T047 Confirm `Skills/RAA/references/Relationship_Extraction.md` contains explicit `diagram_scope` hard rules and references C4 relationship syntax
- [X] T048 Confirm `Skills/RAA/references/C4_Level_Mapping.md` contains `parent_system_id`, `parent_container_id`, implicit-parent, and endpoint-scope rules
- [X] T049 Confirm changes remain confined to `Skills/RAA/references/` and `tests/raa/test_skill_references.py` for this feature

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks reference authoring.
- **User Story 1 (Phase 3)**: Depends on Foundational validation tasks.
- **User Story 2 (Phase 4)**: Depends on User Story 1 because entity, relationship, and level mapping references cite C4 definitions.
- **User Story 3 (Phase 5)**: Depends on User Story 1 because pattern and technology references cite quality attributes and C4 type fields.
- **Polish (Final Phase)**: Depends on all authored references.

### User Story Dependencies

- **User Story 1 (P1)**: Establishes authoritative domain references.
- **User Story 2 (P1)**: Builds hierarchy-critical skill references after C4 reference content exists.
- **User Story 3 (P1)**: Builds pattern, technology, and SAAM references after authoritative references exist.

### Parallel Opportunities

- T001 through T003 can run in parallel.
- T008 through T011 can be added to the same test file sequentially, while T004-T007 define shared structure first.
- T013 through T017 can run in parallel only if edits to `C4.md` and `Quality_Attributes.md` are split by file.
- T020 through T031 can run in parallel by file after US1 is complete.
- T034 through T042 can run in parallel by file after US1 is complete, except T040-T042 must run sequentially within `SAAM.md`.
- T043 can run in parallel with manual checks T044-T049 after all reference authoring is complete.

---

## Parallel Example: User Story 2

```bash
Task: "Author Skills/RAA/references/Entity_Extraction.md with exact sections Purpose, Input, Normative rules, Decision guidelines, Output schema, Error cases, and Examples"
Task: "Author Skills/RAA/references/Relationship_Extraction.md with exact sections Purpose, Input, Normative rules, Decision guidelines, Output schema, Error cases, and Examples"
Task: "Author Skills/RAA/references/C4_Level_Mapping.md with exact sections Purpose, Input, Normative rules, Decision guidelines, Output schema, Error cases, and Examples"
```

## Parallel Example: User Story 3

```bash
Task: "Author Skills/RAA/references/Pattern_Selection.md with exact seven-section structure"
Task: "Author Skills/RAA/references/Technology_Inference.md with exact seven-section structure"
Task: "Refactor Skills/RAA/references/SAAM.md into the requested seven-section skill reference structure while preserving existing SAAM content"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Author `C4.md` and `Quality_Attributes.md`.
3. Validate authoritative references independently.

### Incremental Delivery

1. Deliver authoritative references.
2. Deliver hierarchy-critical references with hard rules.
3. Deliver pattern, technology, and SAAM references.
4. Run the full validation suite and manual hard-rule checks.

### Notes

- Preserve the existing adapted SAAM substance even if `SAAM.md` is reorganized into the requested template.
- Skill Resource Bundle files are design-time references only; runtime prompt constraints live under `raa/prompts/`.
- Use exact section headings for skill references to keep validation deterministic.
