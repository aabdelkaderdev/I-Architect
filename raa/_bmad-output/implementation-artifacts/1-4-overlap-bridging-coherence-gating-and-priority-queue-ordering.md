# Story 1.4: Overlap Bridging, Coherence Gating, and Priority Queue Ordering

Status: done

## Story

As a Pipeline Engineer,
I want to inject bridge requirements, verify semantic coherence, and order the execution queue by risk,
so that the batches are optimized for execution and cross-batch context is preserved.

## Acceptance Criteria

1. **Adjacent batch detection**: Given constructed batches from Story 1.3, when overlap bridging runs, then it must identify related batch pairs when their `group_id` values share the same cluster ID or their centroid cosine similarity is `>= NON_ASR_SIMILARITY_THRESHOLD` (`0.65`).

2. **Bridge requirement injection**: Given a related batch pair, when candidate bridge requirements are evaluated, then the node must inject 1 to 3 shared non-ASR bridge requirements into both batches when qualifying candidates exist, hard-capped by `MAX_BRIDGE_REQUIREMENTS`, and record mappings in `bridge_requirements`.

3. **Coherence scoring**: Given bridged batches and the SQLite embedding caches, when coherence gating runs, then it must calculate each batch's average cosine similarity from all available batch requirement vectors to the batch centroid and store `coherence_score`.

4. **Incoherent batch splitting or fallback**: Given a batch with `coherence_score < COHERENCE_THRESHOLD` (`0.55`), when the coherence gate runs, then it must attempt a deterministic two-way split; if both sub-batches pass coherence, replace the original batch with two sub-batches, otherwise keep the original batch with `reduced_confidence = true` and append an entry to `incoherent_batches`.

5. **Risk-first queue ordering**: Given coherent and reduced-confidence batches plus `quality_weights`, when queue ordering runs, then it must produce `execution_queue` sorted by risk, with security and reliability batches before lower-risk batches, and support selectable alternative strategies: `risk`, `asr_count`, and `quality_weight_frequency`.

6. **Unprocessed requirement isolation**: Given all normalized ASR and non-ASR records, when queue ordering completes, then any requirement ID not present in the final queued batches must be returned in `unprocessed_requirements`.

7. **Story 1.3 compatibility**: All nodes must consume the implemented Story 1.3 batch shape without requiring changes to `raa/nodes/batch_construction.py` or `raa/utils/embedding_cache.py`.

## Tasks / Subtasks

- [x] Task 1: Implement overlap bridging node (AC: #1, #2, #7)
  - [x] 1.1 Create `raa/nodes/overlap_bridging.py` with one public node function: `bridge_overlaps(state: RAAState, config: RunnableConfig) -> dict`
  - [x] 1.2 Read `non_asr_db_path` and optional `embedding_model_name` from `config["configurable"]`; raise `KeyError` for missing `configurable` or `non_asr_db_path`
  - [x] 1.3 Parse cluster IDs from existing 1.3 `group_id` strings using `^cluster_(?P<cluster>-?\d+)_group_`; do not require a new `cluster` field from Story 1.3
  - [x] 1.4 Detect related batch pairs by shared parsed cluster ID or `cosine_similarity(batch_a["centroid"], batch_b["centroid"]) >= NON_ASR_SIMILARITY_THRESHOLD`
  - [x] 1.5 Stream bridge candidates through `EmbeddingCache.iter_all_vectors()` and score each candidate against both centroids; candidate qualifies only when both similarities are `>= NON_ASR_SIMILARITY_THRESHOLD`
  - [x] 1.6 Sort bridge candidates by descending `min(sim_a, sim_b)`, descending average similarity, then ascending requirement ID for deterministic ties
  - [x] 1.7 Inject up to `MAX_BRIDGE_REQUIREMENTS` candidate IDs into both batches, preserving existing `non_asr_ids`, `non_asr_records`, and `similarity_scores`
  - [x] 1.8 Add `bridge_ids` to each affected batch and return `{"batches": bridged_batches, "bridge_requirements": bridge_records}`

- [x] Task 2: Implement coherence gate node (AC: #3, #4, #7)
  - [x] 2.1 Create `raa/nodes/coherence_gate.py` with one public node function: `gate_batch_coherence(state: RAAState, config: RunnableConfig) -> dict`
  - [x] 2.2 Read `asr_db_path`, `non_asr_db_path`, and optional `embedding_model_name` from `config["configurable"]`; mirror the validation style in `build_batches`
  - [x] 2.3 Collect vectors for `batch["asr_ids"]` from the ASR cache and `batch["non_asr_ids"]` from the non-ASR cache using `EmbeddingCache.get_vector()` only
  - [x] 2.4 Compute `coherence_score` as the mean `cosine_similarity(requirement_vector, batch["centroid"])`; if no vectors are available, set score to `0.0`
  - [x] 2.5 Mark batches with score `>= COHERENCE_THRESHOLD` as `reduced_confidence = false`
  - [x] 2.6 For batches below threshold, attempt a deterministic two-way split using farthest-pair seed vectors and nearest-seed assignment by cosine similarity
  - [x] 2.7 Rebuild each sub-batch with suffixed IDs (`{group_id}_split_0`, `{group_id}_split_1`), copied records, recomputed centroid, `source_group_id`, `coherence_score`, and `reduced_confidence = false` only if both sub-batches pass
  - [x] 2.8 If split is impossible or either sub-batch remains below threshold, keep the original batch, set `reduced_confidence = true`, and return an `incoherent_batches` record with `group_id`, score, and reason

- [x] Task 3: Implement priority queue ordering node (AC: #5, #6, #7)
  - [x] 3.1 Create `raa/nodes/batch_queue_ordering.py` with one public node function: `order_batch_queue(state: RAAState, config: RunnableConfig) -> dict`
  - [x] 3.2 Read optional `queue_sort_strategy` from `config["configurable"]`, defaulting to `"risk"`; raise `ValueError` for unsupported strategies
  - [x] 3.3 Calculate batch quality/risk from `asr_records` and `non_asr_records` `quality_attributes`, using `state["quality_weights"]` as authoritative weights and fallback weight `1`
  - [x] 3.4 For default `risk` ordering, sort security/reliability batches first, then descending weighted risk score, descending ASR count, then ascending `group_id`
  - [x] 3.5 For `asr_count`, sort descending ASR count, then default risk tie-breakers
  - [x] 3.6 For `quality_weight_frequency`, sort descending total weighted quality-attribute frequency, then default risk tie-breakers
  - [x] 3.7 Return `{"execution_queue": ordered_batches, "unprocessed_requirements": leftovers}` where leftovers are full normalized records not assigned to any queued batch ID

- [x] Task 4: Unit tests for overlap bridging (AC: #1, #2, #7)
  - [x] 4.1 Create `tests/raa/unit/test_overlap_bridging.py`
  - [x] 4.2 Test shared cluster detection using current `cluster_0_group_0` / `cluster_0_group_1` IDs
  - [x] 4.3 Test centroid similarity detection for different clusters
  - [x] 4.4 Test bridge hard cap at `MAX_BRIDGE_REQUIREMENTS`
  - [x] 4.5 Test injected IDs are present in both batches and bridge records are returned
  - [x] 4.6 Test no related pairs returns unchanged batches and empty bridge list
  - [x] 4.7 Test missing `non_asr_db_path` raises clean `KeyError`

- [x] Task 5: Unit tests for coherence gating (AC: #3, #4, #7)
  - [x] 5.1 Create `tests/raa/unit/test_coherence_gate.py`
  - [x] 5.2 Test coherent batch receives `coherence_score` and `reduced_confidence = false`
  - [x] 5.3 Test empty-vector batch gets score `0.0` and reduced confidence
  - [x] 5.4 Test low-coherence batch is replaced by two passing split batches when split succeeds
  - [x] 5.5 Test low-coherence unsplittable batch remains single with `reduced_confidence = true`
  - [x] 5.6 Test `incoherent_batches` contains actionable metadata
  - [x] 5.7 Test nodes never mutate the original input batch objects in place

- [x] Task 6: Unit tests for queue ordering (AC: #5, #6, #7)
  - [x] 6.1 Create `tests/raa/unit/test_batch_queue_ordering.py`
  - [x] 6.2 Test security and reliability batches sort before lower-risk batches
  - [x] 6.3 Test `asr_count` alternative strategy
  - [x] 6.4 Test `quality_weight_frequency` alternative strategy
  - [x] 6.5 Test deterministic tie-break by `group_id`
  - [x] 6.6 Test leftover normalized records become `unprocessed_requirements`
  - [x] 6.7 Test unsupported queue strategy raises `ValueError`
### Review Findings

- [x] [Review][Patch] Potential AttributeError if configurable is None in order_batch_queue [raa/raa/nodes/batch_queue_ordering.py:29-30]

## Dev Notes

### Compatibility Baseline From Story 1.3

Story 1.3 is implemented and the targeted compatibility test passes:

```bash
python3 -m pytest tests/raa/unit/test_batch_construction.py -q
# 26 passed, 1 warning in 0.61s
```

The warning is from pytest cache writes outside this workspace's writable root and is not a Story 1.3 failure.

Current Story 1.3 batch shape produced by `build_batches`:

```python
{
    "group_id": "cluster_0_group_0",
    "centroid": list[float],
    "asr_ids": list[str],
    "asr_records": list[dict],
    "non_asr_ids": list[str],
    "non_asr_records": list[dict],
    "similarity_scores": dict[str, float],
}
```

Do not require Story 1.3 to add new fields. Story 1.4 may add fields to batches it returns (`bridge_ids`, `coherence_score`, `reduced_confidence`, `source_group_id`), but it must preserve all fields above.

### Existing APIs To Reuse

- `raa.utils.embedding_cache.EmbeddingCache.get_vector(req_id)` returns `list[float] | None` without a hash check.
- `raa.utils.embedding_cache.EmbeddingCache.iter_all_vectors()` streams `(req_id, vector)` pairs and skips corrupt BLOBs with a warning.
- `raa.utils.embedding_cache.cosine_similarity(a, b)` is the implemented pure-Python cosine helper. Use it instead of importing sklearn in new nodes unless a measured need appears.
- `raa.utils.constants` already defines `NON_ASR_SIMILARITY_THRESHOLD`, `COHERENCE_THRESHOLD`, `MAX_BRIDGE_REQUIREMENTS`, `MAX_NON_ASR_PER_BATCH`, `EMBEDDING_DIM`, and `EMBEDDING_MODEL_NAME`.
- `raa.state.schemas.RAAState` already has `batches`, `bridge_requirements`, `execution_queue`, `unprocessed_requirements`, and `incoherent_batches` channels.

### Node Return Contracts

LangGraph nodes must return state updates, not mutate and return the whole state. The docs confirm nodes are Python functions that accept state and optional `RunnableConfig`, and that node functions should return updates to state directly.

Required public node functions:

```python
from langchain_core.runnables import RunnableConfig
from raa.state.schemas import RAAState

def bridge_overlaps(state: RAAState, config: RunnableConfig) -> dict:
    return {"batches": bridged_batches, "bridge_requirements": bridge_records}

def gate_batch_coherence(state: RAAState, config: RunnableConfig) -> dict:
    return {"batches": gated_batches, "incoherent_batches": incoherent_records}

def order_batch_queue(state: RAAState, config: RunnableConfig) -> dict:
    return {"execution_queue": ordered_batches, "unprocessed_requirements": leftovers}
```

### Overlap Bridging Details

Related pair detection:

```python
same_cluster = parsed_cluster_id(a["group_id"]) == parsed_cluster_id(b["group_id"])
similar_centroids = cosine_similarity(a["centroid"], b["centroid"]) >= NON_ASR_SIMILARITY_THRESHOLD
```

Bridge record shape:

```python
{
    "requirement_id": "R17",
    "batch_ids": ["cluster_0_group_0", "cluster_0_group_1"],
    "similarity_scores": {
        "cluster_0_group_0": 0.78,
        "cluster_0_group_1": 0.72,
    },
    "reason": "shared_cluster" | "centroid_similarity",
}
```

When injecting a bridge into a batch:

- Add ID to `non_asr_ids` only if absent.
- Add record to `non_asr_records` from `state["normalized_non_asr"]` when available.
- Add/update `similarity_scores[bridge_id]` with that batch's centroid similarity.
- Add ID to `bridge_ids` without duplicates.
- Copy batches before modifying them. Do not mutate input state objects in place.

### Coherence Gate Details

Batch requirement vectors are gathered from existing IDs:

- ASR vectors: `asr_cache.get_vector(req_id)` for every `batch["asr_ids"]`
- Non-ASR vectors: `non_asr_cache.get_vector(req_id)` for every `batch["non_asr_ids"]`

Missing vectors are recoverable: log a warning and exclude that requirement from the score. If no vectors remain, the score is `0.0` and the batch is reduced-confidence.

Split algorithm must be deterministic:

1. Build `(req_id, kind, record, vector)` entries for all available ASR and non-ASR vectors.
2. If fewer than two vector entries exist, splitting is impossible.
3. Pick the farthest pair by minimum cosine similarity; tie-break by `(req_id_a, req_id_b)`.
4. Assign every entry to the seed with higher cosine similarity; tie-break to seed 0.
5. Reject the split if either side is empty.
6. Recompute each sub-batch centroid from its assigned ASR vectors when any ASR exists; otherwise use the mean of all assigned vectors.
7. Recalculate each sub-batch coherence against its recomputed centroid.
8. Accept the split only when both sub-batches score `>= COHERENCE_THRESHOLD`.

Reduced-confidence batches are intentionally preserved for Story 2.1: the execution loop will route them to RAA-A only, and the Judge will apply the `0.5x` SAAM multiplier.

### Queue Ordering Details

Quality attribute extraction:

```python
for record in batch["asr_records"] + batch["non_asr_records"]:
    attrs.extend(record.get("quality_attributes") or [])
```

Risk scoring:

- `quality_weights` from state is authoritative.
- If an attribute is not present in `quality_weights`, use fallback weight `1`.
- Treat attributes case-insensitively for security/reliability detection.
- The default strategy must put any batch containing `security` or `reliability` ahead of batches without those attributes.

Unprocessed requirements:

```python
assigned_ids = set()
for batch in ordered_batches:
    assigned_ids.update(batch.get("asr_ids", []))
    assigned_ids.update(batch.get("non_asr_ids", []))

leftovers = [
    rec for rec in state.get("normalized_asrs", []) + state.get("normalized_non_asr", [])
    if rec.get("id") not in assigned_ids
]
```

Return full records, not just IDs, so later residual processing has descriptions and attributes.

### File Structure Requirements

Create:

| File | Purpose |
| --- | --- |
| `raa/nodes/overlap_bridging.py` | Phase 3 bridge injection node |
| `raa/nodes/coherence_gate.py` | Phase 4 coherence scoring/splitting node |
| `raa/nodes/batch_queue_ordering.py` | Phase 5 risk-first queue ordering node |
| `tests/raa/unit/test_overlap_bridging.py` | Unit tests for bridge detection/injection |
| `tests/raa/unit/test_coherence_gate.py` | Unit tests for coherence scoring/splitting |
| `tests/raa/unit/test_batch_queue_ordering.py` | Unit tests for queue ordering and leftovers |

Do not modify `raa/nodes/batch_construction.py` for this story unless a failing test proves a compatibility bug. The story is scoped to consuming its output.

### Testing Standards

- Framework: `pytest >= 8.2`
- No live LLM calls.
- No live FastEmbed calls.
- Populate `EmbeddingCache` with deterministic fake vectors in temporary SQLite files, matching the existing Story 1.3 test pattern.
- Run targeted tests:

```bash
python3 -m pytest \
  tests/raa/unit/test_batch_construction.py \
  tests/raa/unit/test_overlap_bridging.py \
  tests/raa/unit/test_coherence_gate.py \
  tests/raa/unit/test_batch_queue_ordering.py -q
```

Run the existing preparation/cache tests if `EmbeddingCache` behavior changes:

```bash
python3 -m pytest tests/raa/unit/test_preparation.py tests/raa/unit/test_embedding_cache.py -q
```

### Files That Must Not Be Broken

| File | Existing Behavior To Preserve |
| --- | --- |
| `raa/nodes/batch_construction.py` | Returns the implemented Story 1.3 batch shape and does not mutate state |
| `raa/utils/embedding_cache.py` | `get_vector`, `iter_all_vectors`, `cosine_similarity`, context manager, closed-cache guards |
| `raa/nodes/preparation.py` | Normalized ASR/Non-ASR record shape and config validation style |
| `raa/state/schemas.py` | Existing state channel names and append reducer on `incoherent_batches` |
| `raa/utils/constants.py` | Existing threshold names and values |

### References

- Source: `_bmad-output/planning-artifacts/epics.md` — Epic 1, Story 1.4 acceptance criteria.
- Source: `_bmad-output/planning-artifacts/prds/prd-raa-2026-05-22/prd.md` — FR-4, FR-5, FR-6.
- Source: `_bmad-output/planning-artifacts/architecture.md` — D2/D3 embedding DB access, file layout for `overlap_bridging.py`, `coherence_gate.py`, and `batch_queue_ordering.py`, node return-pattern enforcement.
- Source: `_bmad-output/implementation-artifacts/1-3-centroid-anchored-batch-construction.md` — previous story output shape and compatibility notes.
- Source: `raa/nodes/batch_construction.py` — implemented batch construction node.
- Source: `raa/utils/embedding_cache.py` — implemented vector access and cosine helper.
- Source: `raa/state/schemas.py` — RAA state channels.
- Source: `raa/utils/constants.py` — threshold and limit constants.
- Source: LangGraph docs `/oss/python/langgraph/graph-api` and `/oss/python/langgraph/use-graph-api` — node functions accept state/config and return state updates directly.

## Story Context Completion Status

Ultimate context engine analysis completed - comprehensive developer guide created.

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context) via Claude Code

### Debug Log References

None.

### Completion Notes List

- Implemented three Phase 3-5 nodes: `bridge_overlaps` (overlap_bridging.py), `gate_batch_coherence` (coherence_gate.py), `order_batch_queue` (batch_queue_ordering.py)
- All nodes follow LangGraph return contract: (state, RunnableConfig) -> dict of state updates
- Batch copy pattern used throughout to prevent input mutation
- Overlap bridging: shared cluster + centroid similarity detection, MAX_BRIDGE_REQUIREMENTS cap, bridge_ids injection
- Coherence gate: mean cosine similarity scoring, deterministic farthest-pair two-way split, reduced_confidence fallback
- Queue ordering: three strategies (risk, asr_count, quality_weight_frequency), security/reliability prioritisation, unprocessed requirement isolation
- 33 new unit tests across three test files covering all ACs
- Full regression: 119 tests pass (26 batch_construction + 60 cache/prep + 33 new)

### File List

- `raa/nodes/overlap_bridging.py` — Phase 3 bridge injection node
- `raa/nodes/coherence_gate.py` — Phase 4 coherence scoring/splitting node
- `raa/nodes/batch_queue_ordering.py` — Phase 5 risk-first queue ordering node
- `tests/raa/unit/test_overlap_bridging.py` — 11 tests for bridge detection/injection
- `tests/raa/unit/test_coherence_gate.py` — 11 tests for coherence scoring/splitting
- `tests/raa/unit/test_batch_queue_ordering.py` — 11 tests for queue ordering and leftovers

### Change Log

- 2026-05-23: Implemented Story 1.4 — overlap bridging, coherence gating, and priority queue ordering (3 nodes, 33 tests, all ACs satisfied)
