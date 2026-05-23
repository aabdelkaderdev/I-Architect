# Story 2.1: Concurrency Orchestrator and Parallel Subgraph Dispatch

Status: done

## Story

As a Pipeline Engineer,
I want to concurrently execute three independent analysis subgraphs using SQLite WAL checkpointing,
so that we process batches through parallel design strategies without write contention.

## Acceptance Criteria

1. **Execution queue batch selection**: Given `execution_queue` from Story 1.4 and `batch_cursor`, when the execution loop runs, then it must select exactly the current batch (`execution_queue[batch_cursor]`) and raise a clear exception if the queue is missing, empty, or the cursor is out of range.

2. **Parent-to-private-state mapping**: Given the current batch, `quality_weights`, `arch_model`, and `bridge_requirements`, when dispatching subgraphs, then the loop must map those parent state values into each private subgraph input without exposing the full parent `RAAState`.

3. **Concurrent strategy dispatch**: Given a coherent batch, when dispatching, then RAA-A, RAA-B, and RAA-C must be invoked concurrently with `asyncio.gather` via each compiled subgraph's `ainvoke(...)`.

4. **Reduced-confidence fallback**: Given a batch with `reduced_confidence = true`, when dispatching, then only RAA-A must run, and the returned metadata must mark parallel strategies as skipped for that batch.

5. **SQLite WAL checkpoint isolation**: Given runtime checkpoint configuration, when subgraphs are compiled for dispatch, then each strategy must use an isolated SQLite checkpointer path in WAL mode (`raa_a`, `raa_b`, `raa_c`) so concurrent writes do not share the same checkpoint database connection.

6. **Stable raw output accumulation**: Given one or more subgraph results, when the loop returns, then it must append raw `ArchFragment` payloads into `batch_outputs` as a list of records containing stable metadata: `batch_id`, `batch_index`, `strategy`, `thread_id`, `reduced_confidence`, and `arch_fragment`.

7. **Reducer-safe ordering**: Because LangGraph reducer ordering for parallel writes is not guaranteed, every `batch_outputs` record must include enough metadata for later deterministic sorting; downstream code must not rely on list insertion order.

8. **No premature cursor advancement**: The execution loop must not increment `batch_cursor` in this story. Cursor advancement must remain coupled to the later Judge/reconciliation state write so crash recovery cannot skip an unmerged batch.

## Tasks / Subtasks

- [x] Task 1: Add minimal fragment and subgraph I/O models (AC: #2, #6)
  - [x] 1.1 Extend `raa/state/models.py` with `C4Entity`, `C4Relationship`, and `ArchFragment` Pydantic v2 models if they do not already exist
  - [x] 1.2 Keep the models permissive enough for Story 2.1 fake/test outputs; strict C4 hierarchy validation belongs to Story 2.2
  - [x] 1.3 Add `cross_cutting_candidates`, `assumption_flags`, and `metadata` defaults to `ArchFragment`
  - [x] 1.4 Create `raa/subgraphs/schemas.py` with private `TypedDict` schemas: `StrategySubgraphInput`, `StrategySubgraphState`, and `StrategySubgraphOutput`
  - [x] 1.5 Private input fields must include only: `batch`, `quality_weights`, `running_model`, `bridge_requirements`, `strategy`, and `reduced_confidence`

- [x] Task 2: Create private subgraph builder scaffolds (AC: #2, #3, #5)
  - [x] 2.1 Create `raa/subgraphs/__init__.py`
  - [x] 2.2 Create `raa/subgraphs/raa_a.py` exposing `build_raa_a_subgraph() -> StateGraph`
  - [x] 2.3 Create `raa/subgraphs/raa_b.py` exposing `build_raa_b_subgraph() -> StateGraph`
  - [x] 2.4 Create `raa/subgraphs/raa_c.py` exposing `build_raa_c_subgraph() -> StateGraph`
  - [x] 2.5 Each builder must return an uncompiled `StateGraph`; the caller controls checkpointer compilation
  - [x] 2.6 Each scaffold node may return an empty/minimal `ArchFragment` with strategy metadata until Stories 2.2/2.3 implement real extraction logic
  - [x] 2.7 Do not put all three strategies in one file; architecture requires separate private subgraph modules

- [x] Task 3: Implement SQLite WAL checkpointer helpers (AC: #5)
  - [x] 3.1 Create `raa/graphs/__init__.py`
  - [x] 3.2 Create `raa/graphs/execution_loop.py`
  - [x] 3.3 Add an async helper that opens an `aiosqlite` connection, executes `PRAGMA journal_mode=WAL`, commits it, wraps it with `langgraph.checkpoint.sqlite.aio.AsyncSqliteSaver`, and calls `await saver.setup()`
  - [x] 3.4 Read checkpoint paths from `config["configurable"]`: prefer explicit `raa_a_checkpoint_db_path`, `raa_b_checkpoint_db_path`, `raa_c_checkpoint_db_path`; otherwise derive sibling paths from required `checkpoint_db_path`
  - [x] 3.5 Derivation must be deterministic, e.g. `raa_checkpoint.db` -> `raa_checkpoint_raa_a.db`, `raa_checkpoint_raa_b.db`, `raa_checkpoint_raa_c.db`
  - [x] 3.6 Never reuse one SQLite connection/checkpointer across the three concurrent strategy subgraphs

- [x] Task 4: Implement execution-loop dispatch node (AC: #1, #2, #3, #4, #6, #7, #8)
  - [x] 4.1 In `raa/graphs/execution_loop.py`, implement `async def dispatch_strategy_subgraphs(state: RAAState, config: RunnableConfig) -> dict`
  - [x] 4.2 Validate `config["configurable"]`, `thread_id`, and checkpoint path configuration with clear `KeyError` messages
  - [x] 4.3 Select `batch = state["execution_queue"][state["batch_cursor"]]`; handle missing/empty/out-of-range cases explicitly
  - [x] 4.4 Build private input using only the fields required by `StrategySubgraphInput`
  - [x] 4.5 For coherent batches, compile and invoke RAA-A/B/C concurrently with `asyncio.gather`
  - [x] 4.6 For `reduced_confidence = true`, invoke only RAA-A and add skip records for RAA-B and RAA-C with `skipped = true` and `skip_reason = "reduced_confidence"`
  - [x] 4.7 Pass child configs with stable role-specific `thread_id` values, e.g. `{parent_thread_id}:{batch_index}:{strategy}`
  - [x] 4.8 Preserve caller-injected LLM slots in child config: `raa_a_llm`, `raa_b_llm`, `raa_c_llm`, and `judge_llm`
  - [x] 4.9 Return `{"batch_outputs": output_records}` only; do not return or mutate `batch_cursor`

- [x] Task 5: Add injectable compiled-graph support for tests (AC: #3, #4, #6)
  - [x] 5.1 Allow tests to inject `raa_a_graph`, `raa_b_graph`, and `raa_c_graph` through `config["configurable"]`
  - [x] 5.2 If injected compiled graphs are present, use them instead of compiling default builders/checkpointers
  - [x] 5.3 Keep the production path as default builder + isolated SQLite checkpointer
  - [x] 5.4 Ensure injected graph outputs follow the same output-record normalization as production graph outputs

- [x] Task 6: Unit tests for dispatch and mapping (AC: #1, #2, #3, #4, #6, #7, #8)
  - [x] 6.1 Create `tests/raa/unit/test_execution_loop.py`
  - [x] 6.2 Test missing `execution_queue`, empty queue, and out-of-range `batch_cursor` raise clear exceptions
  - [x] 6.3 Test private subgraph inputs contain only allowed private fields and not full `RAAState`
  - [x] 6.4 Test coherent batch dispatch invokes RAA-A, RAA-B, and RAA-C
  - [x] 6.5 Test dispatch is genuinely concurrent using injected async fake graphs with sleeps and elapsed-time assertion
  - [x] 6.6 Test reduced-confidence batch invokes only RAA-A and returns skipped records for B/C
  - [x] 6.7 Test `batch_outputs` records include `batch_id`, `batch_index`, `strategy`, `thread_id`, `reduced_confidence`, and `arch_fragment`
  - [x] 6.8 Test `batch_cursor` is not returned and not mutated

- [x] Task 7: Unit tests for SQLite checkpoint path handling (AC: #5)
  - [x] 7.1 Create `tests/raa/unit/test_execution_loop_checkpoints.py` or include these cases in `test_execution_loop.py`
  - [x] 7.2 Test explicit per-role checkpoint paths are used when provided
  - [x] 7.3 Test base `checkpoint_db_path` derives three role-specific paths deterministically
  - [x] 7.4 Test WAL mode is enabled on a temporary SQLite checkpoint database
  - [x] 7.5 Test production helper calls `AsyncSqliteSaver.setup()` before graph invocation

### Review Findings

- [x] [Review][Patch] Potential Connection Leak on Exception [raa/raa/graphs/execution_loop.py:181]
- [x] [Review][Patch] AttributeError on Saver Cleanup [raa/raa/graphs/execution_loop.py:303]
- [x] [Review][Patch] In-memory SQLite Path Derivation File Creation [raa/raa/graphs/execution_loop.py:50]
- [x] [Review][Patch] Ensure Checkpoint Parent Directories Exist [raa/raa/graphs/execution_loop.py:40]
- [x] [Review][Patch] RunnableConfig Safety Check [raa/raa/graphs/execution_loop.py:193]

## Dev Notes

### Current Implementation Baseline

Epic 1 is implemented and regression tests pass:

```bash
python3 -m pytest \
  tests/raa/unit/test_batch_construction.py \
  tests/raa/unit/test_overlap_bridging.py \
  tests/raa/unit/test_coherence_gate.py \
  tests/raa/unit/test_batch_queue_ordering.py \
  tests/raa/unit/test_preparation.py \
  tests/raa/unit/test_embedding_cache.py -q
# 120 passed, 1 warning in 1.04s
```

The warning is pytest cache write access outside this workspace's writable root, not an RAA failure.

### Story 1.4 Output Shape To Consume

`dispatch_strategy_subgraphs` consumes `execution_queue` from `order_batch_queue`. Each queued batch preserves the Story 1.3 fields and may include Story 1.4 fields:

```python
{
    "group_id": "cluster_0_group_0",
    "centroid": list[float],
    "asr_ids": list[str],
    "asr_records": list[dict],
    "non_asr_ids": list[str],
    "non_asr_records": list[dict],
    "similarity_scores": dict[str, float],
    "bridge_ids": list[str],          # optional
    "coherence_score": float,         # from coherence gate
    "reduced_confidence": bool,       # true => RAA-A only
    "source_group_id": str,           # optional for split batches
}
```

`state["bridge_requirements"]` is a list of bridge records. Filter this list to records whose `batch_ids` include the selected batch `group_id`; pass only relevant bridges to private subgraphs.

### LangChain / LangGraph MCP References

Use the LangChain MCP docs as the syntax authority for this story:

- `/oss/python/langgraph/use-subgraphs`: when parent and subgraph schemas differ, call a compiled subgraph inside a node and map parent state to private input, then map output back to parent state.
- `/oss/python/langgraph/use-graph-api`: parallel fan-out uses reducers such as `Annotated[list, operator.add]`; updates from parallel branches may not have deterministic list order, so stable metadata is required.
- `/oss/python/langgraph/persistence`: checkpointers save state by `thread_id`; async graph execution uses async checkpointer methods and therefore `AsyncSqliteSaver` for SQLite.
- `/oss/python/langgraph/add-memory`: subgraphs can receive checkpointers through compilation, but this architecture requires separate isolated checkpointer DBs per private strategy.
- `/oss/python/langgraph/graph-api`: nodes may accept `RunnableConfig`; return state updates as `dict`, not the full state.

Local installed API check confirms this pinned environment has:

```python
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# constructor signature:
AsyncSqliteSaver(conn: aiosqlite.Connection, *, serde=None)

# classmethod:
async with AsyncSqliteSaver.from_conn_string(path) as saver:
    ...

# setup is async:
await saver.setup()
```

For WAL mode, prefer constructing with an explicit `aiosqlite` connection so the helper can execute `PRAGMA journal_mode=WAL` before wrapping the connection:

```python
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

conn = await aiosqlite.connect(path)
await conn.execute("PRAGMA journal_mode=WAL")
await conn.commit()
saver = AsyncSqliteSaver(conn)
await saver.setup()
```

Close the connection after graph invocation.

### Architecture Compliance

1. **Private subgraph schemas differ from parent state.** Use wrapper invocation in `dispatch_strategy_subgraphs`, not direct shared-state subgraph nodes.
2. **Graphs return builders uncompiled.** `build_raa_a_subgraph()`, `build_raa_b_subgraph()`, and `build_raa_c_subgraph()` must return `StateGraph`; compilation happens in the execution loop with the correct checkpointer.
3. **No shared SQLite checkpoint connection.** Each strategy gets an isolated connection and path.
4. **State updates only.** `dispatch_strategy_subgraphs` returns `{"batch_outputs": [...]}` and must not return the whole state.
5. **Append reducer compatibility.** `RAAState.batch_outputs` already uses `Annotated[list[dict], add]`; output records must be list values.
6. **No cursor advancement in this story.** Architecture says `batch_cursor` advancement must be atomic with Judge state write. The Judge does not exist yet.
7. **No LLM instantiation inside nodes.** Any LLM is supplied through `config["configurable"]["raa_a_llm"]`, `raa_b_llm`, or `raa_c_llm`.

### Output Record Contract

Normalize every subgraph result to this record shape before returning:

```python
{
    "batch_id": batch["group_id"],
    "batch_index": state["batch_cursor"],
    "strategy": "raa_a" | "raa_b" | "raa_c",
    "thread_id": child_thread_id,
    "reduced_confidence": bool(batch.get("reduced_confidence", False)),
    "arch_fragment": arch_fragment_dict,
    "skipped": False,
    "skip_reason": None,
}
```

Skipped strategies for reduced-confidence batches use:

```python
{
    "batch_id": batch["group_id"],
    "batch_index": state["batch_cursor"],
    "strategy": "raa_b",
    "thread_id": child_thread_id,
    "reduced_confidence": True,
    "arch_fragment": None,
    "skipped": True,
    "skip_reason": "reduced_confidence",
}
```

Later stories can deterministically sort by `(batch_index, strategy)` before Judge scoring.

### Private Subgraph Input Contract

Each private subgraph receives:

```python
{
    "batch": batch,
    "quality_weights": state.get("quality_weights") or {},
    "running_model": state.get("arch_model") or {},
    "bridge_requirements": relevant_bridge_records,
    "strategy": "raa_a" | "raa_b" | "raa_c",
    "reduced_confidence": bool(batch.get("reduced_confidence", False)),
}
```

Do not include `normalized_asrs`, `normalized_non_asr`, full `execution_queue`, embedding vectors, full `requirements`, or other parent state fields.

### File Structure Requirements

Create:

| File | Purpose |
| --- | --- |
| `raa/graphs/__init__.py` | Graph package marker |
| `raa/graphs/execution_loop.py` | Async batch-level dispatch node and checkpoint helpers |
| `raa/subgraphs/__init__.py` | Subgraph package marker |
| `raa/subgraphs/schemas.py` | Private strategy subgraph TypedDict schemas |
| `raa/subgraphs/raa_a.py` | RAA-A SAAM-first subgraph builder scaffold |
| `raa/subgraphs/raa_b.py` | RAA-B pattern-driven subgraph builder scaffold |
| `raa/subgraphs/raa_c.py` | RAA-C entity/relationship-driven subgraph builder scaffold |
| `tests/raa/unit/test_execution_loop.py` | Async dispatch, mapping, fallback, metadata, checkpoint tests |

Modify:

| File | Change |
| --- | --- |
| `raa/state/models.py` | Add minimal `ArchFragment` and related Pydantic models if absent |

Do not modify Story 1.4 node behavior unless tests expose a direct integration bug.

### Testing Standards

- Use `pytest` and `pytest.mark.asyncio` for async dispatch tests.
- Use injected fake graphs for orchestration tests; fake graphs only need an async `ainvoke(input, config)` method.
- No live LLM calls.
- No live FastEmbed calls.
- Use temporary SQLite files for checkpoint helper tests.
- Run:

```bash
python3 -m pytest tests/raa/unit/test_execution_loop.py -q
python3 -m pytest tests/raa/unit/test_batch_queue_ordering.py tests/raa/unit/test_coherence_gate.py -q
```

Run all RAA unit tests after touching shared state models:

```bash
python3 -m pytest tests/raa/unit -q
```

### Files That Must Not Be Broken

| File | Existing Behavior To Preserve |
| --- | --- |
| `raa/state/schemas.py` | `batch_outputs`, `open_questions`, and `incoherent_batches` append reducers |
| `raa/nodes/batch_queue_ordering.py` | Produces `execution_queue` and `unprocessed_requirements` |
| `raa/nodes/coherence_gate.py` | Uses `reduced_confidence` to flag RAA-A-only batches |
| `raa/nodes/overlap_bridging.py` | Produces `bridge_requirements` and optional `bridge_ids` |
| `raa/state/models.py` | Existing `NormalizedRequirement` remains import-compatible |

### References

- Source: `_bmad-output/planning-artifacts/epics.md` — Epic 2, Story 2.1 acceptance criteria; FR7-FR9.
- Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md` — Feature 6.4, Strategy-Parallel Subgraph Dispatch and WAL checkpointing.
- Source: `_bmad-output/planning-artifacts/architecture.md` — D1, D5, D6, D7; project structure; process patterns.
- Source: `_bmad-output/implementation-artifacts/1-4-overlap-bridging-coherence-gating-and-priority-queue-ordering.md` — completed previous story outputs and test baseline.
- Source: `raa/nodes/batch_queue_ordering.py` — current `execution_queue` producer.
- Source: `raa/nodes/coherence_gate.py` — current `reduced_confidence` producer.
- Source: `raa/nodes/overlap_bridging.py` — current `bridge_requirements` producer.
- Source: `raa/state/schemas.py` — current `RAAState` channels and append reducers.
- Source: `raa/state/models.py` — current Pydantic model location.
- Source: LangChain MCP `/oss/python/langgraph/use-subgraphs` — wrapper invocation for different parent/private schemas.
- Source: LangChain MCP `/oss/python/langgraph/use-graph-api` — parallel reducers, transactional supersteps, non-deterministic parallel update ordering.
- Source: LangChain MCP `/oss/python/langgraph/persistence` — thread IDs, async checkpointer methods, `AsyncSqliteSaver`.
- Source: LangChain MCP `/oss/python/langgraph/graph-api` — node config and state-update return contract.

## Story Context Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context) via Claude Code

### Debug Log References

None.

### Completion Notes List

- Extended `raa/state/models.py` with C4Entity, C4Relationship, ArchFragment Pydantic v2 models
- Created `raa/subgraphs/schemas.py` with private StrategySubgraphInput/State/Output TypedDicts
- Built three uncompiled subgraph scaffolds (raa_a, raa_b, raa_c) each returning StateGraph
- Implemented SQLite WAL checkpointer helper using aiosqlite + AsyncSqliteSaver
- Checkpoint path derivation: explicit per-role paths or deterministic derivation from base path
- `dispatch_strategy_subgraphs` async node: batch selection, private input mapping, concurrent asyncio.gather dispatch, reduced-confidence RAA-A-only path with skip records
- Injectable compiled-graph support via config["configurable"] for test isolation
- 31 unit tests covering: validation errors, path derivation, WAL mode verification, private input mapping, coherent/reduced-confidence dispatch, concurrency proof, output record shape, thread_id determinism, batch_cursor immutability
- Full regression: 151 tests pass (120 previous + 31 new)

### File List

- `raa/state/models.py` — Extended with C4Entity, C4Relationship, ArchFragment
- `raa/subgraphs/__init__.py` — Subgraph package marker
- `raa/subgraphs/schemas.py` — StrategySubgraphInput/State/Output TypedDicts
- `raa/subgraphs/raa_a.py` — RAA-A SAAM-first subgraph builder
- `raa/subgraphs/raa_b.py` — RAA-B pattern-driven subgraph builder
- `raa/subgraphs/raa_c.py` — RAA-C entity/relationship subgraph builder
- `raa/graphs/__init__.py` — Graph package marker
- `raa/graphs/execution_loop.py` — Async dispatch node + WAL checkpointer helpers
- `tests/raa/unit/test_execution_loop.py` — 31 async unit tests

### Change Log

- 2026-05-23: Implemented Story 2.1 — concurrency orchestrator, parallel subgraph dispatch, WAL checkpoint isolation (8 files created, 1 modified, 31 tests, all ACs satisfied)
