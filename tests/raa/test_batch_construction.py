"""Unit tests for raa/nodes/batch_construction.py — batch construction."""

import sqlite3
import struct
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np

# ---------------------------------------------------------------------------
# Constants (match raa/nodes/batch_construction.py)
# ---------------------------------------------------------------------------
_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"
_EMBEDDING_DIM = 1024
_SIMILARITY_THRESHOLD = 0.65
_MAX_CANDIDATES = 10


# ---------------------------------------------------------------------------
# Fake embedding model
# ---------------------------------------------------------------------------
class FakeEmbeddingModel:
    """Deterministic 1024-dim vectors from text length and content."""

    def __init__(self, seed_offset: int = 0):
        self.call_count = 0
        self._offset = seed_offset

    def embed(self, texts, **kwargs):
        self.call_count += len(texts)
        results = []
        for t in texts:
            seed = float((len(t) + self._offset) % 100)
            results.append(np.array([seed + i * 0.001 for i in range(_EMBEDDING_DIM)], dtype=np.float32))
        return results


# ---------------------------------------------------------------------------
# SQLite helpers
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


def _serialize_embedding(vector) -> bytes:
    return struct.pack(f"<{len(vector)}f", *vector)


def _insert_row(conn, req_id: int, embedding: list[float], text_hash: str = "a" * 64):
    conn.execute(
        "INSERT OR REPLACE INTO embeddings (requirement_id, embedding, text_hash, model_name) VALUES (?, ?, ?, ?)",
        (req_id, _serialize_embedding(embedding), text_hash, _MODEL_NAME),
    )


def _make_db(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    _create_embeddings_schema(conn)
    conn.commit()
    conn.close()


def _make_embedding_db(db_path: Path, entries: dict[int, list[float]]):
    """Create a DB and populate it with {requirement_id: vector} entries."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    _create_embeddings_schema(conn)
    for rid, vec in entries.items():
        _insert_row(conn, rid, vec)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
def _make_normalized_vec(seed: float) -> list[float]:
    """Create a unit-length test vector from a seed."""
    raw = np.array([seed + i * 0.001 for i in range(_EMBEDDING_DIM)], dtype=np.float32)
    norm = np.linalg.norm(raw)
    if norm > 0:
        raw = raw / norm
    return raw.tolist()


SAMPLE_ASRS = [
    {"id": 1, "text": "Auth via OAuth 2.0"},
    {"id": 2, "text": "Encrypt data at rest"},
    {"id": 3, "text": "Support 10k concurrent users"},
]

SAMPLE_NON_ASRS = [
    {"id": "R10", "text": "Display dashboard"},
    {"id": "R11", "text": "Log all access events"},
    {"id": "R12", "text": "Role-based access control"},
    {"id": "R13", "text": "Export reports as PDF"},
    {"id": "R14", "text": "Send email notifications"},
    {"id": "R15", "text": "Schedule background jobs"},
    {"id": "R16", "text": "Validate user input"},
    {"id": "R17", "text": "Cache query results"},
    {"id": "R18", "text": "Rate limit API calls"},
    {"id": "R19", "text": "Monitor system health"},
    {"id": "R20", "text": "Audit trail for changes"},
    {"id": "R21", "text": "Backup database daily"},
]

SAMPLE_GROUPS = [
    {
        "group_id": 1,
        "nominal_condition": "Authentication and authorization",
        "requirements": [{"id": 1}, {"id": 2}],
    },
    {
        "group_id": 2,
        "nominal_condition": "Performance and scalability",
        "requirements": [{"id": 3}],
    },
    {
        "group_id": 3,
        "nominal_condition": "Empty group fallback",
        "requirements": [],
    },
]


def _make_raa_state(asrs=None, non_asr=None, condition_groups=None):
    return {
        "asrs": asrs or [],
        "non_asr": non_asr or [],
        "condition_groups": condition_groups or [],
        "quality_weights": {},
        "batch_queue": [],
        "batch_cursor": 0,
        "batch_outputs": {},
        "best_batch_output": {},
        "running_arch_model": None,
        "open_questions": [],
        "bridge_requirements": [],
        "incoherent_batches": [],
        "embeddings_ready": True,
    }


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------
def _run_tests():
    import inspect
    tests = sorted(
        (n, o) for n, o in inspect.getmembers(sys.modules[__name__])
        if n.startswith("test_") and callable(o)
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
# T014: Centroid
# ---------------------------------------------------------------------------
def test_centroid_is_element_wise_average():
    """T014: Centroid is element-wise average of ASR embeddings, L2-normalized."""
    from raa.nodes.batch_construction import _compute_centroid

    v1 = [1.0, 0.0, 0.0] + [0.0] * (_EMBEDDING_DIM - 3)
    v2 = [0.0, 1.0, 0.0] + [0.0] * (_EMBEDDING_DIM - 3)

    centroid = _compute_centroid([v1, v2])
    assert len(centroid) == _EMBEDDING_DIM
    # Average non-zero at indices 0 and 1, zero elsewhere → direction [0.5, 0.5, 0, ...]
    assert centroid[0] > 0 and centroid[1] > 0
    assert abs(centroid[0] - centroid[1]) < 1e-5

    # Verify L2 norm ≈ 1
    norm = np.linalg.norm(np.array(centroid, dtype=np.float32))
    assert abs(norm - 1.0) < 1e-5, f"norm={norm}"


def test_centroid_empty_returns_zero():
    """T014b: Empty vector list returns zero vector."""
    from raa.nodes.batch_construction import _compute_centroid

    centroid = _compute_centroid([])
    assert centroid == [0.0] * _EMBEDDING_DIM


# ---------------------------------------------------------------------------
# T015: Fallback embedding
# ---------------------------------------------------------------------------
def test_fallback_reembeds_nominal_condition():
    """T015: Falls back to re-embedding when no ASR embeddings loadable."""
    fake_model = FakeEmbeddingModel(seed_offset=42)
    with patch("raa.nodes.batch_construction._get_embedding_model", return_value=fake_model):
        from raa.nodes.batch_construction import _centroid_for_group, _embed_nominal_condition

        group = {
            "group_id": 99,
            "nominal_condition": "Performance and scalability",
            "requirements": [],  # No ASRs
        }
        with tempfile.TemporaryDirectory() as tmp:
            asr_db = Path(tmp) / "asr_empty.db"
            _make_db(asr_db)  # Empty DB, no embeddings

            centroid = _centroid_for_group(group, asr_db, model=fake_model)
            assert len(centroid) == _EMBEDDING_DIM
            assert fake_model.call_count > 0, "Model should have been called for fallback"


# ---------------------------------------------------------------------------
# T016: Threshold filter
# ---------------------------------------------------------------------------
def test_cosine_similarity_threshold():
    """T016: Only candidates with cosine similarity >= 0.65 pass filter."""
    from raa.nodes.batch_construction import _cosine_similarity, _search_non_asr_candidates

    # centroid: unit vector along dim 0
    centroid = [1.0] + [0.0] * (_EMBEDDING_DIM - 1)

    # High-similarity: strong component in dim 0, tiny components elsewhere
    high_raw = [0.9] + [0.001] * (_EMBEDDING_DIM - 1)
    high_arr = np.array(high_raw, dtype=np.float32)
    high = (high_arr / np.linalg.norm(high_arr)).tolist()

    # Low: orthogonal — unit vector along dim 1
    low = [0.0, 1.0] + [0.0] * (_EMBEDDING_DIM - 2)

    sim_high = _cosine_similarity(centroid, high)
    sim_low = _cosine_similarity(centroid, low)

    assert sim_high >= 0.65, f"High sim should pass threshold: {sim_high}"
    assert sim_low < 0.65, f"Low sim should fail threshold: {sim_low}"

    # Full search test
    rows = [
        {"requirement_id": 10, "embedding": high, "text_hash": "a", "model_name": "m"},
        {"requirement_id": 11, "embedding": low, "text_hash": "b", "model_name": "m"},
    ]
    payloads = [
        {"id": "R10", "text": "High match"},
        {"id": "R11", "text": "Low match"},
    ]
    candidates = _search_non_asr_candidates(centroid, rows, payloads)
    assert len(candidates) == 1
    # id may be the SQLite int (10) or the payload str ("R10") — check similarity present
    assert candidates[0]["similarity"] >= 0.65


# ---------------------------------------------------------------------------
# T017: Top-10 cap
# ---------------------------------------------------------------------------
def test_candidate_selection_capped_at_10():
    """T017: Non-ASR candidate selection capped at top 10 by similarity."""
    from raa.nodes.batch_construction import _search_non_asr_candidates

    centroid = [1.0] + [0.0] * (_EMBEDDING_DIM - 1)

    # Create 15 high-similarity vectors with decreasing scores
    rows = []
    payloads = []
    for i in range(15):
        factor = 0.95 - i * 0.01  # decreasing similarity
        vec = [factor] + [(1.0 - factor)] + [0.0] * (_EMBEDDING_DIM - 2)
        v_norm = np.linalg.norm(np.array(vec, dtype=np.float32))
        vec = (np.array(vec, dtype=np.float32) / v_norm).tolist()
        rows.append({
            "requirement_id": 100 + i,
            "embedding": vec,
            "text_hash": "c",
            "model_name": "m",
        })
        payloads.append({"id": f"R{100 + i}", "text": f"Item {i}"})

    candidates = _search_non_asr_candidates(centroid, rows, payloads)
    assert len(candidates) == _MAX_CANDIDATES, f"Expected {_MAX_CANDIDATES}, got {len(candidates)}"
    # Verify descending order
    for i in range(len(candidates) - 1):
        assert candidates[i]["similarity"] >= candidates[i + 1]["similarity"]


# ---------------------------------------------------------------------------
# T018: Empty non-ASR pool
# ---------------------------------------------------------------------------
def test_empty_non_asr_pool_assembles_asr_only():
    """T018: Empty non-ASR pool still assembles ASR-only batch."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"

        # Populate ASR DB with group 1 embeddings
        v1 = _make_normalized_vec(1.0)
        v2 = _make_normalized_vec(2.0)
        _make_embedding_db(asr_db, {1: v1, 2: v2})
        _make_db(non_asr_db)  # Empty non-ASR DB

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.batch_construction._get_embedding_model", return_value=fake_model):
            from raa.nodes.batch_construction import construct_batches
            with patch("raa.nodes.batch_construction._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.batch_construction._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(
                        asrs=[{"id": 1, "text": "Auth"}, {"id": 2, "text": "Encrypt"}],
                        non_asr=[],
                        condition_groups=[{"group_id": 1, "nominal_condition": "Security", "requirements": [{"id": 1}, {"id": 2}]}],
                    )
                    result = construct_batches(state)
                    batches = result["batch_queue"]
                    assert len(batches) == 1
                    # Batch should have requirements but empty non_asr_candidates
                    assert len(batches[0]["requirements"]) >= 2  # ASR payloads
                    assert batches[0]["non_asr_candidates"] == []


# ---------------------------------------------------------------------------
# T019: Batch payload assembly
# ---------------------------------------------------------------------------
def test_batch_stores_full_payloads():
    """T019: Batch stores group_id, centroid, similarity_scores, and full requirement payloads."""
    from raa.nodes.batch_construction import _assemble_batch

    centroid = (np.array([5.0 + i * 0.001 for i in range(_EMBEDDING_DIM)], dtype=np.float32))
    centroid = (centroid / np.linalg.norm(centroid)).tolist()

    asr_payloads = [{"id": 1, "text": "Auth via OAuth"}, {"id": 2, "text": "Encrypt data"}]
    candidates = [
        {"id": 10, "text": "Display dashboard", "similarity": 0.82},
        {"id": 11, "text": "Log events", "similarity": 0.71},
    ]
    group = {"group_id": 5, "nominal_condition": "Security"}

    batch = _assemble_batch(5, group, centroid, asr_payloads, candidates)

    assert batch["group_id"] == 5
    assert batch["batch_id"] == 5
    assert "group_centroid" in batch
    assert len(batch["group_centroid"]) == _EMBEDDING_DIM
    assert len(batch["requirements"]) == 4  # 2 ASR + 2 non-ASR
    assert "similarity_scores" in batch
    assert batch["similarity_scores"]["10"] == 0.82
    assert batch["similarity_scores"]["11"] == 0.71
    assert len(batch["non_asr_candidates"]) == 2
    assert batch["cluster"] == ["Security"]


# ---------------------------------------------------------------------------
# T020: Node-level construct_batches
# ---------------------------------------------------------------------------
def test_construct_batches_returns_batch_queue():
    """T020: construct_batches returns batch_queue with one batch per condition group."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"

        # Populate embeddings
        asr_entries = {}
        for i, asr in enumerate(SAMPLE_ASRS):
            asr_entries[asr["id"]] = _make_normalized_vec(float(asr["id"]))
        _make_embedding_db(asr_db, asr_entries)
        _make_db(non_asr_db)  # Empty for simplicity

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.batch_construction._get_embedding_model", return_value=fake_model):
            from raa.nodes.batch_construction import construct_batches
            with patch("raa.nodes.batch_construction._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.batch_construction._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(
                        asrs=SAMPLE_ASRS,
                        non_asr=[],
                        condition_groups=SAMPLE_GROUPS,
                    )
                    result = construct_batches(state)
                    batches = result["batch_queue"]
                    assert len(batches) == 3  # One per condition group

                    # Verify group_id uniqueness
                    gids = [b["group_id"] for b in batches]
                    assert gids == [1, 2, 3]


def test_empty_non_asr_list_produces_zero_batches_gracefully():
    """T013: Empty non_asr list/database is handled gracefully and batches proceed with empty candidates."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"

        # Populate ASR DB
        asr_entries = {1: _make_normalized_vec(1.0), 2: _make_normalized_vec(2.0)}
        _make_embedding_db(asr_db, asr_entries)
        _make_db(non_asr_db)  # Empty DB

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.batch_construction._get_embedding_model", return_value=fake_model):
            from raa.nodes.batch_construction import construct_batches
            with patch("raa.nodes.batch_construction._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.batch_construction._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(
                        asrs=[{"id": 1, "text": "Auth"}, {"id": 2, "text": "Encrypt"}],
                        non_asr=[],
                        condition_groups=[{"group_id": 1, "nominal_condition": "Security", "requirements": [{"id": 1}, {"id": 2}]}],
                    )
                    
                    with patch("raa.nodes.batch_construction.logger.info") as mock_info:
                        result = construct_batches(state)
                        batches = result["batch_queue"]
                        assert len(batches) == 1
                        assert batches[0]["non_asr_candidates"] == []
                        
                        info_called = False
                        for call in mock_info.call_args_list:
                            msg = call[0][0]
                            if "no matching non-ASR candidates" in msg:
                                info_called = True
                                break
                        assert info_called, "Info log about empty candidates was not emitted"


def test_connect_readonly_enables_wal():
    """T016: open_embedding_db in read_only mode still enables WAL mode on connection."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        db_path = tmp_path / "test_wal_read_only.db"
        
        # Create DB
        _make_db(db_path)
        
        from raa.utils.db import open_embedding_db
        conn = open_embedding_db(db_path, read_only=True)
        try:
            mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
            assert mode.upper() == "WAL"
        finally:
            conn.close()


def test_concurrent_readonly_no_lock_errors():
    """T017: Multiple concurrent read-only connections execute queries without locking errors."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        db_path = tmp_path / "test_concurrent.db"
        
        # Create and populate DB
        _make_db(db_path)
        conn_init = sqlite3.connect(str(db_path))
        _create_embeddings_schema(conn_init)
        _insert_row(conn_init, 1, [0.1] * _EMBEDDING_DIM)
        conn_init.commit()
        conn_init.close()
        
        from raa.utils.db import open_embedding_db
        
        # Open 3 concurrent read-only connections
        conn1 = open_embedding_db(db_path, read_only=True)
        conn2 = open_embedding_db(db_path, read_only=True)
        conn3 = open_embedding_db(db_path, read_only=True)
        
        try:
            # Execute queries concurrently
            row1 = conn1.execute("SELECT requirement_id FROM embeddings").fetchone()
            row2 = conn2.execute("SELECT requirement_id FROM embeddings").fetchone()
            row3 = conn3.execute("SELECT requirement_id FROM embeddings").fetchone()
            
            assert row1[0] == 1
            assert row2[0] == 1
            assert row3[0] == 1
        finally:
            conn1.close()
            conn2.close()
            conn3.close()


def test_batch_includes_all_condition_group_asrs():
    """T015: Batch assembly includes all ASRs from the condition group."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"

        # Populate ASR DB with 3 ASRs
        v1 = _make_normalized_vec(1.0)
        v2 = _make_normalized_vec(2.0)
        v3 = _make_normalized_vec(3.0)
        _make_embedding_db(asr_db, {1: v1, 2: v2, 3: v3})
        _make_db(non_asr_db)

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.batch_construction._get_embedding_model", return_value=fake_model):
            from raa.nodes.batch_construction import construct_batches
            with patch("raa.nodes.batch_construction._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.batch_construction._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(
                        asrs=[
                            {"id": 1, "text": "Auth"},
                            {"id": 2, "text": "Encrypt"},
                            {"id": 3, "text": "Scale"}
                        ],
                        non_asr=[],
                        condition_groups=[{
                            "group_id": 1,
                            "nominal_condition": "Security & Scale",
                            "requirements": [{"id": 1}, {"id": 2}, {"id": 3}]
                        }],
                    )
                    result = construct_batches(state)
                    batches = result["batch_queue"]
                    assert len(batches) == 1
                    req_ids = batches[0]["requirement_ids"]
                    assert "1" in req_ids
                    assert "2" in req_ids
                    assert "3" in req_ids


def test_batch_includes_non_asr_candidates():
    """T016: Batch assembly includes non-ASR candidates meeting the similarity threshold."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        asr_db = tmp_path / "asr_embeddings.db"
        non_asr_db = tmp_path / "non_asr_embeddings.db"

        # Unit vector along dim 0
        v_asr = [1.0] + [0.0] * (_EMBEDDING_DIM - 1)
        _make_embedding_db(asr_db, {1: v_asr})

        # Non-ASR embeddings (5 identical to ASR, so similarity = 1.0)
        non_asr_entries = {}
        for rid in range(10, 15):
            non_asr_entries[rid] = v_asr
        _make_embedding_db(non_asr_db, non_asr_entries)

        fake_model = FakeEmbeddingModel()
        with patch("raa.nodes.batch_construction._get_embedding_model", return_value=fake_model):
            from raa.nodes.batch_construction import construct_batches
            with patch("raa.nodes.batch_construction._asr_db_path", return_value=asr_db):
                with patch("raa.nodes.batch_construction._non_asr_db_path", return_value=non_asr_db):
                    state = _make_raa_state(
                        asrs=[{"id": 1, "text": "Auth"}],
                        non_asr=[{"id": f"R{rid}", "text": f"Non-ASR {rid}"} for rid in range(10, 15)],
                        condition_groups=[{
                            "group_id": 1,
                            "nominal_condition": "Security",
                            "requirements": [{"id": 1}]
                        }],
                    )
                    result = construct_batches(state)
                    batches = result["batch_queue"]
                    assert len(batches) == 1
                    non_asr_cands = batches[0]["non_asr_candidates"]
                    assert len(non_asr_cands) == 5
                    for cand in non_asr_cands:
                        assert cand["similarity"] >= 0.65


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ok = _run_tests()
    sys.exit(0 if ok else 1)

