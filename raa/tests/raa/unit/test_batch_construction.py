"""
Unit tests for centroid-anchored batch construction (FR-3).

Covers:
- EmbeddingCache.get_vector / iter_all_vectors
- Centroid computation
- Nearest-neighbor non-ASR selection via cosine similarity
- Batch assembly with full metadata
"""
from __future__ import annotations

import math
import os
import tempfile
from unittest.mock import patch

import pytest

from raa.utils.constants import EMBEDDING_DIM, MAX_NON_ASR_PER_BATCH, NON_ASR_SIMILARITY_THRESHOLD
from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity
from raa.nodes.batch_construction import (
    build_batches,
    _build_single_batch,
    _collect_asr_vectors,
    _compute_centroid,
    _select_non_asr_candidates,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_config(**overrides):
    return {
        "configurable": {
            "thread_id": "test-thread-1",
            "asr_db_path": ":memory:",
            "non_asr_db_path": ":memory:",
            **overrides,
        }
    }


def _make_state(condition_groups=None, normalized_non_asr=None):
    return {
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": condition_groups or [],
        "quality_weights": {},
        "review_mode": "autonomous",
        "normalized_asrs": [],
        "normalized_non_asr": normalized_non_asr or [],
        "embeddings_ready": True,
        "batch_outputs": [],
        "open_questions": [],
        "incoherent_batches": [],
        "batch_cursor": 0,
    }


def _fake_vector(i=0):
    return [(float(idx + i) / 1024.0) % 1.0 for idx in range(EMBEDDING_DIM)]





def _temp_db_paths():
    f1 = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    p1 = f1.name
    f1.close()
    try:
        f2 = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        p2 = f2.name
        f2.close()
        return p1, p2
    except Exception:
        try:
            os.unlink(p1)
        except OSError:
            pass
        raise


def _populate_cache(cache, records):
    """Populate an EmbeddingCache with (req_id, text, vector) tuples."""
    for req_id, text, vec in records:
        h = EmbeddingCache.text_hash(text)
        cache.store_vector(req_id, h, vec)


# ── cosine_similarity tests ──────────────────────────────────────────────────


class TestCosineSimilarity:

    def test_identical_vectors(self):
        v = _fake_vector(0)
        assert math.isclose(cosine_similarity(v, v), 1.0, rel_tol=1e-6)

    def test_orthogonal_vectors(self):
        v1 = [1.0] + [0.0] * (EMBEDDING_DIM - 1)
        v2 = [0.0] + [1.0] + [0.0] * (EMBEDDING_DIM - 2)
        result = cosine_similarity(v1, v2)
        assert math.isclose(result, 0.0, abs_tol=1e-6)

    def test_known_nontrivial_values(self):
        # Two 2D vectors separated by 45 degrees: similarity is 1 / sqrt(2) ≈ 0.7071
        v1 = [1.0, 0.0] + [0.0] * (EMBEDDING_DIM - 2)
        v2 = [1.0, 1.0] + [0.0] * (EMBEDDING_DIM - 2)
        result = cosine_similarity(v1, v2)
        assert math.isclose(result, 1.0 / math.sqrt(2.0), rel_tol=1e-6)

    def test_zero_norm_vectors(self):
        v_zero = [0.0] * EMBEDDING_DIM
        v = _fake_vector(0)
        assert cosine_similarity(v_zero, v) == 0.0
        assert cosine_similarity(v, v_zero) == 0.0
        assert cosine_similarity(v_zero, v_zero) == 0.0


# ── EmbeddingCache extension tests ───────────────────────────────────────────


class TestEmbeddingCacheExtensions:

    def test_get_vector_returns_stored_vector(self):
        with EmbeddingCache(":memory:", "test") as cache:
            vec = _fake_vector(42)
            cache.store_vector("R1", EmbeddingCache.text_hash("text"), vec)
            retrieved = cache.get_vector("R1")
            assert retrieved is not None
            assert len(retrieved) == EMBEDDING_DIM
            for a, b in zip(retrieved, vec):
                assert abs(a - b) < 1e-6

    def test_get_vector_returns_none_for_missing(self):
        with EmbeddingCache(":memory:", "test") as cache:
            assert cache.get_vector("R999") is None

    def test_iter_all_vectors_yields_all(self):
        with EmbeddingCache(":memory:", "test") as cache:
            expected = {}
            for i in range(5):
                rid = f"R{i}"
                vec = _fake_vector(i)
                expected[rid] = vec
                cache.store_vector(rid, EmbeddingCache.text_hash(f"t{i}"), vec)

            seen = dict(cache.iter_all_vectors())
            assert len(seen) == len(expected)
            for rid, vec in expected.items():
                assert rid in seen
                for a, b in zip(seen[rid], vec):
                    assert abs(a - b) < 1e-6

    def test_iter_all_vectors_empty_db(self):
        with EmbeddingCache(":memory:", "test") as cache:
            assert list(cache.iter_all_vectors()) == []


# ── Centroid computation tests ───────────────────────────────────────────────


class TestCentroidComputation:

    def test_single_vector_centroid(self):
        v = _fake_vector(0)
        result = _compute_centroid([v])
        for a, b in zip(result, v):
            assert abs(a - b) < 1e-6

    def test_two_vectors_centroid(self):
        v1 = [1.0] * EMBEDDING_DIM
        v2 = [3.0] * EMBEDDING_DIM
        result = _compute_centroid([v1, v2])
        assert all(abs(x - 2.0) < 1e-6 for x in result)

    def test_empty_vectors_returns_zero_centroid(self):
        result = _compute_centroid([])
        assert len(result) == EMBEDDING_DIM
        assert all(x == 0.0 for x in result)

    def test_collect_asr_vectors_filters_missing(self):
        with EmbeddingCache(":memory:", "test") as cache:
            v1 = _fake_vector(0)
            cache.store_vector("R1", EmbeddingCache.text_hash("t1"), v1)
            # R2 not in cache

            vectors, ids, records = _collect_asr_vectors(
                [{"id": "R1"}, {"id": "R2"}], cache
            )
            assert len(vectors) == 1
            assert ids == ["R1"]
            assert len(records) == 1

    def test_collect_asr_vectors_with_missing_id_key(self):
        with EmbeddingCache(":memory:", "test") as cache:
            vectors, ids, records = _collect_asr_vectors(
                [{"no_id": True}], cache
            )
            assert vectors == []
            assert ids == []


# ── Non-ASR candidate selection tests ────────────────────────────────────────


class TestSelectNonAsrCandidates:

    def test_all_above_threshold(self):
        with EmbeddingCache(":memory:", "test") as cache:
            centroid = [1.0] * EMBEDDING_DIM
            # All non-ASRs point same direction as centroid → high similarity
            for i in range(5):
                vec = [1.0 + i * 0.001] * EMBEDDING_DIM
                cache.store_vector(f"RN{i}", EmbeddingCache.text_hash(f"t{i}"), vec)

            ids, scores = _select_non_asr_candidates(
                centroid, cache, 0.0, MAX_NON_ASR_PER_BATCH
            )
            assert len(ids) == 5

    def test_all_below_threshold(self):
        with EmbeddingCache(":memory:", "test") as cache:
            centroid = [1.0] * EMBEDDING_DIM
            # All non-ASRs point opposite → ~-1 cosine similarity
            for i in range(3):
                vec = [-1.0] * EMBEDDING_DIM
                cache.store_vector(f"RN{i}", EmbeddingCache.text_hash(f"t{i}"), vec)

            ids, scores = _select_non_asr_candidates(
                centroid, cache, NON_ASR_SIMILARITY_THRESHOLD, MAX_NON_ASR_PER_BATCH
            )
            assert len(ids) == 0

    def test_mixed_above_below_sorted_descending(self):
        with EmbeddingCache(":memory:", "test") as cache:
            centroid = _fake_vector(0)
            # Same direction as centroid → cosine ≈ 1.0
            v_high = [x * 1.1 for x in centroid]
            # Different direction → lower similarity
            v_mid = _fake_vector(500)
            # Opposite direction → negative cosine
            v_low = [-x for x in centroid]

            cache.store_vector("RN_high", EmbeddingCache.text_hash("h"), v_high)
            cache.store_vector("RN_mid", EmbeddingCache.text_hash("m"), v_mid)
            cache.store_vector("RN_low", EmbeddingCache.text_hash("l"), v_low)

            ids, scores = _select_non_asr_candidates(
                centroid, cache, 0.1, MAX_NON_ASR_PER_BATCH
            )
            assert len(ids) >= 2
            assert "RN_high" in ids
            assert "RN_mid" in ids
            assert "RN_low" not in ids
            assert ids[0] == "RN_high"
            assert ids[1] == "RN_mid"
            assert scores["RN_high"] > scores["RN_mid"]

    def test_capped_at_max(self):
        with EmbeddingCache(":memory:", "test") as cache:
            centroid = [1.0] * EMBEDDING_DIM
            for i in range(15):
                cache.store_vector(f"RN{i}", EmbeddingCache.text_hash(f"t{i}"), [2.0] * EMBEDDING_DIM)

            ids, _ = _select_non_asr_candidates(
                centroid, cache, 0.0, MAX_NON_ASR_PER_BATCH
            )
            assert len(ids) == MAX_NON_ASR_PER_BATCH

    def test_empty_cache_returns_empty(self):
        with EmbeddingCache(":memory:", "test") as cache:
            centroid = [1.0] * EMBEDDING_DIM
            ids, scores = _select_non_asr_candidates(
                centroid, cache, 0.5, MAX_NON_ASR_PER_BATCH
            )
            assert ids == []
            assert scores == {}


# ── Batch assembly tests ─────────────────────────────────────────────────────


class TestBuildSingleBatch:

    def test_batch_dict_has_all_keys(self):
        with EmbeddingCache(":memory:", "test") as asr_cache, \
             EmbeddingCache(":memory:", "test") as non_asr_cache:

            asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), _fake_vector(0))
            non_asr_cache.store_vector("RN1", EmbeddingCache.text_hash("b"), _fake_vector(0))

            group = {
                "cluster": 0,
                "requirements": [{"id": "R1", "description": "auth"}],
            }
            non_asr_lookup = {"RN1": {"id": "RN1", "description": "log"}}

            batch = _build_single_batch(group, 0, asr_cache, non_asr_cache, non_asr_lookup)
            assert "group_id" in batch
            assert "centroid" in batch
            assert "asr_ids" in batch
            assert "asr_records" in batch
            assert "non_asr_ids" in batch
            assert "non_asr_records" in batch
            assert "similarity_scores" in batch
            assert batch["group_id"] == "cluster_0_group_0"
            assert len(batch["centroid"]) == EMBEDDING_DIM

    def test_empty_group_produces_batch(self):
        with EmbeddingCache(":memory:", "test") as asr_cache, \
             EmbeddingCache(":memory:", "test") as non_asr_cache:

            group = {"requirements": []}
            batch = _build_single_batch(group, 0, asr_cache, non_asr_cache, {})
            assert batch["asr_ids"] == []
            assert batch["non_asr_ids"] == []
            assert all(c == 0.0 for c in batch["centroid"])


# ── build_batches node tests ─────────────────────────────────────────────────


class TestBuildBatchesNode:

    def test_single_condition_group(self):
        asr_db, non_asr_db = _temp_db_paths()
        try:
            # Populate caches
            with EmbeddingCache(asr_db, "test") as asr_cache, \
                 EmbeddingCache(non_asr_db, "test") as non_asr_cache:

                asr_cache.store_vector("R1", EmbeddingCache.text_hash("auth"), _fake_vector(0))
                asr_cache.store_vector("R2", EmbeddingCache.text_hash("log"), _fake_vector(1))
                non_asr_cache.store_vector("RN1", EmbeddingCache.text_hash("perf"), _fake_vector(0))

            state = _make_state(
                condition_groups=[{
                    "cluster": 0,
                    "requirements": [
                        {"id": "R1", "description": "Authenticate users"},
                        {"id": "R2", "description": "Log all access"},
                    ],
                }],
                normalized_non_asr=[
                    {"id": "RN1", "description": "Performance monitoring"},
                ],
            )

            result = build_batches(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            assert "batches" in result
            assert len(result["batches"]) == 1
            b = result["batches"][0]
            assert b["group_id"] == "cluster_0_group_0"
            assert b["asr_ids"] == ["R1", "R2"]
            assert len(b["centroid"]) == EMBEDDING_DIM
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_multiple_condition_groups(self):
        asr_db, non_asr_db = _temp_db_paths()
        try:
            with EmbeddingCache(asr_db, "test") as asr_cache, \
                 EmbeddingCache(non_asr_db, "test") as non_asr_cache:

                for gid in [0, 1]:
                    asr_cache.store_vector(f"R{gid}", EmbeddingCache.text_hash(f"a{gid}"), _fake_vector(gid))
                non_asr_cache.store_vector("RN1", EmbeddingCache.text_hash("n"), _fake_vector(0))

            state = _make_state(
                condition_groups=[
                    {"cluster": 0, "requirements": [{"id": "R0"}]},
                    {"cluster": 1, "requirements": [{"id": "R1"}]},
                ],
                normalized_non_asr=[{"id": "RN1", "description": "perf"}],
            )

            result = build_batches(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            assert len(result["batches"]) == 2
            assert result["batches"][0]["group_id"] == "cluster_0_group_0"
            assert result["batches"][1]["group_id"] == "cluster_1_group_0"
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_missing_asr_vector_excluded(self):
        asr_db, non_asr_db = _temp_db_paths()
        try:
            with EmbeddingCache(asr_db, "test") as asr_cache:
                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), _fake_vector(0))
                # R2 not stored
            with EmbeddingCache(non_asr_db, "test"):
                pass

            state = _make_state(
                condition_groups=[{
                    "cluster": 0,
                    "requirements": [{"id": "R1"}, {"id": "R2"}],
                }],
            )

            result = build_batches(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            b = result["batches"][0]
            assert b["asr_ids"] == ["R1"]  # R2 excluded
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_config_missing_keys_raises(self):
        with pytest.raises(KeyError, match="asr_db_path"):
            build_batches(_make_state(), {"configurable": {}})

    def test_no_condition_groups_produces_empty_batches(self):
        result = build_batches(
            _make_state(condition_groups=[]),
            _make_config(),
        )
        assert result["batches"] == []

    def test_batch_respects_similarity_threshold(self):
        asr_db, non_asr_db = _temp_db_paths()
        try:
            with EmbeddingCache(asr_db, "test") as asr_cache, \
                 EmbeddingCache(non_asr_db, "test") as non_asr_cache:

                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), [1.0] * EMBEDDING_DIM)
                # High similarity non-ASR
                non_asr_cache.store_vector("RN_near", EmbeddingCache.text_hash("n"), [0.9] * EMBEDDING_DIM)
                # Low similarity non-ASR (opposite direction)
                non_asr_cache.store_vector("RN_far", EmbeddingCache.text_hash("f"), [-1.0] * EMBEDDING_DIM)

            state = _make_state(
                condition_groups=[{"cluster": 0, "requirements": [{"id": "R1"}]}],
                normalized_non_asr=[
                    {"id": "RN_near", "description": "near"},
                    {"id": "RN_far", "description": "far"},
                ],
            )

            result = build_batches(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            b = result["batches"][0]
            assert "RN_near" in b["non_asr_ids"]
            assert "RN_far" not in b["non_asr_ids"]
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)
