# Story 2.3: SAAM-First Fragment Scoring

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want the Judge to score each subgraph's fragment using ARLO quality weights,
so that we deterministically designate the highest-quality design as the primary structure.

## Acceptance Criteria

1. **Score all available fragments**: Given raw `ArchFragment` output records from RAA-A, RAA-B, and RAA-C in `batch_outputs`, and ARLO `quality_weights`, when the Judge scores the current batch, then it must calculate one deterministic score record per non-skipped fragment.

2. **Scenario-to-weight mapping**: Given a fragment contains SAAM scenario metadata, when scoring, then each scenario must map to one or more quality attributes and contribute according to `quality_weights` frequency values.

3. **Primary fragment selection**: Given scored fragments, when scoring completes, then the highest-scoring fragment must be selected as the primary structural template for later merge work.

4. **Deterministic tie-breaking**: Given two or more fragments have the same score, when selecting the primary fragment, then the Judge must choose deterministically using strategy order `raa_a`, `raa_b`, `raa_c`, then stable `thread_id`.

5. **Reduced-confidence multiplier**: Given a fragment record has `reduced_confidence = true`, when scoring it, then the Judge must apply the `0.5` SAAM multiplier to that fragment's final score.

6. **Single-strategy fallback**: Given parallel execution was skipped and only RAA-A produced a fragment, when scoring, then the Judge must select the RAA-A fragment as primary and record skipped strategies as non-scored.

7. **No premature merge or cursor advancement**: Given Story 2.3 only ranks fragments, when scoring completes, then it must not deduplicate entities, merge into `arch_model`, or advance `batch_cursor`; those remain later Judge responsibilities.

8. **Auditable score output**: Given scoring completes, when the node returns, then it must expose score details with enough metadata for later Judge merge: `batch_id`, `batch_index`, `strategy`, `thread_id`, raw score, multiplier, final score, scenario contributions, and primary/secondary role.

## Tasks / Subtasks

- [x] Task 1: Add SAAM scoring models to canonical state models (AC: #1, #2, #8)
  - [x] 1.1 Update `raa/state/models.py`; do not create scoring Pydantic models inside `raa/judge/*`.
  - [x] 1.2 Add a permissive `SAAMScenario` model with fields such as `id`, `description`, `quality_attributes`, `satisfaction`, `requirement_ids`, and `metadata`.
  - [x] 1.3 Add `saam_scenarios: list[SAAMScenario] = Field(default_factory=list)` to `ArchFragment`; keep existing fields and defaults compatible with Stories 2.1 and 2.2 tests.
  - [x] 1.4 Add `FragmentScore` or equivalent Pydantic model with `batch_id`, `batch_index`, `strategy`, `thread_id`, `raw_score`, `multiplier`, `final_score`, `scenario_contributions`, and `is_primary`.
  - [x] 1.5 Keep models Pydantic `BaseModel`, not dataclasses.

- [x] Task 2: Create the Judge scoring package (AC: #1, #2, #3, #4, #5, #6, #8)
  - [x] 2.1 Create `raa/judge/__init__.py`.
  - [x] 2.2 Create `raa/judge/scoring.py`.
  - [x] 2.3 Implement a pure scoring function such as `score_fragment_record(record: dict, quality_weights: dict[str, int]) -> FragmentScore | None`.
  - [x] 2.4 Implement a batch ranking function such as `rank_batch_fragments(records: list[dict], quality_weights: dict[str, int]) -> dict`.
  - [x] 2.5 Ignore records with `skipped = true` or `arch_fragment is None`; include them only in skipped metadata, not score calculations.
  - [x] 2.6 Accept both dict fragments and `ArchFragment` instances because Story 2.1 normalizes production records to dicts while tests may use model instances.
  - [x] 2.7 Use strategy tie-break order `raa_a`, `raa_b`, `raa_c`; then sort by `thread_id`.
  - [x] 2.8 Never rely on incoming `batch_outputs` list order. Sort/filter using stable metadata.

- [x] Task 3: Define SAAM scoring semantics (AC: #2, #5, #8)
  - [x] 3.1 Normalize quality attribute keys case-insensitively where practical, but preserve original keys in output metadata.
  - [x] 3.2 Scenario contribution should be deterministic and documented in code. Recommended baseline: contribution equals the sum of matching quality weights multiplied by satisfaction factor.
  - [x] 3.3 Use satisfaction factors such as `satisfied = 1.0`, `partial` or `partially_satisfied = 0.5`, `unsatisfied = 0.0`; unknown satisfaction should be handled explicitly.
  - [x] 3.4 If a fragment has no `saam_scenarios`, fall back to traceable fragment evidence rather than producing random output. Recommended fallback: score by weighted coverage of entity `requirement_ids` whose source requirements carry matching quality attributes, or return `0.0` with an explanatory score note if no mapping exists.
  - [x] 3.5 Apply `SAAM_REDUCED_CONFIDENCE_MULTIPLIER` from constants for reduced-confidence fragments; do not inline `0.5`.
  - [x] 3.6 Keep score calculations pure: no LLM calls, no SQLite access, no embedding access.

- [x] Task 4: Add constants and matrix loading support where needed (AC: #2, #5)
  - [x] 4.1 Update `raa/utils/constants.py` with named constants such as `SAAM_REDUCED_CONFIDENCE_MULTIPLIER = 0.5` and satisfaction factors.
  - [x] 4.2 If scoring uses `matrix.json`, create `raa/utils/matrix_loader.py` and load it once through an explicit function; do not read `matrix.json` inside every scoring call.
  - [x] 4.3 If `matrix.json` is not used in this story, document that decision in the scoring module docstring so later pattern scoring can add it intentionally.

- [x] Task 5: Add a Judge node wrapper without performing merge (AC: #3, #6, #7, #8)
  - [x] 5.1 Create `raa/judge/reconcile.py` only if a node wrapper is needed now; otherwise keep the story scoped to `scoring.py` and tests.
  - [x] 5.2 Implement `select_primary_fragment(state: RAAState, config: RunnableConfig | None = None) -> dict` if adding a node wrapper.
  - [x] 5.3 The node must select records for the current `batch_cursor` only.
  - [x] 5.4 The node must return only state updates, never the full state.
  - [x] 5.5 Do not return `batch_cursor`, do not update `arch_model`, and do not perform deduplication or boundary grouping.
  - [x] 5.6 Store ranking results in an auditable channel or existing metadata shape that later stories can consume. If a new state key is required, update `RAAState` with a `NotRequired` field and explain why it is not an append reducer.

- [x] Task 6: Unit tests for pure scoring (AC: #1, #2, #3, #4, #5, #6, #8)
  - [x] 6.1 Add `tests/raa/unit/test_judge_scoring.py`.
  - [x] 6.2 Test scoring a fragment with multiple SAAM scenarios and quality weights.
  - [x] 6.3 Test partial and unsatisfied scenario satisfaction factors.
  - [x] 6.4 Test reduced-confidence records apply exactly the named `0.5` multiplier.
  - [x] 6.5 Test skipped records and `arch_fragment = None` are excluded from scored fragments.
  - [x] 6.6 Test single RAA-A fallback selects RAA-A primary.
  - [x] 6.7 Test deterministic tie-breaking by strategy order and then `thread_id`.
  - [x] 6.8 Test input order does not affect the selected primary or score ordering.
  - [x] 6.9 Test dict and `ArchFragment` inputs both work.

- [x] Task 7: Regression tests for existing graph/subgraph behavior (AC: #7)
  - [x] 7.1 Run existing Story 2.1 and Story 2.2 tests after model changes.
  - [x] 7.2 Ensure adding `saam_scenarios` to `ArchFragment` does not break prompt parsing, C4 validation, output normalization, or strategy subgraph tests.
  - [x] 7.3 If a node wrapper is added, test that `batch_cursor` is not returned and `arch_model` is not modified.

### Review Findings

- [x] [Review][Decision] Explanatory score note is discarded and lost in `FragmentScore` — The `score_note` variable returned from the fallback scoring function `_score_by_requirement_coverage` is not stored anywhere in `FragmentScore`, which violates AC #8/Task 3.4 requirements to expose enough score detail and metadata for later Judge merge work. (Decision: Embed note in contributions list)
- [x] [Review][Decision] Fallback requirement coverage does not map to quality attributes — In Task 3.4, the recommended fallback is to score by weighted coverage of entity `requirement_ids` whose source requirements carry matching quality attributes. The current implementation assigns a flat weight of `1.0` to each requirement without resolving their quality attributes since it lacks access to the state's `requirements` dictionary. (Decision: Keep simplified fallback and update docstrings)
- [x] [Review][Patch] Missing error handling in `ArchFragment` dictionary instantiation [raa/judge/scoring.py:102]
- [x] [Review][Patch] Potential `AttributeError` on non-string `satisfaction` value [raa/judge/scoring.py:126]
- [x] [Review][Patch] Potential `AttributeError` on non-dict elements in `batch_outputs` [raa/judge/reconcile.py:50-53]
- [x] [Review][Patch] Type hint mismatch for fallback scoring return type [raa/judge/scoring.py:144-147]
- [x] [Review][Patch] Shared mutable state reference mutation in reconcile node [raa/judge/reconcile.py:58-61]
- [x] [Review][Patch] Potential `AttributeError` on non-string quality attribute [raa/judge/scoring.py:140]

## Dev Notes

### Current Implementation Baseline

Completed predecessor stories provide these files and contracts:

| File | Current State | Story 2.3 Change |
| --- | --- | --- |
| `raa/state/models.py` | Defines `NormalizedRequirement`, `C4Entity`, `C4Relationship`, and `ArchFragment`; `ArchFragment` has no SAAM scenario list yet. | Add SAAM scenario and scoring models while preserving backwards-compatible defaults. |
| `raa/state/schemas.py` | `RAAState` has append reducers for `batch_outputs`, `open_questions`, and `incoherent_batches`; no Judge scoring channel exists. | Add only the minimum state key needed for auditable ranking if a node wrapper is implemented. |
| `raa/graphs/execution_loop.py` | Produces `batch_outputs` records with `batch_id`, `batch_index`, `strategy`, `thread_id`, `reduced_confidence`, `arch_fragment`, `skipped`, `skip_reason`; also propagates `open_questions`. | Consume this exact record shape. Do not change dispatch behavior for this story. |
| `raa/subgraphs/raa_a.py` | Produces validated `ArchFragment` via `load_prompt(...)` and `with_structured_output(ArchFragment, include_raw=True)`. | Future RAA-A prompts may populate `saam_scenarios`; scoring must tolerate missing scenarios during transition. |
| `raa/Skills/references/saam.md` | Defines SAAM rules and checklist as tagged skill sections. | Reuse as documentation/source guidance; scoring code should stay deterministic and not parse prompt text. |
| `matrix.json` | Read-only pattern-to-quality matrix exists at project root. | Use only if needed; architecture says load once, not per node invocation. |

There is currently no `raa/judge/` package.

### Story Source

Story 2.3 in the epics file requires the Judge to score raw `ArchFragment` outputs from RAA-A/B/C using ARLO quality weights, select the highest-scoring fragment as the primary structural template, apply a `0.5x` multiplier for `reduced_confidence = true`, and fall back to RAA-A when parallel execution was skipped. [Source: `_bmad-output/planning-artifacts/epics.md#Story 2.3: SAAM-First Fragment Scoring`]

The PRD FR-10 repeats the same behavioral contract: scenarios mapped by subgraphs are evaluated against quality weight frequencies, the highest-scoring fragment becomes primary, and incoherent batches receive the `0.5x` multiplier. [Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md#FR-10: SAAM-First Fragment Scoring`]

### Architecture Guardrails

1. RAA is a LangGraph subgraph module, not a web service. Keep Judge logic as Python package code and optional graph node functions. [Source: `_bmad-output/planning-artifacts/architecture.md#Integration Boundaries`]
2. `batch_outputs` ordering is reducer-safe but not semantically ordered. Use record metadata for deterministic sorting. [Source: `_bmad-output/implementation-artifacts/2-1-concurrency-orchestrator-and-parallel-subgraph-dispatch.md#Output Record Contract`]
3. The 0.5 multiplier is applied by the Judge, not by RAA-A or dispatch. [Source: `_bmad-output/planning-artifacts/architecture.md#D7 - Incoherent Batch Fallback Strategy`]
4. `batch_cursor` advancement must stay coupled to later Judge merge state writes; Story 2.3 must not advance it. [Source: `_bmad-output/planning-artifacts/architecture.md#Key Cross-Cutting Concerns`]
5. All node functions return state update dictionaries and never mutate/return the full state. [Source: `_bmad-output/planning-artifacts/architecture.md#Process Patterns`]
6. Use named constants instead of inline thresholds or multipliers. [Source: `_bmad-output/planning-artifacts/architecture.md#Data Format Patterns`]
7. `matrix.json` access, if used, must be loaded once and passed/configured intentionally; do not re-read inside a node. [Source: `_bmad-output/planning-artifacts/architecture.md#Process Patterns`]

### LangChain Docs MCP References

The LangChain docs MCP was consulted before writing this story:

- `/oss/python/langgraph/graph-api`: LangGraph nodes accept state and may accept `RunnableConfig`; nodes return partial updates, not whole state. Reducers control how updates apply.
- `/oss/python/langgraph/use-graph-api`: parallel/reducer outputs may not have deterministic list order; attach stable metadata and sort when deterministic behavior is required.
- `/oss/python/langchain/models`: `with_structured_output(Model, include_raw=True)` returns parsed model data plus raw message and parsing error metadata. Existing subgraphs already use this; scoring should consume the parsed `ArchFragment`, not raw text.
- `/oss/python/langchain/test/unit-testing`: use fake chat models or in-memory fakes for deterministic unit tests; no live LLM/API calls.

Implementation inference: Story 2.3 scoring should be pure deterministic Python over parsed `ArchFragment`/dict records. It should not introduce LLM calls or depend on LangGraph execution to test scoring.

### SAAM Scoring Guidance

Use `quality_weights` as the authoritative ARLO signal. It is a `dict[str, int]` in `RAAInput` and is passed into private subgraphs by Story 2.1. [Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md#Input Contract`]

`raa/Skills/references/saam.md` defines the design intent: scenarios should have stimulus/context/response, map to quality attributes, and record satisfaction. Use that as a domain guide, but do not parse it at runtime for scoring.

Recommended score model:

```python
scenario_weight = sum(quality_weights.get(attr, 0) for attr in normalized_attrs)
scenario_score = scenario_weight * satisfaction_factor
raw_score = sum(scenario_score for scenario in fragment.saam_scenarios)
final_score = raw_score * (0.5 if reduced_confidence else 1.0)
```

The dev agent may adjust this only if tests and comments make the alternative deterministic and aligned to FR-10.

### Previous Story Intelligence

Story 2.1 established the `batch_outputs` record shape and warns that reducer ordering is not guaranteed. Later stories must sort by `(batch_index, strategy)` or equivalent metadata instead of trusting append order.

Story 2.2 established strict `ArchFragment` parsing and C4 hierarchy validation. It also added `open_questions` propagation from subgraph results. Do not route scoring problems into C4 validation; scoring should produce score metadata, while structural issues remain C4 validator/open-question concerns.

Story 2.6 established `raa/Skills/` and tag-based prompt injection. Do not make scoring depend on prompt text or skill file parsing. The skill bundle is useful for prompt guidance; score calculations must stay code-level deterministic.

### File Structure Requirements

Create:

| File | Purpose |
| --- | --- |
| `raa/judge/__init__.py` | Judge package marker. |
| `raa/judge/scoring.py` | Pure SAAM fragment scoring and ranking. |
| `raa/judge/reconcile.py` | Optional node wrapper for selecting current batch primary fragment; no merge yet. |
| `tests/raa/unit/test_judge_scoring.py` | Pure scoring tests. |
| `tests/raa/unit/test_judge_reconcile.py` | Only if `reconcile.py` node wrapper is added. |

Modify:

| File | Required Change |
| --- | --- |
| `raa/state/models.py` | Add SAAM scenario and score models; extend `ArchFragment` with defaulted `saam_scenarios`. |
| `raa/state/schemas.py` | Add a minimal Judge scoring result channel only if needed by the node wrapper. |
| `raa/utils/constants.py` | Add named SAAM multiplier and satisfaction constants. |
| `raa/utils/matrix_loader.py` | Create only if this story uses `matrix.json`; otherwise defer. |

### Testing Requirements

Run at minimum:

```bash
python3 -m pytest tests/raa/unit/test_judge_scoring.py -q
```

If a node wrapper is added:

```bash
python3 -m pytest tests/raa/unit/test_judge_reconcile.py -q
```

Regression after model changes:

```bash
python3 -m pytest \
  tests/raa/unit/test_execution_loop.py \
  tests/raa/unit/test_c4_validator.py \
  tests/raa/unit/test_strategy_subgraphs.py \
  tests/raa/unit/test_prompt_loader.py -q
```

If time permits, run all RAA unit tests:

```bash
python3 -m pytest tests/raa/unit -q
```

### Implementation Pitfalls To Avoid

- Do not merge fragments into `arch_model`; Story 2.4 and later stories own merge/dedup behavior.
- Do not advance `batch_cursor`.
- Do not trust `batch_outputs` list order.
- Do not score skipped records.
- Do not inline the `0.5` multiplier.
- Do not use LLM calls for scoring.
- Do not parse raw LLM strings.
- Do not read SQLite or embeddings in this story.
- Do not make `matrix.json` loading happen inside a per-fragment scoring loop.
- Do not break existing `ArchFragment(...)` construction by adding required fields without defaults.

### References

- `_bmad-output/planning-artifacts/epics.md#Story 2.3: SAAM-First Fragment Scoring`
- `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md#FR-10: SAAM-First Fragment Scoring`
- `_bmad-output/planning-artifacts/architecture.md#D7 - Incoherent Batch Fallback Strategy`
- `_bmad-output/planning-artifacts/architecture.md#Process Patterns`
- `_bmad-output/implementation-artifacts/2-1-concurrency-orchestrator-and-parallel-subgraph-dispatch.md#Output Record Contract`
- `_bmad-output/implementation-artifacts/2-2-c4-metamodel-hierarchy-enforcement-in-private-subgraphs.md#Completion Notes List`
- `_bmad-output/implementation-artifacts/2-6-skill-resource-bundle-and-tag-based-prompt-injection.md#Completion Notes List`
- LangChain docs MCP: `/oss/python/langgraph/graph-api`
- LangChain docs MCP: `/oss/python/langgraph/use-graph-api`
- LangChain docs MCP: `/oss/python/langchain/models`
- LangChain docs MCP: `/oss/python/langchain/test/unit-testing`

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

### Completion Notes List

- Story context created by BMad create-story workflow on 2026-05-23.
- LangChain docs MCP was queried before story writing, per user instruction.
- **2026-05-23 — Story 2.3 implementation complete (Claude Opus 4.7):**
  - Task 1: Added `SAAMScenario` and `FragmentScore` Pydantic models to `raa/state/models.py`. Added `saam_scenarios: list[SAAMScenario]` field to `ArchFragment` with `default_factory=list` to preserve backwards compatibility. All existing tests pass unchanged.
  - Task 2: Created `raa/judge/` package with `__init__.py` and `scoring.py`. Implemented `score_fragment_record()` (pure scoring of a single record) and `rank_batch_fragments()` (batch ranking with deterministic tie-breaking). Both accept dict and `ArchFragment` inputs. Skipped records and null fragments are excluded from scoring and tracked in metadata.
  - Task 3: Scoring semantics implemented in `scoring.py`: case-insensitive quality attribute matching, satisfaction factors from named constants, per-scenario contribution tracking, requirement-coverage fallback for fragments without SAAM scenarios, and pure scoring with no LLM/SQLite/embedding access.
  - Task 4: Added `SAAM_REDUCED_CONFIDENCE_MULTIPLIER`, `SAAM_SATISFACTION_FACTORS`, and `SAAM_STRATEGY_ORDER` constants to `raa/utils/constants.py`. `matrix.json` is not consumed in this story — documented in scoring module docstring for later addition.
  - Task 5: Created `raa/judge/reconcile.py` with `select_primary_fragment()` node wrapper. Filters by `batch_cursor`, returns only state updates, does not advance cursor or modify `arch_model`. Added `judge_rankings: NotRequired[dict[int, dict]]` to `RAAState` — not an append reducer because each batch is scored exactly once.
  - Task 6: Created `tests/raa/unit/test_judge_scoring.py` (29 tests) covering: multi-scenario scoring, satisfaction factors, reduced-confidence multiplier, skipped/null exclusion, single RAA-A fallback, tie-breaking by strategy order then thread_id, input order independence, dict and ArchFragment input acceptance, edge cases (empty weights, empty records, unknown attributes). Created `tests/raa/unit/test_judge_reconcile.py` (6 tests) covering: primary selection, batch cursor filtering, state update shape, cursor non-advancement, empty batches, ranking preservation across batches.
  - Task 7: Ran full regression suite — all 87 existing Story 2.1/2.2 tests pass. Full unit suite: 305 tests pass, zero regressions.

### File List

- `raa/state/models.py` — Added `SAAMScenario`, `FragmentScore` models; extended `ArchFragment` with `saam_scenarios`
- `raa/state/schemas.py` — Added `judge_rankings: NotRequired[dict[int, dict]]` to `RAAState`
- `raa/utils/constants.py` — Added SAAM scoring constants
- `raa/judge/__init__.py` — New: Judge package marker
- `raa/judge/scoring.py` — New: Pure SAAM scoring and ranking functions
- `raa/judge/reconcile.py` — New: Judge node wrapper for primary fragment selection
- `tests/raa/unit/test_judge_scoring.py` — New: 29 unit tests for pure scoring
- `tests/raa/unit/test_judge_reconcile.py` — New: 6 unit tests for reconcile node

### Change Log

- 2026-05-23: Story 2.3 implementation — SAAM-first fragment scoring with Judge package, pure scoring functions, reconcile node, and comprehensive tests (Claude Opus 4.7)
