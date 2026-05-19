# Tasks: RAA Project Scaffolding

**Input**: Design documents from `specs/003-raa-project-scaffolding/`
**Source Scope**: `RAA_Plan.md` Section 21 only: 21A-0, 21A, 21B, 21C, and 21D
**Tests**: Structural validation only; no runtime logic or prompt content is implemented in this feature

**Organization**: Tasks are grouped by user story so the directory scaffold and prompt tag scaffold can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish root-level runtime storage and repository ignore behavior.

- [X] T001 [P] Create the shared runtime directory `embeddings/` if missing
- [X] T002 [P] Ensure the repository ignore rule includes `embeddings/` in `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm existing scaffold state and protect existing files from accidental overwrite.

- [X] T003 Inventory existing scaffold files under `raa/`, `Skills/RAA/`, and `embeddings/` before edits using `specs/003-raa-project-scaffolding/plan.md`
- [X] T004 Confirm existing `Skills/RAA/SKILL.MD` and `Skills/RAA/references/SAAM.md` are preserved and not overwritten

**Checkpoint**: Existing scaffold state is known; missing placeholder work can proceed safely.

---

## Phase 3: User Story 1 - RAA Project Scaffolding Structure (Priority: P1) MVP

**Goal**: Create the complete empty directory and placeholder-file scaffold for the RAA runtime package and design-time skill bundle.

**Independent Test**: Scan the filesystem and confirm every directory, Python stub, skill file, and reference file listed in `RAA_Plan.md` Section 21A and 21B exists at the expected path.

### Implementation for User Story 1

- [X] T005 [P] [US1] Create the skill bundle directory tree `Skills/RAA/` and `Skills/RAA/references/`
- [X] T006 [P] [US1] Create empty placeholder skill definition file `Skills/RAA/SKILL.MD` if missing without modifying existing content
- [X] T007 [P] [US1] Create empty placeholder authoritative reference files `Skills/RAA/references/C4.md` and `Skills/RAA/references/Quality_Attributes.md`
- [X] T008 [P] [US1] Create empty placeholder operational reference files `Skills/RAA/references/Entity_Extraction.md`, `Skills/RAA/references/Relationship_Extraction.md`, and `Skills/RAA/references/Pattern_Selection.md`
- [X] T009 [P] [US1] Create empty placeholder operational reference files `Skills/RAA/references/Technology_Inference.md`, `Skills/RAA/references/C4_Level_Mapping.md`, and `Skills/RAA/references/SAAM.md` without modifying existing `SAAM.md` content
- [X] T010 [US1] Create the runtime package directory tree `raa/`, `raa/graphs/`, `raa/models/`, `raa/nodes/`, `raa/state/`, `raa/utils/`, `raa/prompts/`, and `raa/prompts/excerpts/`
- [X] T011 [P] [US1] Create Python package stub files `raa/__init__.py`, `raa/graphs/__init__.py`, and `raa/models/__init__.py`
- [X] T012 [P] [US1] Create Python package stub files `raa/nodes/__init__.py`, `raa/state/__init__.py`, and `raa/utils/__init__.py` without modifying existing `raa/state/__init__.py` content
- [X] T013 [P] [US1] Create Python package/resource stub files `raa/prompts/__init__.py` and `raa/prompts/excerpts/__init__.py`
- [X] T014 [P] [US1] Create empty runtime module placeholder files `raa/llm.py` and `raa/runner.py`

**Checkpoint**: The `raa/`, `Skills/RAA/`, and `embeddings/` scaffolds exist with no runtime business logic or authored prompt content.

---

## Phase 4: User Story 2 - Tag-Based Prompt Resource Access Scaffold (Priority: P1)

**Goal**: Create the runtime prompt bundle placeholders and tag-to-file scaffold required by Section 21C and the authority direction in Section 21D.

**Independent Test**: Inspect `raa/prompts/` and confirm each Section 21C tag has a corresponding excerpt placeholder file under `raa/prompts/excerpts/`.

### Implementation for User Story 2

- [X] T015 [P] [US2] Create empty prompt resource placeholder file `raa/prompts/source_register.md`
- [X] T016 [P] [US2] Create empty prompt constraint placeholder files `raa/prompts/c4_constraints.md` and `raa/prompts/saam_constraints.md`
- [X] T017 [P] [US2] Create empty C4 excerpt placeholder files `raa/prompts/excerpts/c4_levels.txt`, `raa/prompts/excerpts/c4_notation.txt`, and `raa/prompts/excerpts/c4_technology.txt`
- [X] T018 [P] [US2] Create empty SAAM excerpt placeholder files `raa/prompts/excerpts/saam_steps.txt` and `raa/prompts/excerpts/saam_scenarios.txt`
- [X] T019 [US2] Document the Section 21C tag-to-file mapping in `specs/003-raa-project-scaffolding/quickstart.md` without adding prompt content to `raa/prompts/`

**Checkpoint**: Prompt resource file paths exist, and the tag scaffold is documented for later prompt-loader implementation.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Verify the scaffold is complete, empty where requested, and safe for Git.

- [X] T020 [P] Run a filesystem existence check for every Section 21 path listed in `specs/003-raa-project-scaffolding/data-model.md`
- [X] T021 [P] Verify `git check-ignore embeddings/` confirms the shared embedding directory is ignored by `.gitignore`
- [X] T022 Confirm no runtime business logic was added to `raa/llm.py`, `raa/runner.py`, or any `raa/**/__init__.py` stub
- [X] T023 Confirm `Skills/RAA/` contains design-time files only and `raa/prompts/` contains runtime prompt placeholder files only, matching the authority direction in `RAA_Plan.md` Section 21D

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks user story work.
- **User Story 1 (Phase 3)**: Depends on Foundational completion.
- **User Story 2 (Phase 4)**: Depends on User Story 1 directory creation because prompt files live under `raa/prompts/`.
- **Polish (Final Phase)**: Depends on both user stories.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational; provides directories required by all later RAA work.
- **User Story 2 (P1)**: Can start after `raa/prompts/` and `raa/prompts/excerpts/` exist from US1.

### Parallel Opportunities

- T001 and T002 can run in parallel.
- T005 through T009 can run in parallel because they target different skill bundle files.
- T011 through T014 can run in parallel after T010 creates the parent directories.
- T015 through T018 can run in parallel after the prompt directories exist.
- T020 and T021 can run in parallel during final validation.

---

## Parallel Example: User Story 1

```bash
Task: "Create empty placeholder authoritative reference files Skills/RAA/references/C4.md and Skills/RAA/references/Quality_Attributes.md"
Task: "Create Python package stub files raa/__init__.py, raa/graphs/__init__.py, and raa/models/__init__.py"
Task: "Create empty runtime module placeholder files raa/llm.py and raa/runner.py"
```

## Parallel Example: User Story 2

```bash
Task: "Create empty prompt resource placeholder file raa/prompts/source_register.md"
Task: "Create empty C4 excerpt placeholder files raa/prompts/excerpts/c4_levels.txt, raa/prompts/excerpts/c4_notation.txt, and raa/prompts/excerpts/c4_technology.txt"
Task: "Create empty SAAM excerpt placeholder files raa/prompts/excerpts/saam_steps.txt and raa/prompts/excerpts/saam_scenarios.txt"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 to ensure `embeddings/` exists and is ignored.
2. Complete Phase 2 to protect existing scaffold files.
3. Complete User Story 1 to create the complete design-time and runtime directory skeleton.
4. Stop and validate the Section 21A and 21B paths independently.

### Incremental Delivery

1. Deliver root infrastructure and skill/runtime directories.
2. Add prompt resource placeholders and tag mapping documentation.
3. Run structural validation and Git ignore checks.

### Notes

- Existing files must be preserved. Create missing placeholders only.
- Do not author prompt content or runtime business logic in this feature.
- `Skills/RAA/` is design-time reference material; `raa/prompts/` is runtime prompt material.
