"""RAA overlap bridging node — inject shared bridge requirements between adjacent batches.

Section 9 of RAA_Plan.md.  After batch construction, this node:
1. Detects adjacent batch pairs (cluster match or centroid cosine >= 0.50).
2. Collects non-ASR candidates from both batches.
3. Scores candidates by dual-centroid multiplicative similarity.
4. Selects up to 3 bridge requirements per pair.
5. Injects bridge payloads into both batches.
6. Records selected IDs in ``bridge_requirements``.
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)

ADJACENCY_THRESHOLD = 0.50
BRIDGE_SIMILARITY_THRESHOLD = 0.0
MAX_BRIDGE_REQUIREMENTS = 3


# ---------------------------------------------------------------------------
# Vector helpers
# ---------------------------------------------------------------------------
def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity (dot product, assumes L2-normalized vectors)."""
    return float(np.dot(np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)))


# ---------------------------------------------------------------------------
# Cluster metadata
# ---------------------------------------------------------------------------
def _batch_cluster(batch: dict) -> object | None:
    """Return the first cluster label from *batch*, or None."""
    cluster = batch.get("cluster")
    if cluster and isinstance(cluster, list) and len(cluster) > 0:
        return cluster[0]
    return None


# ---------------------------------------------------------------------------
# Adjacency
# ---------------------------------------------------------------------------
def _are_adjacent(
    left: dict,
    right: dict,
    threshold: float = ADJACENCY_THRESHOLD,
) -> bool:
    """True when two batches are adjacent by cluster ID or centroid similarity."""
    # 1. Same cluster label
    lc = _batch_cluster(left)
    rc = _batch_cluster(right)
    if lc is not None and rc is not None and lc == rc:
        return True

    # 2. Centroid cosine similarity
    left_c = left.get("group_centroid")
    right_c = right.get("group_centroid")
    if left_c and right_c:
        return _cosine_similarity(left_c, right_c) >= threshold

    return False


def _adjacent_pairs(batches: list[dict]) -> list[tuple[int, int]]:
    """Return index-pairs of adjacent batches.  No duplicates, no self-pairs."""
    pairs: list[tuple[int, int]] = []
    n = len(batches)
    for i in range(n):
        for j in range(i + 1, n):
            if _are_adjacent(batches[i], batches[j]):
                pairs.append((i, j))
    return pairs


# ---------------------------------------------------------------------------
# Candidate pool
# ---------------------------------------------------------------------------
def _candidate_pool(left: dict, right: dict) -> list[dict]:
    """Collect unique non-ASR candidates from both batches."""
    seen: set[str] = set()
    pool: list[dict] = []
    for batch in (left, right):
        for c in batch.get("non_asr_candidates", []):
            cid = str(c.get("id", ""))
            if cid and cid not in seen:
                seen.add(cid)
                pool.append(c)
    return pool


def _candidate_embedding(candidate: dict) -> list[float] | None:
    """Return a candidate's embedding vector when stored on the payload."""
    emb = candidate.get("embedding")
    if emb is not None:
        return emb
    # Also check alternate key names
    for key in ("vector", "emb"):
        val = candidate.get(key)
        if val is not None:
            return val
    return None


# ---------------------------------------------------------------------------
# Bridge scoring & selection
# ---------------------------------------------------------------------------
def _bridge_score(
    candidate: dict,
    left_centroid: list[float],
    right_centroid: list[float],
) -> float:
    """Dual-centroid multiplicative bridge score.

    Returns -1.0 when the candidate has no stored embedding (can't score).
    """
    emb = _candidate_embedding(candidate)
    if emb is None:
        return -1.0
    s1 = _cosine_similarity(emb, left_centroid)
    s2 = _cosine_similarity(emb, right_centroid)
    if s1 <= BRIDGE_SIMILARITY_THRESHOLD or s2 <= BRIDGE_SIMILARITY_THRESHOLD:
        return -1.0
    return s1 * s2


def _select_bridge_requirements(
    left: dict,
    right: dict,
) -> tuple[list[dict], dict[str, float]]:
    """Select up to MAX_BRIDGE_REQUIREMENTS bridge candidates and their scores."""
    pool = _candidate_pool(left, right)
    left_c = left.get("group_centroid", [])
    right_c = right.get("group_centroid", [])

    scored: list[tuple[dict, float]] = []
    for c in pool:
        s = _bridge_score(c, left_c, right_c)
        if s > BRIDGE_SIMILARITY_THRESHOLD:
            scored.append((c, s))

    scored.sort(key=lambda x: x[1], reverse=True)
    selected = scored[:MAX_BRIDGE_REQUIREMENTS]
    bridges = [c for c, _ in selected]
    scores = {str(c["id"]): s for c, s in selected}
    return bridges, scores


# ---------------------------------------------------------------------------
# ID helpers
# ---------------------------------------------------------------------------
def _requirement_id(requirement: dict) -> str:
    """Normalise a requirement ID to a string."""
    rid = requirement.get("id")
    return str(rid) if rid is not None else ""


# ---------------------------------------------------------------------------
# Batch injection
# ---------------------------------------------------------------------------
def _inject_bridge_requirements(
    batch: dict,
    bridges: list[dict],
    pair_scores: dict[str, float],
) -> dict:
    """Return a shallow copy of *batch* with bridge payloads appended.

    Duplicates are skipped — a bridge already present in the batch is not re-added.
    """
    updated = {**batch}
    existing_ids: set[str] = {
        str(r.get("id", "")) for r in updated.get("requirements", [])
    }

    new_reqs: list[dict] = []
    new_ids: list[str] = []
    new_scores: dict[str, float] = {}

    for bridge in bridges:
        bid = _requirement_id(bridge)
        if bid and bid not in existing_ids:
            new_reqs.append(bridge)
            new_ids.append(bid)
            new_scores[bid] = pair_scores.get(bid, bridge.get("similarity", 0.0))
            existing_ids.add(bid)

    if new_reqs:
        updated["requirements"] = list(updated.get("requirements", [])) + new_reqs
        updated["requirement_ids"] = list(updated.get("requirement_ids", [])) + new_ids
        merged_scores = {**updated.get("similarity_scores", {})}
        merged_scores.update(new_scores)
        updated["similarity_scores"] = merged_scores

    return updated


# ---------------------------------------------------------------------------
# Pair key for registry
# ---------------------------------------------------------------------------
def _bridge_pair_key(left: dict, right: dict) -> tuple:
    """Stable-sorted tuple of adjacent batch group IDs."""
    ids = (left.get("group_id"), right.get("group_id"))
    return tuple(sorted(ids))


# ---------------------------------------------------------------------------
# Node entry point
# ---------------------------------------------------------------------------
def apply_overlap_bridging(state: dict) -> dict:
    """Node: detect adjacent batch pairs and inject bridge requirements.

    Reads ``batch_queue`` from the RAA state.  Returns updated
    ``batch_queue`` and ``bridge_requirements`` mapping pair-keys to
    selected bridge requirement IDs.
    """
    batch_queue: list[dict] = list(state.get("batch_queue", []))
    bridge_requirements: dict[tuple, list[str]] = {}

    pairs = _adjacent_pairs(batch_queue)
    if not pairs:
        logger.info("No adjacent batch pairs found.")
        return {
            "batch_queue": batch_queue,
            "bridge_requirements": bridge_requirements,
        }

    for i, j in pairs:
        left = batch_queue[i]
        right = batch_queue[j]

        bridges, pair_scores = _select_bridge_requirements(left, right)

        if bridges:
            pair_key = _bridge_pair_key(left, right)
            bridge_ids = [_requirement_id(b) for b in bridges]
            bridge_requirements[pair_key] = bridge_ids

            batch_queue[i] = _inject_bridge_requirements(left, bridges, pair_scores)
            batch_queue[j] = _inject_bridge_requirements(right, bridges, pair_scores)

            logger.info(
                "Bridged pair %s with %d requirements: %s",
                pair_key,
                len(bridge_ids),
                bridge_ids,
            )
        else:
            logger.debug("No qualifying bridges for pair (%d, %d).", i, j)

    return {
        "batch_queue": batch_queue,
        "bridge_requirements": bridge_requirements,
    }
