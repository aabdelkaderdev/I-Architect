# Tasks: RAA Synthesis and Audit

**Input**: Design documents from `/specs/021-raa-synthesis-audit/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/audit-checklist.md

**Tests**: Not requested — this is a non-destructive audit feature.

**Organization**: Tasks are grouped by user story. US1 audits the 9 deliverables from §20; US2 audits performance and cost profile from §17. A final phase produces the cross-section completion checklist.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Audit Infrastructure)

**Purpose**: Establish the audit workspace and index all files to be inspected.

- [ ] T001 Create audit report scaffold at `specs/021-raa-synthesis-audit/contracts/audit-report.md` with header, summary table, and placeholder sections for each of the 11 checklist items from `contracts/audit-checklist.md`
- [ ] T002 Build a file-to-section mapping index that lists every `raa/`, `tests/raa/`, `embeddings/`, and `Skills/RAA/` file alongside the RAA_Plan.md section(s) it implements — output as a markdown table into the audit report

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Read and internalise the authoritative specification sections before any audit task begins.

**⚠️ CRITICAL**: No audit task can begin until the auditor has re-read the exact text of §4, §8, §9, §10, §12, §13, §14, §16, §17, and §20 of RAA_Plan.md.

- [ ] T003 Re-read RAA_Plan.md §4 (State Schema, lines 108–284) and extract the full list of state channels, types, and ownership annotations into a reference table inside the audit report
- [ ] T004 [P] Re-read RAA_Plan.md §8 (Batch Construction, lines 381–398), §9 (Overlap Bridging, lines 399–412), §10 (Coherence Gate, lines 413–430) and summarise the normative behaviour for each into the audit report
- [ ] T005 [P] Re-read RAA_Plan.md §12 (Parallel Subgraphs, lines 449–543), §13 (Judge Node, lines 544–583) and summarise the normative behaviour for each into the audit report
- [ ] T006 [P] Re-read RAA_Plan.md §14 (Skills, lines 584–668), §16 (Final Merge, lines 680–726), §2 (Source Register, lines 44–90) and summarise the normative behaviour for each into the audit report

**Checkpoint**: Audit reference material is extracted — deliverable audits can now begin.

---

## Phase 3: User Story 1 — Implementation Audit (Priority: P1) 🎯 MVP

**Goal**: Audit all 9 deliverables from RAA_Plan.md §20 against the implemented files. For each deliverable, confirm existence, verify structural correctness, and record findings.

**Independent Test**: Each deliverable can be audited independently by inspecting the corresponding source file(s) and comparing them against the normative section of RAA_Plan.md.

### Deliverable 1: State Schema (§4 → §20.1)

- [ ] T007 [US1] Audit state channels in `raa/state/channels.py` — verify every channel listed in §4 "New State Channels" is declared with the correct type, default, and reducer
- [ ] T008 [P] [US1] Audit type definitions in `raa/state/types.py` — verify every TypedDict, enum, and Pydantic model from §4 "State Channel Type Definitions" is present and structurally matches
- [ ] T009 [P] [US1] Audit the `raa/state/__init__.py` exports — confirm all channels and types are re-exported, and the `RAAState` TypedDict composes correctly
- [ ] T010 [US1] Audit state serialization in `raa/state/serialization.py` — verify custom serializers exist for non-primitive channel types (e.g. `ArchModel`, `BatchQueue`) and that LLM instances are excluded from serialization per Principle III

### Deliverable 2: Batch Construction Node (§8 → §20.2)

- [ ] T011 [US1] Audit `raa/nodes/batch_construction.py` — verify anchor computation from condition groups, ANN-based non-ASR candidate selection, and batch assembly logic match §8
- [ ] T012 [P] [US1] Audit `tests/raa/test_batch_construction.py` — confirm test coverage for anchor computation, ANN search, empty non-ASR pool, and batch assembly

### Deliverable 3: Overlap Bridging Logic (§9 → §20.3)

- [ ] T013 [US1] Audit `raa/nodes/overlap_bridging.py` — verify adjacent group detection, bridge requirement selection, and hard cap of 3 shared requirements per adjacent pair match §9
- [ ] T014 [P] [US1] Audit `tests/raa/test_overlap_bridging.py` — confirm test coverage for adjacent detection, bridge selection, and hard-cap enforcement

### Deliverable 4: Coherence Gate (§10 → §20.4)

- [ ] T015 [US1] Audit `raa/nodes/coherence_gate.py` — verify coherence scoring, split procedure for heterogeneous batches, and `incoherent_batches` fallback behaviour match §10
- [ ] T016 [P] [US1] Audit `tests/raa/test_coherence_gate.py` — confirm test coverage for scoring, splitting, and reduced-confidence marking

### Deliverable 5: Parallel RAA Orchestration (§12 → §20.5)

- [ ] T017 [US1] Audit `raa/graphs/subgraphs/` — verify three-subgraph structure (`raa_a.py`, `raa_b.py`, `raa_c.py`), shared strategy in `common.py`, and routing logic in `routing.py` match §12
- [ ] T018 [P] [US1] Audit `raa/graphs/subgraphs/__init__.py` — verify input contracts (batch data injected to each subgraph) and output schema (per-subgraph `ArchFragment`) match §12
- [ ] T019 [P] [US1] Audit `raa/graphs/main_graph.py` — verify the main graph wires preparation → batch construction → overlap bridging → coherence gate → batch queue → parallel subgraph fan-out → judge → final merge
- [ ] T020 [P] [US1] Audit `tests/raa/test_parallel_subgraphs.py` — confirm test coverage for three-subgraph invocation, LLM context key isolation (`llm_raa_a`, `llm_raa_b`, `llm_raa_c`), and subgraph output format

### Deliverable 6: Judge Node (§13 → §20.6)

- [ ] T021 [US1] Audit `raa/nodes/judge.py` — verify scoring (SAAM-weighted), merge algorithm (entity deduplication, hierarchy conflict detection, `open_questions`), and residual scan before fragment discard match §13
- [ ] T022 [P] [US1] Audit `tests/raa/test_judge.py` — confirm test coverage for merge algorithm, residual scan, reduced-confidence handling, and SAAM scoring correctness

### Deliverable 7: Final JSON Builder (§16 → §20.7)

- [ ] T023 [US1] Audit `raa/nodes/final_merge.py` — verify deterministic merge across all batch outputs, reconciliation pass for `open_questions`, C4 structural validation (every container inside a system, every component inside a container, no cross-level ID reuse), and `diagram_manifest` generation match §16
- [ ] T024 [P] [US1] Audit `raa/utils/model_serialiser.py` — verify the serialiser produces the final JSON output matching the C4 schema and handles manifest completeness checks
- [ ] T025 [P] [US1] Audit `tests/raa/test_final_merge.py` — confirm test coverage for deterministic merge, reconciliation, orphan prevention, and manifest completeness
- [ ] T026 [P] [US1] Audit `tests/raa/fixtures/golden_model.json` — verify golden fixture contains valid C4 structure with systems, containers, components, relationships, and `diagram_manifest`

### Deliverable 8: Prompt Resource Bundle (§2 → §20.8)

- [ ] T027 [US1] Audit `raa/prompts/source_register.md` — verify it contains the Source Register table from §2A with all normative sources and retrieval tags
- [ ] T028 [P] [US1] Audit `raa/prompts/c4_constraints.md` — verify normative C4 constraints from §2B are present
- [ ] T029 [P] [US1] Audit `raa/prompts/saam_constraints.md` — verify normative SAAM constraints from §2B are present
- [ ] T030 [P] [US1] Audit `raa/prompts/excerpts/` — verify Doc Excerpt Blocks exist (`c4_levels.txt`, `c4_notation.txt`, `c4_technology.txt`, `saam_scenarios.txt`, `saam_steps.txt`) and match §2C/§2D retrieval tagging scheme
- [ ] T031 [US1] Audit `raa/utils/prompt_loader.py` — verify the loader resolves tags to excerpt files and injects constraints into prompts per §7
- [ ] T032 [P] [US1] Audit `tests/raa/test_prompt_loader.py` and `tests/raa/test_prompt_resources.py` — confirm test coverage for prompt loading, tag resolution, and constraint injection

### Deliverable 9: Skill Resource Bundle (§14 → §20.9)

- [ ] T033 [US1] Audit `Skills/RAA/SKILL.MD` — verify it documents the RAA skill entry point and references the 8 reference files per §14
- [ ] T034 [P] [US1] Audit `Skills/RAA/references/` — verify all 8 reference files exist: `SAAM.md`, `C4.md`, `Quality_Attributes.md`, `Entity_Extraction.md`, `Relationship_Extraction.md`, `Pattern_Selection.md`, `Technology_Inference.md`, `C4_Level_Mapping.md`
- [ ] T035 [P] [US1] Audit `tests/raa/test_skill_references.py` — confirm test coverage for skill file existence and reference file enumeration

### US1 Summary

- [ ] T036 [US1] Compile all 9 deliverable audit findings into the audit report and update `contracts/audit-checklist.md` items 1–9 with Pass/Fail/Incomplete status

**Checkpoint**: All 9 deliverables from §20 have been individually audited. US1 is independently verifiable.

---

## Phase 4: User Story 2 — Performance & Cost Profile Audit (Priority: P2)

**Goal**: Validate the complexity profile assertions from §17 and confirm the LLM call count formula.

**Independent Test**: Can be verified by tracing code paths for embedding operations and counting LLM invocation points per batch lifecycle.

### Complexity Profile Verification

- [ ] T037 [US2] Audit `raa/nodes/preparation.py` — trace the non-ASR embedding generation path and confirm it operates in O(n) where n = non-ASR count (no nested loops over embeddings, no pairwise comparisons)
- [ ] T038 [P] [US2] Audit `raa/nodes/batch_construction.py` — trace the ANN similarity search path and confirm it operates in O(k × m) where k = condition groups and m = non-ASR pool (no full cosine similarity matrix computation)
- [ ] T039 [P] [US2] Audit `raa/utils/db.py` — confirm SQLite embedding loads are per-batch (O(batch_size)) and that the full embedding corpus is not loaded into memory at once

### Cosine Similarity Matrix Exclusion

- [ ] T040 [US2] Search the entire `raa/` codebase for any pairwise cosine similarity matrix computation (e.g. `cosine_similarity`, `cdist`, `pdist`, full NxN loops over embeddings) — confirm none exist, only ANN-based search is used

### LLM Call Count Formula

- [ ] T041 [US2] Audit `raa/graphs/subgraphs/routing.py` and `raa/graphs/main_graph.py` — trace the normal batch path and confirm exactly 3 LLM calls are made (one per subgraph: `llm_raa_a`, `llm_raa_b`, `llm_raa_c`)
- [ ] T042 [P] [US2] Audit `raa/nodes/coherence_gate.py` and `raa/graphs/subgraphs/routing.py` — trace the incoherent batch path and confirm only 1 LLM call is made (reduced from 3) when `reduced_confidence` is set
- [ ] T043 [P] [US2] Audit `raa/nodes/judge.py` — confirm exactly 1 Judge LLM call per batch using context key `llm_judge`, and that the deterministic merge path does not invoke the LLM (LLM only used for conflict reconciliation)

### Memory Profile

- [ ] T044 [US2] Audit `raa/nodes/preparation.py` and `raa/utils/db.py` — confirm per-batch SQLite loads and that embedding vectors are not cached globally across batches

### US2 Summary

- [ ] T045 [US2] Compile all performance and cost profile findings into the audit report and update `contracts/audit-checklist.md` items 10–11 with Pass/Fail status

**Checkpoint**: Performance and cost profile from §17 has been fully audited. US2 is independently verifiable.

---

## Phase 5: Polish & Cross-Cutting — Completion Checklist

**Purpose**: Produce the final completion checklist confirming every section of RAA_Plan.md has a corresponding implemented node, test, or reference file.

- [ ] T046 Build the section-to-implementation cross-reference table in `specs/021-raa-synthesis-audit/contracts/audit-report.md` covering all 23 sections of RAA_Plan.md (§0–§22):

  | Section | Title | Implemented File(s) | Test File(s) | Reference File(s) |
  |---------|-------|---------------------|--------------|--------------------|
  | §0 | Goal | `RAA_Plan.md` (specification only) | — | — |
  | §1 | Inputs & Assumptions | `raa/nodes/preparation.py` | `test_preparation.py` | — |
  | §2 | Source Register | `raa/prompts/source_register.md`, `raa/prompts/c4_constraints.md`, `raa/prompts/saam_constraints.md`, `raa/prompts/excerpts/` | `test_prompt_resources.py` | — |
  | §3 | Pipeline Overview | `raa/graphs/main_graph.py` | `test_main_graph.py` | — |
  | §4 | State Schema | `raa/state/channels.py`, `raa/state/types.py`, `raa/state/serialization.py` | — | — |
  | §5 | Requirement Normalization | `raa/nodes/preparation.py` | `test_preparation.py` | — |
  | §6 | Embedding Strategy | `raa/nodes/preparation.py`, `raa/utils/db.py`, `embeddings/asr_embeddings.db` | `test_preparation.py` | — |
  | §7 | Prompt Constraint Injection | `raa/utils/prompt_loader.py` | `test_prompt_loader.py` | — |
  | §8 | Batch Construction | `raa/nodes/batch_construction.py` | `test_batch_construction.py` | — |
  | §9 | Overlap Bridging | `raa/nodes/overlap_bridging.py` | `test_overlap_bridging.py` | — |
  | §10 | Coherence Gate | `raa/nodes/coherence_gate.py` | `test_coherence_gate.py` | — |
  | §11 | Batch Queue Ordering | `raa/nodes/batch_queue.py` | `test_batch_queue.py` | — |
  | §12 | Parallel Subgraphs | `raa/graphs/subgraphs/raa_a.py`, `raa_b.py`, `raa_c.py`, `common.py`, `routing.py` | `test_parallel_subgraphs.py` | — |
  | §13 | Judge Node | `raa/nodes/judge.py` | `test_judge.py` | — |
  | §14 | Skills | `Skills/RAA/SKILL.MD`, `Skills/RAA/references/` (8 files) | `test_skill_references.py` | All 8 reference .md files |
  | §15 | Cross-Batch Coherence | `raa/nodes/judge.py` (running_arch_model injection) | `test_judge.py` | — |
  | §16 | Final Merge | `raa/nodes/final_merge.py`, `raa/utils/model_serialiser.py` | `test_final_merge.py`, `test_model_serialiser.py` | `tests/raa/fixtures/golden_model.json` |
  | §17 | Performance & Cost | (validated via code path audit, no dedicated file) | — | — |
  | §18 | Failure Modes | `raa/utils/failure_register.py` | `test_failure_register.py` | — |
  | §19 | Validation & Testing | `tests/raa/` (all 18 test files) | — | — |
  | §20 | Deliverables | (this audit verifies all 9) | — | — |
  | §21 | Directory Layout | `raa/`, `Skills/RAA/`, `embeddings/` (verified by structure) | — | — |
  | §22 | Checkpointing | `raa/runner.py` | `test_checkpoint_recovery.py` | — |

- [ ] T047 [P] Verify the `raa/runner.py` implements SQLite checkpointing configuration per §22A, graph compilation per §22B, thread identity per §22C, and fresh-start vs. resume logic per §22D
- [ ] T048 [P] Verify `raa/utils/failure_register.py` implements the Failure Modes Register from §18/§22H
- [ ] T049 [P] Verify `tests/raa/test_integration_flow.py` covers the end-to-end integration test from §19 (3-batch flow with known overlaps)
- [ ] T050 Finalize the audit report: update all Pass/Fail/Incomplete statuses, write executive summary, and confirm the audit-checklist in `specs/021-raa-synthesis-audit/contracts/audit-checklist.md` has all 11 items resolved

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all audit work
- **US1 (Phase 3)**: Depends on Phase 2 — 9 deliverable audits are parallelizable within the phase
- **US2 (Phase 4)**: Depends on Phase 2 — can run in parallel with US1
- **Polish (Phase 5)**: Depends on US1 and US2 completion

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — no dependency on US2
- **US2 (P2)**: Can start after Phase 2 — no dependency on US1

### Within Each User Story

- Audit source code files first, then test files
- Deliverables within US1 are independently auditable (T007–T035 have no inter-deliverable dependencies)
- US2 complexity checks (T037–T040) can run in parallel with LLM call count checks (T041–T043)

### Parallel Opportunities

- All Phase 2 tasks marked [P] can run in parallel
- Within US1: deliverables 1–9 can be audited in parallel (different files, no dependencies)
- Within US2: complexity, LLM count, and memory tasks can run in parallel
- US1 and US2 can run in parallel after Phase 2 completes

---

## Parallel Example: User Story 1

```bash
# Launch all deliverable audits for US1 together (after Phase 2):
# Deliverable 1 (State Schema):
Task: "Audit state channels in raa/state/channels.py"
Task: "Audit type definitions in raa/state/types.py"
Task: "Audit state exports in raa/state/__init__.py"

# Deliverable 2 (Batch Construction):
Task: "Audit raa/nodes/batch_construction.py"
Task: "Audit tests/raa/test_batch_construction.py"

# ... all deliverable audits can fan out simultaneously
```

## Parallel Example: User Story 2

```bash
# Launch all performance checks for US2 together:
Task: "Audit O(n) embedding generation in raa/nodes/preparation.py"
Task: "Audit O(k×m) ANN search in raa/nodes/batch_construction.py"
Task: "Search for cosine similarity matrix in raa/"
Task: "Trace 3 LLM calls per normal batch"
Task: "Trace 1 LLM call per incoherent batch"
Task: "Confirm 1 Judge LLM call per batch"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (audit scaffold)
2. Complete Phase 2: Foundational (read normative sections)
3. Complete Phase 3: User Story 1 (audit 9 deliverables)
4. **STOP and VALIDATE**: Verify audit-checklist items 1–9 are resolved
5. Report deliverable completion status

### Incremental Delivery

1. Setup + Foundational → Audit infrastructure ready
2. Add US1 → Audit all 9 deliverables → Report (MVP!)
3. Add US2 → Audit performance and cost profile → Report
4. Add Polish → Cross-section completion checklist → Final Report
5. Each phase adds verification coverage without invalidating previous findings

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- This is a **non-destructive audit** — no source code is modified
- Audit findings are recorded in `specs/021-raa-synthesis-audit/contracts/audit-report.md`
- The audit-checklist in `contracts/audit-checklist.md` is the final deliverable
- Commit after each deliverable audit or logical group
- Stop at any checkpoint to validate story independently
