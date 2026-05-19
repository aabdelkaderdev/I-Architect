"""Unit tests for raa/nodes/batch_queue.py — batch queue ordering."""

import sys


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
def _req(req_id: str, is_asr: bool = True, quality_attrs=None) -> dict:
    """A requirement payload with optional quality attributes."""
    r = {"id": req_id, "text": f"Requirement {req_id}", "is_asr": is_asr}
    if quality_attrs:
        r["quality_attributes"] = quality_attrs
    return r


def _batch(gid: int, reqs=None) -> dict:
    if reqs is None:
        reqs = []
    return {
        "batch_id": gid,
        "group_id": gid,
        "requirement_ids": [r["id"] for r in reqs],
        "requirements": reqs,
        "similarity_scores": {},
        "group_centroid": [],
        "reduced_confidence": False,
        "cluster": [],
        "non_asr_candidates": [],
    }


def _state(queues=None, strategy=None, quality_weights=None, asrs=None):
    return {
        "batch_queue": queues or [],
        "batch_ordering_strategy": strategy,
        "quality_weights": quality_weights or {},
        "asrs": asrs or [],
        "non_asr": [], "condition_groups": [],
        "batch_cursor": 0, "batch_outputs": {},
        "best_batch_output": {}, "running_arch_model": None,
        "open_questions": [], "bridge_requirements": {},
        "incoherent_batches": [], "embeddings_ready": True,
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
# T013: risk_first default ordering
# ---------------------------------------------------------------------------
def test_risk_first_ordering():
    from raa.nodes.batch_queue import order_batch_queue

    asrs = [
        {"id": "R1", "quality_attributes": ["Security"]},
        {"id": "R2", "quality_attributes": ["Performance"]},
        {"id": "R3", "quality_attributes": ["Reliability"]},
        {"id": "R4", "quality_attributes": ["Usability"]},
    ]

    b1 = _batch(1, [_req("R1", quality_attrs=["Security"])])
    b2 = _batch(2, [_req("R4", quality_attrs=["Usability"])])
    b3 = _batch(3, [_req("R3", quality_attrs=["Reliability"])])
    b4 = _batch(4, [_req("R2", quality_attrs=["Performance"])])

    result = order_batch_queue(_state([b1, b2, b3, b4], asrs=asrs))
    ordered = result["batch_queue"]
    gids = [b["group_id"] for b in ordered]
    # Security(4) = 1, Reliability(3) = 3, Performance(2) = 4, Usability(1) = 2
    assert gids[0] == 1, f"Security should be first, got {gids}"
    assert gids[1] == 3, f"Reliability should be second, got {gids}"
    assert gids[2] == 4, f"Performance should be third, got {gids}"
    assert gids[3] == 2, f"Usability should be fourth, got {gids}"


# ---------------------------------------------------------------------------
# T014: asr_count strategy
# ---------------------------------------------------------------------------
def test_asr_count_ordering():
    from raa.nodes.batch_queue import order_batch_queue

    asrs = [{"id": f"R{i}"} for i in range(1, 8)]

    b1 = _batch(1, [_req("R1"), _req("R2"), _req("R3")])  # 3 ASRs
    b2 = _batch(2, [_req("R4")])                            # 1 ASR
    b3 = _batch(3, [_req("R5"), _req("R6"), _req("R7"), _req("R8", is_asr=False)])  # 3 ASR + 1 non

    result = order_batch_queue(_state([b1, b2, b3], strategy="asr_count", asrs=asrs))
    ordered = result["batch_queue"]
    # b1=3, b2=1, b3=3 — ties broken by group_id ascending → b1 first, then b3
    assert ordered[0]["group_id"] == 1  # 3 ASRs, lower gid
    assert ordered[1]["group_id"] == 3  # 3 ASRs
    assert ordered[2]["group_id"] == 2  # 1 ASR


# ---------------------------------------------------------------------------
# T015: quality_weight strategy
# ---------------------------------------------------------------------------
def test_quality_weight_ordering():
    from raa.nodes.batch_queue import order_batch_queue

    asrs = [
        {"id": "R1", "quality_attributes": ["Security"]},
        {"id": "R2", "quality_attributes": ["Performance"]},
        {"id": "R3", "quality_attributes": ["Usability"]},
    ]
    weights = {"Security": 5, "Performance": 2, "Usability": 1}

    b1 = _batch(1, [_req("R1", quality_attrs=["Security"])])
    b2 = _batch(2, [_req("R2", quality_attrs=["Performance"])])
    b3 = _batch(3, [_req("R3", quality_attrs=["Usability"])])

    result = order_batch_queue(_state([b1, b2, b3], strategy="quality_weight",
                                      quality_weights=weights, asrs=asrs))
    ordered = result["batch_queue"]
    # Security=5 > Performance=2 > Usability=1
    assert ordered[0]["group_id"] == 1
    assert ordered[1]["group_id"] == 2
    assert ordered[2]["group_id"] == 3


# ---------------------------------------------------------------------------
# T016: Sorting metadata on every batch
# ---------------------------------------------------------------------------
def test_sorting_metadata_present():
    from raa.nodes.batch_queue import order_batch_queue

    asrs = [{"id": "R1"}]
    b = _batch(1, [_req("R1")])
    result = order_batch_queue(_state([b], asrs=asrs))

    for batch in result["batch_queue"]:
        sm = batch.get("sorting_metadata")
        assert sm is not None, "Missing sorting_metadata"
        assert "score" in sm
        assert "strategy" in sm
        assert "tie_breaker" in sm


# ---------------------------------------------------------------------------
# T017: Tie-breaking by group_id
# ---------------------------------------------------------------------------
def test_tie_breaking_deterministic():
    from raa.nodes.batch_queue import order_batch_queue

    asrs = [{"id": "R1"}]
    # Same score (same ASR count) → ordered by group_id
    b5 = _batch(5, [_req("R1")])
    b2 = _batch(2, [_req("R1")])
    b9 = _batch(9, [_req("R1")])

    result = order_batch_queue(_state([b5, b2, b9], strategy="asr_count", asrs=asrs))
    ordered = result["batch_queue"]
    gids = [b["group_id"] for b in ordered]
    assert gids == [2, 5, 9], f"Expected [2,5,9], got {gids}"


# ---------------------------------------------------------------------------
# T018: Invalid strategy falls back to risk_first
# ---------------------------------------------------------------------------
def test_invalid_strategy_fallback():
    from raa.nodes.batch_queue import order_batch_queue

    asrs = [
        {"id": "R1", "quality_attributes": ["Security"]},
        {"id": "R2", "quality_attributes": ["Usability"]},
    ]
    b1 = _batch(1, [_req("R1", quality_attrs=["Security"])])
    b2 = _batch(2, [_req("R2", quality_attrs=["Usability"])])

    result = order_batch_queue(_state([b1, b2], strategy="nonexistent_strategy", asrs=asrs))
    ordered = result["batch_queue"]
    # Should use risk_first → Security(4) first
    assert ordered[0]["group_id"] == 1
    sm = ordered[0]["sorting_metadata"]
    assert sm["strategy"] == "risk_first"


# ---------------------------------------------------------------------------
# T019: Returns only batch_queue
# ---------------------------------------------------------------------------
def test_order_batch_queue_returns_batch_queue():
    from raa.nodes.batch_queue import order_batch_queue

    asrs = [{"id": "R1"}]
    b = _batch(1, [_req("R1")])
    result = order_batch_queue(_state([b], asrs=asrs))
    assert "batch_queue" in result
    assert len(result["batch_queue"]) == 1
    # Preserves original fields
    ob = result["batch_queue"][0]
    assert ob["group_id"] == 1


# ---------------------------------------------------------------------------
# T020: Empty queue
# ---------------------------------------------------------------------------
def test_empty_batch_queue():
    from raa.nodes.batch_queue import order_batch_queue
    result = order_batch_queue(_state([]))
    assert result["batch_queue"] == []


if __name__ == "__main__":
    ok = _run_tests()
    sys.exit(0 if ok else 1)
