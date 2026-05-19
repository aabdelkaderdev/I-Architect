"""RAA preparation node — ASR embedding verification and non-ASR embedding persistence.

Reads RAAState, verifies every ASR has a row in asr_embeddings.db, generates
non-ASR embeddings for missing or stale rows, persists them to
non_asr_embeddings.db, and returns {"embeddings_ready": True}.

Section 6 of RAA_Plan.md.
"""

from __future__ import annotations

import hashlib
import logging
import re
import sqlite3
import struct
from pathlib import Path

from fastembed import TextEmbedding

from raa.utils.db import open_embedding_db

logger = logging.getLogger(__name__)

_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"
_EMBEDDING_DIM = 1024

_embedding_model: TextEmbedding | None = None


# ---------------------------------------------------------------------------
# Path helpers — functions (not constants) so tests can patch them
# ---------------------------------------------------------------------------
def _project_root() -> Path:
    return Path(__file__).parent.parent.parent


def _asr_db_path() -> Path:
    return _project_root() / "embeddings" / "asr_embeddings.db"


def _non_asr_db_path() -> Path:
    return _project_root() / "embeddings" / "non_asr_embeddings.db"


# ---------------------------------------------------------------------------
# SQLite schema
# ---------------------------------------------------------------------------


def _ensure_embeddings_schema(conn: sqlite3.Connection):
    """Create the shared embeddings table if it does not exist."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS embeddings ("
        "  requirement_id INTEGER PRIMARY KEY,"
        "  embedding BLOB NOT NULL,"
        "  text_hash TEXT NOT NULL,"
        "  model_name TEXT NOT NULL"
        ")"
    )


# ---------------------------------------------------------------------------
# ID / text helpers
# ---------------------------------------------------------------------------
def _requirement_id_int(requirement: dict) -> int:
    """Map a requirement dict to an integer id.

    Handles raw ints ("R12" → 12), string ints ("12" → 12), and raw ints (1 → 1).
    """
    raw = requirement.get("id")
    if raw is None:
        raise ValueError(f"Requirement missing 'id' field: {requirement}")
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        m = re.search(r"\d+", raw)
        if m:
            return int(m.group())
        raise ValueError(f"Cannot extract integer id from: {raw!r}")
    raise TypeError(f"Unexpected id type {type(raw).__name__}: {raw!r}")


def _hash_text(text: str) -> str:
    """SHA-256 hex digest for cache-integrity checks."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _serialize_embedding(vector: list[float]) -> bytes:
    """Pack a 1024-element float list into a binary blob."""
    return struct.pack(f"<{len(vector)}f", *vector)


def _non_asr_text(
    requirement: dict, requirements: dict[str, str] | None = None
) -> str:
    """Extract the text to embed from a non-ASR requirement dict.

    Uses the normalized ``text`` field first. Falls back to a parent
    ``requirements`` lookup dict keyed by requirement id.
    """
    text = requirement.get("text")
    if text:
        return text
    if requirements:
        req_id = requirement.get("id")
        if req_id and req_id in requirements:
            return requirements[req_id]
    return ""


# ---------------------------------------------------------------------------
# Embedding model
# ---------------------------------------------------------------------------
def _get_embedding_model() -> TextEmbedding:
    """Lazy-initialize the FastEmbed TextEmbedding singleton."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name=_MODEL_NAME)
        logger.info("FastEmbed model loaded: %s", _MODEL_NAME)
    return _embedding_model


def _embed_texts(
    texts: list[str], model: TextEmbedding | None = None
) -> list[list[float]]:
    """Embed a list of text strings.

    When *model* is None the module-level singleton is used.  Tests inject
    a fake model via the *model* parameter to avoid downloading FastEmbed.
    """
    if not texts:
        return []
    emb = model if model is not None else _get_embedding_model()
    results = []
    for vec in emb.embed(texts):
        results.append(vec.tolist() if hasattr(vec, "tolist") else list(vec))
    return results


# ---------------------------------------------------------------------------
# ASR verification
# ---------------------------------------------------------------------------
def _verify_asr_embeddings(asrs: list[dict], asr_db_path: Path):
    """Verify every ASR has a row in asr_embeddings.db.

    Raises FileNotFoundError if the database file does not exist.
    Raises RuntimeError if any ASR requirement_id is missing from the DB.
    """
    if not asr_db_path.exists():
        raise FileNotFoundError(
            f"ASR embeddings database not found: {asr_db_path}\n"
            "Re-run ARLO to generate ASR embeddings before running RAA."
        )

    conn = open_embedding_db(asr_db_path, read_only=True)
    try:
        # Check model name consistency
        rows = conn.execute("SELECT DISTINCT model_name FROM embeddings").fetchall()
        for (model_name,) in rows:
            if model_name != _MODEL_NAME:
                raise ValueError(
                    f"ASR embedding database uses model '{model_name}', "
                    f"but expected '{_MODEL_NAME}'"
                )

        existing = set(
            row[0] for row in conn.execute("SELECT requirement_id FROM embeddings")
        )

        missing = []
        for asr in asrs:
            req_id = _requirement_id_int(asr)
            if req_id not in existing:
                missing.append(req_id)

        if missing:
            raise RuntimeError(
                f"Missing ASR embeddings for requirement IDs: {sorted(missing)}\n"
                "Re-run ARLO to regenerate ASR embeddings before running RAA."
            )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Non-ASR persistence
# ---------------------------------------------------------------------------
def _load_cached_hashes(conn: sqlite3.Connection) -> dict[int, str]:
    """Return {requirement_id: text_hash} for all rows in the non-ASR DB."""
    rows = conn.execute("SELECT requirement_id, text_hash FROM embeddings").fetchall()
    return {row[0]: row[1] for row in rows}


def _persist_non_asr_embeddings(
    non_asrs: list[dict],
    non_asr_db_path: Path,
    model: TextEmbedding | None = None,
):
    """Generate and persist non-ASR embeddings.

    Only requirements whose current text_hash differs from the stored value
    (or that are absent from the DB) are embedded.  Already-fresh rows are
    skipped, making reruns idempotent.
    """
    _EMBEDDINGS_DIR = _project_root() / "embeddings"
    _EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    conn = open_embedding_db(non_asr_db_path, read_only=False)
    try:
        _ensure_embeddings_schema(conn)

        # Check model name consistency
        rows = conn.execute("SELECT DISTINCT model_name FROM embeddings").fetchall()
        for (model_name,) in rows:
            if model_name != _MODEL_NAME:
                raise ValueError(
                    f"non-ASR embedding database uses model '{model_name}', "
                    f"but expected '{_MODEL_NAME}'"
                )

        cached = _load_cached_hashes(conn)

        # Determine which requirements need (re)embedding
        to_embed: list[dict] = []
        for req in non_asrs:
            text = _non_asr_text(req)
            current_hash = _hash_text(text) if text else ""
            req_id = _requirement_id_int(req)

            if req_id not in cached:
                to_embed.append(req)
            elif cached[req_id] != current_hash:
                logger.warning("Stale embedding detected for requirement ID %d. Recomputing.", req_id)
                to_embed.append(req)
            else:
                logger.debug("Skipping requirement %d — hash unchanged.", req_id)

        if to_embed:
            texts = [_non_asr_text(req) for req in to_embed]
            embeddings = _embed_texts(texts, model=model)

            for req, embedding in zip(to_embed, embeddings):
                req_id = _requirement_id_int(req)
                text = _non_asr_text(req)
                conn.execute(
                    "INSERT OR REPLACE INTO embeddings "
                    "(requirement_id, embedding, text_hash, model_name) "
                    "VALUES (?, ?, ?, ?)",
                    (
                        req_id,
                        _serialize_embedding(embedding),
                        _hash_text(text),
                        _MODEL_NAME,
                    ),
                )

            conn.commit()
            logger.info(
                "Persisted %d non-ASR embeddings to %s", len(to_embed), non_asr_db_path
            )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Node entry point
# ---------------------------------------------------------------------------
def prepare_embeddings(state: dict) -> dict:
    """Preparation node: verify ASR embeddings + persist non-ASR embeddings.

    Reads ``asrs`` and ``non_asr`` from the RAA state.  Returns
    ``{"embeddings_ready": True}`` when both steps succeed.

    This node never loads embedding vectors into LangGraph state channels —
    embeddings stay in SQLite and are read by downstream batch-construction
    nodes on demand.
    """
    if state.get("embeddings_ready", False) is True:
        return {}

    asrs = state.get("asrs", [])
    non_asrs = state.get("non_asr", [])

    asr_db = _asr_db_path()
    non_asr_db = _non_asr_db_path()

    try:
        _verify_asr_embeddings(asrs, asr_db)
    except sqlite3.DatabaseError as e:
        raise RuntimeError(
            f"ASR embedding database is corrupt: {e}. Please re-run ARLO."
        ) from e

    model = _get_embedding_model()
    try:
        _persist_non_asr_embeddings(non_asrs, non_asr_db, model=model)
    except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
        logger.warning(
            "Non-ASR embedding DB is corrupt or missing: %s. Rebuilding from scratch.",
            e,
        )
        non_asr_db.unlink(missing_ok=True)
        _persist_non_asr_embeddings(non_asrs, non_asr_db, model=model)

    logger.info(
        "Embedding readiness confirmed — %d ASRs verified, %d non-ASRs persisted.",
        len(asrs),
        len(non_asrs),
    )
    return {"embeddings_ready": True}
