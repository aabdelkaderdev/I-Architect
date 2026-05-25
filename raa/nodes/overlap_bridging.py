"""
Phase 3 node: Overlap bridging (FR-4).

Identifies related batch pairs via shared cluster ID or centroid similarity,
then injects shared non-ASR bridge requirements between pairs to preserve
cross-batch context.
"""
from __future__ import annotations

import logging
import re

from langchain_core.runnables import RunnableConfig

from raa.state.schemas import RAAState
from raa.utils.constants import MAX_BRIDGE_REQUIREMENTS, NON_ASR_SIMILARITY_THRESHOLD
from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity

logger = logging.getLogger(__name__)

_GROUP_ID_RE = re.compile(r"^cluster_(?P<cluster>-?\d+)_group_")


def bridge_overlaps(state: RAAState, config: RunnableConfig) -> dict:
    """Detect related batch pairs and inject shared bridge requirements.

    Config keys expected in ``config["configurable"]``:
        ``non_asr_db_path``

    Returns:
        dict with keys ``batches`` and ``bridge_requirements``.
    """
    configurable = config.get("configurable")
    if configurable is None:
        raise KeyError("RunnableConfig is missing 'configurable' key")
    if "non_asr_db_path" not in configurable:
        raise KeyError("Missing required configurable key: 'non_asr_db_path'")

    non_asr_db_path = configurable["non_asr_db_path"]
    model_name = configurable.get("embedding_model_name", "overlap-bridging")

    batches = state.get("batches") or []
    if not batches:
        return {"batches": [], "bridge_requirements": []}

    normalized_non_asr = state.get("normalized_non_asr") or []
    non_asr_lookup = {r["id"]: r for r in normalized_non_asr if "id" in r}

    # Copy batches to avoid mutating input
    bridged_batches = [_copy_batch(b) for b in batches]

    with EmbeddingCache(non_asr_db_path, model_name) as non_asr_cache:
        related_pairs = _find_related_pairs(bridged_batches)

        bridge_records = []
        for idx_a, idx_b, reason in related_pairs:
            batch_a = bridged_batches[idx_a]
            batch_b = bridged_batches[idx_b]

            candidates = _score_bridge_candidates(
                batch_a["centroid"],
                batch_b["centroid"],
                non_asr_cache,
                threshold=NON_ASR_SIMILARITY_THRESHOLD,
                max_candidates=MAX_BRIDGE_REQUIREMENTS,
            )

            for bridge_id, sim_a, sim_b in candidates:
                _inject_bridge(batch_a, bridge_id, sim_a, non_asr_lookup)
                _inject_bridge(batch_b, bridge_id, sim_b, non_asr_lookup)

                bridge_records.append({
                    "requirement_id": bridge_id,
                    "batch_ids": [batch_a["group_id"], batch_b["group_id"]],
                    "similarity_scores": {
                        batch_a["group_id"]: sim_a,
                        batch_b["group_id"]: sim_b,
                    },
                    "reason": reason,
                })

    return {"batches": bridged_batches, "bridge_requirements": bridge_records}


# ── Private helpers ─────────────────────────────────────────────────────────


def _parse_cluster_id(group_id: str) -> int | None:
    """Extract the cluster number from a group_id like ``cluster_0_group_0``."""
    m = _GROUP_ID_RE.match(group_id)
    if m is None:
        return None
    return int(m.group("cluster"))


def _find_related_pairs(batches: list[dict]) -> list[tuple[int, int, str]]:
    """Return (idx_a, idx_b, reason) for related batch pairs.

    A pair is related when batches share the same parsed cluster ID or
    have centroid cosine similarity >= NON_ASR_SIMILARITY_THRESHOLD.
    """
    n = len(batches)
    pairs: list[tuple[int, int, str]] = []

    for i in range(n):
        for j in range(i + 1, n):
            cluster_i = _parse_cluster_id(batches[i].get("group_id", ""))
            cluster_j = _parse_cluster_id(batches[j].get("group_id", ""))

            if cluster_i is not None and cluster_j is not None and cluster_i == cluster_j:
                pairs.append((i, j, "shared_cluster"))
                continue

            sim = cosine_similarity(batches[i]["centroid"], batches[j]["centroid"])
            if sim >= NON_ASR_SIMILARITY_THRESHOLD:
                pairs.append((i, j, "centroid_similarity"))

    return pairs


def _score_bridge_candidates(
    centroid_a: list[float],
    centroid_b: list[float],
    non_asr_cache: EmbeddingCache,
    threshold: float,
    max_candidates: int,
) -> list[tuple[str, float, float]]:
    """Score non-ASR candidates against both centroids.

    Returns up to ``max_candidates`` (req_id, sim_a, sim_b) tuples sorted by
    descending min(sim_a, sim_b), then descending average, then ascending ID.
    """
    scored: list[tuple[float, float, float, str]] = []

    for req_id, vec in non_asr_cache.iter_all_vectors():
        sim_a = cosine_similarity(centroid_a, vec)
        sim_b = cosine_similarity(centroid_b, vec)
        if sim_a >= threshold and sim_b >= threshold:
            min_sim = min(sim_a, sim_b)
            avg_sim = (sim_a + sim_b) / 2.0
            scored.append((min_sim, avg_sim, sim_a, sim_b, req_id))

    # Sort: descending min_sim, descending avg_sim, ascending req_id
    scored.sort(key=lambda x: (-x[0], -x[1], x[4]))

    return [(req_id, float(sim_a), float(sim_b))
            for _, _, sim_a, sim_b, req_id in scored[:max_candidates]]


def _inject_bridge(
    batch: dict,
    bridge_id: str,
    similarity: float,
    non_asr_lookup: dict[str, dict],
) -> None:
    """Inject a bridge requirement into a batch, mutating it in place."""
    if bridge_id not in batch["non_asr_ids"]:
        batch["non_asr_ids"].append(bridge_id)

    rec = non_asr_lookup.get(bridge_id)
    if rec is not None and rec not in batch["non_asr_records"]:
        batch["non_asr_records"].append(rec)

    batch["similarity_scores"][bridge_id] = similarity

    if "bridge_ids" not in batch:
        batch["bridge_ids"] = []
    if bridge_id not in batch["bridge_ids"]:
        batch["bridge_ids"].append(bridge_id)


def _copy_batch(batch: dict) -> dict:
    """Shallow-copy a batch with deep copies of mutable collections."""
    return {
        "group_id": batch["group_id"],
        "centroid": list(batch["centroid"]),
        "asr_ids": list(batch.get("asr_ids", [])),
        "asr_records": list(batch.get("asr_records", [])),
        "non_asr_ids": list(batch.get("non_asr_ids", [])),
        "non_asr_records": list(batch.get("non_asr_records", [])),
        "similarity_scores": dict(batch.get("similarity_scores", {})),
    }
