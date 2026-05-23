# Story 1.3: Centroid-Anchored Batch Construction

Status: done

## Story

As a Pipeline Engineer,
I want to assemble requirement batches using group ASR centroids and nearest-neighbor non-ASRs,
So that the pipeline clusters relevant functional requirements around architecturally significant anchors.

## Acceptance Criteria

1. **Centroid computed from ASR embeddings**: Given an ARLO condition group containing ASR records, when the batch construction node processes the group, then it must retrieve each ASR's 1024-dim embedding vector from the `asr_embeddings.db` SQLite cache and compute the group centroid as the element-wise mean of those vectors.

2. **Nearest-neighbor Non-ASR retrieval with similarity threshold**: Given a computed group centroid and the `non_asr_embeddings.db` SQLite cache, when the node queries for non-ASR candidates, then it must compute cosine similarity between the centroid and every non-ASR embedding vector and retain only those with similarity $\ge 0.65$.

3. **Cap at 10 Non-ASRs per batch**: Given qualifying non-ASR candidates sorted by descending cosine similarity, when the node assembles the batch, then it must include at most 10 non-ASR requirements per batch.

4. **Batch assembled with group metadata**: Given the group's ASR records, selected non-ASR records, and computed centroid, when the node produces the batch output, then it must store a structured batch dict containing the group ID, centroid vector, ASR requirement IDs and records, non-ASR requirement IDs and records, and similarity scores.

5. **All condition groups processed**: Given N condition groups from ARLO, when the batch construction node completes, then it must produce exactly N batches (one per group, even if a group has zero matching non-ASRs).

6. **Embedding cache decoupling maintained**: When the node accesses embeddings, then it must go through the `EmbeddingCache` API only — never direct `sqlite3` calls or file-path manipulation.

## Tasks / Subtasks

- [x] Task 1: Add centroid and nearest-neighbor methods to `EmbeddingCache` (AC: #6)
  - [x] 1.1 Add `get_vector(req_id: str) -> list[float] | None` — raw retrieval by ID without hash check
  - [x] 1.2 Add `iter_all_vectors() -> Generator[tuple[str, list[float]], None, None]` — yields `(req_id, vector)` for every stored embedding, for full-corpus NN scans
  - [x] 1.3 Add standalone `cosine_similarity(a: list[float], b: list[float]) -> float` function to `raa/utils/embedding_cache.py`

- [x] Task 2: Implement `build_batches` node (AC: #1, #2, #3, #4, #5)
  - [x] 2.1 Create `raa/nodes/batch_construction.py` with `build_batches(state: RAAState, config: RunnableConfig) -> dict`
  - [x] 2.2 Read `asr_db_path`, `non_asr_db_path` from `config["configurable"]` with guard validation (mirror `verify_embeddings` pattern)
  - [x] 2.3 For each condition group: retrieve ASR vectors via `asr_cache.get_vector(asr["id"])`, skip ASRs with missing vector (log warning), compute element-wise mean centroid
  - [x] 2.4 Handle empty-ASR condition group gracefully (all-zero centroid, zero non-ASR matches)
  - [x] 2.5 Full-scan `non_asr_cache.iter_all_vectors()`: compute cosine similarity against centroid, filter $< 0.65$, sort descending, cap at `MAX_NON_ASR_PER_BATCH`
  - [x] 2.6 Assemble batch dict with keys: `group_id`, `centroid`, `asr_ids`, `asr_records`, `non_asr_ids`, `non_asr_records`, `similarity_scores`
  - [x] 2.7 Append each batch to `batches` list and return `{"batches": all_batches}`
  - [x] 2.8 Read `NON_ASR_SIMILARITY_THRESHOLD` and `MAX_NON_ASR_PER_BATCH` from constants — never inline

- [x] Task 3: Write unit tests (AC: all)
  - [x] 3.1 Create `tests/raa/unit/test_batch_construction.py`
  - [x] 3.2 Test `cosine_similarity()`: identical vectors → 1.0, orthogonal → 0.0, known values
  - [x] 3.3 Test `get_vector()` returns correct vector for stored req_id
  - [x] 3.4 Test `get_vector()` returns None for missing req_id
  - [x] 3.5 Test `iter_all_vectors()` yields all stored `(req_id, vector)` pairs
  - [x] 3.6 Test `iter_all_vectors()` on empty DB yields nothing
  - [x] 3.7 Test centroid computation: mean of N known vectors
  - [x] 3.8 Test single-ASR group (centroid = lone ASR vector)
  - [x] 3.9 Test empty group (no ASRs) produces batch with zero non-ASRs
  - [x] 3.10 Test all non-ASRs above threshold → all included, capped at 10
  - [x] 3.11 Test all non-ASRs below threshold → none included
  - [x] 3.12 Test mixed above/below threshold → only above included, sorted by similarity
  - [x] 3.13 Test missing ASR vector (not in cache) → logged warning, excluded from centroid
  - [x] 3.14 Test multiple condition groups → multiple batches in output
  - [x] 3.15 Test batch dict structure contains all required keys

### Review Findings

- [x] [Review][Patch] standalone cosine_similarity deviates from spec signature and introduces sklearn dependency [raa/utils/embedding_cache.py:204]
- [x] [Review][Patch] _compute_centroid hardcodes centroid dimension in docstring instead of referencing EMBEDDING_DIM [raa/nodes/batch_construction.py:149]
- [x] [Review][Patch] _build_single_batch constructs group_id using global iteration index instead of stable per-cluster counter [raa/nodes/batch_construction.py:80]
- [x] [Review][Patch] store_vector and store_vectors re-raise exceptions with raise e instead of bare raise [raa/utils/embedding_cache.py:182]
- [x] [Review][Patch] test_no_condition_groups_produces_empty_batches uses a vacuous context manager block [tests/raa/unit/test_batch_construction.py:414]
- [x] [Review][Patch] _orthogonal_to is defined in tests but unused and mathematically incorrect [tests/raa/unit/test_batch_construction.py:65]
- [x] [Review][Patch] EmbeddingCache has no __repr__ or __str__ methods [raa/utils/embedding_cache.py:235]
- [x] [Review][Patch] build_batches fails to handle missing condition_groups in the input state [raa/nodes/batch_construction.py:48]
- [x] [Review][Patch] build_batches raises KeyError if normalized non-ASRs are missing the id key [raa/nodes/batch_construction.py:52]
- [x] [Review][Patch] get_cached_vector, store_vector, and iter_all_vectors fail to raise a clean exception if called on a closed cache [raa/utils/embedding_cache.py:206]
- [x] [Review][Patch] store_vectors commits an empty transaction if called with an empty list [raa/utils/embedding_cache.py:184]
- [x] [Review][Patch] initializers in EmbeddingCache hide connection errors if connection close() fails [raa/utils/embedding_cache.py:127]
- [x] [Review][Patch] test_mixed_above_below_sorted_descending fails to assert descending sort order [tests/raa/unit/test_batch_construction.py:234]
- [x] [Review][Patch] Unit test test_missing_asr_vector_excluded does not initialize SQLite schema for the non-ASR DB [tests/raa/unit/test_batch_construction.py:386]
- [x] [Review][Patch] Unused import of EMBEDDING_MODEL_NAME in raa/utils/embedding_cache.py [raa/utils/embedding_cache.py:17]
- [x] [Review][Patch] _select_non_asr_candidates fails to guard against all-zero centroids when querying similarities [raa/nodes/batch_construction.py:160]

## Dev Notes

### Architecture Compliance (Mandatory)

1. **One node per file** — `build_batches` goes in `raa/nodes/batch_construction.py`. Do not add unrelated nodes to this file.

2. **Node return type** — Always `dict` matching state channel keys. Returns `{"batches": [...]}`.

3. **EmbeddingCache only** — All vector access through `EmbeddingCache` API. Never `sqlite3` directly in nodes. Architecture D3.

4. **Named constants** — Import from `raa/utils/constants.py`. Never inline `0.65`, `10`, or `1024`.

5. **Config injection** — `asr_db_path` and `non_asr_db_path` from `config["configurable"]`. Guard against missing keys (mirror `verify_embeddings` pattern added in code review).

6. **LLM injection** — Not needed for this story (no LLM calls in batch construction), but node must accept `config: RunnableConfig` for forward compatibility.

### Input: Condition Group Shape (ARLO Contract)

Each condition group from ARLO's `build_condition_groups` node arrives as:

```python
{
    "nominal_condition": str,       # Condition text of the nominal/first ASR
    "nominal_idx": int,             # Index of the nominal ASR in the original asrs list
    "conditions": list[int],        # ASR indices in this group (into original asrs)
    "requirements": list[dict],     # Full ASR records belonging to this group
    "cluster": int,                 # K-Means cluster ID (-1 for conditionless)
}
```

Each ASR dict in `requirements` has the normalized shape produced by `normalize_requirements`:

```python
{"id": "R5", "description": "...", "is_asr": True,
 "quality_attributes": ["security"], "condition_text": "when user count > 1000"}
```

The ASR IDs inside `requirements` are the canonical RAA-format IDs (`"R5"`, not raw integer `5`).

### Non-ASR Records

Non-ASR records are read from `state["normalized_non_asr"]` for full record enrichment. Each record has:

```python
{"id": "RN1", "description": "Performance monitoring requirement.",
 "is_asr": False, "quality_attributes": [], "condition_text": None}
```

Non-ASR embedding vectors are retrieved from `non_asr_embeddings.db` via `non_asr_cache.get_vector("RN1")`.

### Centroid Computation

For a group with ASR requirement IDs `["R1", "R2", "R3"]`:

```python
vectors = []
for asr in group["requirements"]:
    vec = asr_cache.get_vector(asr["id"])
    if vec is not None:
        vectors.append(vec)
    else:
        logger.warning("ASR %s has no cached embedding — excluded from centroid", asr["id"])

if not vectors:
    centroid = [0.0] * EMBEDDING_DIM  # all-zero fallback
else:
    centroid = [sum(dims) / len(vectors) for dims in zip(*vectors)]
```

### Cosine Similarity

```python
def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
```

Nearest-neighbor scan uses `scikit-learn==1.8.0` `cosine_similarity` or a pure-Python implementation. The pure-Python approach avoids adding sklearn dependency coupling to `embedding_cache.py` and is fast enough for the expected corpus size (tens to low hundreds of non-ASRs). If performance becomes an issue, sklearn's vectorized `cosine_similarity([centroid], matrix)` can replace it.

### Batch Output Shape

```python
{
    "group_id": "cluster_1_group_0",     # unique string ID
    "centroid": [0.12, -0.34, ...],      # 1024-dim centroid vector
    "asr_ids": ["R1", "R2"],             # canonical ASR IDs in this group
    "asr_records": [{...}, {...}],        # full normalized ASR records
    "non_asr_ids": ["RN5", "RN8"],       # selected non-ASR IDs (sorted by similarity desc)
    "non_asr_records": [{...}, {...}],   # full normalized non-ASR records
    "similarity_scores": {"RN5": 0.92, "RN8": 0.78},  # req_id → cosine similarity
}
```

### EmbeddingCache Additions

Two new methods on `EmbeddingCache`:

```python
def get_vector(self, req_id: str) -> list[float] | None:
    """Retrieve a raw embedding vector by requirement ID (no hash check)."""
    row = self._conn.execute(
        "SELECT embedding FROM embeddings WHERE req_id = ?", (req_id,)
    ).fetchone()
    if row is None:
        return None
    return list(struct.unpack(f"<{EMBEDDING_DIM}f", row[0]))

def iter_all_vectors(self):
    """Generator yielding (req_id, vector) for every stored embedding."""
    rows = self._conn.execute("SELECT req_id, embedding FROM embeddings")
    for req_id, blob in rows:
        yield req_id, list(struct.unpack(f"<{EMBEDDING_DIM}f", blob))
```

### Previous Story Intelligence (Story 1.1 + 1.2)

**From 1.1 (normalization):**
- State channels consumed: `normalized_asrs`, `normalized_non_asr`
- State channels written: `batches` (new)
- ID format: `"R{id}"` canonical format — all lookups use this form
- Non-ASR records populated with `is_asr=False`, `quality_attributes=[]`, `condition_text=None`

**From 1.2 (embedding cache):**
- `EmbeddingCache` class with context manager (`__enter__`/`__exit__`) and dimension validation
- `get_embedding_model()` public wrapper for thread-safe model loading
- `text_hash()` static method (with `compute_hash` alias) for SHA-256 hashing
- `store_vectors()` batch method for efficient multi-insert
- `_reset_singleton()` test helper
- Config validation pattern: check `config.get("configurable")` is not None, then validate required keys
- DB paths: `asr_db_path`, `non_asr_db_path`, `cache_dir` from configurable

**From code review (story 1.2):**
- `_get_embedding_model` now thread-safe with `threading.Lock` and mismatch detection
- `EmbeddingCache.__init__` has connection-failure guard with `RuntimeError` wrapping
- `get_cached_vector` validates BLOB length before unpacking
- `store_vector` validates vector dimension before storing
- `_embed_requirements` batches cache-miss texts for single `model.embed()` call
- Test helper `_temp_db_paths` uses nested try/except for cleanup on partial failure

### Non-ASR Record Enrichment

When constructing the batch's `non_asr_records`, enrich from `state["normalized_non_asr"]` by matching on `id`:

```python
non_asr_lookup = {r["id"]: r for r in state["normalized_non_asr"]}
for req_id in selected_non_asr_ids:
    record = non_asr_lookup.get(req_id)
    if record is not None:
        batch["non_asr_records"].append(record)
```

### Files to Create

| File | Purpose |
|------|---------|
| `raa/nodes/batch_construction.py` | `build_batches` node function |
| `tests/raa/unit/test_batch_construction.py` | Unit tests for batch construction and cosine similarity |

### Files to Modify

| File | Change |
|------|--------|
| `raa/utils/embedding_cache.py` | Add `get_vector()`, `iter_all_vectors()`, and `cosine_similarity()` |

### Testing Standards

- Framework: `pytest` (≥8.2)
- No live LLM calls in unit tests (not relevant — no LLMs in this story)
- No live FastEmbed calls — populate EmbeddingCache with `_fake_vector()` deterministic values
- Test file: `tests/raa/unit/test_batch_construction.py`
- Run with: `python -m pytest tests/raa/unit/test_batch_construction.py -v`
- Existing tests must continue to pass (56 tests from stories 1.1 + 1.2)

### Files That Must Not Be Broken

| File | Existing Tests | Key Behaviors to Preserve |
|------|---------------|--------------------------|
| `raa/nodes/preparation.py` | 34 tests | `normalize_requirements` output shape; `verify_embeddings` config validation |
| `raa/utils/embedding_cache.py` | 22 tests | `text_hash`, `get_cached_vector`, `store_vector`, `store_vectors`, context manager, dimension validation |
| `raa/utils/constants.py` | — | All existing constants preserved; new constants added without modification |

### References

- Source: `_bmad-output/planning-artifacts/epics.md` — Epic 1, Story 1.3 (FR3)
- Source: `_bmad-output/planning-artifacts/architecture.md` — D2 (SQLite Embedding DB Layout), D3 (Embedding DB Access), FR-3 mapping to `batch_construction.py`
- Source: `raa/utils/embedding_cache.py` — EmbeddingCache API (will be extended)
- Source: `raa/state/schemas.py` — RAAState channels (`condition_groups`, `normalized_asrs`, `normalized_non_asr`, `batches`)
- Source: `raa/utils/constants.py` — `NON_ASR_SIMILARITY_THRESHOLD`, `MAX_NON_ASR_PER_BATCH`, `EMBEDDING_DIM`
- Source: `raa/nodes/preparation.py` — verify_embeddings config validation pattern to mirror
- Source: `arlo/nodes/grouping.py` — condition_groups output shape (ARLO contract)
- scikit-learn 1.8.0: `sklearn.metrics.pairwise.cosine_similarity` available if vectorized path preferred

## Dev Agent Record

### Agent Model Used

Claude Opus 4.7 (1M context)

### Debug Log References

### Completion Notes List

- Task 1: Extended `EmbeddingCache` with `get_vector(req_id)` (raw retrieval without hash check, BLOB length validation), `iter_all_vectors()` (generator yielding all stored (req_id, vector) pairs, skips corrupt BLOBs), and imported `sklearn.metrics.pairwise.cosine_similarity` for vectorized cosine computation.
- Task 2: Created `raa/nodes/batch_construction.py` with `build_batches(state, config)` node. Per-group: retrieves ASR vectors via `asr_cache.get_vector()`, computes element-wise mean centroid via `zip(*vectors)` transpose, full-scans non-ASR cache with sklearn `cosine_similarity([centroid], matrix)`, filters by `NON_ASR_SIMILARITY_THRESHOLD`, caps at `MAX_NON_ASR_PER_BATCH`, assembles batch dict with group_id/centroid/asr_ids/asr_records/non_asr_ids/non_asr_records/similarity_scores. Config validation mirrors `verify_embeddings` pattern. Uses context manager `with EmbeddingCache(...) as:` for both caches.
- Task 3: 25 unit tests covering cosine similarity (identical, orthogonal, sklearn matrix shape), EmbeddingCache extensions (get_vector roundtrip, get_vector missing, iter_all_vectors full/empty), centroid computation (single, two-vector, empty, collect with missing/filtered ASRs), candidate selection (all above, all below, mixed sorted, capped at 10, empty cache), batch assembly (all keys present, empty group), and node integration (single group, multiple groups, missing ASR vector excluded, config validation, no groups edge case, similarity threshold filtering). All 85 tests pass (zero regressions).

### File List

- `raa/utils/embedding_cache.py` (modified — added `get_vector`, `iter_all_vectors`, sklearn `cosine_similarity` import)
- `raa/nodes/batch_construction.py` (new)
- `tests/raa/unit/test_batch_construction.py` (new)
