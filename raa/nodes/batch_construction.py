"""
Phase 2 node: Centroid-anchored batch construction (FR-3).

Assembles requirement batches by computing group ASR centroids and
retrieving nearest-neighbor non-ASR candidates via cosine similarity
from the SQLite embedding cache.
"""
from __future__ import annotations

import logging

from langchain_core.runnables import RunnableConfig

from raa.state.schemas import RAAState
from raa.utils.constants import EMBEDDING_DIM, MAX_NON_ASR_PER_BATCH, NON_ASR_SIMILARITY_THRESHOLD
from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity

logger = logging.getLogger(__name__)


def build_batches(state: RAAState, config: RunnableConfig) -> dict:
    """Assemble requirement batches from ARLO condition groups and cached embeddings.

    For each condition group:
    1. Retrieve ASR embedding vectors and compute the element-wise mean centroid.
    2. Full-scan the non-ASR embedding cache for cosine similarity ≥ threshold.
    3. Select top-N non-ASRs (capped at ``MAX_NON_ASR_PER_BATCH``).
    4. Assemble a batch dict with group metadata and requirement records.

    Config keys expected in ``config["configurable"]``:
        ``asr_db_path``, ``non_asr_db_path``

    Returns:
        dict with key ``batches`` — list of batch dicts, one per condition group.
    """
    configurable = config.get("configurable")
    if configurable is None:
        raise KeyError("RunnableConfig is missing 'configurable' key")

    missing = [k for k in ("asr_db_path", "non_asr_db_path") if k not in configurable]
    if missing:
        raise KeyError(f"Missing required configurable paths: {', '.join(missing)}")

    asr_db_path = configurable["asr_db_path"]
    non_asr_db_path = configurable["non_asr_db_path"]
    model_name = configurable.get("embedding_model_name", "batch-construction")

    condition_groups = state.get("condition_groups") or []
    normalized_non_asr = state.get("normalized_non_asr") or []

    # O(1) lookup for non-ASR record enrichment
    non_asr_lookup = {r["id"]: r for r in normalized_non_asr if "id" in r}

    with EmbeddingCache(asr_db_path, model_name) as asr_cache, \
         EmbeddingCache(non_asr_db_path, model_name) as non_asr_cache:

        cluster_counters: dict[int, int] = {}
        batches = []
        for group in condition_groups:
            cluster = group.get("cluster", -1)
            group_cnt = cluster_counters.get(cluster, 0)
            cluster_counters[cluster] = group_cnt + 1
            
            batch = _build_single_batch(
                group=group,
                group_cnt=group_cnt,
                asr_cache=asr_cache,
                non_asr_cache=non_asr_cache,
                non_asr_lookup=non_asr_lookup,
            )
            batches.append(batch)

    return {"batches": batches}


def _build_single_batch(
    group: dict,
    group_cnt: int,
    asr_cache: EmbeddingCache,
    non_asr_cache: EmbeddingCache,
    non_asr_lookup: dict[str, dict],
) -> dict:
    """Build a single batch for one condition group."""
    cluster = group.get("cluster", -1)
    group_id = f"cluster_{cluster}_group_{group_cnt}"

    # ── 1. Retrieve ASR vectors and compute centroid ──────────────────────
    asr_vectors, asr_ids, asr_records = _collect_asr_vectors(
        group.get("requirements", []), asr_cache
    )
    centroid = _compute_centroid(asr_vectors)

    # ── 2. Nearest-neighbor non-ASR scan ──────────────────────────────────
    selected_ids, similarity_scores = _select_non_asr_candidates(
        centroid=centroid,
        non_asr_cache=non_asr_cache,
        threshold=NON_ASR_SIMILARITY_THRESHOLD,
        max_candidates=MAX_NON_ASR_PER_BATCH,
    )

    # ── 3. Enrich with full non-ASR records ───────────────────────────────
    non_asr_records = []
    for req_id in selected_ids:
        rec = non_asr_lookup.get(req_id)
        if rec is not None:
            non_asr_records.append(rec)
        else:
            logger.warning("Non-ASR %s has embedding but no normalized record", req_id)

    return {
        "group_id": group_id,
        "centroid": centroid,
        "asr_ids": asr_ids,
        "asr_records": asr_records,
        "non_asr_ids": selected_ids,
        "non_asr_records": non_asr_records,
        "similarity_scores": similarity_scores,
    }


# ── Private helpers ─────────────────────────────────────────────────────────


def _collect_asr_vectors(
    asr_requirements: list[dict],
    asr_cache: EmbeddingCache,
) -> tuple[list[list[float]], list[str], list[dict]]:
    """Retrieve embedding vectors for ASR requirements in a group.

    Returns:
        (vectors, ids, records) — ASRs missing cached vectors are excluded
        with a logged warning.
    """
    vectors: list[list[float]] = []
    ids: list[str] = []
    records: list[dict] = []

    for asr in asr_requirements:
        asr_id = asr.get("id")
        if not asr_id:
            logger.warning("ASR record missing 'id' key: %r", asr)
            continue
        vec = asr_cache.get_vector(asr_id)
        if vec is None:
            logger.warning("ASR %s has no cached embedding — excluded from centroid", asr_id)
            continue
        vectors.append(vec)
        ids.append(asr_id)
        records.append(asr)

    return vectors, ids, records


def _compute_centroid(vectors: list[list[float]]) -> list[float]:
    """Element-wise mean of N vectors.

    Returns an all-zero vector of EMBEDDING_DIM dimension when the input list is empty.
    """
    if not vectors:
        return [0.0] * EMBEDDING_DIM
    n = len(vectors)
    return [sum(dims) / n for dims in zip(*vectors)]


def _select_non_asr_candidates(
    centroid: list[float],
    non_asr_cache: EmbeddingCache,
    threshold: float,
    max_candidates: int,
) -> tuple[list[str], dict[str, float]]:
    """Scan non-ASR cache for cosine similarity >= threshold.

    Returns (selected_ids, similarity_scores) sorted by similarity descending.
    """
    if not centroid or not any(centroid):
        return [], {}

    scored: list[tuple[float, str]] = []

    for req_id, vec in non_asr_cache.iter_all_vectors():
        sim = cosine_similarity(centroid, vec)
        if sim >= threshold:
            scored.append((sim, req_id))

    if not scored:
        return [], {}

    # Filter, sort, cap
    scored.sort(key=lambda x: x[0], reverse=True)
    scored = scored[:max_candidates]

    selected_ids = [rid for _, rid in scored]
    similarity_scores = {rid: float(s) for s, rid in scored}
    return selected_ids, similarity_scores
