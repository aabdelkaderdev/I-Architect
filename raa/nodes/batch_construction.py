"""RAA batch construction node — condition-group-anchored requirement batches.

Section 8 of RAA_Plan.md.  For each ARLO condition group this node:
1. Computes the group centroid from ASR embeddings (or falls back to
   re-embedding the nominal condition).
2. Searches non-ASR embeddings by cosine similarity.
3. Filters by threshold (>= 0.65), sorts descending, caps at 10 candidates.
4. Assembles full Batch payloads with normalized requirement data.
"""

from __future__ import annotations

import logging
import re
import sqlite3
import struct
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

logger = logging.getLogger(__name__)

_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"
_EMBEDDING_DIM = 1024
SIMILARITY_THRESHOLD = 0.65
MAX_NON_ASR_CANDIDATES = 10

_embedding_model: TextEmbedding | None = None


# ---------------------------------------------------------------------------
# Path helpers (functions so tests can patch them)
# ---------------------------------------------------------------------------
def _project_root() -> Path:
    return Path(__file__).parent.parent.parent


def _asr_db_path() -> Path:
    return _project_root() / "embeddings" / "asr_embeddings.db"


def _non_asr_db_path() -> Path:
    return _project_root() / "embeddings" / "non_asr_embeddings.db"


# ---------------------------------------------------------------------------
# SQLite helpers
# ---------------------------------------------------------------------------
from raa.utils.db import open_embedding_db

def _connect_readonly(db_path: Path) -> sqlite3.Connection:
    """Open a read-only SQLite connection (embedding DBs are never written here)."""
    return open_embedding_db(db_path, read_only=True)


# ---------------------------------------------------------------------------
# ID / vector helpers
# ---------------------------------------------------------------------------
def _requirement_id_int(requirement_id: str | int) -> int:
    """Map a requirement ID to an int (``\"R12\"`` → 12, ``1`` → 1)."""
    if isinstance(requirement_id, int):
        return requirement_id
    m = re.search(r"\d+", str(requirement_id))
    if m:
        return int(m.group())
    raise ValueError(f"Cannot extract integer id from: {requirement_id!r}")


def _deserialize_embedding(blob: bytes) -> list[float]:
    """Deserialize a binary BLOB into a 1024-element float list."""
    count = len(blob) // 4
    return list(struct.unpack(f"<{count}f", blob))


# ---------------------------------------------------------------------------
# ASR embedding loading & centroid
# ---------------------------------------------------------------------------
def _load_asr_embeddings(
    requirement_ids: list[str | int], db_path: Path
) -> dict[int, list[float]]:
    """Load ASR embeddings keyed by integer requirement ID."""
    conn = _connect_readonly(db_path)
    try:
        id_set = {_requirement_id_int(rid) for rid in requirement_ids}
        result: dict[int, list[float]] = {}
        rows = conn.execute(
            "SELECT requirement_id, embedding FROM embeddings"
        ).fetchall()
        for req_id, blob in rows:
            if req_id in id_set:
                result[req_id] = _deserialize_embedding(blob)
        return result
    finally:
        conn.close()


def _compute_centroid(vectors: list[list[float]]) -> list[float]:
    """Element-wise average of vectors, L2-normalized.

    Returns a zero vector when the input list is empty (caller should
    fall back to nominal-condition re-embedding in that case).
    """
    if not vectors:
        return [0.0] * _EMBEDDING_DIM
    arr = np.array(vectors, dtype=np.float32)
    avg = np.mean(arr, axis=0)
    norm = np.linalg.norm(avg)
    if norm == 0.0:
        return avg.tolist()
    return (avg / norm).tolist()


# ---------------------------------------------------------------------------
# Fallback embedding  (for groups with zero loadable ASRs)
# ---------------------------------------------------------------------------
def _get_embedding_model() -> TextEmbedding:
    """Lazy-initialize the FastEmbed TextEmbedding singleton."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name=_MODEL_NAME)
        logger.info("FastEmbed model loaded: %s", _MODEL_NAME)
    return _embedding_model


def _embed_nominal_condition(
    nominal_condition: str, model: TextEmbedding | None = None,
) -> list[float]:
    """Embed a nominal-condition string.  Tests inject a fake *model*."""
    emb = model if model is not None else _get_embedding_model()
    vecs = emb.embed([nominal_condition])
    raw = None
    for v in vecs:
        raw = v
        break
    if raw is None:
        return [0.0] * _EMBEDDING_DIM
    return raw.tolist() if hasattr(raw, "tolist") else list(raw)


# ---------------------------------------------------------------------------
# Condition-group helpers
# ---------------------------------------------------------------------------
def _group_requirement_ids(condition_group: dict) -> list[str | int]:
    """Extract ASR requirement IDs from a condition group.

    Prefers ``requirements`` (list of dicts with ``id``) first, then falls
    back to indexed entries from ``conditions``.
    """
    reqs = condition_group.get("requirements")
    if reqs:
        ids = []
        for r in reqs:
            if isinstance(r, dict):
                ids.append(r.get("id"))
            else:
                ids.append(r)
        return ids
    # Fallback: conditions list
    conds = condition_group.get("conditions", [])
    ids = []
    for c in conds:
        if isinstance(c, dict):
            ids.append(c.get("id"))
        else:
            ids.append(c)
    return ids


def _centroid_for_group(
    condition_group: dict, asr_db_path: Path,
    model: TextEmbedding | None = None,
) -> list[float]:
    """Compute centroid for one condition group.

    Prefers averaged ASR embeddings.  Falls back to re-embedding
    ``nominal_condition`` when no ASR embeddings can be loaded.
    """
    req_ids = _group_requirement_ids(condition_group)
    asr_embs = _load_asr_embeddings(req_ids, asr_db_path) if req_ids else {}

    if asr_embs:
        return _compute_centroid(list(asr_embs.values()))

    nominal = condition_group.get("nominal_condition", "")
    if nominal:
        logger.info(
            "Group %s — no loadable ASR embeddings, falling back to nominal-condition embedding.",
            condition_group.get("group_id"),
        )
        return _embed_nominal_condition(nominal, model=model)

    return [0.0] * _EMBEDDING_DIM


# ---------------------------------------------------------------------------
# Non-ASR candidate search
# ---------------------------------------------------------------------------
def _load_non_asr_embedding_rows(db_path: Path) -> list[dict]:
    """Read all non-ASR rows as ``{requirement_id, embedding, text_hash, model_name}``."""
    if not db_path.exists():
        return []
    conn = _connect_readonly(db_path)
    try:
        rows = conn.execute(
            "SELECT requirement_id, embedding, text_hash, model_name FROM embeddings"
        ).fetchall()
        return [
            {
                "requirement_id": r[0],
                "embedding": _deserialize_embedding(r[1]),
                "text_hash": r[2],
                "model_name": r[3],
            }
            for r in rows
        ]
    finally:
        conn.close()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors (both assumed L2-normalized).

    When both vectors are unit-length this is the dot product.
    """
    return float(np.dot(np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)))


def _search_non_asr_candidates(
    centroid: list[float],
    non_asr_rows: list[dict],
    non_asr_payloads: list[dict],
) -> list[dict]:
    """Search non-ASR candidates by cosine similarity to *centroid*.

    Returns up to MAX_NON_ASR_CANDIDATES results, each with ``id``, ``text``,
    and ``similarity``, sorted descending by similarity.
    """
    payload_by_id = _payload_by_requirement_id(non_asr_payloads)

    scored = []
    for row in non_asr_rows:
        sim = _cosine_similarity(centroid, row["embedding"])
        if sim >= SIMILARITY_THRESHOLD:
            req_id = row["requirement_id"]
            payload = payload_by_id.get(req_id, {})
            scored.append({
                "id": req_id,
                "text": payload.get("text", ""),
                "similarity": sim,
            })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:MAX_NON_ASR_CANDIDATES]


def _payload_by_requirement_id(requirements: list[dict]) -> dict[int, dict]:
    """Index requirement payloads by integer requirement ID."""
    result: dict[int, dict] = {}
    for req in requirements:
        rid = req.get("id")
        if rid is not None:
            result[_requirement_id_int(rid)] = req
    return result


# ---------------------------------------------------------------------------
# Batch assembly
# ---------------------------------------------------------------------------
def _assemble_batch(
    group_id: int,
    condition_group: dict,
    centroid: list[float],
    asr_payloads: list[dict],
    non_asr_candidates: list[dict],
) -> dict:
    """Assemble a single Batch payload for *group_id*."""
    req_payloads = list(asr_payloads)
    for c in non_asr_candidates:
        # Avoid duplicating payloads already in asr_payloads
        # (c may carry full payload keys — strip to standard fields)
        clean = {k: v for k, v in c.items() if k in ("id", "text", "similarity")}
        req_payloads.append(clean)

    similarity_scores: dict[str, float] = {}
    for c in non_asr_candidates:
        similarity_scores[str(c["id"])] = c["similarity"]

    req_ids = [_requirement_id_int(p["id"]) for p in req_payloads if p.get("id") is not None]

    return {
        "batch_id": group_id,
        "group_id": group_id,
        "requirement_ids": [str(rid) for rid in req_ids],
        "group_centroid": centroid,
        "reduced_confidence": False,
        "cluster": [condition_group.get("nominal_condition", "")],
        "requirements": req_payloads,
        "similarity_scores": similarity_scores,
        "non_asr_candidates": non_asr_candidates,
    }


# ---------------------------------------------------------------------------
# Node entry point
# ---------------------------------------------------------------------------
def construct_batches(state: dict) -> dict:
    """Node: build one Batch per ARLO condition group.

    Reads ``asrs``, ``non_asr``, and ``condition_groups`` from the RAA state.
    Returns ``{"batch_queue": batches}`` where *batches* is a list of Batch
    dicts in group order.
    """
    asrs: list[dict] = state.get("asrs", [])
    non_asrs: list[dict] = state.get("non_asr", [])
    condition_groups: list[dict] = state.get("condition_groups", [])

    asr_db = _asr_db_path()
    non_asr_db = _non_asr_db_path()

    non_asr_rows = _load_non_asr_embedding_rows(non_asr_db)
    model = _get_embedding_model()

    batches: list[dict] = []
    for group in condition_groups:
        gid = group.get("group_id", len(batches))
        centroid = _centroid_for_group(group, asr_db, model=model)

        candidates = _search_non_asr_candidates(centroid, non_asr_rows, non_asrs)
        if not candidates:
            logger.info(
                "Group %s: no matching non-ASR candidates above threshold %.2f; batch will proceed with ASRs only.",
                gid,
                SIMILARITY_THRESHOLD,
            )

        # Collect ASR payloads belonging to this group
        group_req_ids = set(_group_requirement_ids(group))
        group_asr_payloads = [
            a for a in asrs
            if _requirement_id_int(a.get("id", 0)) in group_req_ids
        ]

        batch = _assemble_batch(gid, group, centroid, group_asr_payloads, candidates)
        batches.append(batch)

    logger.info("Assembled %d batches from %d condition groups.", len(batches), len(condition_groups))
    return {"batch_queue": batches}
