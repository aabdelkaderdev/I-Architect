"""
Unit tests for coherence gating node (FR-5).

Covers:
- Coherent batch scoring
- Empty-vector batch fallback
- Successful two-way split
- Unsplittable batch fallback
- Incoherent batch metadata
- No input mutation
"""
from __future__ import annotations

import math
import os
import tempfile

import pytest

from raa.utils.constants import COHERENCE_THRESHOLD, EMBEDDING_DIM
from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity
from raa.nodes.coherence_gate import gate_batch_coherence


# ── Helpers ──────────────────────────────────────────────────────────────────


def _fake_vector(i=0):
    return [(float(idx + i) / 1024.0) % 1.0 for idx in range(EMBEDDING_DIM)]


def _make_config(**overrides):
    return {
        "configurable": {
            "thread_id": "test-thread-1",
            "asr_db_path": ":memory:",
            "non_asr_db_path": ":memory:",
            **overrides,
        }
    }


def _make_state(batches=None):
    return {
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "quality_weights": {},
        "review_mode": "autonomous",
        "normalized_asrs": [],
        "normalized_non_asr": [],
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


class TestCoherenceGate:

    def test_coherent_batch_gets_score_and_not_reduced(self):
        """Batch with vectors all similar to centroid passes coherence."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            centroid = _fake_vector(0)
            # Store ASR vectors identical to centroid → perfect coherence
            with EmbeddingCache(asr_db, "test") as asr_cache:
                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), centroid)
                asr_cache.store_vector("R2", EmbeddingCache.text_hash("b"), centroid)
            with EmbeddingCache(non_asr_db, "test"):
                pass

            state = _make_state(batches=[
                _make_batch("cluster_0_group_0", centroid_seed=0,
                           asr_ids=["R1", "R2"],
                           asr_records=[{"id": "R1"}, {"id": "R2"}]),
            ])

            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            assert len(result["batches"]) == 1
            b = result["batches"][0]
            assert "coherence_score" in b
            assert b["coherence_score"] >= COHERENCE_THRESHOLD
            assert b["reduced_confidence"] is False
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_empty_vector_batch_gets_zero_score(self):
        """Batch with no vectors in cache gets coherence_score = 0.0."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            with EmbeddingCache(asr_db, "test"):
                pass
            with EmbeddingCache(non_asr_db, "test"):
                pass

            state = _make_state(batches=[
                _make_batch("cluster_0_group_0", asr_ids=["R_missing"]),
            ])

            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            b = result["batches"][0]
            assert b["coherence_score"] == 0.0
            assert b["reduced_confidence"] is True
            assert len(result["incoherent_batches"]) >= 1
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_split_succeeds_replaces_batch(self):
        """Low-coherence batch with separable vectors is replaced by two sub-batches."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            # Opposite vectors → centroid at origin → coherence = 0.0 → split triggered
            v_pos = [1.0] * EMBEDDING_DIM
            v_neg = [-1.0] * EMBEDDING_DIM
            zero_centroid = [0.0] * EMBEDDING_DIM

            with EmbeddingCache(asr_db, "test") as asr_cache:
                asr_cache.store_vector("R_pos", EmbeddingCache.text_hash("p"), v_pos)
                asr_cache.store_vector("R_neg", EmbeddingCache.text_hash("n"), v_neg)
            with EmbeddingCache(non_asr_db, "test"):
                pass

            state = _make_state(batches=[{
                "group_id": "cluster_0_group_0",
                "centroid": zero_centroid,
                "asr_ids": ["R_pos", "R_neg"],
                "asr_records": [{"id": "R_pos"}, {"id": "R_neg"}],
                "non_asr_ids": [],
                "non_asr_records": [],
                "similarity_scores": {},
            }])

            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            # Should split into two sub-batches
            assert len(result["batches"]) == 2
            b0, b1 = result["batches"]
            assert b0["source_group_id"] == "cluster_0_group_0"
            assert b1["source_group_id"] == "cluster_0_group_0"
            assert b0["group_id"] != b1["group_id"]
            assert b0["reduced_confidence"] is False
            assert b1["reduced_confidence"] is False
            assert b0["coherence_score"] >= COHERENCE_THRESHOLD
            assert b1["coherence_score"] >= COHERENCE_THRESHOLD
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_unsplittable_batch_gets_reduced_confidence(self):
        """Single-vector batch below threshold cannot split."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            v = [1.0] * EMBEDDING_DIM
            with EmbeddingCache(asr_db, "test") as asr_cache:
                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), v)
            with EmbeddingCache(non_asr_db, "test"):
                pass

            # Centroid opposite to the only vector → low coherence, but only 1 entry → can't split
            far_centroid = [-1.0] * EMBEDDING_DIM

            state = _make_state(batches=[{
                "group_id": "cluster_0_group_0",
                "centroid": far_centroid,
                "asr_ids": ["R1"],
                "asr_records": [{"id": "R1"}],
                "non_asr_ids": [],
                "non_asr_records": [],
                "similarity_scores": {},
            }])

            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            assert len(result["batches"]) == 1
            b = result["batches"][0]
            assert b["reduced_confidence"] is True
            assert len(result["incoherent_batches"]) >= 1
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_incoherent_batches_has_metadata(self):
        """Incoherent batch record contains group_id, score, and reason."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            with EmbeddingCache(asr_db, "test"):
                pass
            with EmbeddingCache(non_asr_db, "test"):
                pass

            state = _make_state(batches=[
                _make_batch("cluster_0_group_0", asr_ids=["R_missing"]),
            ])

            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            ib = result["incoherent_batches"][0]
            assert "group_id" in ib
            assert ib["group_id"] == "cluster_0_group_0"
            assert "coherence_score" in ib
            assert "reason" in ib
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_no_mutation_of_input_batches(self):
        """Original input batch objects are not mutated in place."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            centroid = _fake_vector(0)
            with EmbeddingCache(asr_db, "test") as asr_cache:
                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), centroid)
            with EmbeddingCache(non_asr_db, "test"):
                pass

            orig = _make_batch("cluster_0_group_0", centroid_seed=0,
                              asr_ids=["R1"], asr_records=[{"id": "R1"}])
            state = _make_state(batches=[orig])

            orig_keys = set(orig.keys())
            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            # Original should not gain coherence_score or reduced_confidence
            assert "coherence_score" not in orig
            assert "reduced_confidence" not in orig
            # Result batches have the new fields
            assert "coherence_score" in result["batches"][0]
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_sub_batch_split_has_coherence_score(self):
        """Sub-batches from successful split both have their own coherence_score and reduced_confidence."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            # Opposite vectors → zero centroid → coherence = 0.0 → split triggered
            v_pos = [1.0] * EMBEDDING_DIM
            v_neg = [-1.0] * EMBEDDING_DIM
            zero_centroid = [0.0] * EMBEDDING_DIM

            with EmbeddingCache(asr_db, "test") as asr_cache:
                asr_cache.store_vector("R_pos", EmbeddingCache.text_hash("p"), v_pos)
                asr_cache.store_vector("R_neg", EmbeddingCache.text_hash("n"), v_neg)
            with EmbeddingCache(non_asr_db, "test"):
                pass

            state = _make_state(batches=[{
                "group_id": "cluster_0_group_0",
                "centroid": zero_centroid,
                "asr_ids": ["R_pos", "R_neg"],
                "asr_records": [{"id": "R_pos"}, {"id": "R_neg"}],
                "non_asr_ids": [],
                "non_asr_records": [],
                "similarity_scores": {},
            }])

            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            for b in result["batches"]:
                assert "coherence_score" in b
                assert "reduced_confidence" in b
                assert b["reduced_confidence"] is False
                assert b["coherence_score"] >= COHERENCE_THRESHOLD
                assert b["source_group_id"] == "cluster_0_group_0"
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_missing_config_keys_raises(self):
        state = _make_state(batches=[_make_batch("g0")])
        with pytest.raises(KeyError, match="asr_db_path"):
            gate_batch_coherence(state, {"configurable": {}})

    def test_empty_batches_returns_empty(self):
        state = _make_state(batches=[])
        result = gate_batch_coherence(state, _make_config())
        assert result["batches"] == []
        assert result["incoherent_batches"] == []

    def test_preserves_bridge_ids(self):
        """Bridge IDs from overlap bridging are preserved in gated batches."""
        asr_db = _temp_db_path()
        non_asr_db = _temp_db_path()
        try:
            centroid = _fake_vector(0)
            with EmbeddingCache(asr_db, "test") as asr_cache:
                asr_cache.store_vector("R1", EmbeddingCache.text_hash("a"), centroid)
            with EmbeddingCache(non_asr_db, "test"):
                pass

            state = _make_state(batches=[{
                "group_id": "cluster_0_group_0",
                "centroid": centroid,
                "asr_ids": ["R1"],
                "asr_records": [{"id": "R1"}],
                "non_asr_ids": [],
                "non_asr_records": [],
                "similarity_scores": {},
                "bridge_ids": ["RN_bridge_1", "RN_bridge_2"],
            }])

            result = gate_batch_coherence(state, _make_config(
                asr_db_path=asr_db, non_asr_db_path=non_asr_db,
            ))
            b = result["batches"][0]
            assert "bridge_ids" in b
            assert b["bridge_ids"] == ["RN_bridge_1", "RN_bridge_2"]
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)
