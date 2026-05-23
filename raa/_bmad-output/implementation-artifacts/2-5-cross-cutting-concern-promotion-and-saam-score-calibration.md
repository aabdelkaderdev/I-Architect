# Story 2.5: Cross-Cutting Concern Promotion and SAAM Score Calibration

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an Architect,
I want the Judge to promote global requirements to first-class components and calibrate SAAM scores,
so that cross-cutting infrastructure concerns are clearly modeled and design quality is accurately reflected.

## Acceptance Criteria

1. **Cross-Cutting Detection**: Given the reconciled batch fragment (primary fragment after deduplication/merge), when the Judge finalizes the batch merge, then it must scan entity `cross_cutting_candidates` annotations for global patterns (e.g., security, compliance, logging, monitoring, authentication) using the `INFRA_KEYWORDS` constant list from `raa/utils/constants.py` AND a new `CROSS_CUTTING_PATTERNS` constant list.
2. **Structural Promotion**: When a cross-cutting candidate is detected, the Judge must promote it to a concrete structural boundary component (`c4_type = "component"`) in the `arch_model`, linked to an appropriate parent container.
3. **Relationship Arrow Update**: All affected relationship arrows that previously referenced the cross-cutting concern indirectly (through entities whose `cross_cutting_candidates` list contained the promoted pattern) must be updated to point directly to the promoted component.
4. **Requirement ID Linking**: The cross-cutting requirement ID must be mapped directly to the promoted component's `requirement_ids` rather than being repeated on all arrows or scattered across multiple entities.
5. **SAAM Score Field**: Each `C4Entity` in `state/models.py` must carry a `saam_score: float` field (default `0.0`) for per-entity quality calibration.
6. **Perfect Score Reservation**: A `saam_score` of `1.0` is reserved *only* for entities that have a component-level diagram (i.e., `c4_type == "component"`), no functional overlap with other entities (no shared requirement IDs with entities in the same `boundary_group`), and all direct scenarios passing (every `SAAMScenario` mapped to the entity's requirement IDs has `satisfaction == "satisfied"`).
7. **Reduced Score for Deduplicated/Overlapping Entities**: Entities that were merged (via deduplication) or that participate in boundary groups must receive a reduced SAAM score (< 1.0), calibrated proportionally to overlap and merge status.
8. **Integration Point**: Both cross-cutting promotion and SAAM calibration run inside the Judge reconciliation node (`raa/judge/reconcile.py`) after the deduplication pass from Story 2.4 but before the final state return.
9. **Deterministic Execution**: Cross-cutting promotion and SAAM score calibration must be fully deterministic — no LLM calls, no randomness.
10. **Regression Safety**: All existing tests (scoring, deduplication, reconcile, c4_validator, subgraphs) must continue to pass.

## Tasks / Subtasks

- [x] Task 1: Add `saam_score` field to `C4Entity` model (AC: #5)
  - [x] 1.1 Add `saam_score: float = 0.0` to `C4Entity` in `raa/state/models.py`.
  - [x] 1.2 Verify backward compatibility — existing code that constructs `C4Entity` without `saam_score` must not break (Pydantic default handles this).

- [x] Task 2: Add new constants for cross-cutting and SAAM calibration (AC: #1, #6, #7)
  - [x] 2.1 Add `CROSS_CUTTING_PATTERNS` list to `raa/utils/constants.py` containing global concern keywords: `["security", "compliance", "logging", "monitoring", "authentication", "authorization", "audit", "observability", "rate_limiting", "caching"]`.
  - [x] 2.2 Add `SAAM_PERFECT_SCORE = 1.0` constant.
  - [x] 2.3 Add `SAAM_DEDUP_PENALTY = 0.15` constant (score reduction per merge event).
  - [x] 2.4 Add `SAAM_BOUNDARY_GROUP_PENALTY = 0.10` constant (score reduction for boundary group membership).
  - [x] 2.5 Add `SAAM_BASE_SCORE = 0.70` constant (starting score for entities that don't meet perfect criteria).

- [x] Task 3: Create the Cross-Cutting Promotion Engine (`raa/judge/cross_cutting.py`) (AC: #1, #2, #3, #4, #9)
  - [x] 3.1 Implement `detect_cross_cutting_candidates(arch_model: dict, patterns: list[str]) -> list[dict]` — scans entities in `arch_model` whose `cross_cutting_candidates` field contains any pattern from `CROSS_CUTTING_PATTERNS` or `INFRA_KEYWORDS`. Returns a list of detection records with `entity_id`, `candidate_pattern`, and `requirement_ids`.
  - [x] 3.2 Implement `promote_cross_cutting_to_component(detection: dict, arch_model: dict) -> tuple[C4Entity, list[str]]` — creates a new `C4Entity` with `c4_type="component"`, a generated `id` based on the pattern (e.g., `cc_security`), sets `parent_container_id` to the first container found that references the pattern (or leaves `None` for later resolution), and returns the promoted entity plus a list of entity IDs whose `cross_cutting_candidates` list contributed. The second return element is the list of affected source entity IDs for relationship rewriting.
  - [x] 3.3 Implement `rewrite_relationships_for_promotion(relationships: list[dict], affected_entity_ids: list[str], promoted_component_id: str) -> list[dict]` — for each relationship where `source_id` or `target_id` is in `affected_entity_ids` AND the relationship appears to route through the cross-cutting concern (heuristic: relationship description or metadata mentions the pattern), update the endpoint to point to the promoted component.
  - [x] 3.4 Implement `promote_all_cross_cutting(arch_model: dict) -> tuple[dict, list[dict]]` — orchestrator function that calls detect → promote → rewrite for all detected patterns. Returns updated `arch_model` and any open questions (e.g., ambiguous parent container resolution).
  - [x] 3.5 Ensure requirement IDs from the original cross-cutting annotation are linked to the promoted component's `requirement_ids`, not duplicated across entities.

- [x] Task 4: Create the SAAM Score Calibration Engine (`raa/judge/saam_calibration.py`) (AC: #5, #6, #7, #9)
  - [x] 4.1 Implement `calibrate_entity_saam_scores(arch_model: dict, saam_scenarios: list[dict], boundary_groups: list[dict], merge_log: list[dict]) -> dict` — assigns a `saam_score` to each entity in the model.
  - [x] 4.2 For each entity, start at `SAAM_BASE_SCORE` (0.70).
  - [x] 4.3 Check perfect score eligibility: `c4_type == "component"` AND no shared `requirement_ids` with any entity in the same boundary group AND all `SAAMScenario` entries whose `requirement_ids` intersect the entity's `requirement_ids` have `satisfaction == "satisfied"`. If all conditions are met, set `saam_score = SAAM_PERFECT_SCORE` (1.0).
  - [x] 4.4 Apply `SAAM_DEDUP_PENALTY` for each merge event the entity participated in (from `merge_log`).
  - [x] 4.5 Apply `SAAM_BOUNDARY_GROUP_PENALTY` if the entity is a member of any boundary group.
  - [x] 4.6 Clamp final score to `[0.0, 1.0]`.
  - [x] 4.7 Return the updated `arch_model` with `saam_score` set on every entity.

- [x] Task 5: Integrate into reconciliation node (`raa/judge/reconcile.py`) (AC: #8)
  - [x] 5.1 After the deduplication pass (Story 2.4's `deduplicate_and_merge_fragment`), call `promote_all_cross_cutting(new_arch_model)`.
  - [x] 5.2 After promotion, call `calibrate_entity_saam_scores(...)` passing the model, available SAAM scenarios from the winning fragment, boundary groups, and the dedup merge log.
  - [x] 5.3 Append any cross-cutting open questions to the returned `open_questions` list.
  - [x] 5.4 Return the fully updated `arch_model` with promoted components and calibrated scores.

- [x] Task 6: Update deduplication engine to emit merge log (AC: #7)
  - [x] 6.1 Modify `deduplicate_and_merge_fragment` in `raa/judge/deduplication.py` to return a third element: `merge_log: list[dict]` — each entry records `{"merged_entity_id": str, "source_entity_ids": list[str], "merge_type": "exact_id"|"similarity"}`.
  - [x] 6.2 Update the return type annotation to `tuple[dict, list[dict], list[dict]]`.
  - [x] 6.3 Update all callers in `reconcile.py` to accept the three-element return.

- [x] Task 7: Author comprehensive unit tests (AC: #10)
  - [x] 7.1 Create `tests/raa/unit/test_judge_cross_cutting.py`:
    - Test detection of cross-cutting candidates from entity annotations.
    - Test promotion creates correct component with proper `c4_type`, `requirement_ids`, and generated ID.
    - Test relationship rewriting points affected arrows to promoted component.
    - Test no promotion occurs when no cross-cutting candidates exist.
    - Test multiple cross-cutting patterns produce separate promoted components.
    - Test determinism (same input → same output).
  - [x] 7.2 Create `tests/raa/unit/test_judge_saam_calibration.py`:
    - Test perfect score (1.0) assigned only when all three conditions met.
    - Test base score applied to non-component entities.
    - Test dedup penalty reduces score per merge.
    - Test boundary group penalty reduces score.
    - Test score clamping to [0.0, 1.0].
    - Test empty model returns empty model.
  - [x] 7.3 Update `tests/raa/unit/test_judge_reconcile.py`:
    - Test that reconcile now calls cross-cutting promotion and SAAM calibration after dedup.
    - Test that `C4Entity` objects in returned `arch_model` carry `saam_score` values.
    - Test that merge_log from dedup is properly consumed by calibration.
  - [x] 7.4 Update `tests/raa/unit/test_judge_deduplication.py`:
    - Test that `deduplicate_and_merge_fragment` now returns a 3-tuple with `merge_log`.
    - Test merge_log entries have correct structure.
  - [x] 7.5 Run full regression suite:
    ```bash
    python3 -m pytest tests/raa/unit -q
    ```

### Review Findings

- [x] [Review][Patch] SAAM score degradation of previous components across batches [raa/raa/judge/reconcile.py:129]
- [x] [Review][Patch] Overwriting cross-cutting candidates in reconciliation node [raa/raa/judge/reconcile.py:124]
- [x] [Review][Patch] Missing entity metadata cross-cutting scan on model-level candidates [raa/raa/judge/cross_cutting.py:36]
- [x] [Review][Patch] Self-referential relationships from cross-cutting rewriting [raa/raa/judge/cross_cutting.py:187]
- [x] [Review][Patch] Undercounted merge event penalties in score calibration [raa/raa/judge/saam_calibration.py:25]
- [x] [Review][Patch] Overlapping boundary group check relies on fragile metadata [raa/raa/judge/saam_calibration.py:57]
- [x] [Review][Patch] Loss of deduplication penalties in subsequent batches due to transient merge log [raa/raa/judge/reconcile.py:129]

## Dev Notes

### Current Implementation Baseline

Completed predecessor stories provide these files and contracts:

| File | Current State | Story 2.5 Change |
| --- | --- | --- |
| `raa/judge/reconcile.py` | Scores fragments (Story 2.3), deduplicates and merges primary fragment into `arch_model`, advances `batch_cursor` (Story 2.4). Returns `judge_rankings`, `arch_model`, `batch_cursor`, `open_questions`. | **UPDATE**: After dedup pass, add cross-cutting promotion and SAAM calibration calls. Accept 3-tuple from dedup. |
| `raa/judge/deduplication.py` | Implements conservative entity dedup, merging (similarity ≥ 0.80 + ID overlap), boundary grouping (0.60–0.80), and relationship rewriting. Returns `(updated_model, open_questions)`. | **UPDATE**: Emit a third return element `merge_log` tracking which entities were merged and how. |
| `raa/judge/scoring.py` | Pure SAAM fragment scoring and ranking. Calculates `FragmentScore` with `raw_score`, `multiplier`, `final_score`. Includes `saam_scenarios` from `ArchFragment`. | **UNCHANGED** — scoring ranks fragments; calibration assigns per-entity scores. Different concerns. |
| `raa/state/models.py` | `C4Entity` has `id`, `name`, `description`, `c4_type`, `technology`, `parent_system_id`, `parent_container_id`, `requirement_ids`, `metadata`. `ArchFragment` has `cross_cutting_candidates: list[str]`. | **UPDATE**: Add `saam_score: float = 0.0` to `C4Entity`. |
| `raa/utils/constants.py` | Contains `DEDUP_MERGE_THRESHOLD`, `DEDUP_GROUP_THRESHOLD_LOW/HIGH`, `INFRA_KEYWORDS`, `SAAM_REDUCED_CONFIDENCE_MULTIPLIER`, etc. | **UPDATE**: Add `CROSS_CUTTING_PATTERNS`, `SAAM_PERFECT_SCORE`, `SAAM_BASE_SCORE`, `SAAM_DEDUP_PENALTY`, `SAAM_BOUNDARY_GROUP_PENALTY`. |
| `raa/utils/c4_validator.py` | Passes through `cross_cutting_candidates` during fragment validation. | **UNCHANGED** — validator preserves cross-cutting annotations; this story consumes them. |

### Story Source

Story 2.5 in the epics file combines FR-12 (Cross-Cutting Concern Promotion) and FR-13 (SAAM Score Calibration). [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.5: Cross-Cutting Concern Promotion and SAAM Score Calibration`]

PRD FR-12: The Judge identifies cross-cutting candidates in `ArchFragments` and promotes them to concrete structural boundary components. Affected relationship arrows are updated to point to the promoted component. The cross-cutting requirement is mapped to the promoted component's `requirement_ids`. [Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md`]

PRD FR-13: A `saam_score` of `1.0` is reserved only for entities that have a component-level diagram, no functional overlap, and all direct scenarios passing. Deduplicated or overlapping entities receive a reduced SAAM score. [Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md`]

### Architecture Guardrails

1. **One Node Per File**: Cross-cutting promotion goes in `raa/judge/cross_cutting.py`; SAAM calibration goes in `raa/judge/saam_calibration.py`. Both are pure deterministic engines. The reconcile node in `raa/judge/reconcile.py` orchestrates the calls.
2. **Deterministic Engine**: No LLM calls, no randomness. Pattern matching is keyword-based using `CROSS_CUTTING_PATTERNS` and `INFRA_KEYWORDS` constants.
3. **Named Constants Only**: All thresholds and score values must come from `raa/utils/constants.py` — never inline magic numbers.
4. **State Immutability**: Never mutate input dicts or lists in place. Construct and return new objects.
5. **Pydantic v2 Patterns**: Use `C4Entity.model_validate(dict)` for coercion, not `C4Entity(**dict)`. Add `saam_score` with `Field(default=0.0)`.
6. **Return Dict From Node**: `reconcile.py` must return `dict` matching state channel names — never return full state.
7. **Existing Tests Must Pass**: The `saam_score` default of `0.0` ensures backward compatibility with all existing `C4Entity` construction patterns.
8. **Import from `raa/state/models.py`**: Use the canonical `C4Entity`, `C4Relationship`, `ArchFragment` models — never redefine them.

### Previous Story Intelligence (Story 2.4)

**Key learnings from Story 2.4 deduplication implementation:**
- `EmbeddingCache` and `get_embedding_model` are loaded conditionally — only when both the primary fragment and running model have entities to compare. The first batch (empty running model) skips model loading.
- Model loading is skipped when `cache=None`/`model=None` — dedup falls back to exact normalized-ID matching.
- Pure deterministic engine in separate module, LangGraph node wrapper in `reconcile.py` stays clean.
- `_to_entity()` and `_to_relationship()` coercion helpers use `model_validate()` (Pydantic v2), not double-splat.
- Boundary groups are stored in `arch_model["boundary_groups"]` as `list[dict]` with `group_id`, `entity_ids`, `similarity`, `rationale`.
- Open questions use `question_type` (not `type`) for classification — values include `change_risk`, `high_coupling`.
- Entity metadata carries `boundary_group_id` when an entity is assigned to a boundary group.
- The reconcile node extracts `configurable` from `RunnableConfig` with robust fallback handling.
- All 352+ unit tests passed after Story 2.4.

**Review patches applied in 2.4:**
- Parent C4 hierarchy mismatch flagged as open question on merge.
- Critical relationship referential integrity fixed on entity merge.
- Missing boundary group assignment in entity metadata fixed.
- Dangling boundary groups for merged entities cleaned up.
- Potential `TypeError` crash when relationship metadata is `None` fixed.
- Duplicate technology tags from case sensitivity fixed.
- Non-compliant open question classification fixed.
- ID normalization now filters illegal special characters.
- Pydantic validation uses `model_validate` instead of double-splat.
- RunnableConfig extraction uses robust fallback.

### Git Intelligence

Recent commits show:
- `547dabb` feat(raa): implement Story 2.3 - SAAM-first fragment scoring and judge reconciliation
- `f99c7b8` feat: complete Story 2.6 skill resource loader and tag-based prompt injection
- `f14d721` feat(raa): implement Story 2.1 parallel subgraph execution and state routing

Story 2.4 changes are staged but not yet committed. Files modified: `raa/judge/deduplication.py`, `raa/judge/reconcile.py`, `raa/state/models.py`, `raa/utils/constants.py`, and their tests.

### ArchFragment `cross_cutting_candidates` Usage

The `ArchFragment` model (in `state/models.py`) has `cross_cutting_candidates: list[str]` — a list of string identifiers for cross-cutting concerns detected by the strategy subgraphs. Each subgraph (RAA-A, RAA-B, RAA-C) can populate this field during extraction.

The `c4_validator.py` passes `cross_cutting_candidates` through during validation (line 150). Currently, no downstream code consumes these annotations — this story is where they get acted upon.

### SAAMScenario Model

`SAAMScenario` (in `state/models.py`) has:
- `id: str`
- `description: str`
- `quality_attributes: list[str]`
- `satisfaction: str` — one of `"satisfied"`, `"partial"`, `"unsatisfied"`, `"unknown"`
- `requirement_ids: list[str]`
- `metadata: dict`

SAAM scenarios are part of `ArchFragment.saam_scenarios`. The calibration engine needs access to these to check scenario satisfaction for the perfect score condition.

### Project Structure Notes

New files follow the existing `raa/judge/` module pattern — one engine per file:

```text
raa/judge/
├── __init__.py           # Update docstring to include cross-cutting and calibration
├── reconcile.py          # UPDATE: orchestrate cross-cutting + calibration after dedup
├── deduplication.py      # UPDATE: emit merge_log as third return element
├── scoring.py            # UNCHANGED
├── cross_cutting.py      # NEW: cross-cutting concern promotion engine
└── saam_calibration.py   # NEW: per-entity SAAM score calibration engine
```

Tests follow the existing `tests/raa/unit/` pattern:

```text
tests/raa/unit/
├── test_judge_cross_cutting.py       # NEW
├── test_judge_saam_calibration.py    # NEW
├── test_judge_deduplication.py       # UPDATE (merge_log tests)
└── test_judge_reconcile.py           # UPDATE (integration tests)
```

### Implementation Pitfalls To Avoid

- **Do not conflate fragment scoring with entity calibration.** `scoring.py` (Story 2.3) ranks competing fragments. `saam_calibration.py` (this story) assigns per-entity quality scores after merge. Different concerns, different files.
- **Do not use LLM calls for cross-cutting detection.** Pattern matching is keyword-based and deterministic.
- **Do not modify `scoring.py`.** The SAAM scoring for fragment ranking is complete and correct. Entity-level calibration is a separate layer.
- **Do not break the dedup return signature silently.** Update the return type annotation in `deduplication.py` AND update all callers in `reconcile.py` before running tests.
- **Do not duplicate requirement IDs across promoted components.** When promoting a cross-cutting concern, move (not copy) the requirement ID from scattered entities to the promoted component.
- **Do not mutate `arch_model` in place.** Return new dicts.
- **Do not hardcode score values.** All calibration numbers must be named constants from `constants.py`.
- **Do not forget backward compatibility.** The `saam_score = 0.0` default on `C4Entity` ensures existing tests and code that constructs entities without this field continue working.
- **Do not skip relationship rewriting after promotion.** When a cross-cutting concern is promoted to a component, relationship arrows must be updated to reference the promoted component — same pattern as dedup's relationship rewriting.

### Testing Requirements

Run at minimum:

```bash
python3 -m pytest tests/raa/unit/test_judge_cross_cutting.py -q
python3 -m pytest tests/raa/unit/test_judge_saam_calibration.py -q
python3 -m pytest tests/raa/unit/test_judge_deduplication.py -q
python3 -m pytest tests/raa/unit/test_judge_reconcile.py -q
```

Then run full regression:

```bash
python3 -m pytest tests/raa/unit -q
```

### References

- [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.5: Cross-Cutting Concern Promotion and SAAM Score Calibration`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#Core Architectural Decisions`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#Implementation Patterns & Consistency Rules`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#Project Structure & Boundaries`]
- [Source: `_bmad-output/implementation-artifacts/2-4-conservative-entity-deduplication-and-c4-boundary-grouping.md`]
- [Source: `raa/judge/deduplication.py` — current dedup engine implementation]
- [Source: `raa/judge/reconcile.py` — current reconcile node implementation]
- [Source: `raa/state/models.py` — current C4Entity and ArchFragment models]
- [Source: `raa/utils/constants.py` — current named constants]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

No debug logs — all 414 tests passed on first implementation pass.

### Completion Notes List

- **Task 1**: Added `saam_score: float = Field(default=0.0)` to `C4Entity` in `raa/state/models.py`. Backward compatible — Pydantic default handles all existing construction patterns.
- **Task 2**: Added `CROSS_CUTTING_PATTERNS`, `SAAM_PERFECT_SCORE`, `SAAM_BASE_SCORE`, `SAAM_DEDUP_PENALTY`, `SAAM_BOUNDARY_GROUP_PENALTY` to `raa/utils/constants.py`.
- **Task 3**: Created `raa/judge/cross_cutting.py` with `detect_cross_cutting_candidates`, `promote_cross_cutting_to_component`, `rewrite_relationships_for_promotion`, and `promote_all_cross_cutting`. Detection scans both arch_model-level `cross_cutting_candidates` and entity metadata. Promotion creates `c4_type="component"` entities with generated IDs (`cc_{pattern}`). Requirement IDs are moved (not copied) from affected entities to promoted components.
- **Task 4**: Created `raa/judge/saam_calibration.py` with `calibrate_entity_saam_scores`. Perfect score (1.0) requires: component type, no shared requirement IDs with boundary group members, and all SAAM scenarios satisfied. Base score (0.70) with penalties for dedup merges (-0.15 each) and boundary group membership (-0.10). Clamped to [0.0, 1.0].
- **Task 5**: Integrated into `raa/judge/reconcile.py`. After dedup pass: stores `cross_cutting_candidates` from winning fragment in arch_model, calls `promote_all_cross_cutting`, then `calibrate_entity_saam_scores`. Passes SAAM scenarios and merge_log through the pipeline.
- **Task 6**: Modified `deduplicate_and_merge_fragment` to return 3-tuple `(updated_model, open_questions, merge_log)`. Merge log records `merged_entity_id`, `source_entity_ids`, and `merge_type` ("exact_id" or "similarity") per merge event.
- **Task 7**: Created 51 new tests (24 cross-cutting, 24 calibration, 4 dedup merge_log, 5 reconcile integration). All 414 unit tests pass with zero regressions.

### File List

- `raa/state/models.py` — Added `saam_score` field to `C4Entity`
- `raa/utils/constants.py` — Added `CROSS_CUTTING_PATTERNS`, SAAM calibration constants
- `raa/judge/__init__.py` — Updated docstring
- `raa/judge/cross_cutting.py` — **NEW**: Cross-cutting concern promotion engine
- `raa/judge/saam_calibration.py` — **NEW**: Per-entity SAAM score calibration engine
- `raa/judge/reconcile.py` — Integrated cross-cutting promotion and SAAM calibration after dedup
- `raa/judge/deduplication.py` — Added merge_log as third return element
- `tests/raa/unit/test_judge_cross_cutting.py` — **NEW**: 24 tests for cross-cutting engine
- `tests/raa/unit/test_judge_saam_calibration.py` — **NEW**: 24 tests for SAAM calibration
- `tests/raa/unit/test_judge_deduplication.py` — Added 4 merge_log structure tests
- `tests/raa/unit/test_judge_reconcile.py` — Added 5 integration tests for Story 2.5
