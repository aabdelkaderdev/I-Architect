"""
Unit tests for overlap bridging node (FR-4).

Covers:
- Shared cluster detection
- Centroid similarity detection
- Bridge injection with hard cap
- Bridge record shape
- No-related-pairs no-op
- Missing config key raises KeyError
"""
from __future__ import annotations

import math
import os
import tempfile

import pytest

from raa.utils.constants import EMBEDDING_DIM, MAX_BRIDGE_REQUIREMENTS, NON_ASR_SIMILARITY_THRESHOLD
from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity
from raa.nodes.overlap_bridging import bridge_overlaps


# ── Helpers ──────────────────────────────────────────────────────────────────


def _fake_vector(i=0):
    return [(float(idx + i) / 1024.0) % 1.0 for idx in range(EMBEDDING_DIM)]


def _make_config(**overrides):
    return {
        "configurable": {
            "thread_id": "test-thread-1",
            "non_asr_db_path": ":memory:",
            **overrides,
        }
    }


def _make_state(batches=None, normalized_non_asr=None):
    return {
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "quality_weights": {},
        "review_mode": "autonomous",
        "normalized_asrs": [],
        "normalized_non_asr": normalized_non_asr or [],
        "embeddings_ready": True,
        "batches": batches or [],
        "batch_outputs": [],
        "open_questions": [],
        "incoherent_batches": [],
        "batch_cursor": 0,
    }


def _temp_db_path():
    f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    p = f.name
    f.close()
    return p


def _make_batch(group_id, centroid_seed=0, asr_ids=None, non_asr_ids=None,
                asr_records=None, non_asr_records=None, similarity_scores=None):
    return {
        "group_id": group_id,
        "centroid": _fake_vector(centroid_seed),
        "asr_ids": asr_ids or [],
        "asr_records": asr_records or [],
        "non_asr_ids": non_asr_ids or [],
        "non_asr_records": non_asr_records or [],
        "similarity_scores": similarity_scores or {},
    }


# ── Tests ────────────────────────────────────────────────────────────────────


class TestOverlapBridging:

    def test_shared_cluster_detection(self):
        """Batches with same cluster ID are detected as related."""
        db = _temp_db_path()
        try:
            with EmbeddingCache(db, "test") as cache:
                # Pre-populate with a bridge candidate
                vec = _fake_vector(0)
                cache.store_vector("RN_bridge", EmbeddingCache.text_hash("b"), vec)

            state = _make_state(
                batches=[
                    _make_batch("cluster_0_group_0", centroid_seed=0),
                    _make_batch("cluster_0_group_1", centroid_seed=1),
                ],
                normalized_non_asr=[
                    {"id": "RN_bridge", "description": "shared concern"},
                ],
            )

            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            assert "batches" in result
            assert "bridge_requirements" in result
            # At least one bridge record should exist if a candidate qualifies
        finally:
            os.unlink(db)

    def test_centroid_similarity_detection(self):
        """Different clusters but similar centroids are detected."""
        db = _temp_db_path()
        try:
            # Create nearly identical centroids for different clusters
            centroid = _fake_vector(0)
            # A bridge candidate similar to both centroids
            bridge_vec = [x * 1.01 for x in centroid]

            with EmbeddingCache(db, "test") as cache:
                cache.store_vector("RN_bridge", EmbeddingCache.text_hash("b"), bridge_vec)

            state = _make_state(
                batches=[
                    _make_batch("cluster_0_group_0", centroid_seed=0),
                    _make_batch("cluster_1_group_0", centroid_seed=0),  # same centroid
                ],
                normalized_non_asr=[
                    {"id": "RN_bridge", "description": "shared concern"},
                ],
            )

            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            # Same centroid → similarity ≈ 1.0 → should detect as centroid_similarity
            assert len(result["bridge_requirements"]) >= 1
        finally:
            os.unlink(db)

    def test_bridge_hard_cap(self):
        """At most MAX_BRIDGE_REQUIREMENTS injected per pair."""
        db = _temp_db_path()
        try:
            centroid = _fake_vector(0)
            # Store many qualifying candidates
            with EmbeddingCache(db, "test") as cache:
                for i in range(10):
                    vec = [x * (1.0 + i * 0.001) for x in centroid]
                    cache.store_vector(f"RN{i}", EmbeddingCache.text_hash(f"t{i}"), vec)

            state = _make_state(
                batches=[
                    _make_batch("cluster_0_group_0", centroid_seed=0),
                    _make_batch("cluster_0_group_1", centroid_seed=0),
                ],
                normalized_non_asr=[
                    {"id": f"RN{i}", "description": f"desc {i}"} for i in range(10)
                ],
            )

            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            assert len(result["bridge_requirements"]) <= MAX_BRIDGE_REQUIREMENTS
        finally:
            os.unlink(db)

    def test_injected_ids_in_both_batches(self):
        """Bridge IDs appear in both batches and bridge_requirements."""
        db = _temp_db_path()
        try:
            centroid = _fake_vector(0)
            bridge_vec = _fake_vector(0)

            with EmbeddingCache(db, "test") as cache:
                cache.store_vector("RN_shared", EmbeddingCache.text_hash("s"), bridge_vec)

            state = _make_state(
                batches=[
                    _make_batch("cluster_0_group_0", centroid_seed=0),
                    _make_batch("cluster_0_group_1", centroid_seed=0),
                ],
                normalized_non_asr=[
                    {"id": "RN_shared", "description": "shared"},
                ],
            )

            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            br = result["bridge_requirements"]
            assert len(br) >= 1
            assert br[0]["requirement_id"] == "RN_shared"
            assert br[0]["batch_ids"] == ["cluster_0_group_0", "cluster_0_group_1"]
            # Both batches have the bridge ID
            b0 = result["batches"][0]
            b1 = result["batches"][1]
            assert "RN_shared" in b0["non_asr_ids"]
            assert "RN_shared" in b1["non_asr_ids"]
            assert "RN_shared" in b0["bridge_ids"]
            assert "RN_shared" in b1["bridge_ids"]
        finally:
            os.unlink(db)

    def test_no_related_pairs_returns_unchanged(self):
        """Unrelated batches pass through unchanged with empty bridge list."""
        db = _temp_db_path()
        try:
            with EmbeddingCache(db, "test") as cache:
                cache.store_vector("RN1", EmbeddingCache.text_hash("x"), _fake_vector(0))

            state = _make_state(
                batches=[
                    _make_batch("cluster_0_group_0", centroid_seed=0),
                    # Far centroid (orthogonal-ish)
                    _make_batch("cluster_1_group_0", centroid_seed=500),
                ],
                normalized_non_asr=[
                    {"id": "RN1", "description": "x"},
                ],
            )

            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            assert result["bridge_requirements"] == []
            # Batches are returned (same count)
            assert len(result["batches"]) == 2
        finally:
            os.unlink(db)

    def test_missing_non_asr_db_path_raises(self):
        state = _make_state(batches=[_make_batch("cluster_0_group_0")])
        with pytest.raises(KeyError, match="non_asr_db_path"):
            bridge_overlaps(state, {"configurable": {}})

    def test_missing_configurable_raises(self):
        state = _make_state()
        with pytest.raises(KeyError, match="configurable"):
            bridge_overlaps(state, {})

    def test_empty_batches_returns_empty(self):
        state = _make_state(batches=[])
        result = bridge_overlaps(state, _make_config())
        assert result["batches"] == []
        assert result["bridge_requirements"] == []

    def test_no_candidate_qualifies_returns_no_bridges(self):
        """When no non-ASR candidate scores above threshold for both centroids."""
        db = _temp_db_path()
        try:
            # Candidate near centroid_a but far from centroid_b
            centroid_a = _fake_vector(0)
            centroid_b = _fake_vector(500)  # different

            near_a = _fake_vector(0)   # similar to a
            # far from b by design

            with EmbeddingCache(db, "test") as cache:
                cache.store_vector("RN_only_a", EmbeddingCache.text_hash("a"), near_a)

            state = _make_state(
                batches=[
                    _make_batch("cluster_0_group_0", centroid_seed=0),
                    _make_batch("cluster_0_group_1", centroid_seed=500),
                ],
                normalized_non_asr=[
                    {"id": "RN_only_a", "description": "only near a"},
                ],
            )

            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            assert result["bridge_requirements"] == []
        finally:
            os.unlink(db)

    def test_bridge_requirements_has_correct_shape(self):
        """Each bridge record has requirement_id, batch_ids, similarity_scores, reason."""
        db = _temp_db_path()
        try:
            centroid = _fake_vector(0)
            bridge_vec = _fake_vector(0)

            with EmbeddingCache(db, "test") as cache:
                cache.store_vector("RN_shape", EmbeddingCache.text_hash("s"), bridge_vec)

            state = _make_state(
                batches=[
                    _make_batch("cluster_0_group_0", centroid_seed=0),
                    _make_batch("cluster_0_group_1", centroid_seed=0),
                ],
                normalized_non_asr=[
                    {"id": "RN_shape", "description": "shape test"},
                ],
            )

            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            br = result["bridge_requirements"][0]
            assert "requirement_id" in br
            assert "batch_ids" in br
            assert "similarity_scores" in br
            assert "reason" in br
            assert br["reason"] in ("shared_cluster", "centroid_similarity")
        finally:
            os.unlink(db)

    def test_batches_not_mutated_in_place(self):
        """Original input batch objects are not mutated."""
        db = _temp_db_path()
        try:
            centroid = _fake_vector(0)
            bridge_vec = _fake_vector(0)

            with EmbeddingCache(db, "test") as cache:
                cache.store_vector("RN_no_mut", EmbeddingCache.text_hash("m"), bridge_vec)

            orig_batch = _make_batch("cluster_0_group_0", centroid_seed=0)
            state = _make_state(
                batches=[orig_batch, _make_batch("cluster_0_group_1", centroid_seed=0)],
                normalized_non_asr=[
                    {"id": "RN_no_mut", "description": "no mutate"},
                ],
            )

            orig_non_asr_ids = list(orig_batch["non_asr_ids"])
            result = bridge_overlaps(state, _make_config(non_asr_db_path=db))
            # Original batch unchanged
            assert orig_batch["non_asr_ids"] == orig_non_asr_ids
            # Result batch has new IDs
            assert len(result["batches"][0]["non_asr_ids"]) > len(orig_non_asr_ids)
        finally:
            os.unlink(db)
