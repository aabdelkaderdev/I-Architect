# Tasks: RAA Validation and Testing

**Input**: Design documents from `/specs/020-raa-validation-testing/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: This feature **is** a test suite — every task produces test code. Tests are the primary deliverable.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Test root**: `tests/raa/`
- **Fixture root**: `tests/raa/fixtures/`
- **Source code**: `raa/` (existing; tests validate against this code)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the test directory scaffold, shared fixtures, and mock infrastructure required by all user stories.

- [x] T001 Create test directory structure: `tests/raa/__init__.py`, `tests/raa/fixtures/` directory, and verify `conftest.py` import path resolves in `tests/raa/conftest.py`
- [x] T002 Implement `FakeChatModel` mock class conforming to `BaseChatModel` interface in `tests/raa/conftest.py` — accepts a `responses: dict[str, str]` mapping prompt substrings to deterministic responses; supports all four context keys (`llm_raa_a`, `llm_raa_b`, `llm_raa_c`, `llm_judge`)
- [x] T003 [P] Implement `mock_arlo_output` pytest fixture in `tests/raa/conftest.py` — returns a valid `ARLOOutput` dict with 5 `asrs`, 10 `non_asr` items, 2 `condition_groups`, and simulated `quality_weights` per data-model.md
- [x] T004 [P] Implement `mock_arch_fragment` pytest fixture in `tests/raa/conftest.py` — returns a simulated `ArchFragment` with 1 system, 2 containers, 3 components, and varied relationships per data-model.md §4
- [x] T005 [P] Implement `mock_sqlite_db` pytest fixture in `tests/raa/conftest.py` — uses `tmp_path` to create isolated `asr_embeddings.db` and `non_asr_embeddings.db` with correct schema (requirement_id, embedding, text_hash, model_name columns)
- [x] T006 [P] Create golden fixture file `tests/raa/fixtures/golden_model.json` — a static, 100% C4-compliant `ArchModel` JSON with 2 systems, 3 containers (distributed across systems), 4 components, 2 persons, 1 external system, and correct relationships with `diagram_scope` values

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared helper utilities used across multiple user stories.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T007 Implement `build_test_batch` helper function in `tests/raa/conftest.py` — constructs a synthetic batch dict from a list of normalized requirement dicts, a condition group ID, and a centroid vector; used by US1 and US2 tests
- [x] T008 [P] Implement `build_running_arch_model` helper function in `tests/raa/conftest.py` — constructs a hierarchical `ArchModel` from a simplified dict specification (systems→containers→components) for use in judge and integration tests
- [x] T009 [P] Implement `assert_c4_structural_integrity` reusable assertion function in `tests/raa/conftest.py` — validates hierarchy nesting, no cross-level ID reuse, relationship endpoint resolution, and `diagram_scope` consistency per §12 scoping rules; used by US3 functional tests

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 — Unit Test Coverage for RAA Core Nodes (Priority: P1) 🎯 MVP

**Goal**: Validate isolated behavior of RAA preparation, batch assembly, coherence gate, and entity deduplication nodes.

**Independent Test**: Run `pytest tests/raa/test_preparation.py tests/raa/test_batching.py tests/raa/test_judge.py -v`

### Unit Tests: Embedding Model Consistency (FR-001)

- [x] T010 [P] [US1] Write test `test_model_name_consistency` in `tests/raa/test_preparation.py` — populate `asr_embeddings.db` and `non_asr_embeddings.db` with rows using the same `model_name` value (`mixedbread-ai/mxbai-embed-large-v1`), then assert the preparation node does not raise; then populate with mismatched `model_name` values and assert the preparation node raises a `ValueError` or equivalent rejection

### Unit Tests: Preparation Node Rejection (§6, §19 Unit Tests bullet 2)

- [x] T011 [P] [US1] Write test `test_preparation_rejects_missing_asr_db` in `tests/raa/test_preparation.py` — invoke the preparation node with no `asr_embeddings.db` file present and assert a blocking error is raised with instructions to re-run ARLO
- [x] T012 [P] [US1] Write test `test_preparation_rejects_incomplete_asr_ids` in `tests/raa/test_preparation.py` — populate `asr_embeddings.db` with only 3 of 5 expected ASR IDs, invoke the preparation node, and assert a blocking error identifying the 2 missing ASR IDs

### Unit Tests: Stale Text Hash Recomputation (§6, §19 Unit Tests bullet 3)

- [x] T013 [P] [US1] Write test `test_stale_text_hash_triggers_recomputation` in `tests/raa/test_preparation.py` — insert a row into `non_asr_embeddings.db` with a `text_hash` that does not match the current requirement text's SHA-256, invoke the preparation node, and assert the embedding blob is updated and `text_hash` now matches
- [x] T014 [P] [US1] Write test `test_fresh_text_hash_skips_recomputation` in `tests/raa/test_preparation.py` — insert a row with a matching `text_hash`, invoke the preparation node, and assert the embedding blob is unchanged (not recomputed)

### Unit Tests: Batch Assembly Completeness (§8, §19 Unit Tests bullet 4)

- [x] T015 [P] [US1] Write test `test_batch_includes_all_condition_group_asrs` in `tests/raa/test_batching.py` — create a condition group with 3 ASR IDs and corresponding embeddings, run batch assembly, and assert all 3 ASR IDs appear in the resulting batch
- [x] T016 [P] [US1] Write test `test_batch_includes_non_asr_candidates` in `tests/raa/test_batching.py` — create a condition group with 2 ASRs and 5 non-ASR candidates with similarity ≥ 0.65, run batch assembly, and assert non-ASR candidates meeting the threshold are included (capped at 10)

### Unit Tests: Bridge Requirement Cap Enforcement (§9, §19 Unit Tests bullet 5, FR-002)

- [x] T017 [P] [US1] Write test `test_bridge_cap_enforcement` in `tests/raa/test_batching.py` — provide 5 candidate bridge requirements for an adjacent pair, run the overlap bridging logic, and assert that exactly 3 (hard cap) bridge requirements are selected
- [x] T018 [P] [US1] Write test `test_bridge_requirements_appear_in_both_batches` in `tests/raa/test_batching.py` — with 2 adjacent batches and 2 bridge requirements, assert each bridge requirement ID appears in both batches' requirement lists

### Unit Tests: Coherence Gate Split Correctness (§10, §19 Unit Tests bullet 6)

- [x] T019 [P] [US1] Write test `test_coherence_gate_passes_homogeneous_batch` in `tests/raa/test_batching.py` — create a synthetic batch where all embeddings have intra-batch cosine similarity ≥ 0.55, run the coherence gate, and assert the batch passes without splitting
- [x] T020 [P] [US1] Write test `test_coherence_gate_splits_heterogeneous_batch` in `tests/raa/test_batching.py` — create a synthetic batch with two distinct embedding clusters (cosine similarity < 0.55), run the coherence gate, and assert the output is 2 sub-batches replacing the original
- [x] T021 [P] [US1] Write test `test_coherence_gate_flags_incoherent_after_split` in `tests/raa/test_batching.py` — create a batch where even after splitting both sub-clusters remain below 0.55, and assert the batch is added to `incoherent_batches` with `reduced_confidence = true`

### Unit Tests: Per-Type Entity Deduplication with Hierarchy Conflict Detection (§13, §19 Unit Tests bullet 7, FR-003, FR-004)

- [x] T022 [P] [US1] Write test `test_entity_dedup_per_type` in `tests/raa/test_judge.py` — provide 3 synthetic `ArchFragment`s with overlapping system, container, and component IDs across fragments; assert deduplication operates per entity type (systems against systems, containers against containers, etc.) and produces canonical IDs in deterministic order regardless of input fragment order
- [x] T023 [P] [US1] Write test `test_entity_dedup_longest_description_wins` in `tests/raa/test_judge.py` — provide 2 fragments with the same container ID but different description lengths; assert the merged entity uses the longest description
- [x] T024 [P] [US1] Write test `test_hierarchy_conflict_detection` in `tests/raa/test_judge.py` — provide 2 fragments with the same container canonical ID but different `parent_system_id` values; assert a `hierarchy_conflict` entry is recorded in `open_questions` with the correct `entity_id`
- [x] T025 [P] [US1] Write test `test_hierarchy_conflict_component_level` in `tests/raa/test_judge.py` — provide 2 fragments with the same component canonical ID but different `parent_container_id` values; assert a `hierarchy_conflict` entry is recorded in `open_questions`
- [x] T026 [P] [US1] Write test `test_no_cross_level_id_reuse` in `tests/raa/test_judge.py` — provide a fragment where the same string ID is used as both a system ID and a container ID; assert the deduplication/validation step detects and flags this as an error (FR-004)
- [x] T027 [P] [US1] Write test `test_deterministic_canonical_id_order` in `tests/raa/test_judge.py` — provide 3 fragments in different input orders (shuffled), run deduplication twice, and assert the output entity lists are identical in order both times (FR-003)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 — Integration Test Coverage for Cross-Batch Operations (Priority: P1)

**Goal**: Validate data flow and state consistency across multiple batch runs, bridge overlap logic, and the judge's merge process.

**Independent Test**: Run `pytest tests/raa/test_integration.py -v`

### Integration Tests: End-to-End 3-Batch Bridge Overlap (§19 Integration Tests bullet 1)

- [x] T028 [US2] Write test `test_3_batch_bridge_overlap_end_to_end` in `tests/raa/test_integration.py` — construct 3 synthetic batches with known overlaps (batch 1↔2 share 2 bridge reqs, batch 2↔3 share 1 bridge req), invoke the full pipeline (preparation → batch construction → overlap bridging → coherence gate → subgraph fan-out → judge) using `FakeChatModel` stubs, and assert: (a) bridge requirements appear in both adjacent batches, (b) total bridge count per pair ≤ 3, (c) `bridge_requirements` state channel is populated correctly

### Integration Tests: Judge Running Arch Model Non-Contradiction (§19 Integration Tests bullet 2, FR-005)

- [x] T029 [US2] Write test `test_judge_running_arch_model_non_contradiction` in `tests/raa/test_integration.py` — process 2 sequential batches where batch 1 establishes entities (1 system, 1 container with a relationship), and batch 2 introduces entities that reference the same IDs; assert that `running_arch_model` after batch 2 contains no contradictory relationship directions (same `source_id`→`target_id` pair, same `interaction_type`) compared to batch 1's output
- [x] T030 [P] [US2] Write test `test_cross_batch_entity_consistency` in `tests/raa/test_integration.py` — process 2 batches where both mention the same canonical container ID; assert after merge the container retains a single consistent entry (not duplicated), and its `parent_system_id` is consistent across batches (FR-005)

### Integration Tests: Incoherent Batch Reduced Confidence Propagation (§19 Integration Tests bullet 3)

- [x] T031 [US2] Write test `test_incoherent_batch_reduced_confidence_propagation` in `tests/raa/test_integration.py` — construct 3 batches where batch 2 is flagged as incoherent by the coherence gate (`reduced_confidence = true`), process end-to-end, and assert: (a) entities originating from batch 2 have `reduced_confidence = true` in `confidence_metadata`, (b) the 0.5× SAAM weight multiplier is applied to batch 2's scores, (c) the incoherent batch ran a single RAA subgraph (not three parallel)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 — Functional Test Coverage for Output Validation (Priority: P1)

**Goal**: Guarantee that the final `C4JsonModel` output strictly adheres to C4 constraints and that SAAM judge scoring is correct.

**Independent Test**: Run `pytest tests/raa/test_final_merge.py -v`

### Functional Tests: Structural Integrity Assertions (§19 Functional Tests bullet 1)

- [x] T032 [P] [US3] Write test `test_hierarchy_nesting_containers_in_systems` in `tests/raa/test_final_merge.py` — load `golden_model.json`, assert every container exists nested inside a system node's `containers` list (not floating at top level)
- [x] T033 [P] [US3] Write test `test_hierarchy_nesting_components_in_containers` in `tests/raa/test_final_merge.py` — load `golden_model.json`, assert every component exists nested inside a container node's `components` list
- [x] T034 [P] [US3] Write test `test_no_cross_level_id_reuse_functional` in `tests/raa/test_final_merge.py` — collect all entity IDs from the final output (systems, containers, components, persons, external_systems) and assert no ID string appears at more than one level in the hierarchy (FR-004)
- [x] T035 [P] [US3] Write test `test_all_relationship_endpoints_resolve` in `tests/raa/test_final_merge.py` — collect all `source_id` and `target_id` values from every relationship in the model (context_relationships, container_relationships, component_relationships) and assert each resolves to an entity that exists somewhere in the model (systems, containers, components, persons, or external_systems)
- [x] T036 [P] [US3] Write test `test_diagram_scope_endpoint_consistency` in `tests/raa/test_final_merge.py` — for every relationship in the model, verify its `diagram_scope` is consistent with the types of its endpoints according to the §12 scoping rules: system↔system/person/external → `context`, container↔container/person/external → `container`, component↔component/container/external → `component`
- [x] T037 [P] [US3] Write test `test_structural_integrity_on_synthetic_output` in `tests/raa/test_final_merge.py` — run the final merge node on the `mock_arch_fragment` fixture list (3 fragments) and apply `assert_c4_structural_integrity` (from T009) to the merged output, ensuring all invariants hold on dynamically produced output (not just the static golden file)

### Functional Tests: Manifest Completeness Formula Verification (§19 Functional Tests bullet 2)

- [x] T038 [P] [US3] Write test `test_manifest_completeness_formula` in `tests/raa/test_final_merge.py` — given the `golden_model.json` output, assert `len(diagram_manifest) == (2 * len(systems)) + sum(len(s.containers) for s in systems)` and that the manifest contains exactly 1 context entry + 1 container entry per system, and exactly 1 component entry per container
- [x] T039 [P] [US3] Write test `test_manifest_entry_ids_match_entities` in `tests/raa/test_final_merge.py` — assert every `focus_entity_id` in the `diagram_manifest` resolves to an actual entity in the model, and every `diagram_id` follows the canonical naming (`ctx-{id}`, `cnt-{id}`, `cmp-{id}`)

### Functional Tests: Orphan Prevention (§19 Functional Tests bullet 3)

- [x] T040 [P] [US3] Write test `test_orphan_component_rejected` in `tests/raa/test_final_merge.py` — provide a synthetic fragment containing a component with a `parent_container_id` that does not exist in the running model or the same fragment; assert the judge records a `coverage_gap` in `open_questions` and does NOT add the component to the merged output
- [x] T041 [P] [US3] Write test `test_orphan_container_rejected` in `tests/raa/test_final_merge.py` — provide a synthetic fragment containing a container with a `parent_system_id` that does not exist in the running model or the same fragment; assert the judge records a `coverage_gap` in `open_questions` and does NOT add the container to the merged output

### Functional Tests: Cross-Batch Entity Consistency (§19 Functional Tests bullet 4)

- [x] T042 [US3] Write test `test_cross_batch_entity_no_contradictory_directions` in `tests/raa/test_final_merge.py` — provide 2 batch outputs where the same relationship (`source_id`, `target_id`) exists but with contradictory `interaction_type` or reversed direction; assert the final merge resolves the conflict (selecting higher SAAM score) and records a warning in `open_questions`

### Functional Tests: SAAM Scoring Correctness (§19 Functional Tests bullet 5)

- [x] T043 [US3] Write test `test_saam_scoring_correctness` in `tests/raa/test_final_merge.py` — provide 2 synthetic `ArchFragment`s with known quality-attribute coverage profiles (fragment A covers Security+Reliability with higher weights, fragment B covers only Usability); assert the judge ranks fragment A higher, verified against a golden fixture with ground-truth expected ranking
- [x] T044 [P] [US3] Write test `test_saam_reduced_confidence_multiplier` in `tests/raa/test_final_merge.py` — provide a fragment marked `reduced_confidence = true` and a normal fragment with equal raw SAAM scores; assert the reduced-confidence fragment's effective score is 0.5× the normal fragment's score after the multiplier is applied

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T045 [P] Add pytest markers `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.functional` to all test functions in `tests/raa/test_preparation.py`, `tests/raa/test_batching.py`, `tests/raa/test_judge.py`, `tests/raa/test_integration.py`, `tests/raa/test_final_merge.py`
- [x] T046 [P] Add `pytest.ini` or `pyproject.toml` marker registration for `unit`, `integration`, `functional` markers to suppress warnings
- [x] T047 Run full test suite `pytest tests/raa/ -v` and verify all tests pass within the < 2 minutes sequential execution target (SC-003)
- [x] T048 [P] Run quickstart.md validation — execute all commands from `specs/020-raa-validation-testing/quickstart.md` and confirm expected outputs
- [x] T049 Verify SC-002 coverage: cross-reference every bullet in RAA_Plan.md §19 (Unit Tests, Integration Tests, Functional Tests) against task IDs and confirm 100% coverage

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) — Uses `FakeChatModel` and fixtures from Phase 1-2; independent of US1 test files
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) — Uses `golden_model.json` from T006 and `assert_c4_structural_integrity` from T009

### §19 Criterion → Task Traceability

| §19 Criterion | Task ID(s) |
|---|---|
| Unit: model_name consistency | T010 |
| Unit: preparation rejects missing ASR IDs | T011, T012 |
| Unit: stale text_hash recomputation | T013, T014 |
| Unit: batch assembly completeness | T015, T016 |
| Unit: bridge cap ≤ 3 | T017, T018 |
| Unit: coherence gate split | T019, T020, T021 |
| Unit: per-type entity dedup + hierarchy conflict | T022–T027 |
| Integration: 3-batch bridge overlap | T028 |
| Integration: judge running_arch_model non-contradiction | T029, T030 |
| Integration: incoherent batch reduced_confidence | T031 |
| Functional: structural integrity | T032–T037 |
| Functional: manifest completeness | T038, T039 |
| Functional: orphan prevention | T040, T041 |
| Functional: cross-batch consistency | T042 |
| Functional: SAAM scoring correctness | T043, T044 |

### Parallel Opportunities

**Within Phase 1 (Setup):**
```
T003 (mock_arlo_output) ‖ T004 (mock_arch_fragment) ‖ T005 (mock_sqlite_db) ‖ T006 (golden_model.json)
```

**Within Phase 3 (US1) — all [P] tasks can run in parallel since they target different test functions:**
```
T010 ‖ T011 ‖ T012 ‖ T013 ‖ T014    # preparation tests
T015 ‖ T016 ‖ T017 ‖ T018           # batching tests
T019 ‖ T020 ‖ T021                   # coherence gate tests
T022 ‖ T023 ‖ T024 ‖ T025 ‖ T026 ‖ T027  # judge dedup tests
```

**Across User Stories (after Phase 2):**
```
US1 (test_preparation + test_batching + test_judge) ‖ US2 (test_integration) ‖ US3 (test_final_merge)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (fixtures + mocks)
2. Complete Phase 2: Foundational (helpers)
3. Complete Phase 3: User Story 1 (unit tests)
4. **STOP and VALIDATE**: `pytest tests/raa/test_preparation.py tests/raa/test_batching.py tests/raa/test_judge.py -v`
5. All 18 unit tests pass → MVP delivered

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → Test independently → 18 unit tests passing (MVP!)
3. Add US2 → Test independently → 4 integration tests passing
4. Add US3 → Test independently → 13 functional tests passing
5. Each story adds validation coverage without breaking previous stories

---

## Notes

- [x] tasks = completed
- [P] tasks = different files or functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All tests MUST use mocked LLMs (`FakeChatModel`) — zero network calls (FR-006)
- All SQLite DBs MUST use `tmp_path` fixtures for isolation (research.md decision)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
