"""
Unit tests for embedding cache and verification node (FR-2).

Covers:
- EmbeddingCache: roundtrip, hash determinism, upsert, stale cache, missing keys
- ModelNonExistentException: raised for absent model directory
- verify_embeddings: empty inputs, pre-cached, partial cache, all-new, stale,
  config path injection
"""
from __future__ import annotations

import hashlib
import os
import tempfile
import struct
from unittest.mock import MagicMock, patch

import pytest

from raa.utils.constants import EMBEDDING_DIM
from raa.utils.embedding_cache import (
    EmbeddingCache,
    ModelNonExistentException,
    _get_embedding_model,
    get_embedding_model,
    _reset_singleton,
)
from raa.nodes.preparation import verify_embeddings
from raa.state.schemas import RAAState


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_config(**overrides):
    return {
        "configurable": {
            "thread_id": "test-thread-1",
            "asr_db_path": ":memory:",
            "non_asr_db_path": ":memory:",
            "cache_dir": "/nonexistent-for-tests",
            **overrides,
        }
    }


def _make_state(asrs=None, non_asr=None):
    return {
        "requirements": {},
        "asrs": [],
        "non_asr": [],
        "condition_groups": [],
        "quality_weights": {},
        "review_mode": "autonomous",
        "normalized_asrs": asrs or [],
        "normalized_non_asr": non_asr or [],
        "embeddings_ready": False,
        "batch_outputs": [],
        "open_questions": [],
        "incoherent_batches": [],
        "batch_cursor": 0,
    }


def _fake_vector(i=0):
    """Deterministic pseudo-vector for testing."""
    return [(float(idx + i) / 1024.0) % 1.0 for idx in range(EMBEDDING_DIM)]


class FakeModel:
    """Mock FastEmbed TextEmbedding — returns deterministic vectors."""

    def __init__(self):
        self.call_count = 0
        self.total_texts_embedded = 0

    def embed(self, texts):
        self.call_count += 1
        results = []
        for _ in texts:
            self.total_texts_embedded += 1
            results.append(_fake_vector(self.total_texts_embedded))
        return results


def _temp_db_paths():
    """Create two temp SQLite DB files and return (asr_path, non_asr_path)."""
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


# ── EmbeddingCache unit tests ────────────────────────────────────────────────


class TestEmbeddingCache:

    def test_text_hash_is_deterministic(self):
        h1 = EmbeddingCache.text_hash("hello world")
        h2 = EmbeddingCache.text_hash("hello world")
        assert h1 == h2
        assert len(h1) == 64

    def test_text_hash_differs_for_different_text(self):
        assert EmbeddingCache.text_hash("hello") != EmbeddingCache.text_hash("world")

    def test_text_hash_empty_string(self):
        h = EmbeddingCache.text_hash("")
        assert h == hashlib.sha256(b"").hexdigest()

    def test_cache_db_path_property(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            assert cache.db_path == ":memory:"

    def test_store_and_retrieve_roundtrip(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            vec = _fake_vector(0)
            h = EmbeddingCache.text_hash("requirement text")
            cache.store_vector("R1", h, vec)
            retrieved = cache.get_cached_vector("R1", h)
            assert retrieved is not None
            assert len(retrieved) == EMBEDDING_DIM
            for a, b in zip(retrieved, vec):
                assert abs(a - b) < 1e-6

    def test_get_none_for_missing_req_id(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            assert cache.get_cached_vector("R999", EmbeddingCache.text_hash("text")) is None

    def test_get_none_for_mismatched_hash(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            vec = _fake_vector(0)
            cache.store_vector("R1", EmbeddingCache.text_hash("original"), vec)
            assert cache.get_cached_vector("R1", EmbeddingCache.text_hash("modified")) is None

    def test_upsert_replaces_existing_row(self):
        db_path, _ = _temp_db_paths()
        try:
            with EmbeddingCache(db_path, "test-model") as cache:
                vec1 = _fake_vector(0)
                vec2 = _fake_vector(100)
                h1 = EmbeddingCache.text_hash("text v1")
                h2 = EmbeddingCache.text_hash("text v2")

                cache.store_vector("R1", h1, vec1)
                cache.store_vector("R1", h2, vec2)

                assert cache.get_cached_vector("R1", h1) is None
                retrieved = cache.get_cached_vector("R1", h2)
                assert retrieved is not None
                for a, b in zip(retrieved, vec2):
                    assert abs(a - b) < 1e-6

                # Only one row for R1
                row = cache._conn.execute(
                    "SELECT COUNT(*) FROM embeddings WHERE req_id = 'R1'"
                ).fetchone()
                assert row[0] == 1
        finally:
            os.unlink(db_path)

    def test_multiple_requirement_ids(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            for i in range(5):
                rid = f"R{i}"
                vec = _fake_vector(i)
                h = EmbeddingCache.text_hash(f"text {i}")
                cache.store_vector(rid, h, vec)

            for i in range(5):
                rid = f"R{i}"
                h = EmbeddingCache.text_hash(f"text {i}")
                retrieved = cache.get_cached_vector(rid, h)
                assert retrieved is not None, f"Missing {rid}"
                assert len(retrieved) == EMBEDDING_DIM

    def test_schema_persists_across_connections(self):
        db_path, _ = _temp_db_paths()
        try:
            with EmbeddingCache(db_path, "test-model") as cache1:
                vec = _fake_vector(42)
                h = EmbeddingCache.text_hash("persistent text")
                cache1.store_vector("R_PERSIST", h, vec)

            with EmbeddingCache(db_path, "test-model") as cache2:
                retrieved = cache2.get_cached_vector("R_PERSIST", h)
                assert retrieved is not None
                assert len(retrieved) == EMBEDDING_DIM
        finally:
            os.unlink(db_path)

    def test_store_vectors_batch(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            records = [
                ("R1", EmbeddingCache.text_hash("t1"), _fake_vector(1)),
                ("R2", EmbeddingCache.text_hash("t2"), _fake_vector(2)),
            ]
            cache.store_vectors(records)
            for rid, text, vec in [("R1", "t1", _fake_vector(1)), ("R2", "t2", _fake_vector(2))]:
                retrieved = cache.get_cached_vector(rid, EmbeddingCache.text_hash(text))
                assert retrieved is not None
                assert retrieved == vec

    def test_invalid_vector_dimension_raises(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            with pytest.raises(ValueError, match="Expected vector of length"):
                cache.store_vector("R1", "hash", [1.0, 2.0])
            with pytest.raises(ValueError, match="Expected vector of length"):
                cache.store_vectors([("R1", "hash", [1.0, 2.0])])

    def test_corrupt_blob_length_returns_none(self):
        with EmbeddingCache(":memory:", "test-model") as cache:
            # Manually insert corrupt short blob
            cache._conn.execute(
                "INSERT INTO embeddings (req_id, embedding, text_hash, model_name) VALUES (?, ?, ?, ?)",
                ("R1", struct.pack("<2f", 1.0, 2.0), "hash", "test-model")
            )
            cache._conn.commit()
            assert cache.get_cached_vector("R1", "hash") is None


# ── ModelNonExistentException tests ───────────────────────────────────────────


class TestModelNonExistentException:

    def test_exception_message_includes_cache_dir_and_model_name(self):
        with pytest.raises(ModelNonExistentException) as exc_info:
            _get_embedding_model("/tmp/does-not-exist", "some/model")
        msg = str(exc_info.value)
        assert "does-not-exist" in msg
        assert "some--model" in msg

    def test_exception_attributes(self):
        with pytest.raises(ModelNonExistentException) as exc_info:
            _get_embedding_model("/tmp/does-not-exist", "some/model")
        assert exc_info.value.cache_dir == "/tmp/does-not-exist"
        assert exc_info.value.model_name == "some/model"

    def test_no_exception_when_model_dir_exists(self, tmp_path):
        model_name = "test-model"
        model_dir = tmp_path / ("models--" + model_name.replace("/", "--"))
        model_dir.mkdir(parents=True)

        _reset_singleton()
        try:
            with patch("raa.utils.embedding_cache.TextEmbedding") as mock_te:
                mock_te.return_value = MagicMock()
                model = _get_embedding_model(str(tmp_path), model_name)
                assert model is not None
                mock_te.assert_called_once_with(
                    model_name=model_name,
                    cache_dir=str(tmp_path),
                )
        finally:
            _reset_singleton()


# ── verify_embeddings node tests ─────────────────────────────────────────────


class TestVerifyEmbeddings:

    def test_empty_inputs_returns_embeddings_ready(self):
        state = _make_state()
        with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
            mock_get.return_value = FakeModel()
            result = verify_embeddings(state, _make_config())
        assert result["embeddings_ready"] is True

    def test_embeds_new_asr_requirements(self):
        state = _make_state(
            asrs=[
                {"id": "R1", "condition_text": "The system shall authenticate users."},
                {"id": "R2", "condition_text": "The system shall log all access."},
            ],
        )
        with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
            fake = FakeModel()
            mock_get.return_value = fake
            result = verify_embeddings(state, _make_config())
        assert result["embeddings_ready"] is True
        assert fake.call_count == 1
        assert fake.total_texts_embedded == 2

    def test_embeds_new_non_asr_requirements(self):
        state = _make_state(
            non_asr=[
                {"id": "RN1", "description": "Performance monitoring requirement."},
                {"id": "RN2", "description": "Compliance audit requirement."},
            ],
        )
        with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
            fake = FakeModel()
            mock_get.return_value = fake
            result = verify_embeddings(state, _make_config())
        assert result["embeddings_ready"] is True
        assert fake.call_count == 1
        assert fake.total_texts_embedded == 2

    def test_skips_pre_cached_requirements(self):
        """Pre-populate cache → second run produces zero FastEmbed calls."""
        asr_db, non_asr_db = _temp_db_paths()
        try:
            state = _make_state(
                asrs=[
                    {"id": "R1", "condition_text": "already cached"},
                    {"id": "R2", "condition_text": "also cached"},
                ],
            )
            with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
                fake = FakeModel()
                mock_get.return_value = fake

                cfg = _make_config(asr_db_path=asr_db, non_asr_db_path=non_asr_db)
                r1 = verify_embeddings(state, cfg)
                assert r1["embeddings_ready"] is True
                assert fake.call_count == 1
                assert fake.total_texts_embedded == 2

                fake2 = FakeModel()
                mock_get.return_value = fake2
                r2 = verify_embeddings(state, cfg)
                assert r2["embeddings_ready"] is True
                assert fake2.call_count == 0
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_partial_cache_embeds_only_new(self):
        """Cached items skip; new/stale items get embedded."""
        asr_db, non_asr_db = _temp_db_paths()
        try:
            state = _make_state(
                asrs=[
                    {"id": "R1", "condition_text": "shared text"},
                    {"id": "R2", "condition_text": "unique to R2"},
                ],
            )
            with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
                cfg = _make_config(asr_db_path=asr_db, non_asr_db_path=non_asr_db)
                mock_get.return_value = FakeModel()
                verify_embeddings(state, cfg)

                # R1 unchanged, R2 changed → only R2 re-embeds
                state["normalized_asrs"] = [
                    {"id": "R1", "condition_text": "shared text"},
                    {"id": "R2", "condition_text": "updated text"},
                ]
                fake2 = FakeModel()
                mock_get.return_value = fake2
                verify_embeddings(state, cfg)
                assert fake2.call_count == 1
                assert fake2.total_texts_embedded == 1
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_stale_cache_re_embeds(self):
        """Text changed → hash mismatch triggers re-embed."""
        asr_db, non_asr_db = _temp_db_paths()
        try:
            state = _make_state(asrs=[{"id": "R1", "condition_text": "original text"}])
            with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
                cfg = _make_config(asr_db_path=asr_db, non_asr_db_path=non_asr_db)
                mock_get.return_value = FakeModel()
                verify_embeddings(state, cfg)

                state["normalized_asrs"] = [{"id": "R1", "condition_text": "modified text"}]
                fake2 = FakeModel()
                mock_get.return_value = fake2
                verify_embeddings(state, cfg)
                assert fake2.call_count == 1
                assert fake2.total_texts_embedded == 1
        finally:
            os.unlink(asr_db)
            os.unlink(non_asr_db)

    def test_null_condition_text_treated_as_empty(self):
        state = _make_state(asrs=[{"id": "R1", "condition_text": None}])
        with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
            fake = FakeModel()
            mock_get.return_value = fake
            result = verify_embeddings(state, _make_config())
        assert result["embeddings_ready"] is True
        assert fake.call_count == 1
        assert fake.total_texts_embedded == 1

    def test_db_paths_read_from_config(self):
        state = _make_state(asrs=[{"id": "R1", "condition_text": "test"}])
        with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
            mock_get.return_value = FakeModel()
            with patch("raa.utils.embedding_cache.EmbeddingCache") as mock_cache_cls:
                mock_cache = MagicMock()
                mock_cache.get_cached_vector.return_value = None
                mock_cache_cls.return_value = mock_cache

                cfg = _make_config(
                    asr_db_path="/custom/asr.db",
                    non_asr_db_path="/custom/non_asr.db",
                )
                verify_embeddings(state, cfg)

                calls = [c[0][0] for c in mock_cache_cls.call_args_list]
                assert "/custom/asr.db" in calls
                assert "/custom/non_asr.db" in calls

    def test_asr_and_non_asr_both_processed(self):
        state = _make_state(
            asrs=[{"id": "R1", "condition_text": "auth requirement"}],
            non_asr=[{"id": "RN1", "description": "logging requirement"}],
        )
        with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
            fake = FakeModel()
            mock_get.return_value = fake
            result = verify_embeddings(state, _make_config())
        assert result["embeddings_ready"] is True
        assert fake.call_count == 2
        assert fake.total_texts_embedded == 2

    def test_verify_embeddings_persists_verifiable_data(self):
        """all reqs embedded, all stored in DB and roundtrips successfully (AC 4.11)."""
        asr_db, non_asr_db = _temp_db_paths()
        try:
            state = _make_state(
                asrs=[{"id": "R1", "condition_text": "auth requirement"}],
                non_asr=[{"id": "RN1", "description": "logging requirement"}],
            )
            with patch("raa.utils.embedding_cache.get_embedding_model") as mock_get:
                fake = FakeModel()
                mock_get.return_value = fake
                cfg = _make_config(asr_db_path=asr_db, non_asr_db_path=non_asr_db)
                result = verify_embeddings(state, cfg)
                assert result["embeddings_ready"] is True
                assert fake.call_count == 2
                assert fake.total_texts_embedded == 2
                
                with EmbeddingCache(asr_db, "some/model") as cache:
                    vec = cache.get_cached_vector("R1", EmbeddingCache.text_hash("auth requirement"))
                    assert vec is not None
                    assert len(vec) == 1024
                    
                with EmbeddingCache(non_asr_db, "some/model") as cache:
                    vec = cache.get_cached_vector("RN1", EmbeddingCache.text_hash("logging requirement"))
                    assert vec is not None
                    assert len(vec) == 1024
        finally:
            if os.path.exists(asr_db):
                os.unlink(asr_db)
            if os.path.exists(non_asr_db):
                os.unlink(non_asr_db)
