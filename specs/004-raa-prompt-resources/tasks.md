# Tasks: RAA Prompt Resource Bundle and Source Register

**Input**: Design documents from `specs/004-raa-prompt-resources/`
**Source Scope**: `RAA_Plan.md` Section 2 only: 2A, 2B, 2C, and 2D
**Tests**: Included because `specs/004-raa-prompt-resources/spec.md` explicitly requires validation for source register structure, required constraints, retrieval tags, and excerpt word limits.

**Organization**: Tasks are grouped by independently testable user stories for source/constraint population and tagged excerpt population.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm prompt resource paths and test directory exist before writing validation checks or content.

- [X] T001 [P] Confirm prompt resource directory exists at `raa/prompts/`
- [X] T002 [P] Confirm excerpt resource directory exists at `raa/prompts/excerpts/`
- [X] T003 [P] Create prompt resource test directory `tests/raa/` if missing

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define the validation expectations that all prompt resource content must satisfy.

- [X] T004 Create `tests/raa/test_prompt_resources.py` with expected source register rows for `C4 Model - Diagrams`, `C4 Model - Notation`, and `SAAM - SEI Technical Report`
- [X] T005 Add required C4 constraint assertions for levels, element metadata, technology annotations, and relationship descriptions in `tests/raa/test_prompt_resources.py`
- [X] T006 Add required SAAM constraint assertions for the ordered five-step process in `tests/raa/test_prompt_resources.py`
- [X] T007 Add expected retrieval tag mapping assertions for `c4:levels`, `c4:notation`, `c4:technology`, `saam:steps`, and `saam:scenarios` in `tests/raa/test_prompt_resources.py`
- [X] T008 Add excerpt word-count validation that fails when any `raa/prompts/excerpts/*.txt` file exceeds 25 words in `tests/raa/test_prompt_resources.py`

**Checkpoint**: Prompt resource validation exists and should fail until the prompt files are populated.

---

## Phase 3: User Story 1 - Authoritative Source Register and Normative Constraints (Priority: P1) MVP

**Goal**: Populate the source register and full C4/SAAM constraint markdown files so prompt-driven nodes have authoritative, explicit rules.

**Independent Test**: Run `tests/raa/test_prompt_resources.py` and confirm source register rows and mandatory C4/SAAM constraints are present.

### Tests for User Story 1

- [X] T009 [P] [US1] Verify the source register validation in `tests/raa/test_prompt_resources.py` fails before `raa/prompts/source_register.md` is populated
- [X] T010 [P] [US1] Verify the C4 and SAAM constraint validation in `tests/raa/test_prompt_resources.py` fails before `raa/prompts/c4_constraints.md` and `raa/prompts/saam_constraints.md` are populated

### Implementation for User Story 1

- [X] T011 [US1] Populate `raa/prompts/source_register.md` with the Section 2A markdown table columns `Source`, `URL`, `Retrieval Date`, and `Governs`
- [X] T012 [US1] Add the Section 2A source row for `C4 Model - Diagrams` with URL `https://c4model.com/diagrams` and governance scope in `raa/prompts/source_register.md`
- [X] T013 [US1] Add the Section 2A source row for `C4 Model - Notation` with URL `https://c4model.com/diagrams/notation` and governance scope in `raa/prompts/source_register.md`
- [X] T014 [US1] Add the Section 2A source row for `SAAM - SEI Technical Report` with URL `https://sei.cmu.edu/documents/150/2007_019_001_29297.pdf` and governance scope in `raa/prompts/source_register.md`
- [X] T015 [US1] Add a Section 2D retrieval policy section to `raa/prompts/source_register.md` stating that full source documents are never copied into prompts
- [X] T016 [US1] Populate `raa/prompts/c4_constraints.md` with Section 2B C4 rules for Context, Container, and Component levels
- [X] T017 [US1] Add Section 2B C4 element rules requiring type label, short description, and clearly labelled relationships in `raa/prompts/c4_constraints.md`
- [X] T018 [US1] Add Section 2B C4 technology and relationship direction rules in `raa/prompts/c4_constraints.md`
- [X] T019 [US1] Populate `raa/prompts/saam_constraints.md` with the Section 2B ordered SAAM steps from partitioning through evaluation
- [X] T020 [US1] Add quality-attribute scenario guidance using ARLO quality weights to `raa/prompts/saam_constraints.md`

**Checkpoint**: Source register plus C4 and SAAM normative constraint files are populated.

---

## Phase 4: User Story 2 - Tagged Excerpt Blocks and Retrieval Policy (Priority: P1)

**Goal**: Populate the five short excerpt files and record the retrieval tag scheme used by prompt-driven nodes.

**Independent Test**: Run `tests/raa/test_prompt_resources.py` and confirm all five excerpt files exist, each has 25 words or fewer, and every expected retrieval tag maps to the intended file.

### Tests for User Story 2

- [X] T021 [P] [US2] Verify the retrieval tag mapping validation in `tests/raa/test_prompt_resources.py` fails before the tag mapping is documented in `raa/prompts/source_register.md`
- [X] T022 [P] [US2] Verify excerpt word-count validation in `tests/raa/test_prompt_resources.py` fails before the five files under `raa/prompts/excerpts/` are populated

### Implementation for User Story 2

- [X] T023 [US2] Add a retrieval tag mapping table to `raa/prompts/source_register.md` mapping `c4:levels` to `raa/prompts/excerpts/c4_levels.txt`
- [X] T024 [US2] Add retrieval tag mapping rows for `c4:notation` and `c4:technology` to `raa/prompts/source_register.md`
- [X] T025 [US2] Add retrieval tag mapping rows for `saam:steps` and `saam:scenarios` to `raa/prompts/source_register.md`
- [X] T026 [P] [US2] Populate `raa/prompts/excerpts/c4_levels.txt` with one paraphrased C4 level excerpt of 25 words or fewer
- [X] T027 [P] [US2] Populate `raa/prompts/excerpts/c4_notation.txt` with one paraphrased C4 notation excerpt of 25 words or fewer
- [X] T028 [P] [US2] Populate `raa/prompts/excerpts/c4_technology.txt` with one paraphrased C4 technology excerpt of 25 words or fewer
- [X] T029 [P] [US2] Populate `raa/prompts/excerpts/saam_steps.txt` with one paraphrased SAAM step excerpt of 25 words or fewer
- [X] T030 [P] [US2] Populate `raa/prompts/excerpts/saam_scenarios.txt` with one paraphrased SAAM scenario excerpt of 25 words or fewer
- [X] T031 [US2] Add Section 2D authority direction text to `raa/prompts/source_register.md` showing Source Register to Prompt Resource Bundle to skill prompts

**Checkpoint**: Tagged excerpt files and retrieval policy are available for later prompt-loader implementation.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate content boundaries, word limits, and retrieval-policy compliance.

- [X] T032 [P] Run prompt resource validation tests in `tests/raa/test_prompt_resources.py`
- [X] T033 Confirm no full C4 or SAAM source document text was copied into `raa/prompts/source_register.md`, `raa/prompts/c4_constraints.md`, `raa/prompts/saam_constraints.md`, or `raa/prompts/excerpts/*.txt`
- [X] T034 Confirm every excerpt file under `raa/prompts/excerpts/` contains exactly one paraphrased constraint block and no file exceeds 25 words
- [X] T035 Confirm `raa/prompts/source_register.md` keeps the Source Register as the authority for `raa/prompts/c4_constraints.md`, `raa/prompts/saam_constraints.md`, and `raa/prompts/excerpts/*.txt`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks content population.
- **User Story 1 (Phase 3)**: Depends on Foundational validation tasks.
- **User Story 2 (Phase 4)**: Depends on Foundational validation tasks and can run after the source register file exists.
- **Polish (Final Phase)**: Depends on User Story 1 and User Story 2 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 and provides the authoritative source and constraint markdown files.
- **User Story 2 (P1)**: Can start after Phase 2, but T023-T025 and T031 require `raa/prompts/source_register.md` from US1.

### Parallel Opportunities

- T001 through T003 can run in parallel.
- T009 and T010 can run in parallel after T004-T008.
- T016 through T020 can run in parallel with source register row work if merge conflicts in `raa/prompts/source_register.md` are avoided.
- T026 through T030 can run in parallel because each task writes a different excerpt file.
- T032 can run in parallel with manual content boundary checks T033-T035 after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Populate raa/prompts/c4_constraints.md with Section 2B C4 rules for Context, Container, and Component levels"
Task: "Populate raa/prompts/saam_constraints.md with the Section 2B ordered SAAM steps from partitioning through evaluation"
```

## Parallel Example: User Story 2

```bash
Task: "Populate raa/prompts/excerpts/c4_levels.txt with one paraphrased C4 level excerpt of 25 words or fewer"
Task: "Populate raa/prompts/excerpts/c4_technology.txt with one paraphrased C4 technology excerpt of 25 words or fewer"
Task: "Populate raa/prompts/excerpts/saam_steps.txt with one paraphrased SAAM step excerpt of 25 words or fewer"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Populate `raa/prompts/source_register.md`, `raa/prompts/c4_constraints.md`, and `raa/prompts/saam_constraints.md`.
3. Validate source rows and mandatory constraints independently.

### Incremental Delivery

1. Deliver the source register and normative constraint markdown files.
2. Add excerpt files and tag mappings.
3. Run the complete prompt resource validation suite.

### Notes

- Keep excerpt files paraphrased and at 25 words or fewer.
- Do not copy full source documents into runtime prompts.
- Retrieval tags are documented now; executable tag-loading code belongs to the later prompt-loader feature.
