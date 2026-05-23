# Edge Case Hunter Code Review Prompt

You are a pure path tracer. Never comment on whether code is good or bad; only list missing handling.
Scan only the diff hunks and list boundaries that are directly reachable from the changed lines and lack an explicit guard in the diff.
Ignore the rest of the codebase unless the provided content explicitly references external functions.

Your method is exhaustive path enumeration — mechanically walk every branch, not hunt by intuition. Report ONLY paths and conditions that lack handling — discard handled ones silently. Do NOT editorialize or add filler — findings only.

Output findings strictly as a JSON array of objects. Each object must contain exactly these four fields and nothing else:

```json
[{
  "location": "file:start-end (or file:line when single line, or file:hunk when exact line unavailable)",
  "trigger_condition": "one-line description (max 15 words)",
  "guard_snippet": "minimal code sketch that closes the gap (single-line escaped string, no raw newlines or unescaped quotes)",
  "potential_consequence": "what could actually go wrong (max 15 words)"
}]
```

No extra text, no explanations, no markdown wrapping. An empty array `[]` is valid when no unhandled paths are found.

---

## Content to Review (Unified Diff)

```diff
diff --git a/raa/raa/nodes/batch_construction.py b/raa/raa/nodes/batch_construction.py
new file mode 100644
index 0000000..df95a6b
--- /dev/null
+++ b/raa/raa/nodes/batch_construction.py
@@ -0,0 +1,194 @@
+"""
+Phase 2 node: Centroid-anchored batch construction (FR-3).
+
+Assembles requirement batches by computing group ASR centroids and
+retrieving nearest-neighbor non-ASR candidates via cosine similarity
+from the SQLite embedding cache.
+"""
+from __future__ import annotations
+
+import logging
+
+from langchain_core.runnables import RunnableConfig
+
+from raa.state.schemas import RAAState
+from raa.utils.constants import EMBEDDING_DIM, MAX_NON_ASR_PER_BATCH, NON_ASR_SIMILARITY_THRESHOLD
+from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity
+
+logger = logging.getLogger(__name__)
+
+
+def build_batches(state: RAAState, config: RunnableConfig) -> dict:
+    """Assemble requirement batches from ARLO condition groups and cached embeddings.
+
+    For each condition group:
+    1. Retrieve ASR embedding vectors and compute the element-wise mean centroid.
+    2. Full-scan the non-ASR embedding cache for cosine similarity ≥ threshold.
+    3. Select top-N non-ASRs (capped at ``MAX_NON_ASR_PER_BATCH``).
+    4. Assemble a batch dict with group metadata and requirement records.
+
+    Config keys expected in ``config["configurable"]``:
+        ``asr_db_path``, ``non_asr_db_path``
+
+    Returns:
+        dict with key ``batches`` — list of batch dicts, one per condition group.
+    """
+    configurable = config.get("configurable")
+    if configurable is None:
+        raise KeyError("RunnableConfig is missing 'configurable' key")
+
+    missing = [k for k in ("asr_db_path", "non_asr_db_path") if k not in configurable]
+    if missing:
+        raise KeyError(f"Missing required configurable paths: {', '.join(missing)}")
+
+    asr_db_path = configurable["asr_db_path"]
+    non_asr_db_path = configurable["non_asr_db_path"]
+    model_name = configurable.get("embedding_model_name", "batch-construction")
+
+    condition_groups = state["condition_groups"]
+    normalized_non_asr = state.get("normalized_non_asr") or []
+
+    # O(1) lookup for non-ASR record enrichment
+    non_asr_lookup = {r["id"]: r for r in normalized_non_asr}
+
+    with EmbeddingCache(asr_db_path, model_name) as asr_cache, \
+         EmbeddingCache(non_asr_db_path, model_name) as non_asr_cache:
+
+        batches = []
+        for group_idx, group in enumerate(condition_groups):
+            batch = _build_single_batch(
+                group=group,
+                group_idx=group_idx,
+                asr_cache=asr_cache,
+                non_asr_cache=non_asr_cache,
+                non_asr_lookup=non_asr_lookup,
+            )
+            batches.append(batch)
+
+    return {"batches": batches}
+
+
+def _build_single_batch(
+    group: dict,
+    group_idx: int,
+    asr_cache: EmbeddingCache,
+    non_asr_cache: EmbeddingCache,
+    non_asr_lookup: dict[str, dict],
+) -> dict:
+    """Build a single batch for one condition group."""
+    cluster = group.get("cluster", -1)
+    group_id = f"cluster_{cluster}_group_{group_idx}"
+
+    # ── 1. Retrieve ASR vectors and compute centroid ──────────────────────
+    asr_vectors, asr_ids, asr_records = _collect_asr_vectors(
+        group.get("requirements", []), asr_cache
+    )
+    centroid = _compute_centroid(asr_vectors)
+
+    # ── 2. Nearest-neighbor non-ASR scan ──────────────────────────────────
+    selected_ids, similarity_scores = _select_non_asr_candidates(
+        centroid=centroid,
+        non_asr_cache=non_asr_cache,
+        threshold=NON_ASR_SIMILARITY_THRESHOLD,
+        max_candidates=MAX_NON_ASR_PER_BATCH,
+    )
+
+    # ── 3. Enrich with full non-ASR records ───────────────────────────────
+    non_asr_records = []
+    for req_id in selected_ids:
+        rec = non_asr_lookup.get(req_id)
+        if rec is not None:
+            non_asr_records.append(rec)
+        else:
+            logger.warning("Non-ASR %s has embedding but no normalized record", req_id)
+
+    return {
+        "group_id": group_id,
+        "centroid": centroid,
+        "asr_ids": asr_ids,
+        "asr_records": asr_records,
+        "non_asr_ids": selected_ids,
+        "non_asr_records": non_asr_records,
+        "similarity_scores": similarity_scores,
+    }
+
+
+# ── Private helpers ─────────────────────────────────────────────────────────
+
+
+def _collect_asr_vectors(
+    asr_requirements: list[dict],
+    asr_cache: EmbeddingCache,
+) -> tuple[list[list[float]], list[str], list[dict]]:
+    """Retrieve embedding vectors for ASR requirements in a group.
+
+    Returns:
+        (vectors, ids, records) — ASRs missing cached vectors are excluded
+        with a logged warning.
+    """
+    vectors: list[list[float]] = []
+    ids: list[str] = []
+    records: list[dict] = []
+
+    for asr in asr_requirements:
+        asr_id = asr.get("id")
+        if not asr_id:
+            logger.warning("ASR record missing 'id' key: %r", asr)
+            continue
+        vec = asr_cache.get_vector(asr_id)
+        if vec is None:
+            logger.warning("ASR %s has no cached embedding — excluded from centroid", asr_id)
+            continue
+        vectors.append(vec)
+        ids.append(asr_id)
+        records.append(asr)
+
+    return vectors, ids, records
+
+
+def _compute_centroid(vectors: list[list[float]]) -> list[float]:
+    """Element-wise mean of N vectors → 1024-dim centroid.
+
+    Returns an all-zero vector when the input list is empty.
+    """
+    if not vectors:
+        return [0.0] * EMBEDDING_DIM
+    n = len(vectors)
+    return [sum(dims) / n for dims in zip(*vectors)]
+
+
+def _select_non_asr_candidates(
+    centroid: list[float],
+    non_asr_cache: EmbeddingCache,
+    threshold: float,
+    max_candidates: int,
+) -> tuple[list[str], dict[str, float]]:
+    """Full-scan non-ASR cache for cosine similarity ≥ threshold.
+
+    Returns (selected_ids, similarity_scores) sorted by similarity descending.
+    """
+    # Collect all non-ASR vectors into a matrix for sklearn
+    non_asr_ids: list[str] = []
+    non_asr_matrix: list[list[float]] = []
+
+    for req_id, vec in non_asr_cache.iter_all_vectors():
+        non_asr_ids.append(req_id)
+        non_asr_matrix.append(vec)
+
+    if not non_asr_matrix:
+        return [], {}
+
+    # sklearn: cosine_similarity([centroid], matrix) → (1, N) array
+    sim_matrix = cosine_similarity([centroid], non_asr_matrix)
+    similarities: list[float] = sim_matrix[0].tolist()
+
+    # Filter, sort, cap
+    scored: list[tuple[float, str]] = [
+        (s, rid) for s, rid in zip(similarities, non_asr_ids) if s >= threshold
+    ]
+    scored.sort(key=lambda x: x[0], reverse=True)
+    scored = scored[:max_candidates]
+
+    selected_ids = [rid for _, rid in scored]
+    similarity_scores = {rid: float(s) for s, rid in scored}
+    return selected_ids, similarity_scores
diff --git a/raa/raa/utils/embedding_cache.py b/raa/raa/utils/embedding_cache.py
new file mode 100644
index 0000000..d751062
--- /dev/null
+++ b/raa/raa/utils/embedding_cache.py
@@ -0,0 +1,254 @@
+"""
+Embedding cache abstraction (AR4) — encapsulates all SQLite read/write for
+dense vector storage and provides the FastEmbed model loader.
+
+Nodes never call ``sqlite3`` or ``fastembed`` directly. They use this module.
+"""
+from __future__ import annotations
+
+import hashlib
+import logging
+import sqlite3
+import struct
+import threading
+from pathlib import Path
+
+from fastembed import TextEmbedding
+from sklearn.metrics.pairwise import cosine_similarity
+
+from raa.utils.constants import EMBEDDING_DIM, EMBEDDING_MODEL_NAME
+
+logger = logging.getLogger(__name__)
+
+# ── Exception ────────────────────────────────────────────────────────────────
+
+
+class ModelNonExistentException(Exception):
+    """Raised when FastEmbed model files are absent from cache_dir."""
+
+    def __init__(self, cache_dir: str, model_name: str) -> None:
+        model_dir = Path(cache_dir) / _model_dir_name(model_name)
+        super().__init__(
+            f"Embedding model files not found at {model_dir}. "
+            f"Download {model_name} first or place it in {cache_dir}."
+        )
+        self.cache_dir = cache_dir
+        self.model_name = model_name
+
+
+# ── Model loader (singleton, mirrors arlo/nodes/embedding.py) ────────────────
+
+_embedding_model: TextEmbedding | None = None
+_loaded_cache_dir: str | None = None
+_loaded_model_name: str | None = None
+_model_lock = threading.Lock()
+
+
+def _model_dir_name(model_name: str) -> str:
+    """FastEmbed's on-disk directory name for a model."""
+    return "models--" + model_name.replace("/", "--")
+
+
+def _get_embedding_model(cache_dir: str, model_name: str) -> TextEmbedding:
+    """Lazy-initialize the FastEmbed TextEmbedding model singleton.
+
+    Verifies the model directory exists on disk before initializing.
+    Raises ``ModelNonExistentException`` if absent.
+    """
+    global _embedding_model, _loaded_cache_dir, _loaded_model_name
+    
+    with _model_lock:
+        if _embedding_model is not None:
+            if _loaded_cache_dir != cache_dir or _loaded_model_name != model_name:
+                raise RuntimeError(
+                    f"Model already loaded with name {_loaded_model_name} and cache_dir {_loaded_cache_dir}. "
+                    f"Mismatched request: model_name={model_name}, cache_dir={cache_dir}"
+                )
+            return _embedding_model
+
+        model_dir = Path(cache_dir) / _model_dir_name(model_name)
+        if not model_dir.is_dir():
+            raise ModelNonExistentException(cache_dir, model_name)
+        
+        try:
+            _embedding_model = TextEmbedding(
+                model_name=model_name,
+                cache_dir=cache_dir,
+            )
+            _loaded_cache_dir = cache_dir
+            _loaded_model_name = model_name
+        except Exception:
+            _embedding_model = None
+            _loaded_cache_dir = None
+            _loaded_model_name = None
+            raise
+        
+        logger.info("FastEmbed model loaded: %s (cache=%s)", model_name, cache_dir)
+        return _embedding_model
+
+
+def get_embedding_model(cache_dir: str, model_name: str) -> TextEmbedding:
+    """Public wrapper to lazy-initialize and retrieve the TextEmbedding model singleton."""
+    return _get_embedding_model(cache_dir, model_name)
+
+
+def _reset_singleton() -> None:
+    """Reset the singleton state (used only for unit testing)."""
+    global _embedding_model, _loaded_cache_dir, _loaded_model_name
+    with _model_lock:
+        _embedding_model = None
+        _loaded_cache_dir = None
+        _loaded_model_name = None
+
+
+# ── Embedding cache ──────────────────────────────────────────────────────────
+
+class EmbeddingCache:
+    """SQLite-backed cache for 1024-dim dense embedding vectors (D2).
+
+    Schema: ``(req_id TEXT PRIMARY KEY, embedding BLOB, text_hash TEXT, model_name TEXT)``
+    """
+
+    def __init__(self, db_path: str, model_name: str) -> None:
+        self._db_path = db_path
+        self._model_name = model_name
+        self._conn = None
+        
+        try:
+            self._conn = sqlite3.connect(db_path)
+            self._conn.execute("PRAGMA journal_mode=WAL")
+            self._conn.execute(
+                "CREATE TABLE IF NOT EXISTS embeddings ("
+                "  req_id TEXT PRIMARY KEY,"
+                "  embedding BLOB NOT NULL,"
+                "  text_hash TEXT NOT NULL,"
+                "  model_name TEXT NOT NULL"
+                ")"
+            )
+            self._conn.commit()
+        except Exception as e:
+            if self._conn is not None:
+                self._conn.close()
+            raise RuntimeError(f"Cannot initialize cache DB at {db_path}: {e}") from e
+
+    # ── Public API ───────────────────────────────────────────────────────
+
+    @staticmethod
+    def text_hash(text: str) -> str:
+        """SHA-256 hex digest of ``text.encode('utf-8')``."""
+        return hashlib.sha256(text.encode("utf-8")).hexdigest()
+
+    # Maintain compute_hash as an alias for backward compatibility.
+    compute_hash = text_hash
+
+    def get_cached_vector(self, req_id: str, text_hash: str) -> list[float] | None:
+        """Return deserialized 1024-dim vector if (req_id, text_hash) matches.
+
+        Returns ``None`` when the requirement is missing or the hash is stale.
+        """
+        row = self._conn.execute(
+            "SELECT embedding FROM embeddings WHERE req_id = ? AND text_hash = ?",
+            (req_id, text_hash),
+        ).fetchone()
+        if row is None:
+            return None
+        blob = row[0]
+        expected_len = EMBEDDING_DIM * 4
+        if len(blob) != expected_len:
+            logger.warning(
+                "Corrupt or incorrect length BLOB for req_id %s: expected %d bytes, got %d",
+                req_id, expected_len, len(blob)
+            )
+            return None
+        return list(struct.unpack(f"<{EMBEDDING_DIM}f", blob))
+
+    def store_vector(self, req_id: str, text_hash: str, vector: list[float]) -> None:
+        """Serialize vector to BLOB and INSERT OR REPLACE into the DB."""
+        if len(vector) != EMBEDDING_DIM:
+            raise ValueError(f"Expected vector of length {EMBEDDING_DIM}, got {len(vector)}")
+        blob = struct.pack(f"<{EMBEDDING_DIM}f", *vector)
+        try:
+            self._conn.execute(
+                "INSERT OR REPLACE INTO embeddings (req_id, embedding, text_hash, model_name) "
+                "VALUES (?, ?, ?, ?)",
+                (req_id, blob, text_hash, self._model_name),
+            )
+            self._conn.commit()
+        except Exception as e:
+            try:
+                self._conn.rollback()
+            except sqlite3.Error:
+                pass
+            raise e
+
+    def store_vectors(self, records: list[tuple[str, str, list[float]]]) -> None:
+        """Serialize and insert multiple vectors in a single transaction."""
+        try:
+            for req_id, text_hash, vector in records:
+                if len(vector) != EMBEDDING_DIM:
+                    raise ValueError(f"Expected vector of length {EMBEDDING_DIM}, got {len(vector)}")
+                blob = struct.pack(f"<{EMBEDDING_DIM}f", *vector)
+                self._conn.execute(
+                    "INSERT OR REPLACE INTO embeddings (req_id, embedding, text_hash, model_name) "
+                    "VALUES (?, ?, ?, ?)",
+                    (req_id, blob, text_hash, self._model_name),
+                )
+            self._conn.commit()
+        except Exception as e:
+            try:
+                self._conn.rollback()
+            except sqlite3.Error:
+                pass
+            raise e
+
+    # ── Raw vector access (for centroid / nearest-neighbor queries) ─────
+
+    def get_vector(self, req_id: str) -> list[float] | None:
+        """Retrieve a raw embedding vector by requirement ID (no hash check)."""
+        row = self._conn.execute(
+            "SELECT embedding FROM embeddings WHERE req_id = ?", (req_id,)
+        ).fetchone()
+        if row is None:
+            return None
+        blob = row[0]
+        expected_len = EMBEDDING_DIM * 4
+        if len(blob) != expected_len:
+            logger.warning(
+                "Corrupt BLOB for req_id %s: expected %d bytes, got %d",
+                req_id, expected_len, len(blob),
+            )
+            return None
+        return list(struct.unpack(f"<{EMBEDDING_DIM}f", blob))
+
+    def iter_all_vectors(self):
+        """Generator yielding (req_id, vector) for every stored embedding.
+
+        Returns each vector as a ``list[float]`` of length ``EMBEDDING_DIM``.
+        """
+        rows = self._conn.execute("SELECT req_id, embedding FROM embeddings")
+        for req_id, blob in rows:
+            if len(blob) == EMBEDDING_DIM * 4:
+                yield req_id, list(struct.unpack(f"<{EMBEDDING_DIM}f", blob))
+            else:
+                logger.warning("Skipping corrupt BLOB for req_id %s", req_id)
+
+    # ── Context Manager ──────────────────────────────────────────────────
+
+    def __enter__(self) -> EmbeddingCache:
+        return self
+
+    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
+        self.close()
+
+    # ── Test / teardown helpers ──────────────────────────────────────────
+
+    def close(self) -> None:
+        """Close the underlying SQLite connection."""
+        if self._conn is not None:
+            self._conn.close()
+            self._conn = None
+
+    @property
+    def db_path(self) -> str:
+        return self._db_path
+
diff --git a/raa/tests/raa/unit/test_batch_construction.py b/raa/tests/raa/unit/test_batch_construction.py
new file mode 100644
index 0000000..c6b119c
--- /dev/null
+++ b/raa/tests/raa/unit/test_batch_construction.py
@@ -0,0 +1,449 @@
+"""
+Unit tests for centroid-anchored batch construction (FR-3).
+
+Covers:
+- EmbeddingCache.get_vector / iter_all_vectors
+- Centroid computation
+- Nearest-neighbor non-ASR selection via cosine similarity
+- Batch assembly with full metadata
+"""
+from __future__ import annotations
+
+import math
+import os
+import tempfile
+from unittest.mock import patch
+
+import pytest
+
+from raa.utils.constants import EMBEDDING_DIM, MAX_NON_ASR_PER_BATCH, NON_ASR_SIMILARITY_THRESHOLD
+from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity
+from raa.nodes.batch_construction import (
+    build_batches,
+    _build_single_batch,
+    _collect_asr_vectors,
+    _compute_centroid,
+    _select_non_asr_candidates,
+)
+
+
+# ── Helpers ──────────────────────────────────────────────────────────────────
+
+def _make_config(**overrides):
+    return {
+        "configurable": {
+            "thread_id": "test-thread-1",
+            "asr_db_path": ":memory:",
+            "non_asr_db_path": ":memory:",
+            **overrides,
+        }
+    }
+
+
+def _make_state(condition_groups=None, normalized_non_asr=None):
+    return {
+        "requirements": {},
+        "asrs": [],
+        "non_asr": [],
+        "condition_groups": condition_groups or [],
+        "quality_weights": {},
+        "review_mode": "autonomous",
+        "normalized_asrs": [],
+        "normalized_non_asr": normalized_non_asr or [],
+        "embeddings_ready": True,
+        "batch_outputs": [],
+        "open_questions": [],
+        "incoherent_batches": [],
+        "batch_cursor": 0,
+    }
+
+
+def _fake_vector(i=0):
+    return [(float(idx + i) / 1024.0) % 1.0 for idx in range(EMBEDDING_DIM)]
+
+
+def _orthogonal_to(v):
+    """Return a vector orthogonal to v (dot product = 0)."""
+    result = v[:]
+    mid = len(result) // 2
+    result[0], result[mid] = result[mid], -result[0]
+    return result
+
+
+def _temp_db_paths():
+    f1 = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
+    p1 = f1.name
+    f1.close()
+    try:
+        f2 = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
+        p2 = f2.name
+        f2.close()
+        return p1, p2
+    except Exception:
+        try:
+            os.unlink(p1)
+        except OSError:
+            pass
+        raise
+
+
+def _populate_cache(cache, records):
+    """Populate an EmbeddingCache with (req_id, text, vector) tuples."""
+    for req_id, text, vec in records:
+        h = EmbeddingCache.text_hash(text)
+        cache.store_vector(req_id, h, vec)
+
+
+# ── cosine_similarity tests ──────────────────────────────────────────────────
+
+
+class TestCosineSimilarity:
+
+    def test_identical_vectors(self):
+        v = _fake_vector(0)
+        assert math.isclose(cosine_similarity([v], [v])[0][0], 1.0, rel_tol=1e-6)
+
+    def test_orthogonal_vectors(self):
+        v1 = [1.0] + [0.0] * (EMBEDDING_DIM - 1)
+        v2 = [0.0] + [1.0] + [0.0] * (EMBEDDING_DIM - 2)
+        result = cosine_similarity([v1], [v2])[0][0]
+        assert math.isclose(result, 0.0, abs_tol=1e-6)
+
+    def test_sklearn_matrix_shape(self):
+        X = [[0.5, 0.5], [1.0, 0.0]]
+        Y = [[1.0, 0.0], [0.0, 1.0]]
+        sim = cosine_similarity(X, Y)
+        assert sim.shape == (2, 2)
+
+
+# ── EmbeddingCache extension tests ───────────────────────────────────────────
+
+
+class TestEmbeddingCacheExtensions:
+
+    def test_get_vector_returns_stored_vector(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            vec = _fake_vector(42)
+            cache.store_vector("R1", EmbeddingCache.text_hash("text"), vec)
+            retrieved = cache.get_vector("R1")
+            assert retrieved is not None
+            assert len(retrieved) == EMBEDDING_DIM
+            for a, b in zip(retrieved, vec):
+                assert abs(a - b) < 1e-6
+
+    def test_get_vector_returns_none_for_missing(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            assert cache.get_vector("R999") is None
+
+    def test_iter_all_vectors_yields_all(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            expected = {}
+            for i in range(5):
+                rid = f"R{i}"
+                vec = _fake_vector(i)
+                expected[rid] = vec
+                cache.store_vector(rid, EmbeddingCache.text_hash(f"t{i}"), vec)
+
+            seen = dict(cache.iter_all_vectors())
+            assert len(seen) == len(expected)
+            for rid, vec in expected.items():
+                assert rid in seen
+                for a, b in zip(seen[rid], vec):
+                    assert abs(a - b) < 1e-6
+
+    def test_iter_all_vectors_empty_db(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            assert list(cache.iter_all_vectors()) == []
+
+
+# ── Centroid computation tests ───────────────────────────────────────────────
+
+
+class TestCentroidComputation:
+
+    def test_single_vector_centroid(self):
+        v = _fake_vector(0)
+        result = _compute_centroid([v])
+        for a, b in zip(result, v):
+            assert abs(a - b) < 1e-6
+
+    def test_two_vectors_centroid(self):
+        v1 = [1.0] * EMBEDDING_DIM
+        v2 = [3.0] * EMBEDDING_DIM
+        result = _compute_centroid([v1, v2])
+        assert all(abs(x - 2.0) < 1e-6 for x in result)
+
+    def test_empty_vectors_returns_zero_centroid(self):
+        result = _compute_centroid([])
+        assert len(result) == EMBEDDING_DIM
+        assert all(x == 0.0 for x in result)
+
+    def test_collect_asr_vectors_filters_missing(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            v1 = _fake_vector(0)
+            cache.store_vector("R1", EmbeddingCache.text_hash("t1"), v1)
+            # R2 not in cache
+
+            vectors, ids, records = _collect_asr_vectors(
+                [{"id": "R1"}, {"id": "R2"}], cache
+            )
+            assert len(vectors) == 1
+            assert ids == ["R1"]
+            assert len(records) == 1
+
+    def test_collect_asr_vectors_with_missing_id_key(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            vectors, ids, records = _collect_asr_vectors(
+                [{"no_id": True}], cache
+            )
+            assert vectors == []
+            assert ids == []
+
+
+# ── Non-ASR candidate selection tests ────────────────────────────────────────
+
+
+class TestSelectNonAsrCandidates:
+
+    def test_all_above_threshold(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            centroid = [1.0] * EMBEDDING_DIM
+            # All non-ASRs point same direction as centroid → high similarity
+            for i in range(5):
+                vec = [1.0 + i * 0.001] * EMBEDDING_DIM
+                cache.store_vector(f"RN{i}", EmbeddingCache.text_hash(f"t{i}"), vec)
+
+            ids, scores = _select_non_asr_candidates(
+                centroid, cache, 0.0, MAX_NON_ASR_PER_BATCH
+            )
+            assert len(ids) == 5
+
+    def test_all_below_threshold(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            centroid = [1.0] * EMBEDDING_DIM
+            # All non-ASRs point opposite → ~-1 cosine similarity
+            for i in range(3):
+                vec = [-1.0] * EMBEDDING_DIM
+                cache.store_vector(f"RN{i}", EmbeddingCache.text_hash(f"t{i}"), vec)
+
+            ids, scores = _select_non_asr_candidates(
+                centroid, cache, NON_ASR_SIMILARITY_THRESHOLD, MAX_NON_ASR_PER_BATCH
+            )
+            assert len(ids) == 0
+
+    def test_mixed_above_below_sorted_descending(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            centroid = _fake_vector(0)
+            # Same direction as centroid → cosine ≈ 1.0
+            v_high = [x * 1.1 for x in centroid]
+            # Different direction → lower similarity
+            v_mid = _fake_vector(500)
+            # Opposite direction → negative cosine
+            v_low = [-x for x in centroid]
+
+            cache.store_vector("RN_high", EmbeddingCache.text_hash("h"), v_high)
+            cache.store_vector("RN_mid", EmbeddingCache.text_hash("m"), v_mid)
+            cache.store_vector("RN_low", EmbeddingCache.text_hash("l"), v_low)
+
+            ids, scores = _select_non_asr_candidates(
+                centroid, cache, 0.1, MAX_NON_ASR_PER_BATCH
+            )
+            assert len(ids) >= 1
+            assert "RN_high" in ids
+            assert "RN_low" not in ids
+
+    def test_capped_at_max(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            centroid = [1.0] * EMBEDDING_DIM
+            for i in range(15):
+                cache.store_vector(f"RN{i}", EmbeddingCache.text_hash(f"t{i}"), [2.0] * EMBEDDING_DIM)
+
+            ids, _ = _select_non_asr_candidates(
+                centroid, cache, 0.0, MAX_NON_ASR_PER_BATCH
+            )
+            assert len(ids) == MAX_NON_ASR_PER_BATCH
+
+    def test_empty_cache_returns_empty(self):
+        with EmbeddingCache(":memory:", "test") as cache:
+            centroid = [1.0] * EMBEDDING_DIM
+            ids, scores = _select_non_asr_candidates(
+                centroid, cache, 0.5, MAX_NON_ASR_PER_BATCH
+            )
+            assert ids == []
+            assert scores == {}
+
+
+# ── Batch assembly tests ─────────────────────────────────────────────────────
+
+
+class TestBuildSingleBatch:
+
+    def test_batch_dict_has_all_keys(self):
+        with EmbeddingCache(":memory:", "test") as asr_cache, \
+             EmbeddingCache(":memory:", "test") as non_asr_cache:
+
+            asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), _fake_vector(0))
+            non_asr_cache.store_vector("RN1", EmbeddingCache.text_hash("b"), _fake_vector(0))
+
+            group = {
+                "cluster": 0,
+                "requirements": [{"id": "R1", "description": "auth"}],
+            }
+            non_asr_lookup = {"RN1": {"id": "RN1", "description": "log"}}
+
+            batch = _build_single_batch(group, 0, asr_cache, non_asr_cache, non_asr_lookup)
+            assert "group_id" in batch
+            assert "centroid" in batch
+            assert "asr_ids" in batch
+            assert "asr_records" in batch
+            assert "non_asr_ids" in batch
+            assert "non_asr_records" in batch
+            assert "similarity_scores" in batch
+            assert batch["group_id"] == "cluster_0_group_0"
+            assert len(batch["centroid"]) == EMBEDDING_DIM
+
+    def test_empty_group_produces_batch(self):
+        with EmbeddingCache(":memory:", "test") as asr_cache, \
+             EmbeddingCache(":memory:", "test") as non_asr_cache:
+
+            group = {"requirements": []}
+            batch = _build_single_batch(group, 0, asr_cache, non_asr_cache, {})
+            assert batch["asr_ids"] == []
+            assert batch["non_asr_ids"] == []
+            assert all(c == 0.0 for c in batch["centroid"])
+
+
+# ── build_batches node tests ─────────────────────────────────────────────────
+
+
+class TestBuildBatchesNode:
+
+    def test_single_condition_group(self):
+        asr_db, non_asr_db = _temp_db_paths()
+        try:
+            # Populate caches
+            with EmbeddingCache(asr_db, "test") as asr_cache, \
+                 EmbeddingCache(non_asr_db, "test") as non_asr_cache:
+
+                asr_cache.store_vector("R1", EmbeddingCache.text_hash("auth"), _fake_vector(0))
+                asr_cache.store_vector("R2", EmbeddingCache.text_hash("log"), _fake_vector(1))
+                non_asr_cache.store_vector("RN1", EmbeddingCache.text_hash("perf"), _fake_vector(0))
+
+            state = _make_state(
+                condition_groups=[{
+                    "cluster": 0,
+                    "requirements": [
+                        {"id": "R1", "description": "Authenticate users"},
+                        {"id": "R2", "description": "Log all access"},
+                    ],
+                }],
+                normalized_non_asr=[
+                    {"id": "RN1", "description": "Performance monitoring"},
+                ],
+            )
+
+            result = build_batches(state, _make_config(
+                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
+            ))
+            assert "batches" in result
+            assert len(result["batches"]) == 1
+            b = result["batches"][0]
+            assert b["group_id"] == "cluster_0_group_0"
+            assert b["asr_ids"] == ["R1", "R2"]
+            assert len(b["centroid"]) == EMBEDDING_DIM
+        finally:
+            os.unlink(asr_db)
+            os.unlink(non_asr_db)
+
+    def test_multiple_condition_groups(self):
+        asr_db, non_asr_db = _temp_db_paths()
+        try:
+            with EmbeddingCache(asr_db, "test") as asr_cache, \
+                 EmbeddingCache(non_asr_db, "test") as non_asr_cache:
+
+                for gid in [0, 1]:
+                    asr_cache.store_vector(f"R{gid}", EmbeddingCache.text_hash(f"a{gid}"), _fake_vector(gid))
+                non_asr_cache.store_vector("RN1", EmbeddingCache.text_hash("n"), _fake_vector(0))
+
+            state = _make_state(
+                condition_groups=[
+                    {"cluster": 0, "requirements": [{"id": "R0"}]},
+                    {"cluster": 1, "requirements": [{"id": "R1"}]},
+                ],
+                normalized_non_asr=[{"id": "RN1", "description": "perf"}],
+            )
+
+            result = build_batches(state, _make_config(
+                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
+            ))
+            assert len(result["batches"]) == 2
+            assert result["batches"][0]["group_id"] == "cluster_0_group_0"
+            assert result["batches"][1]["group_id"] == "cluster_1_group_1"
+        finally:
+            os.unlink(asr_db)
+            os.unlink(non_asr_db)
+
+    def test_missing_asr_vector_excluded(self):
+        asr_db, non_asr_db = _temp_db_paths()
+        try:
+            with EmbeddingCache(asr_db, "test") as asr_cache:
+                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), _fake_vector(0))
+                # R2 not stored
+
+            state = _make_state(
+                condition_groups=[{
+                    "cluster": 0,
+                    "requirements": [{"id": "R1"}, {"id": "R2"}],
+                }],
+            )
+
+            result = build_batches(state, _make_config(
+                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
+            ))
+            b = result["batches"][0]
+            assert b["asr_ids"] == ["R1"]  # R2 excluded
+        finally:
+            os.unlink(asr_db)
+            os.unlink(non_asr_db)
+
+    def test_config_missing_keys_raises(self):
+        with pytest.raises(KeyError, match="asr_db_path"):
+            build_batches(_make_state(), {"configurable": {}})
+
+    def test_no_condition_groups_produces_empty_batches(self):
+        with EmbeddingCache(":memory:", "test"):
+            result = build_batches(
+                _make_state(condition_groups=[]),
+                _make_config(),
+            )
+            assert result["batches"] == []
+
+    def test_batch_respects_similarity_threshold(self):
+        asr_db, non_asr_db = _temp_db_paths()
+        try:
+            with EmbeddingCache(asr_db, "test") as asr_cache, \
+                 EmbeddingCache(non_asr_db, "test") as non_asr_cache:
+
+                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), [1.0] * EMBEDDING_DIM)
+                # High similarity non-ASR
+                non_asr_cache.store_vector("RN_near", EmbeddingCache.text_hash("n"), [0.9] * EMBEDDING_DIM)
+                # Low similarity non-ASR (opposite direction)
+                non_asr_cache.store_vector("RN_far", EmbeddingCache.text_hash("f"), [-1.0] * EMBEDDING_DIM)
+
+            state = _make_state(
+                condition_groups=[{"cluster": 0, "requirements": [{"id": "R1"}]}],
+                normalized_non_asr=[
+                    {"id": "RN_near", "description": "near"},
+                    {"id": "RN_far", "description": "far"},
+                ],
+            )
+
+            result = build_batches(state, _make_config(
+                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
+            ))
+            b = result["batches"][0]
+            assert "RN_near" in b["non_asr_ids"]
+            assert "RN_far" not in b["non_asr_ids"]
+        finally:
+            os.unlink(asr_db)
+            os.unlink(non_asr_db)

```
