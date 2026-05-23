"""
Phase 4 node: Coherence gating (FR-5).

Scores each batch's semantic coherence and splits batches that fall below
the coherence threshold. Reduced-confidence batches are flagged for the
RAA-A / Judge path in Story 2.1.
"""
from __future__ import annotations

import logging

from langchain_core.runnables import RunnableConfig

from raa.state.schemas import RAAState
from raa.utils.constants import COHERENCE_THRESHOLD, EMBEDDING_DIM
from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity

logger = logging.getLogger(__name__)


def gate_batch_coherence(state: RAAState, config: RunnableConfig) -> dict:
    """Score batch coherence and split batches below threshold.

    Config keys expected in ``config["configurable"]``:
        ``asr_db_path``, ``non_asr_db_path``

    Returns:
        dict with keys ``batches`` and ``incoherent_batches``.
    """
    configurable = config.get("configurable")
    if configurable is None:
        raise KeyError("RunnableConfig is missing 'configurable' key")

    missing = [k for k in ("asr_db_path", "non_asr_db_path") if k not in configurable]
    if missing:
        raise KeyError(f"Missing required configurable paths: {', '.join(missing)}")

    asr_db_path = configurable["asr_db_path"]
    non_asr_db_path = configurable["non_asr_db_path"]
    model_name = configurable.get("embedding_model_name", "coherence-gate")

    batches = state.get("batches") or []
    if not batches:
        return {"batches": [], "incoherent_batches": []}

    with EmbeddingCache(asr_db_path, model_name) as asr_cache, \
         EmbeddingCache(non_asr_db_path, model_name) as non_asr_cache:

        gated_batches = []
        incoherent_records = []

        for batch in batches:
            _process_batch(
                batch, asr_cache, non_asr_cache,
                gated_batches, incoherent_records,
            )

    return {"batches": gated_batches, "incoherent_batches": incoherent_records}


# ── Private helpers ─────────────────────────────────────────────────────────


def _compute_coherence_score(
    batch: dict,
    asr_cache: EmbeddingCache,
    non_asr_cache: EmbeddingCache,
) -> float:
    """Compute mean cosine similarity of all available requirement vectors to the batch centroid."""
    similarities: list[float] = []

    for req_id in batch.get("asr_ids", []):
        vec = asr_cache.get_vector(req_id)
        if vec is not None:
            similarities.append(cosine_similarity(batch["centroid"], vec))
        else:
            logger.warning("ASR %s has no cached embedding — excluded from coherence", req_id)

    for req_id in batch.get("non_asr_ids", []):
        vec = non_asr_cache.get_vector(req_id)
        if vec is not None:
            similarities.append(cosine_similarity(batch["centroid"], vec))
        else:
            logger.warning("Non-ASR %s has no cached embedding — excluded from coherence", req_id)

    if not similarities:
        return 0.0
    return sum(similarities) / len(similarities)


def _gather_vector_entries(
    batch: dict,
    asr_cache: EmbeddingCache,
    non_asr_cache: EmbeddingCache,
) -> list[tuple[str, str, dict, list[float]]]:
    """Collect (req_id, kind, record, vector) for all available requirement vectors."""
    entries: list[tuple[str, str, dict, list[float]]] = []

    asr_lookup = {r["id"]: r for r in batch.get("asr_records", []) if "id" in r}
    for req_id in batch.get("asr_ids", []):
        vec = asr_cache.get_vector(req_id)
        if vec is not None:
            entries.append((req_id, "asr", asr_lookup.get(req_id, {}), vec))
        else:
            logger.warning("ASR %s has no cached embedding — excluded from split", req_id)

    non_asr_lookup = {r["id"]: r for r in batch.get("non_asr_records", []) if "id" in r}
    for req_id in batch.get("non_asr_ids", []):
        vec = non_asr_cache.get_vector(req_id)
        if vec is not None:
            entries.append((req_id, "non_asr", non_asr_lookup.get(req_id, {}), vec))
        else:
            logger.warning("Non-ASR %s has no cached embedding — excluded from split", req_id)

    return entries


def _build_sub_batch(
    entries: list[tuple[str, str, dict, list[float]]],
    group_id: str,
    source_group_id: str,
) -> dict:
    """Build a sub-batch dict from assigned vector entries."""
    asr_ids: list[str] = []
    asr_records: list[dict] = []
    non_asr_ids: list[str] = []
    non_asr_records: list[dict] = []
    vectors: list[list[float]] = []

    for req_id, kind, rec, vec in entries:
        vectors.append(vec)
        if kind == "asr":
            asr_ids.append(req_id)
            if rec:
                asr_records.append(rec)
        else:
            non_asr_ids.append(req_id)
            if rec:
                non_asr_records.append(rec)

    # Recompute centroid from ASR vectors when available; fall back to all vectors
    asr_vecs = [v for (_, kind, _, v) in entries if kind == "asr"]
    if asr_vecs:
        centroid = _compute_centroid(asr_vecs)
    elif vectors:
        centroid = _compute_centroid(vectors)
    else:
        centroid = [0.0] * EMBEDDING_DIM

    # Compute similarity scores from centroid for each vector
    similarity_scores = {req_id: cosine_similarity(centroid, vec) for req_id, _, _, vec in entries}

    return {
        "group_id": group_id,
        "centroid": centroid,
        "asr_ids": asr_ids,
        "asr_records": asr_records,
        "non_asr_ids": non_asr_ids,
        "non_asr_records": non_asr_records,
        "similarity_scores": similarity_scores,
        "source_group_id": source_group_id,
    }


def _compute_centroid(vectors: list[list[float]]) -> list[float]:
    """Element-wise mean of N vectors."""
    if not vectors:
        return [0.0] * EMBEDDING_DIM
    n = len(vectors)
    return [sum(dims) / n for dims in zip(*vectors)]


def _process_batch(
    batch: dict,
    asr_cache: EmbeddingCache,
    non_asr_cache: EmbeddingCache,
    gated_batches: list[dict],
    incoherent_records: list[dict],
) -> None:
    """Score, split, or flag a single batch. Appends result to gated_batches."""
    # Copy to avoid mutating input
    b = {
        "group_id": batch["group_id"],
        "centroid": list(batch["centroid"]),
        "asr_ids": list(batch.get("asr_ids", [])),
        "asr_records": list(batch.get("asr_records", [])),
        "non_asr_ids": list(batch.get("non_asr_ids", [])),
        "non_asr_records": list(batch.get("non_asr_records", [])),
        "similarity_scores": dict(batch.get("similarity_scores", {})),
    }
    # Preserve bridge_ids if present
    if "bridge_ids" in batch:
        b["bridge_ids"] = list(batch["bridge_ids"])

    coherence = _compute_coherence_score(b, asr_cache, non_asr_cache)
    b["coherence_score"] = coherence

    if coherence >= COHERENCE_THRESHOLD:
        b["reduced_confidence"] = False
        gated_batches.append(b)
        return

    # Attempt split
    entries = _gather_vector_entries(b, asr_cache, non_asr_cache)
    if len(entries) < 2:
        b["reduced_confidence"] = True
        gated_batches.append(b)
        incoherent_records.append({
            "group_id": batch["group_id"],
            "coherence_score": coherence,
            "reason": "insufficient_vectors_for_split",
        })
        return

    split_a, split_b = _deterministic_split(entries)

    if not split_a or not split_b:
        b["reduced_confidence"] = True
        gated_batches.append(b)
        incoherent_records.append({
            "group_id": batch["group_id"],
            "coherence_score": coherence,
            "reason": "split_produced_empty_side",
        })
        return

    # Rebuild sub-batches
    sub_a = _build_sub_batch(split_a, f"{b['group_id']}_split_0", b["group_id"])
    sub_b = _build_sub_batch(split_b, f"{b['group_id']}_split_1", b["group_id"])

    # Recalculate coherence for each sub-batch using recomputed centroids
    coh_a = _recalc_coherence(sub_a, asr_cache, non_asr_cache)
    coh_b = _recalc_coherence(sub_b, asr_cache, non_asr_cache)

    if coh_a >= COHERENCE_THRESHOLD and coh_b >= COHERENCE_THRESHOLD:
        sub_a["coherence_score"] = coh_a
        sub_a["reduced_confidence"] = False
        sub_b["coherence_score"] = coh_b
        sub_b["reduced_confidence"] = False
        gated_batches.append(sub_a)
        gated_batches.append(sub_b)
    else:
        b["reduced_confidence"] = True
        gated_batches.append(b)
        reasons = []
        if coh_a < COHERENCE_THRESHOLD:
            reasons.append(f"sub_batch_0_coherence={coh_a:.4f}")
        if coh_b < COHERENCE_THRESHOLD:
            reasons.append(f"sub_batch_1_coherence={coh_b:.4f}")
        incoherent_records.append({
            "group_id": batch["group_id"],
            "coherence_score": coherence,
            "reason": "split_sub_batches_below_threshold: " + "; ".join(reasons),
        })


def _recalc_coherence(
    batch: dict,
    asr_cache: EmbeddingCache,
    non_asr_cache: EmbeddingCache,
) -> float:
    """Recompute coherence for a newly built sub-batch against its own centroid."""
    similarities: list[float] = []

    for req_id in batch.get("asr_ids", []):
        vec = asr_cache.get_vector(req_id)
        if vec is not None:
            similarities.append(cosine_similarity(batch["centroid"], vec))

    for req_id in batch.get("non_asr_ids", []):
        vec = non_asr_cache.get_vector(req_id)
        if vec is not None:
            similarities.append(cosine_similarity(batch["centroid"], vec))

    if not similarities:
        return 0.0
    return sum(similarities) / len(similarities)


def _deterministic_split(
    entries: list[tuple[str, str, dict, list[float]]],
) -> tuple[list, list]:
    """Farthest-pair deterministic two-way split.

    1. Find farthest pair by minimum cosine similarity; tie-break by (req_id_a, req_id_b).
    2. Assign every entry to the seed with higher cosine similarity; tie-break to seed 0.
    """
    n = len(entries)
    best_pair = (0, 1)
    best_sim = 2.0  # cos similarity is in [-1, 1]; start above max

    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine_similarity(entries[i][3], entries[j][3])
            if sim < best_sim - 1e-9:
                best_sim = sim
                best_pair = (i, j)
            elif abs(sim - best_sim) < 1e-9:
                # Tie-break by (req_id_a, req_id_b) ascending
                curr = (entries[i][0], entries[j][0])
                best = (entries[best_pair[0]][0], entries[best_pair[1]][0])
                if curr < best:
                    best_pair = (i, j)

    seed_vecs = (entries[best_pair[0]][3], entries[best_pair[1]][3])
    side_a: list = []
    side_b: list = []

    for entry in entries:
        sim_a = cosine_similarity(entry[3], seed_vecs[0])
        sim_b = cosine_similarity(entry[3], seed_vecs[1])
        if sim_a >= sim_b:
            side_a.append(entry)
        else:
            side_b.append(entry)

    return side_a, side_b
