# Story 2.2: C4 Metamodel Hierarchy Enforcement in Private Subgraphs

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Pipeline Engineer,
I want each subgraph to output structural C4 components and relationships that strictly adhere to nesting rules,
so that we prevent orphan components or out-of-scope relationship arrows from corrupting the running model.

## Acceptance Criteria

1. **Container parent enforcement**: Given an execution batch, running model constraints, and a private subgraph LLM prompt template, when a subgraph extracts C4 elements, then every container must have a valid `parent_system_id` pointing to a system in the fragment or the running model.

2. **Component parent enforcement**: Given extracted components from any private subgraph, when the fragment is normalized, then every component must have a valid `parent_container_id` pointing to a container in the fragment or the running model.

3. **Relationship scope assignment**: Given extracted relationships, when endpoints are resolved, then each relationship must receive a `diagram_scope` matching endpoint depth: person/system/external-system endpoints use `context`, container endpoints use `container`, and component endpoints use `component`.

4. **Strict fragment shape**: Given a successful extraction, when the subgraph returns, then the returned payload must match the canonical `ArchFragment` Pydantic model from `raa/state/models.py`; do not introduce duplicate fragment models in subgraph modules.

5. **Recoverable hierarchy violations become open questions**: Given an orphan entity or unresolved relationship endpoint, when the subgraph cannot safely repair it from the fragment or running model, then it must exclude the invalid item from the fragment and emit a `coverage_gap` or `hierarchy_conflict` open question with enough batch, strategy, requirement, and entity context for later Judge/HITL processing.

6. **Private state remains isolated**: Given Story 2.1's private-state boundary, when implementing hierarchy enforcement, then the subgraphs must continue to receive only `StrategySubgraphInput` fields and must not read or mutate full `RAAState`.

7. **No live LLM calls in unit tests**: Given LLM-dependent extraction, when tests run, then they must use fakes or injected structured-output stubs and assert deterministic Pydantic parsing, validation, filtering, and scope assignment.

## Tasks / Subtasks

- [x] Task 1: Tighten canonical C4 fragment models (AC: #1, #2, #3, #4)
  - [x] 1.1 Update `raa/state/models.py`; do not define C4 models in `raa/subgraphs/*`.
  - [x] 1.2 Extend `C4Entity` to support `c4_type` values needed by this story: `person`, `system`, `external_system`, `container`, and `component`.
  - [x] 1.3 Add explicit optional parent fields: `parent_system_id` for containers and `parent_container_id` for components. Preserve existing fields (`id`, `name`, `description`, `technology`, `metadata`) so Story 2.1 tests and output normalization remain compatible.
  - [x] 1.4 Extend `C4Relationship` with `diagram_scope: str` and preserve `source_id`, `target_id`, `description`, `relationship_type`, and `metadata`.
  - [x] 1.5 Add Pydantic validators or helper methods only where they improve local validation. Cross-fragment/running-model checks belong in the C4 validator utility, not in field-level validators that cannot see the running model.

- [x] Task 2: Add shared C4 hierarchy enforcement utility (AC: #1, #2, #3, #5)
  - [x] 2.1 Create `raa/utils/c4_validator.py`.
  - [x] 2.2 Implement a pure function such as `enforce_fragment_hierarchy(fragment: ArchFragment, running_model: dict, *, batch_id: str, strategy: str) -> tuple[ArchFragment, list[dict]]`.
  - [x] 2.3 Build lookup maps from both the current fragment and `running_model`; support common running-model shapes from architecture docs, such as top-level `systems`, `containers`, `components`, and nested system/container lists.
  - [x] 2.4 Validate containers: keep only containers whose `parent_system_id` resolves to a system in the fragment or running model.
  - [x] 2.5 Validate components: keep only components whose `parent_container_id` resolves to a container in the fragment or running model.
  - [x] 2.6 Validate relationships: keep only relationships whose endpoints resolve after invalid entities are removed.
  - [x] 2.7 Assign `diagram_scope` deterministically from endpoint types. Use the deepest endpoint level: component -> `component`, container -> `container`, otherwise `context`.
  - [x] 2.8 Emit open question dicts for excluded entities/relationships with fields: `type`, `reason`, `batch_id`, `strategy`, `requirement_ids`, `entity_id` or `relationship_id`, and `suggested_resolution`.
  - [x] 2.9 Do not raise exceptions for recoverable orphan/hierarchy issues. Exceptions are only for malformed programmer inputs that cannot be processed.

- [x] Task 3: Add prompt loading and strategy prompt templates (AC: #4, #6, #7)
  - [x] 3.1 Create `raa/prompts/` if absent.
  - [x] 3.2 Add concise mustache templates for private extraction:
    - `raa/prompts/saam_analysis.md`
    - `raa/prompts/pattern_matching.md`
    - `raa/prompts/entity_extraction.md`
  - [x] 3.3 Create `raa/utils/prompt_loader.py` with a small `load_prompt(template_name: str, context: dict) -> str` helper using `chevron.render()`.
  - [x] 3.4 Templates must instruct the model to return the canonical `ArchFragment` shape and include the C4 hierarchy rules from this story.
  - [x] 3.5 Keep templates short and runtime-focused. Long design references belong in future `Skills/references/` files, not copied wholesale into prompts.

- [x] Task 4: Replace scaffold subgraph nodes with structured extraction paths (AC: #1, #2, #3, #4, #6)
  - [x] 4.1 Update `raa/subgraphs/raa_a.py`, `raa/subgraphs/raa_b.py`, and `raa/subgraphs/raa_c.py` in place.
  - [x] 4.2 Each node must read its LLM from `config["configurable"]["raa_a_llm"]`, `raa_b_llm`, or `raa_c_llm`; never instantiate an LLM inside a node.
  - [x] 4.3 Node functions may accept `RunnableConfig` per LangGraph docs. Preserve the existing `StateGraph(StrategySubgraphState)` builders and keep them uncompiled.
  - [x] 4.4 Use `llm.with_structured_output(ArchFragment, include_raw=True)` for extraction.
  - [x] 4.5 Normalize the structured-output response: use `response["parsed"]` when `include_raw=True`; if the injected fake returns an `ArchFragment` directly, accept it for tests.
  - [x] 4.6 Run `enforce_fragment_hierarchy(...)` before returning.
  - [x] 4.7 Return only private state updates, for example `{"arch_fragment": valid_fragment, "open_questions": questions}`.
  - [x] 4.8 Keep RAA-A, RAA-B, and RAA-C strategy-specific prompts separated; do not collapse all strategies into one module.

- [x] Task 5: Carry recoverable hierarchy questions back to parent dispatch (AC: #5, #6)
  - [x] 5.1 Extend `raa/subgraphs/schemas.py` so private output/state can include `open_questions: list[dict]`.
  - [x] 5.2 Update `raa/graphs/execution_loop.py` normalization to preserve `arch_fragment` behavior from Story 2.1.
  - [x] 5.3 If a subgraph result contains `open_questions`, have `dispatch_strategy_subgraphs` return them through the parent `open_questions` append reducer in addition to `batch_outputs`.
  - [x] 5.4 Preserve Story 2.1 guarantees: no full parent state exposure, no shared checkpoint connection, no `batch_cursor` increment, stable output record metadata, and reduced-confidence mode still runs only RAA-A.

- [x] Task 6: Unit tests for C4 hierarchy and scope enforcement (AC: #1, #2, #3, #5, #7)
  - [x] 6.1 Add `tests/raa/unit/test_c4_validator.py`.
  - [x] 6.2 Test valid container parent in fragment is kept.
  - [x] 6.3 Test valid container parent in running model is kept.
  - [x] 6.4 Test orphan container is excluded and creates an open question.
  - [x] 6.5 Test valid component parent in fragment and running model is kept.
  - [x] 6.6 Test orphan component is excluded and creates an open question.
  - [x] 6.7 Test unresolved relationship endpoint is excluded and creates an open question.
  - [x] 6.8 Test relationship scope assignment for context, container, and component endpoints.
  - [x] 6.9 Test invalid entity removal happens before relationship validation.

- [x] Task 7: Unit tests for structured subgraph extraction (AC: #4, #6, #7)
  - [x] 7.1 Extend `tests/raa/unit/test_execution_loop.py` or add `tests/raa/unit/test_strategy_subgraphs.py`.
  - [x] 7.2 Use injected fake LLMs or small fake structured-output wrappers; no network or live model calls.
  - [x] 7.3 Test each builder still returns an uncompiled `StateGraph`.
  - [x] 7.4 Test each strategy node reads only its own configured LLM key.
  - [x] 7.5 Test `with_structured_output(ArchFragment, include_raw=True)` is used by fake wrapper assertions.
  - [x] 7.6 Test subgraph return includes a valid `ArchFragment` and propagates validator open questions.
  - [x] 7.7 Test dispatch can return parent `open_questions` without changing `batch_outputs` metadata or `batch_cursor`.

- [x] Task 8: Regression test Story 2.1 behavior (AC: #6, #7)
  - [x] 8.1 Run the existing execution loop tests after adding hierarchy behavior.
  - [x] 8.2 Run focused Epic 1 regression tests if shared models or constants are touched.

## Dev Notes

### Current Implementation Baseline

Story 2.1 is complete and `sprint-status.yaml` marks it `done`. Existing files to extend:

| File | Current State | Story 2.2 Change |
| --- | --- | --- |
| `raa/state/models.py` | Defines permissive `C4Entity`, `C4Relationship`, and `ArchFragment`; strict hierarchy explicitly deferred to Story 2.2. | Add parent fields, `diagram_scope`, supported C4 types, and keep compatibility with existing model construction. |
| `raa/subgraphs/raa_a.py` | Builds an uncompiled private `StateGraph`; inner node returns minimal metadata-only `ArchFragment`. | Replace scaffold node with structured extraction, prompt render, hierarchy enforcement, and open-question output. |
| `raa/subgraphs/raa_b.py` | Same scaffold pattern for pattern-driven strategy. | Same structured extraction path using `pattern_matching.md`. |
| `raa/subgraphs/raa_c.py` | Same scaffold pattern for entity/relationship strategy. | Same structured extraction path using `entity_extraction.md`. |
| `raa/subgraphs/schemas.py` | Private input includes `batch`, `quality_weights`, `running_model`, `bridge_requirements`, `strategy`, and `reduced_confidence`; output includes `arch_fragment`. | Add optional `open_questions`; do not add parent `RAAState` fields. |
| `raa/graphs/execution_loop.py` | Selects current batch, maps private input, invokes private graphs, normalizes `batch_outputs`, preserves `batch_cursor`. | Preserve all Story 2.1 behavior and additionally carry recoverable hierarchy questions to parent `open_questions`. |
| `tests/raa/unit/test_execution_loop.py` | Covers dispatch validation, private input isolation, checkpoint paths, WAL, reduced-confidence dispatch, and output metadata. | Extend or add tests for open-question propagation without weakening existing assertions. |

No `raa/prompts/`, `raa/utils/prompt_loader.py`, or `raa/utils/c4_validator.py` exists yet.

### Epic And PRD Context

Epic 2 processes requirement batches through three parallel analysis subgraphs, then reconciles outputs through a Judge using scoring, semantic deduplication, C4 boundary grouping, and cross-cutting concern promotion. Story 2.2 is the structural safety layer before scoring and reconciliation. [Source: `_bmad-output/planning-artifacts/epics.md#Epic 2: Strategy-Parallel Subgraph Execution and Judge Reconciliation (Phase 6)`]

FR-8 requires every subgraph `ArchFragment` to strictly follow C4 structure. PRD requirements specify: containers nest under systems, components nest under containers, and relationship scopes must match endpoint hierarchy depth. [Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md#FR-8: C4 Metamodel Hierarchy Enforcement`]

The PRD defines RAA output scope as System Context, Container, and Component levels. A Person or External System may appear as context-level relationship endpoints, but RAA should not invent deeper nesting under them. [Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md#Glossary`]

### Architecture Guardrails

1. RAA is a pure backend LangGraph module, not a web service. Integration boundary remains `graph.invoke(input: RAAInput, config: RunnableConfig) -> RAAOutput`. [Source: `_bmad-output/planning-artifacts/architecture.md#Integration Boundaries`]
2. Parent and private subgraph state schemas are intentionally different. Continue using wrapper invocation and parent-to-private mapping from Story 2.1. [Source: `_bmad-output/planning-artifacts/architecture.md#D2 - Private Subgraphs vs Shared Nodes`]
3. `batch_outputs`, `open_questions`, and `incoherent_batches` use append reducers. Returning `open_questions` from dispatch is compatible with the parent reducer pattern. [Source: `_bmad-output/planning-artifacts/architecture.md#State Management`]
4. All node functions return state update dictionaries. Never return or mutate the full state. [Source: `_bmad-output/planning-artifacts/architecture.md#Enforcement Rules`]
5. All LLM calls use injected config slots and structured output. Do not instantiate LLMs inside nodes and do not parse raw JSON strings. [Source: `_bmad-output/planning-artifacts/architecture.md#Enforcement Rules`]
6. Prompt text must be externalized to `.md` templates and rendered with `chevron`. Do not use f-strings or `.format()` for prompts. [Source: `_bmad-output/planning-artifacts/architecture.md#Enforcement Rules`]
7. Recoverable structural issues, including orphan entities and scope conflicts, produce `OpenQuestion` entries and do not raise exceptions. [Source: `_bmad-output/planning-artifacts/architecture.md#Data Format Patterns`]
8. Embedding vectors stay out of graph state. This story does not need embedding access. [Source: `_bmad-output/planning-artifacts/architecture.md#Key Decisions and Constraints`]

### C4 Model Contract For This Story

Use a flat fragment shape during subgraph extraction. Do not nest entities inside other entities in `ArchFragment`; nesting/tree assembly happens later in Judge/final merge.

Expected entity guidance:

```python
C4Entity(
    id="container_api",
    name="API Service",
    c4_type="container",
    parent_system_id="system_ia",
    requirement_ids=["R1"],
)
```

```python
C4Entity(
    id="component_auth",
    name="Auth Component",
    c4_type="component",
    parent_container_id="container_api",
    requirement_ids=["R2"],
)
```

Expected relationship guidance:

```python
C4Relationship(
    id="rel_api_db",
    source_id="container_api",
    target_id="container_db",
    description="Reads and writes persisted state",
    diagram_scope="container",
)
```

If an extracted component references a missing container, exclude that component and emit an open question. Do not silently promote it to a container and do not attach it to an arbitrary parent.

### LangChain / LangGraph MCP References

Use the LangChain docs MCP as syntax authority for implementation:

- `/oss/python/langgraph/use-subgraphs`: when parent and subgraph schemas differ, invoke a compiled subgraph inside a node/wrapper and map parent state to subgraph input and output back to parent state.
- `/oss/python/langgraph/graph-api`: `StateGraph` uses a state schema, nodes return updates, reducers apply updates to state channels, and graphs must be compiled before invocation.
- `/oss/python/langchain/models`: use `with_structured_output(ArchFragment, include_raw=True)` when the caller needs both parsed structured output and raw message metadata.
- `/oss/python/langchain/test/unit-testing`: use `GenericFakeChatModel` or equivalent in-memory fakes for unit tests; tests must not require API keys or live model calls.

MCP-relevant implementation note: `with_structured_output(..., include_raw=True)` returns a dict with `raw`, `parsed`, and `parsing_error`. The node should treat non-null `parsing_error` or missing `parsed` as a recoverable extraction failure that emits an open question for the batch/strategy, unless the fake test object intentionally returns an `ArchFragment` directly.

### Previous Story Intelligence

Story 2.1 established these contracts that must not regress:

- `dispatch_strategy_subgraphs` selects `execution_queue[batch_cursor]` and raises clear errors for missing, empty, or out-of-range queues.
- Private input contains only `batch`, `quality_weights`, `running_model`, `bridge_requirements`, `strategy`, and `reduced_confidence`.
- Coherent batches run RAA-A, RAA-B, and RAA-C concurrently; reduced-confidence batches run only RAA-A and add skip records for B/C.
- Subgraph builders return uncompiled `StateGraph` instances; the execution loop controls checkpointer compilation.
- Each production strategy uses an isolated SQLite WAL checkpointer path.
- `batch_outputs` records include stable `batch_id`, `batch_index`, `strategy`, `thread_id`, `reduced_confidence`, `arch_fragment`, `skipped`, and `skip_reason`.
- `batch_cursor` is not returned or mutated; cursor advancement belongs to later Judge/reconciliation work.

[Source: `_bmad-output/implementation-artifacts/2-1-concurrency-orchestrator-and-parallel-subgraph-dispatch.md#Dev Notes`]

### Git Intelligence Summary

Recent implementation work introduced the RAA package structure, Epic 1 nodes, Story 2.1 subgraph scaffolds, and pytest coverage. The repo currently has uncommitted Story 2.1 implementation files and review prompt updates; do not revert or rewrite them while implementing this story. Work with the current files in place.

### File Structure Requirements

Create:

| File | Purpose |
| --- | --- |
| `raa/utils/c4_validator.py` | Shared hierarchy and relationship-scope enforcement. |
| `raa/utils/prompt_loader.py` | Chevron prompt template loader. |
| `raa/prompts/saam_analysis.md` | RAA-A extraction prompt. |
| `raa/prompts/pattern_matching.md` | RAA-B extraction prompt. |
| `raa/prompts/entity_extraction.md` | RAA-C extraction prompt. |
| `tests/raa/unit/test_c4_validator.py` | Pure validator coverage. |
| `tests/raa/unit/test_strategy_subgraphs.py` | Strategy node structured-output coverage, unless folded cleanly into `test_execution_loop.py`. |

Modify:

| File | Required Change |
| --- | --- |
| `raa/state/models.py` | Canonical C4 parent fields, relationship scope, compatible Pydantic model changes. |
| `raa/subgraphs/schemas.py` | Add optional private `open_questions`. |
| `raa/subgraphs/raa_a.py` | Structured SAAM-first extraction plus enforcement. |
| `raa/subgraphs/raa_b.py` | Structured pattern-driven extraction plus enforcement. |
| `raa/subgraphs/raa_c.py` | Structured entity-driven extraction plus enforcement. |
| `raa/graphs/execution_loop.py` | Propagate subgraph `open_questions` while preserving `batch_outputs`. |
| `tests/raa/unit/test_execution_loop.py` | Regression coverage for dispatch open-question propagation, if not covered elsewhere. |

### Testing Requirements

Run at minimum:

```bash
python3 -m pytest tests/raa/unit/test_c4_validator.py tests/raa/unit/test_strategy_subgraphs.py tests/raa/unit/test_execution_loop.py -q
```

If `raa/state/models.py` changes break broader assumptions, also run:

```bash
python3 -m pytest tests/raa/unit -q
```

Expected test style:

- Pure validator tests use no LangGraph runtime.
- Subgraph tests use fake structured-output wrappers or `GenericFakeChatModel`; no live model calls.
- Dispatch tests use injected compiled/fake graphs where possible to avoid unnecessary SQLite/checkpointer setup.
- Keep tests under `tests/raa/`; do not add tests beside source files.

### Implementation Pitfalls To Avoid

- Do not make `ArchFragment` nested. The fragment stage remains flat.
- Do not treat `parent_id` as sufficient for this story. The acceptance criteria require explicit `parent_system_id` and `parent_container_id` semantics.
- Do not silently attach orphans to the first available system/container. That corrupts traceability.
- Do not throw for recoverable LLM extraction mistakes. Emit open questions and return the valid remainder.
- Do not parse raw LLM text with `json.loads`.
- Do not add direct `sqlite3` or embedding-cache logic to this story.
- Do not collapse all three private strategies into one file or one prompt.
- Do not rely on reducer/list insertion order for batch outputs or questions; include batch and strategy metadata.

### References

- `_bmad-output/planning-artifacts/epics.md#Story 2.2: C4 Metamodel Hierarchy Enforcement in Private Subgraphs`
- `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md#FR-8: C4 Metamodel Hierarchy Enforcement`
- `_bmad-output/planning-artifacts/architecture.md#Key Decisions and Constraints`
- `_bmad-output/planning-artifacts/architecture.md#Enforcement Rules`
- `_bmad-output/implementation-artifacts/2-1-concurrency-orchestrator-and-parallel-subgraph-dispatch.md#Dev Notes`
- LangChain docs MCP: `/oss/python/langgraph/use-subgraphs`
- LangChain docs MCP: `/oss/python/langgraph/graph-api`
- LangChain docs MCP: `/oss/python/langchain/models`
- LangChain docs MCP: `/oss/python/langchain/test/unit-testing`

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context) via Claude Code

### Debug Log References

None.

### Completion Notes List

- Tightened C4Entity/C4Relationship Pydantic models with parent_system_id, parent_container_id, requirement_ids, diagram_scope
- Created shared c4_validator.py with enforce_fragment_hierarchy() — validates containers, components, relationships, and assigns diagram_scope
- Created prompt_loader.py using chevron mustache rendering
- Three prompt templates: saam_analysis.md, pattern_matching.md, entity_extraction.md
- Updated all three subgraph builders (raa_a/b/c) with structured extraction via with_structured_output(ArchFragment, include_raw=True)
- Each builder: loads prompt → runs LLM extraction → enforces C4 hierarchy → returns clean fragment + open_questions
- Updated execution_loop.py dispatch to propagate open_questions from subgraph results to parent state
- 38 new unit tests (18 c4_validator + 17 strategy_subgraphs + 3 implicit regression)
- Full regression: 189 tests pass (151 previous + 38 new), no regressions

### File List

- `raa/state/models.py` — C4Entity parent fields, C4Relationship diagram_scope
- `raa/subgraphs/schemas.py` — Added open_questions to state/output
- `raa/subgraphs/raa_a.py` — SAAM-first structured extraction + enforcement
- `raa/subgraphs/raa_b.py` — Pattern-driven structured extraction + enforcement
- `raa/subgraphs/raa_c.py` — Entity/relationship structured extraction + enforcement
- `raa/graphs/execution_loop.py` — Propagate subgraph open_questions to parent
- `raa/utils/c4_validator.py` — C4 hierarchy enforcement utility
- `raa/utils/prompt_loader.py` — Chevron template loader
- `raa/prompts/saam_analysis.md` — RAA-A prompt template
- `raa/prompts/pattern_matching.md` — RAA-B prompt template
- `raa/prompts/entity_extraction.md` — RAA-C prompt template
- `tests/raa/unit/test_c4_validator.py` — 18 pure validator tests
- `tests/raa/unit/test_strategy_subgraphs.py` — 17 structured extraction + enforcement tests

### Change Log

- 2026-05-23: Implemented Story 2.2 — C4 metamodel hierarchy enforcement, structured extraction in private subgraphs, open question propagation (7 files created, 6 modified, 38 tests, all ACs satisfied)

### Review Findings

- [x] [Review][Patch] Relationship validation discards valid relationships to existing entities in the running model [raa/raa/utils/c4_validator.py:112]
- [x] [Review][Patch] Cascading orphan component validation leak ignores parent container exclusion [raa/raa/utils/c4_validator.py:73]
- [x] [Review][Patch] Unsafe system.get call on string elements in _model_containers [raa/raa/utils/c4_validator.py:202]
- [x] [Review][Patch] Duplicate skill context key overwrite in prompt loader [raa/raa/utils/prompt_loader.py:50]
- [x] [Review][Patch] Double checkpointer saver connection close on dispatch [raa/raa/graphs/execution_loop.py:192]
