"""Unit tests for raa/nodes/preparation.py — embedding readiness verification."""

import os
import sqlite3
import struct
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Constants (must match raa/nodes/preparation.py)
# ---------------------------------------------------------------------------
_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"
_EMBEDDING_DIM = 1024


# ---------------------------------------------------------------------------
# Fake embedding model
# ---------------------------------------------------------------------------
class FakeEmbeddingModel:
    """Returns deterministic 1024-dim vectors seeded from input text length."""

    def __init__(self):
        self.call_count = 0

    def embed(self, texts, **kwargs):
        self.call_count += len(texts)
        results = []
        for t in texts:
            seed = float(len(t) % 100)
            results.append([seed + i * 0.001 for i in range(_EMBEDDING_DIM)])
        return results


# ---------------------------------------------------------------------------
# SQLite helpers shared across tests
# ---------------------------------------------------------------------------
def _create_embeddings_schema(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS embeddings ("
        "  requirement_id INTEGER PRIMARY KEY,"
        "  embedding BLOB NOT NULL,"
        "  text_hash TEXT NOT NULL,"
        "  model_name TEXT NOT NULL"
        ")"
    )


def _wal_mode_enabled(conn):
    row = conn.execute("PRAGMA journal_mode").fetchone()
    return row[0].upper() == "WAL"


def _serialize_embedding(vector):
    return struct.pack(f"<{len(vector)}f", *vector)


def _hash_text(text):
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _insert_embedding(conn, req_id, text):
    """Insert a row using the fake model + sha256 hash."""
    model = FakeEmbeddingModel()
    vec = model.embed([text])[0]
    conn.execute(
        "INSERT OR REPLACE INTO embeddings (requirement_id, embedding, text_hash, model_name) VALUES (?, ?, ?, ?)",
        (req_id, _serialize_embedding(vec), _hash_text(text), _MODEL_NAME),
    )


def _make_embedding_db(db_path):
    """Create a fresh SQLite DB with WAL and embeddings table."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    _create_embeddings_schema(conn)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
SAMPLE_ASRS = [
    {"id": 1, "text": "The system shall authenticate users via OAuth 2.0"},
    {"id": 2, "text": "The system shall encrypt data at rest"},
    {"id": 3, "text": "The system shall support 10,000 concurrent users"},
]

SAMPLE_NON_ASRS = [
    {"id": "R10", "text": "The UI shall display a dashboard"},
    {"id": "R11", "text": "The system shall log all access events"},
    {"id": "R12", "text": "The admin panel shall support role-based access"},
]


def _make_raa_state(asrs=None, non_asr=None):
    """Build a minimal RAAState dict for tests."""
    return {
        "asrs": asrs or [],
        "non_asr": non_asr or [],
        "condition_groups": [],
        "quality_weights": {},
        "batch_queue": [],
        "batch_cursor": 0,
        "batch_outputs": {},
        "best_batch_output": {},
        "running_arch_model": None,
        "open_questions": [],
        "bridge_requirements": [],
        "incoherent_batches": [],
        "embeddings_ready": False,
    }


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------
def _run_tests():
    """Discover and run all test_ functions."""
    import inspect

    frame = inspect.currentframe()
    mod = inspect.getmodule(frame)
    tests = sorted(
        (name, obj) for name, obj in inspect.getmembers(sys.modules[__name__])
        if name.startswith("test_") and callable(obj)
    )
    passed = 0
    failed = 0
    for name, func in tests:
        try:
            func()
            print(f"  PASS {name}")
            passed += 1
        except Exception as e:
            import traceback
            print(f"  FAIL {name} — {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    return failed == 0


# ---------------------------------------------------------------------------
# Tests: ASR verification (T010-T012)
# ---------------------------------------------------------------------------
def test_missing_asr_db_raises_blocking_error():
    """T010: Missing asr_embeddings.db raises blocking error."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        missing_db = tmp_path / "nonexistent_asr.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(non_asr_db)

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=missing_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(asrs=SAMPLE_ASRS)
                    try:
                        prepare_embeddings(state)
                        raise AssertionError("Expected FileNotFoundError but no exception raised")
                    except FileNotFoundError:
                        pass  # expected


def test_missing_asr_row_raises_blocking_error():
    """T011: Missing ASR ID raises blocking error listing the ID."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(asr_db)
        _make_embedding_db(non_asr_db)

        # Populate asr_db with only requirement_id=1 and 2 — 3 is missing
        conn = sqlite3.connect(str(asr_db))
        _insert_embedding(conn, 1, SAMPLE_ASRS[0]["text"])
        _insert_embedding(conn, 2, SAMPLE_ASRS[1]["text"])
        conn.commit()
        conn.close()

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(asrs=SAMPLE_ASRS)
                    try:
                        prepare_embeddings(state)
                        raise AssertionError("Expected RuntimeError but no exception raised")
                    except RuntimeError as e:
                        err_msg = str(e).lower()
                        assert "3" in str(e), f"Error should mention missing ID 3: {e}"


def test_asr_verification_passes_all_present():
    """T012: ASR verification passes when every ASR has a row."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(asr_db)
        _make_embedding_db(non_asr_db)

        # Populate all ASR rows
        conn = sqlite3.connect(str(asr_db))
        for asr in SAMPLE_ASRS:
            _insert_embedding(conn, asr["id"], asr["text"])
        conn.commit()
        conn.close()

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(asrs=SAMPLE_ASRS)
                    result = prepare_embeddings(state)
                    assert result.get("embeddings_ready") is True


# ---------------------------------------------------------------------------
# Tests: Non-ASR persistence (T013)
# ---------------------------------------------------------------------------
def test_non_asr_embeddings_written_to_db():
    """T013: Non-ASR embeddings written with correct columns."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(asr_db)
        _make_embedding_db(non_asr_db)

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(non_asr=SAMPLE_NON_ASRS)
                    result = prepare_embeddings(state)
                    assert result.get("embeddings_ready") is True

                    # Verify rows in non_asr_embeddings.db
                    conn2 = sqlite3.connect(str(non_asr_db))
                    rows = conn2.execute(
                        "SELECT requirement_id, embedding, text_hash, model_name FROM embeddings ORDER BY requirement_id"
                    ).fetchall()
                    conn2.close()

                    assert len(rows) == 3
                    for row in rows:
                        req_id, embedding_blob, text_hash, model_name = row
                        assert isinstance(req_id, int)
                        assert isinstance(embedding_blob, bytes)
                        assert len(text_hash) == 64
                        assert model_name == _MODEL_NAME


# ---------------------------------------------------------------------------
# Tests: Stale hash recomputation (T014)
# ---------------------------------------------------------------------------
def test_stale_text_hash_triggers_recomputation():
    """T014: Stale text_hash triggers recomputation and updates the row."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(asr_db)
        _make_embedding_db(non_asr_db)

        # Pre-populate non_asr_db with a stale hash for R10
        conn = sqlite3.connect(str(non_asr_db))
        stale_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        stale_blob = _serialize_embedding([0.0] * _EMBEDDING_DIM)
        conn.execute(
            "INSERT INTO embeddings (requirement_id, embedding, text_hash, model_name) VALUES (?, ?, ?, ?)",
            (10, stale_blob, stale_hash, _MODEL_NAME),
        )
        conn.commit()
        conn.close()

        fake_model = FakeEmbeddingModel()
        initial_count = fake_model.call_count

        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(non_asr=SAMPLE_NON_ASRS)
                    result = prepare_embeddings(state)
                    assert result.get("embeddings_ready") is True

                    # Model was called at least for the stale row
                    assert fake_model.call_count > initial_count

                    # Verify the stale row was updated
                    conn2 = sqlite3.connect(str(non_asr_db))
                    row = conn2.execute(
                        "SELECT text_hash FROM embeddings WHERE requirement_id = 10"
                    ).fetchone()
                    conn2.close()
                    assert row is not None
                    assert row[0] != stale_hash


# ---------------------------------------------------------------------------
# Tests: Idempotent rerun (T015)
# ---------------------------------------------------------------------------
def test_idempotent_rerun_skips_model():
    """T015: Idempotent rerun skips fake model when hashes already match."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(asr_db)
        _make_embedding_db(non_asr_db)

        fake_model = FakeEmbeddingModel()

        # Pre-populate non_asr_db with fresh (correct) hashes for all three non-ASRs
        conn = sqlite3.connect(str(non_asr_db))
        for req in SAMPLE_NON_ASRS:
            req_id = int(req["id"][1:])  # "R10" -> 10
            vec = fake_model.embed([req["text"]])[0]
            conn.execute(
                "INSERT INTO embeddings (requirement_id, embedding, text_hash, model_name) VALUES (?, ?, ?, ?)",
                (req_id, _serialize_embedding(vec), _hash_text(req["text"]), _MODEL_NAME),
            )
        conn.commit()
        conn.close()

        initial_count = fake_model.call_count

        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(non_asr=SAMPLE_NON_ASRS)
                    result = prepare_embeddings(state)
                    assert result.get("embeddings_ready") is True

                    # No new model calls — all hashes were current
                    assert fake_model.call_count == initial_count, (
                        f"Expected call_count={initial_count}, got {fake_model.call_count}"
                    )


# ---------------------------------------------------------------------------
# Tests: Return value (T016)
# ---------------------------------------------------------------------------
def test_prepare_embeddings_returns_ready_true():
    """T016: Preparation node returns {'embeddings_ready': True}."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(asr_db)
        _make_embedding_db(non_asr_db)

        # Populate all ASR rows
        conn = sqlite3.connect(str(asr_db))
        for asr in SAMPLE_ASRS:
            _insert_embedding(conn, asr["id"], asr["text"])
        conn.commit()
        conn.close()

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(asrs=SAMPLE_ASRS)
                    result = prepare_embeddings(state)
                    assert isinstance(result, dict)
                    assert result["embeddings_ready"] is True


# ---------------------------------------------------------------------------
# Tests: WAL mode (T017)
# ---------------------------------------------------------------------------
def test_sqlite_connections_use_wal():
    """T017: SQLite connections for both DBs use WAL mode."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"
        _make_embedding_db(asr_db)
        _make_embedding_db(non_asr_db)

        # Populate all ASR rows
        conn = sqlite3.connect(str(asr_db))
        for asr in SAMPLE_ASRS:
            _insert_embedding(conn, asr["id"], asr["text"])
        conn.commit()
        conn.close()

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.preparation._get_embedding_model", return_value=fake_model):
            from raa.nodes.preparation import prepare_embeddings
            with patch("raa.nodes.preparation._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.preparation._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(asrs=SAMPLE_ASRS)
                    prepare_embeddings(state)

                    # Verify both DBs are in WAL mode
                    for db_path in (asr_db, non_asr_db):
                        c = sqlite3.connect(str(db_path))
                        mode = c.execute("PRAGMA journal_mode").fetchone()[0]
                        c.close()
                        assert mode.upper() == "WAL", f"{db_path} journal_mode={mode}, expected WAL"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ok = _run_tests()
    sys.exit(0 if ok else 1)
