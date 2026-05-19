"""Unit tests for raa/nodes/overlap_bridging.py — overlap bridging."""

import sys

import numpy as np

_EMBEDDING_DIM = 1024


# ---------------------------------------------------------------------------
# Vector helpers
# ---------------------------------------------------------------------------
def _unit_vec(dim: int, *active_axes: tuple[int, float]) -> list[float]:
    """Construct a normalised vector with non-zero values at designated axes."""
    arr = np.zeros(dim, dtype=np.float32)
    for axis, val in active_axes:
        arr[axis] = float(val)
    norm = np.linalg.norm(arr)
    if norm > 0:
        arr = arr / norm
    return arr.tolist()


def _centroid(axis: int) -> list[float]:
    """Unit vector along one axis — orthogonal to other axes."""
    return _unit_vec(_EMBEDDING_DIM, (axis, 1.0))


def _candidate(req_id: str, text: str, emb_axis_a: int, emb_axis_b: int) -> dict:
    """A candidate with embedding spanning two axes (good for bridge tests)."""
    emb = _unit_vec(_EMBEDDING_DIM, (emb_axis_a, 1.0), (emb_axis_b, 0.7))
    return {"id": req_id, "text": text, "similarity": 0.75, "embedding": emb}


def _batch(gid: int, cluster: str, centroid_axis: int, candidates=None) -> dict:
    return {
        "batch_id": gid,
        "group_id": gid,
        "requirement_ids": [],
        "group_centroid": _centroid(centroid_axis),
        "reduced_confidence": False,
        "cluster": [cluster],
        "requirements": [],
        "similarity_scores": {},
        "non_asr_candidates": candidates or [],
    }


def _state(batches=None):
    return {
        "batch_queue": batches or [],
        "bridge_requirements": {},
        "asrs": [], "non_asr": [], "condition_groups": [],
        "quality_weights": {}, "batch_cursor": 0,
        "batch_outputs": {}, "best_batch_output": {},
        "running_arch_model": None, "open_questions": [],
        "incoherent_batches": [], "embeddings_ready": True,
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
# T012: Adjacency by cluster ID
# ---------------------------------------------------------------------------
def test_adjacent_by_cluster():
    from raa.nodes.overlap_bridging import _are_adjacent

    b1 = _batch(1, "Security", 0)
    b2 = _batch(2, "Security", 0)
    assert _are_adjacent(b1, b2) is True  # same cluster

    b3 = _batch(3, "Performance", 10)     # different cluster, orthogonal centroid
    assert _are_adjacent(b1, b3) is False


# ---------------------------------------------------------------------------
# T013: Adjacency by centroid similarity
# ---------------------------------------------------------------------------
def test_adjacent_by_centroid():
    from raa.nodes.overlap_bridging import _are_adjacent

    c_near = _unit_vec(_EMBEDDING_DIM, (0, 0.999), (1, 0.01))  # nearly axis-0

    b1 = {"group_id": 1, "cluster": ["A"], "group_centroid": _centroid(0)}
    b2 = {"group_id": 2, "cluster": ["B"], "group_centroid": c_near}
    assert _are_adjacent(b1, b2) is True   # high centroid similarity

    b3 = {"group_id": 3, "cluster": ["C"], "group_centroid": _centroid(50)}
    assert _are_adjacent(b1, b3) is False  # orthogonal


# ---------------------------------------------------------------------------
# T014: Non-adjacent batches produce no bridges
# ---------------------------------------------------------------------------
def test_non_adjacent_batches_unchanged():
    from raa.nodes.overlap_bridging import apply_overlap_bridging

    b1 = _batch(1, "Security", 0, [_candidate("R10", "Auth", 0, 1)])
    b2 = _batch(2, "Performance", 50, [_candidate("R20", "Speed", 50, 51)])

    result = apply_overlap_bridging(_state([b1, b2]))
    assert result["batch_queue"] == [b1, b2]
    assert result["bridge_requirements"] == {}


# ---------------------------------------------------------------------------
# T015: Dual-centroid bridge scoring
# ---------------------------------------------------------------------------
def test_dual_centroid_bridge_scoring():
    from raa.nodes.overlap_bridging import _bridge_score

    left_c = _centroid(0)
    right_c = _centroid(1)

    # Equally close to both axes → strong bridge
    cand_strong = {"id": "R99", "embedding": _unit_vec(_EMBEDDING_DIM, (0, 1.0), (1, 1.0))}
    # Close only to left
    cand_left = {"id": "R98", "embedding": left_c}

    s_strong = _bridge_score(cand_strong, left_c, right_c)
    s_left = _bridge_score(cand_left, left_c, right_c)
    assert s_strong > s_left, f"strong={s_strong}, left-only={s_left}"

    # Right-only has ~0 similarity to left → negative score
    s_right = _bridge_score({"id": "R97", "embedding": right_c}, left_c, right_c)
    assert s_right < 0, f"right-only score={s_right}"


# ---------------------------------------------------------------------------
# T016: Hard cap of 3 bridge requirements
# ---------------------------------------------------------------------------
def test_bridge_selection_capped_at_3():
    from raa.nodes.overlap_bridging import _select_bridge_requirements

    left_c = _centroid(0)
    right_c = _centroid(1)

    # 5 candidates at varying mid-points between axes
    candidates = []
    for i in range(5):
        w = 0.95 - i * 0.18
        c = _unit_vec(_EMBEDDING_DIM, (0, w), (1, 1.0 - w))
        candidates.append({"id": f"R{10+i}", "text": f"C{i}", "similarity": w, "embedding": c})

    left = _batch(1, "X", 0, candidates)
    right = _batch(2, "X", 1, [])

    bridges, scores = _select_bridge_requirements(left, right)
    assert len(bridges) <= 3, f"Expected <= 3, got {len(bridges)}"


# ---------------------------------------------------------------------------
# T017: Fewer than 3 candidates selected without padding
# ---------------------------------------------------------------------------
def test_fewer_than_3_candidates_no_padding():
    from raa.nodes.overlap_bridging import _select_bridge_requirements

    mid = _unit_vec(_EMBEDDING_DIM, (0, 1.0), (1, 1.0))
    left = _batch(1, "X", 0, [{"id": "R10", "text": "Only", "similarity": 0.8, "embedding": mid}])
    right = _batch(2, "X", 1, [])

    bridges, scores = _select_bridge_requirements(left, right)
    assert len(bridges) == 1
    assert bridges[0]["id"] == "R10"


# ---------------------------------------------------------------------------
# T018: Bridge injection into both adjacent batches
# ---------------------------------------------------------------------------
def test_bridge_injected_into_both_batches():
    from raa.nodes.overlap_bridging import apply_overlap_bridging

    mid = _unit_vec(_EMBEDDING_DIM, (0, 1.0), (1, 1.0))
    cand = {"id": "R50", "text": "Bridge req", "similarity": 0.85, "embedding": mid}

    b1 = _batch(1, "Shared", 0, [cand])
    b2 = _batch(2, "Shared", 1, [])

    result = apply_overlap_bridging(_state([b1, b2]))
    for b in result["batch_queue"]:
        ids = [r.get("id") for r in b.get("requirements", [])]
        assert "R50" in ids, f"Batch {b['group_id']} missing R50"


# ---------------------------------------------------------------------------
# T019: Injected IDs present in requirement_ids and similarity_scores
# ---------------------------------------------------------------------------
def test_injected_ids_in_requirement_ids_and_scores():
    from raa.nodes.overlap_bridging import apply_overlap_bridging

    mid = _unit_vec(_EMBEDDING_DIM, (0, 1.0), (1, 1.0))
    cand = {"id": "R60", "text": "Bridge", "similarity": 0.9, "embedding": mid}

    b1 = _batch(1, "S", 0, [cand])
    b2 = _batch(2, "S", 1, [])

    result = apply_overlap_bridging(_state([b1, b2]))
    for b in result["batch_queue"]:
        assert "R60" in b["requirement_ids"], f"Batch {b['group_id']} missing R60 in ids"
        assert "R60" in b["similarity_scores"], f"Batch {b['group_id']} missing R60 in scores"
        assert b["similarity_scores"]["R60"] > 0


# ---------------------------------------------------------------------------
# T020: Node-level apply_overlap_bridging
# ---------------------------------------------------------------------------
def test_apply_overlap_bridging_returns_bridge_requirements():
    from raa.nodes.overlap_bridging import apply_overlap_bridging

    mid = _unit_vec(_EMBEDDING_DIM, (0, 1.0), (1, 1.0))
    cand = {"id": "R70", "text": "Bridge", "similarity": 0.88, "embedding": mid}

    b1 = _batch(1, "ClusterA", 0, [cand])
    b2 = _batch(2, "ClusterA", 1, [])

    result = apply_overlap_bridging(_state([b1, b2]))
    br = result["bridge_requirements"]
    assert len(br) == 1
    assert list(br.keys())[0] == (1, 2)
    assert "R70" in br[(1, 2)]
    assert len(result["batch_queue"]) == 2


def test_bridge_cap_enforcement():
    """T017: Overlap bridging enforces a hard cap of 3 selected bridge requirements."""
    from raa.nodes.overlap_bridging import _select_bridge_requirements

    left_c = _centroid(0)
    right_c = _centroid(1)

    # 5 candidates at varying mid-points between axes
    candidates = []
    for i in range(5):
        w = 0.95 - i * 0.18
        c = _unit_vec(_EMBEDDING_DIM, (0, w), (1, 1.0 - w))
        candidates.append({"id": f"R{10+i}", "text": f"C{i}", "similarity": w, "embedding": c})

    left = _batch(1, "X", 0, candidates)
    right = _batch(2, "X", 1, [])

    bridges, scores = _select_bridge_requirements(left, right)
    assert len(bridges) == 3


def test_bridge_requirements_appear_in_both_batches():
    """T018: Selected bridge requirements appear in the requirements list of both adjacent batches."""
    from raa.nodes.overlap_bridging import apply_overlap_bridging

    mid = _unit_vec(_EMBEDDING_DIM, (0, 1.0), (1, 1.0))
    cand = {"id": "R50", "text": "Bridge req", "similarity": 0.85, "embedding": mid}

    b1 = _batch(1, "Shared", 0, [cand])
    b2 = _batch(2, "Shared", 1, [])

    result = apply_overlap_bridging(_state([b1, b2]))
    for b in result["batch_queue"]:
        ids = [r.get("id") for r in b.get("requirements", [])]
        assert "R50" in ids


if __name__ == "__main__":
    ok = _run_tests()
    sys.exit(0 if ok else 1)

