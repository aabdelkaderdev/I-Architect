# Tasks: RAA Prompt Constraint Injection

**Input**: Design documents from `specs/008-raa-prompt-injection/`
**Source Scope**: `RAA_Plan.md` Section 7 and Section 21C only
**Tests**: Included because the feature specification requires validation for valid tag lookup, node-specific retrieval, whitespace stripping, and missing-asset errors.

**Organization**: Tasks are grouped by independently testable prompt-loader behavior.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm prompt resources and test locations exist before implementing retrieval helpers.

- [X] T001 [P] Confirm prompt excerpt directory exists at `raa/prompts/excerpts/`
- [X] T002 [P] Confirm utility package exists at `raa/utils/`
- [X] T003 [P] Confirm RAA test package exists at `tests/raa/`
- [X] T004 [P] Confirm all excerpt files exist at `raa/prompts/excerpts/c4_levels.txt`, `raa/prompts/excerpts/c4_notation.txt`, `raa/prompts/excerpts/c4_technology.txt`, `raa/prompts/excerpts/saam_steps.txt`, and `raa/prompts/excerpts/saam_scenarios.txt`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Align the feature documentation and define the test expectations before implementation.

- [X] T005 Update `specs/008-raa-prompt-injection/plan.md` to name the implementation module `raa/utils/prompt_loader.py` instead of `raa/utils/prompts.py`
- [X] T006 Update `specs/008-raa-prompt-injection/quickstart.md` imports to use `raa.utils.prompt_loader`
- [X] T007 Create `tests/raa/test_prompt_loader.py` with expected Section 21C node registry values for `entity_extraction`, `relationship_extraction`, `pattern_selection`, `saam_tradeoff`, and `final_merge`
- [X] T008 Add test fixtures in `tests/raa/test_prompt_loader.py` for temporary excerpt files with leading and trailing whitespace

**Checkpoint**: The feature docs and tests target the same module and Section 21C mapping.

---

## Phase 3: User Story 1 - Retrieve Prompt Excerpts by Tag (Priority: P1) MVP

**Goal**: Runtime nodes can retrieve a single tagged excerpt from `raa/prompts/excerpts/` without loading the whole Prompt Resource Bundle.

**Independent Test**: Run `tests/raa/test_prompt_loader.py` and confirm every supported tag maps to the correct excerpt file and returns stripped text content.

### Tests for User Story 1

- [X] T009 [P] [US1] Add a unit test verifying `c4:levels` maps to `raa/prompts/excerpts/c4_levels.txt` in `tests/raa/test_prompt_loader.py`
- [X] T010 [P] [US1] Add a unit test verifying `c4:notation` maps to `raa/prompts/excerpts/c4_notation.txt` in `tests/raa/test_prompt_loader.py`
- [X] T011 [P] [US1] Add a unit test verifying `c4:technology` maps to `raa/prompts/excerpts/c4_technology.txt` in `tests/raa/test_prompt_loader.py`
- [X] T012 [P] [US1] Add a unit test verifying `saam:steps` maps to `raa/prompts/excerpts/saam_steps.txt` in `tests/raa/test_prompt_loader.py`
- [X] T013 [P] [US1] Add a unit test verifying `saam:scenarios` maps to `raa/prompts/excerpts/saam_scenarios.txt` in `tests/raa/test_prompt_loader.py`
- [X] T014 [P] [US1] Add a unit test verifying `load_excerpt` strips leading and trailing whitespace in `tests/raa/test_prompt_loader.py`
- [X] T015 [P] [US1] Add a unit test verifying `load_excerpt` raises `FileNotFoundError` when a translated excerpt path is missing in `tests/raa/test_prompt_loader.py`

### Implementation for User Story 1

- [X] T016 [US1] Create `raa/utils/prompt_loader.py` with constants for `PROMPTS_DIR`, `EXCERPTS_DIR`, and supported tags from Section 21C
- [X] T017 [US1] Implement `tag_to_filename(tag: str) -> str` that maps `:` to `_` and appends `.txt` in `raa/utils/prompt_loader.py`
- [X] T018 [US1] Implement `excerpt_path(tag: str, excerpts_dir: Path | None = None) -> Path` resolving paths under `raa/prompts/excerpts/` in `raa/utils/prompt_loader.py`
- [X] T019 [US1] Implement `load_excerpt(tag: str, excerpts_dir: Path | None = None) -> str` that reads the translated `.txt` file and strips surrounding whitespace in `raa/utils/prompt_loader.py`
- [X] T020 [US1] Ensure `load_excerpt` raises `FileNotFoundError` with the missing path when the excerpt file does not exist in `raa/utils/prompt_loader.py`
- [X] T021 [US1] Add `functools.lru_cache` caching for default-path `load_excerpt` reads without caching test-injected `excerpts_dir` reads in `raa/utils/prompt_loader.py`

**Checkpoint**: Single-tag excerpt retrieval is working and scoped to the excerpt files only.

---

## Phase 4: User Story 2 - Retrieve Only Node-Specific Constraint Excerpts (Priority: P1)

**Goal**: Each RAA node receives only the excerpts listed for that node in the Section 21C tagging table.

**Independent Test**: Run `tests/raa/test_prompt_loader.py` and confirm every node returns exactly its allowed tags and no unrelated excerpt text.

### Tests for User Story 2

- [X] T022 [P] [US2] Add a unit test verifying `entity_extraction` retrieves only `c4:levels` and `c4:notation` in `tests/raa/test_prompt_loader.py`
- [X] T023 [P] [US2] Add a unit test verifying `relationship_extraction` retrieves only `c4:notation` and `c4:technology` in `tests/raa/test_prompt_loader.py`
- [X] T024 [P] [US2] Add a unit test verifying `pattern_selection` retrieves only `c4:levels` in `tests/raa/test_prompt_loader.py`
- [X] T025 [P] [US2] Add a unit test verifying `saam_tradeoff` retrieves only `saam:steps` and `saam:scenarios` in `tests/raa/test_prompt_loader.py`
- [X] T026 [P] [US2] Add a unit test verifying `final_merge` retrieves only `c4:levels`, `c4:notation`, and `c4:technology` in `tests/raa/test_prompt_loader.py`
- [X] T027 [P] [US2] Add a unit test verifying an unknown node name raises `KeyError` in `tests/raa/test_prompt_loader.py`
- [X] T028 [P] [US2] Add a unit test verifying formatted constraint blocks include tag labels and only the provided excerpts in `tests/raa/test_prompt_loader.py`

### Implementation for User Story 2

- [X] T029 [US2] Define `NODE_TAG_REGISTRY` exactly matching `RAA_Plan.md` Section 21C in `raa/utils/prompt_loader.py`
- [X] T030 [US2] Implement `get_node_tags(node_name: str) -> tuple[str, ...]` that returns immutable Section 21C tag lists and raises `KeyError` for unknown nodes in `raa/utils/prompt_loader.py`
- [X] T031 [US2] Implement `get_node_constraints(node_name: str, excerpts_dir: Path | None = None) -> dict[str, str]` that loads only the tags returned by `get_node_tags` in `raa/utils/prompt_loader.py`
- [X] T032 [US2] Implement `format_constraints_block(constraints: dict[str, str]) -> str` with tag-labeled excerpt sections in `raa/utils/prompt_loader.py`
- [X] T033 [US2] Export `load_excerpt`, `get_node_tags`, `get_node_constraints`, and `format_constraints_block` from `raa/utils/__init__.py`

**Checkpoint**: Node-specific prompt constraint retrieval enforces Section 21C isolation.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Validate retrieval policy compliance and keep this feature scoped to prompt loading.

- [X] T034 [P] Run `pytest tests/raa/test_prompt_loader.py`
- [X] T035 [P] Run Python syntax validation for `raa/utils/prompt_loader.py` and `raa/utils/__init__.py`
- [X] T036 Confirm `raa/utils/prompt_loader.py` never reads `raa/prompts/source_register.md`, `raa/prompts/c4_constraints.md`, or `raa/prompts/saam_constraints.md` when loading node excerpts
- [X] T037 Confirm every node in `NODE_TAG_REGISTRY` receives only the excerpts listed in `RAA_Plan.md` Section 21C and no full Prompt Resource Bundle content
- [X] T038 Confirm unsupported Section 7 example-style tags such as `c4:relationships` are not silently mapped unless a corresponding excerpt file and Section 21C mapping are added
- [X] T039 Confirm implementation remains read-only and does not modify any files under `raa/prompts/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational tests and implements single-tag retrieval.
- **User Story 2 (Phase 4)**: Depends on User Story 1 because node retrieval uses single-tag loading.
- **Polish (Final Phase)**: Depends on User Story 1 and User Story 2 completion.

### User Story Dependencies

- **User Story 1 (P1)**: Provides tag-to-file lookup and excerpt loading.
- **User Story 2 (P1)**: Builds node-specific retrieval on top of the single-tag loader.

### Within Each User Story

- Write tests before implementation tasks.
- Implement path translation before file loading.
- Implement node registry before node-specific constraint loading.

### Parallel Opportunities

- T001 through T004 can run in parallel.
- T009 through T015 can be drafted in parallel only if edits to `tests/raa/test_prompt_loader.py` are coordinated.
- T022 through T028 can be drafted in parallel only if edits to `tests/raa/test_prompt_loader.py` are coordinated.
- T034 and T035 can run in parallel after implementation is complete.

---

## Parallel Example: User Story 1

```bash
Task: "Add a unit test verifying c4:levels maps to raa/prompts/excerpts/c4_levels.txt in tests/raa/test_prompt_loader.py"
Task: "Add a unit test verifying saam:steps maps to raa/prompts/excerpts/saam_steps.txt in tests/raa/test_prompt_loader.py"
Task: "Add a unit test verifying load_excerpt strips leading and trailing whitespace in tests/raa/test_prompt_loader.py"
```

## Parallel Example: User Story 2

```bash
Task: "Add a unit test verifying entity_extraction retrieves only c4:levels and c4:notation in tests/raa/test_prompt_loader.py"
Task: "Add a unit test verifying saam_tradeoff retrieves only saam:steps and saam:scenarios in tests/raa/test_prompt_loader.py"
Task: "Add a unit test verifying final_merge retrieves only c4:levels, c4:notation, and c4:technology in tests/raa/test_prompt_loader.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write tests for tag-to-file translation and single excerpt loading.
3. Implement `raa/utils/prompt_loader.py` single-tag retrieval.
4. Validate single-tag retrieval independently.

### Incremental Delivery

1. Deliver tag-to-file excerpt loading.
2. Add Section 21C node registry and node-specific retrieval.
3. Add formatted constraint block helper.
4. Run tests and verify no full prompt bundle files are loaded.

### Notes

- This feature is read-only against `raa/prompts/`.
- Do not implement RAA subgraphs here; they will consume this loader later.
- Keep the module name `raa/utils/prompt_loader.py` to match the current tasking prompt.
