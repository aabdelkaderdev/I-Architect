"""RAA coherence gate — evaluate intra-batch coherence and split incoherent batches.

Section 10 of RAA_Plan.md.  For each batch in the queue this node:
1. Extracts requirement embeddings from batch payloads.
2. Computes the average cosine similarity to the batch centroid.
3. Passes batches with score >= 0.55 (or ≤ 2 requirements) unchanged.
4. Splits low-coherence batches via deterministic 2-way clustering.
5. Keeps the original batch with reduced_confidence=True when splitting fails.
"""

from __future__ import annotations

import logging

import numpy as np

from raa.state.types import IncoherentBatchRecord

logger = logging.getLogger(__name__)

COHERENCE_THRESHOLD = 0.55
MAX_SPLIT_CLUSTERS = 2
MAX_KMEANS_ITERATIONS = 10


# ---------------------------------------------------------------------------
# Vector helpers
# ---------------------------------------------------------------------------
def _as_float_array(vector: list[float]) -> np.ndarray:
    """Convert a list to a float32 array.  Zero-length input → empty array."""
    return np.array(vector, dtype=np.float32)


def _normalize(vector: np.ndarray) -> np.ndarray:
    """L2-normalise a vector.  Zero vectors are returned unchanged."""
    norm = np.linalg.norm(vector)
    if norm == 0.0:
        return vector
    return vector / norm


def _cosine_similarity(
    a: list[float] | np.ndarray,
    b: list[float] | np.ndarray,
) -> float:
    """Cosine similarity (dot product of L2-normalised vectors)."""
    aa = _as_float_array(a) if isinstance(a, list) else a
    bb = _as_float_array(b) if isinstance(b, list) else b
    return float(np.dot(aa, bb))


# ---------------------------------------------------------------------------
# Embedding extraction
# ---------------------------------------------------------------------------
def _requirement_embedding(requirement: dict) -> list[float]:
    """Extract embedding vector from a requirement payload.

    Checks ``embedding`` first, then ``vector``.  Raises ``ValueError``
    when neither key is present.
    """
    for key in ("embedding", "vector"):
        val = requirement.get(key)
        if val is not None:
            return val
    raise ValueError(
        f"Requirement {requirement.get('id', '?')} has no 'embedding' or 'vector' key"
    )


def _batch_embeddings(batch: dict) -> list[list[float]]:
    """Extract embeddings from every requirement in *batch*."""
    reqs = batch.get("requirements", [])
    return [_requirement_embedding(r) for r in reqs]


# ---------------------------------------------------------------------------
# Centroid & coherence scoring
# ---------------------------------------------------------------------------
def _compute_centroid(vectors: list[list[float]]) -> list[float]:
    """Element-wise average followed by L2 normalisation."""
    if not vectors:
        return []
    arr = np.array(vectors, dtype=np.float32)
    avg = np.mean(arr, axis=0)
    return _normalize(avg).tolist()


def _compute_coherence_score(vectors: list[list[float]]) -> float:
    """Average cosine similarity of each vector to the batch centroid.

    Batches with 2 or fewer vectors always score 1.0 (automatic pass).
    """
    if len(vectors) <= 2:
        return 1.0
    centroid = _compute_centroid(vectors)
    sims = [_cosine_similarity(v, centroid) for v in vectors]
    return float(np.mean(sims))


# ---------------------------------------------------------------------------
# Pre-check
# ---------------------------------------------------------------------------
def _should_pass_without_split(batch: dict) -> bool:
    """Batches with 2 or fewer requirements always pass."""
    return len(batch.get("requirements", [])) <= 2


# ---------------------------------------------------------------------------
# Deterministic 2-way split
# ---------------------------------------------------------------------------
def _furthest_pair_indices(vectors: list[list[float]]) -> tuple[int, int]:
    """Return the indices of the two least-similar vectors (seeds for k=2)."""
    arr = np.array(vectors, dtype=np.float32)
    sim = np.dot(arr, arr.T)
    np.fill_diagonal(sim, 2.0)  # exclude self-pairs
    i, j = divmod(int(np.argmin(sim)), len(vectors))
    return (i, j)


def _split_vectors_k2(
    vectors: list[list[float]],
) -> tuple[list[int], list[int]]:
    """Deterministic 2-way vector clustering.

    Seeded from the furthest pair, iterates centroid assignments up to
    ``MAX_KMEANS_ITERATIONS`` times.  Returns two index lists.
    """
    arr = np.array(vectors, dtype=np.float32)
    n = len(arr)

    fi, fj = _furthest_pair_indices(vectors)
    c1 = arr[fi].copy()
    c2 = arr[fj].copy()

    labels = np.full(n, -1, dtype=np.int32)
    for _ in range(MAX_KMEANS_ITERATIONS):
        s1 = np.dot(arr, c1)
        s2 = np.dot(arr, c2)
        new_labels = np.where(s1 >= s2, 0, 1)
        if np.array_equal(labels, new_labels):
            break
        labels = new_labels

        idx1 = np.where(labels == 0)[0]
        idx2 = np.where(labels == 1)[0]
        if len(idx1) == 0 or len(idx2) == 0:
            break

        c1 = _normalize(np.mean(arr[idx1], axis=0))
        c2 = _normalize(np.mean(arr[idx2], axis=0))

    return (np.where(labels == 0)[0].tolist(), np.where(labels == 1)[0].tolist())


# ---------------------------------------------------------------------------
# Sub-batch assembly
# ---------------------------------------------------------------------------
def _build_sub_batch(
    batch: dict,
    selected_indices: list[int],
    sub_index: int,
) -> dict:
    """Build a sub-batch from selected requirement indices."""
    reqs = batch.get("requirements", [])
    ids = batch.get("requirement_ids", [])
    scores = batch.get("similarity_scores", {})

    sub_reqs = [reqs[i] for i in selected_indices]

    sub_ids: list[str] = []
    for i in selected_indices:
        if i < len(ids):
            sub_ids.append(str(ids[i]))
        elif i < len(reqs):
            sub_ids.append(str(reqs[i].get("id", i)))

    sub_scores: dict[str, float] = {}
    for sid in sub_ids:
        if sid in scores:
            sub_scores[sid] = scores[sid]

    vectors = [r.get("embedding") or r.get("vector") for r in sub_reqs]
    coherence = _compute_coherence_score([v for v in vectors if v is not None])

    return {
        "batch_id": batch.get("batch_id"),
        "group_id": batch.get("group_id"),
        "requirement_ids": sub_ids,
        "requirements": sub_reqs,
        "similarity_scores": sub_scores,
        "group_centroid": batch.get("group_centroid"),
        "reduced_confidence": batch.get("reduced_confidence", False),
        "cluster": batch.get("cluster", []),
        "non_asr_candidates": batch.get("non_asr_candidates", []),
        "coherence_score": coherence,
        "is_split": True,
        "source_batch_id": batch.get("batch_id"),
    }


# ---------------------------------------------------------------------------
# Single-batch evaluation
# ---------------------------------------------------------------------------
def _evaluate_batch(
    batch: dict,
) -> tuple[list[dict], IncoherentBatchRecord | None]:
    """Evaluate one batch and return (output_batches, incoherent_record_or_none)."""
    vectors = _batch_embeddings(batch)

    if _should_pass_without_split(batch):
        batch["coherence_score"] = 1.0
        return [batch], None

    score = _compute_coherence_score(vectors)
    batch["coherence_score"] = score

    if score >= COHERENCE_THRESHOLD:
        return [batch], None

    # --- Split ---
    try:
        idx1, idx2 = _split_vectors_k2(vectors)
    except Exception:
        logger.exception("Split failed for batch %s", batch.get("batch_id"))
        batch["reduced_confidence"] = True
        return [batch], IncoherentBatchRecord(
            batch_id=batch.get("batch_id", 0),
            coherence_score=score,
            reduced_confidence=True,
        )

    if len(idx1) == 0 or len(idx2) == 0:
        batch["reduced_confidence"] = True
        return [batch], IncoherentBatchRecord(
            batch_id=batch.get("batch_id", 0),
            coherence_score=score,
            reduced_confidence=True,
        )

    sub1 = _build_sub_batch(batch, idx1, 0)
    sub2 = _build_sub_batch(batch, idx2, 1)

    if (
        sub1.get("coherence_score", 0) >= COHERENCE_THRESHOLD
        and sub2.get("coherence_score", 0) >= COHERENCE_THRESHOLD
    ):
        logger.info(
            "Batch %d split into two coherent sub-batches (%d + %d requirements).",
            batch.get("batch_id"),
            len(idx1),
            len(idx2),
        )
        return [sub1, sub2], None

    # Split failed — one or both sub-batches still incoherent
    batch["reduced_confidence"] = True
    logger.warning(
        "Batch %d split failed — sub-batches still below threshold. "
        "Marking reduced_confidence.",
        batch.get("batch_id"),
    )
    return [batch], IncoherentBatchRecord(
        batch_id=batch.get("batch_id", 0),
        coherence_score=score,
        reduced_confidence=True,
    )


# ---------------------------------------------------------------------------
# Queue renumbering
# ---------------------------------------------------------------------------
def _renumber_batch_queue(batches: list[dict]) -> list[dict]:
    """Assign sequential ``batch_id`` values while preserving ``source_batch_id``."""
    for i, b in enumerate(batches):
        if "source_batch_id" not in b:
            b["source_batch_id"] = b.get("batch_id")
        b["batch_id"] = i
    return batches


# ---------------------------------------------------------------------------
# Node entry point
# ---------------------------------------------------------------------------
def apply_coherence_gate(state: dict) -> dict:
    """Node: evaluate every batch in ``batch_queue`` for coherence.

    Returns updated ``batch_queue`` and ``incoherent_batches`` list.
    """
    batch_queue: list[dict] = list(state.get("batch_queue", []))
    incoherent_batches: list[IncoherentBatchRecord] = list(
        state.get("incoherent_batches", [])
    )

    output_batches: list[dict] = []
    for batch in batch_queue:
        results, record = _evaluate_batch(batch)
        output_batches.extend(results)
        if record is not None:
            incoherent_batches.append(record)

    output_batches = _renumber_batch_queue(output_batches)

    logger.info(
        "Coherence gate: %d batches in → %d out, %d incoherent.",
        len(batch_queue),
        len(output_batches),
        len(incoherent_batches) - len(state.get("incoherent_batches", [])),
    )

    return {
        "batch_queue": output_batches,
        "incoherent_batches": incoherent_batches,
    }
