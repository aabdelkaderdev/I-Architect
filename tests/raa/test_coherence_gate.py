"""Unit tests for raa/nodes/coherence_gate.py — coherence gate."""

import sys

import numpy as np

_EMBEDDING_DIM = 1024


# ---------------------------------------------------------------------------
# Vector / batch helpers
# ---------------------------------------------------------------------------
def _unit_vec(dim: int, *active: tuple[int, float]) -> list[float]:
    arr = np.zeros(dim, dtype=np.float32)
    for axis, val in active:
        arr[axis] = float(val)
    norm = np.linalg.norm(arr)
    if norm > 0:
        arr = arr / norm
    return arr.tolist()


def _req(req_id: str, emb_axis: int, emb_val: float = 1.0) -> dict:
    """Requirement payload with an embedding along a single axis."""
    emb = _unit_vec(_EMBEDDING_DIM, (emb_axis, emb_val))
    return {"id": req_id, "text": f"Requirement {req_id}", "embedding": emb}


def _req_custom(req_id: str, *axes: tuple[int, float]) -> dict:
    """Requirement with custom embedding direction."""
    return {
        "id": req_id,
        "text": f"Requirement {req_id}",
        "embedding": _unit_vec(_EMBEDDING_DIM, *axes),
    }


def _batch(gid: int, reqs=None) -> dict:
    if reqs is None:
        reqs = []
    return {
        "batch_id": gid,
        "group_id": gid,
        "requirement_ids": [r["id"] for r in reqs],
        "requirements": reqs,
        "similarity_scores": {},
        "group_centroid": _unit_vec(_EMBEDDING_DIM, (0, 1.0)),
        "reduced_confidence": False,
        "cluster": ["cluster_x"],
        "non_asr_candidates": [],
    }


def _state(queues=None):
    return {
        "batch_queue": queues or [],
        "incoherent_batches": [],
        "asrs": [], "non_asr": [], "condition_groups": [],
        "quality_weights": {}, "batch_cursor": 0,
        "batch_outputs": {}, "best_batch_output": {},
        "running_arch_model": None, "open_questions": [],
        "bridge_requirements": {}, "embeddings_ready": True,
    }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def _run_tests():
    import inspect
    tests = sorted((n, o) for n, o in inspect.getmembers(sys.modules[__name__])
                   if n.startswith("test_") and callable(o))
    passed = failed = 0
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
# T011: Centroid
# ---------------------------------------------------------------------------
def test_compute_centroid():
    from raa.nodes.coherence_gate import _compute_centroid

    v1 = _unit_vec(_EMBEDDING_DIM, (0, 1.0))
    v2 = _unit_vec(_EMBEDDING_DIM, (1, 1.0))

    c = _compute_centroid([v1, v2])
    assert len(c) == _EMBEDDING_DIM
    assert c[0] > 0 and c[1] > 0
    # L2 ≈ 1
    assert abs(np.linalg.norm(np.array(c, dtype=np.float32)) - 1.0) < 1e-5


# ---------------------------------------------------------------------------
# T012: Coherence score
# ---------------------------------------------------------------------------
def test_compute_coherence_score():
    from raa.nodes.coherence_gate import _compute_coherence_score

    # Three identical vectors → score ≈ 1.0
    v = _unit_vec(_EMBEDDING_DIM, (0, 1.0))
    s = _compute_coherence_score([v, v, v])
    assert s > 0.99, f"Identical vectors should score ~1.0, got {s}"

    # Two orthogonal vectors → score ≈ 0.5
    v1 = _unit_vec(_EMBEDDING_DIM, (0, 1.0))
    v2 = _unit_vec(_EMBEDDING_DIM, (1, 1.0))
    s2 = _compute_coherence_score([v1, v2] * 3)  # 6 vectors, half axis-0, half axis-1
    # Centroid at (0.5, 0.5): each vector's sim ≈ 1/√2 ≈ 0.707
    assert 0.6 < s2 < 0.8, f"Mixed vectors: {s2}"


# ---------------------------------------------------------------------------
# T013: Coherence threshold is 0.55, not 0.65
# ---------------------------------------------------------------------------
def test_coherence_threshold_is_055():
    from raa.nodes.coherence_gate import COHERENCE_THRESHOLD

    assert COHERENCE_THRESHOLD == 0.55
    assert COHERENCE_THRESHOLD != 0.65


# ---------------------------------------------------------------------------
# T014: ≤2 requirements pass automatically
# ---------------------------------------------------------------------------
def test_small_batches_pass_automatically():
    from raa.nodes.coherence_gate import _should_pass_without_split, _evaluate_batch

    b = _batch(1, [_req("R1", 0), _req("R2", 50)])  # orthogonal, but only 2 → auto-pass
    assert _should_pass_without_split(b) is True

    results, record = _evaluate_batch(b)
    assert record is None
    assert len(results) == 1
    assert results[0]["coherence_score"] == 1.0


# ---------------------------------------------------------------------------
# T015: Homogeneous pass — score ≥ 0.55 stays unchanged (except metadata)
# ---------------------------------------------------------------------------
def test_homogeneous_pass():
    from raa.nodes.coherence_gate import _evaluate_batch

    # All vectors point same way → high coherence
    reqs = [_req(f"R{i}", 0) for i in range(5)]
    b = _batch(1, reqs)
    results, record = _evaluate_batch(b)
    assert record is None
    assert len(results) == 1
    assert results[0]["coherence_score"] >= 0.55


# ---------------------------------------------------------------------------
# T016: Heterogeneous split into two passing sub-batches
# ---------------------------------------------------------------------------
def test_heterogeneous_split():
    from raa.nodes.coherence_gate import _evaluate_batch

    # 4 orthogonal clusters → coherence ≈ 0.5 < 0.55 → triggers split
    # K=2 groups them into 2 sub-groups of 2 clusters each → both pass
    reqs = [_req(f"Ra{i}", 0) for i in range(4)]
    reqs += [_req(f"Rb{i}", 51) for i in range(4)]
    reqs += [_req(f"Rc{i}", 102) for i in range(4)]
    reqs += [_req(f"Rd{i}", 153) for i in range(4)]
    b = _batch(1, reqs)
    results, record = _evaluate_batch(b)

    assert record is None
    assert len(results) == 2, f"Expected 2 sub-batches, got {len(results)}"
    for sub in results:
        assert sub["is_split"] is True
        assert sub["coherence_score"] >= 0.55
        assert sub["source_batch_id"] == 1


# ---------------------------------------------------------------------------
# T017: Split preserves payloads, IDs, scores, group metadata, source_batch_id
# ---------------------------------------------------------------------------
def test_split_preserves_metadata():
    from raa.nodes.coherence_gate import _evaluate_batch

    # 4 clusters to trigger split
    reqs = [_req(f"Ra{i}", 0) for i in range(3)]
    reqs += [_req(f"Rb{i}", 51) for i in range(3)]
    reqs += [_req(f"Rc{i}", 102) for i in range(3)]
    reqs += [_req(f"Rd{i}", 153) for i in range(3)]
    b = _batch(42, reqs)
    b["similarity_scores"] = {r["id"]: 0.8 for r in reqs}

    results, _ = _evaluate_batch(b)
    assert len(results) == 2

    # All requirement IDs should appear across sub-batches
    all_ids = set()
    for sub in results:
        all_ids.update(sub["requirement_ids"])
        assert sub["group_id"] == 42
        assert sub["source_batch_id"] == 42

    assert len(all_ids) == 12  # All requirements accounted for


# ---------------------------------------------------------------------------
# T018: Deterministic split stability
# ---------------------------------------------------------------------------
def test_split_is_deterministic():
    from raa.nodes.coherence_gate import _split_vectors_k2

    v1 = _unit_vec(_EMBEDDING_DIM, (0, 1.0))
    v2 = _unit_vec(_EMBEDDING_DIM, (0, 1.02))  # close to v1
    v3 = _unit_vec(_EMBEDDING_DIM, (100, 1.0))
    v4 = _unit_vec(_EMBEDDING_DIM, (100, 1.02))

    vectors = [v1, v2, v3, v4]
    idx1_a, idx2_a = _split_vectors_k2(vectors)
    idx1_b, idx2_b = _split_vectors_k2(vectors)

    assert idx1_a == idx1_b
    assert idx2_a == idx2_b


# ---------------------------------------------------------------------------
# T019: Split failure → reduced_confidence + IncoherentBatchRecord
# ---------------------------------------------------------------------------
def test_split_failure_marks_reduced_confidence():
    from raa.nodes.coherence_gate import _evaluate_batch
    from raa.state.types import IncoherentBatchRecord

    # 5 orthogonal clusters + slight perturbation → extremely low coherence
    # K=2 split tries but sub-batches will still have low coherence
    reqs = [_req(f"Ra{i}", 0) for i in range(3)]
    reqs += [_req(f"Rb{i}", 51) for i in range(3)]
    reqs += [_req(f"Rc{i}", 102) for i in range(3)]
    reqs += [_req(f"Rd{i}", 153) for i in range(3)]
    reqs += [_req(f"Re{i}", 204) for i in range(3)]
    b = _batch(1, reqs)

    results, record = _evaluate_batch(b)

    # With 5 clusters and k=2, sub-batches will still be incoherent
    # → batch kept as-is with reduced_confidence
    assert results[0]["reduced_confidence"] is True
    assert record is not None
    assert isinstance(record, IncoherentBatchRecord)
    assert record.reduced_confidence is True


# ---------------------------------------------------------------------------
# T020: Node-level apply_coherence_gate
# ---------------------------------------------------------------------------
def test_apply_coherence_gate_returns_both_channels():
    from raa.nodes.coherence_gate import apply_coherence_gate

    # High-coherence batch → passes
    b1 = _batch(1, [_req(f"R{i}", 0) for i in range(5)])
    b2 = _batch(2, [_req(f"R{i}", 0) for i in range(3)])

    result = apply_coherence_gate(_state([b1, b2]))
    assert "batch_queue" in result
    assert "incoherent_batches" in result
    assert len(result["batch_queue"]) >= 2  # at least the two original batches


# ---------------------------------------------------------------------------
# T021: Missing embedding raises ValueError
# ---------------------------------------------------------------------------
def test_missing_embedding_raises_error():
    from raa.nodes.coherence_gate import _requirement_embedding

    try:
        _requirement_embedding({"id": "R99", "text": "no embedding here"})
        raise AssertionError("Expected ValueError")
    except ValueError as e:
        assert "embedding" in str(e).lower() or "vector" in str(e).lower()


def test_coherence_gate_passes_homogeneous_batch():
    """T019: Coherence gate passes a homogeneous batch without splitting."""
    from raa.nodes.coherence_gate import _evaluate_batch
    # All vectors point same way → high coherence
    reqs = [_req(f"R{i}", 0) for i in range(5)]
    b = _batch(1, reqs)
    results, record = _evaluate_batch(b)
    assert record is None
    assert len(results) == 1
    assert results[0]["coherence_score"] >= 0.55
    assert results[0].get("is_split", False) is False


def test_coherence_gate_splits_heterogeneous_batch():
    """T020: Coherence gate splits a heterogeneous batch into two sub-batches."""
    from raa.nodes.coherence_gate import _evaluate_batch
    # Trigger split using 4 orthogonal clusters
    reqs = [_req(f"Ra{i}", 0) for i in range(4)]
    reqs += [_req(f"Rb{i}", 51) for i in range(4)]
    reqs += [_req(f"Rc{i}", 102) for i in range(4)]
    reqs += [_req(f"Rd{i}", 153) for i in range(4)]
    b = _batch(1, reqs)
    results, record = _evaluate_batch(b)
    assert record is None
    assert len(results) == 2
    for sub in results:
        assert sub["is_split"] is True
        assert sub["coherence_score"] >= 0.55


def test_coherence_gate_flags_incoherent_after_split():
    """T021: Coherence gate flags the batch as incoherent with reduced confidence when split sub-batches remain incoherent."""
    from raa.nodes.coherence_gate import _evaluate_batch
    # Low coherence after split
    reqs = [_req(f"Ra{i}", 0) for i in range(3)]
    reqs += [_req(f"Rb{i}", 51) for i in range(3)]
    reqs += [_req(f"Rc{i}", 102) for i in range(3)]
    reqs += [_req(f"Rd{i}", 153) for i in range(3)]
    reqs += [_req(f"Re{i}", 204) for i in range(3)]
    b = _batch(1, reqs)
    results, record = _evaluate_batch(b)
    assert results[0]["reduced_confidence"] is True
    assert record is not None
    assert record.reduced_confidence is True


if __name__ == "__main__":
    ok = _run_tests()
    sys.exit(0 if ok else 1)

