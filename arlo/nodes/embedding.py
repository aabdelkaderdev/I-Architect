"""
Semantic embedding generation using FastEmbed (CPU).

Uses mixedbread-ai/mxbai-embed-large-v1 (1024-dim) for dense semantic
embeddings. Runs locally on CPU — no API key required.

Model files are cached in arlo/models/ (project-relative) on first run.
Subsequent runs load from local cache — no re-download needed.

Install:  pip install fastembed
"""
from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path

from fastembed import TextEmbedding

from arlo.state.schemas import ARLOState

logger = logging.getLogger(__name__)

_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"
_CACHE_DIR = Path(__file__).parent.parent / "models"  # → arlo/models/
_PROJECT_ROOT = Path(__file__).parent.parent.parent  # → project root
_EMBEDDINGS_DIR = _PROJECT_ROOT / "embeddings"
_DB_PATH = _EMBEDDINGS_DIR / "asr_embeddings.db"

# Module-level singleton — initialized once on first call.
_embedding_model: TextEmbedding | None = None


def _get_model() -> TextEmbedding:
    """Lazy-initialize the TextEmbedding model singleton."""
    global _embedding_model
    if _embedding_model is None:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _embedding_model = TextEmbedding(
            model_name=_MODEL_NAME,
            cache_dir=str(_CACHE_DIR),
        )
        logger.info("FastEmbed model loaded: %s (cache=%s)", _MODEL_NAME, _CACHE_DIR)
    return _embedding_model


def generate_embeddings(state: ARLOState) -> dict:
    """Node: Generate dense semantic embeddings for ASR condition texts.

    Reads: asrs
    Writes: embeddings

    Each ASR's condition_text is embedded into a 1024-dim dense vector
    using mxbai-embed-large-v1. The full corpus is embedded in a single
    batch call for efficiency.
    """
    asrs = state["asrs"]

    if not asrs:
        return {"embeddings": []}

    texts = [asr.get("condition_text", "") for asr in asrs]

    model = _get_model()
    embeddings = [vec.tolist() for vec in model.embed(texts)]

    logger.info("Generated %d embeddings (dim=%d).", len(embeddings), len(embeddings[0]))

    # Persist ASR embeddings to SQLite for RAA consumption
    _EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.execute(
        "CREATE TABLE IF NOT EXISTS asr_embeddings ("
        "  requirement_id TEXT PRIMARY KEY,"
        "  embedding_json TEXT NOT NULL"
        ")"
    )
    persisted = 0
    for asr, embedding in zip(asrs, embeddings):
        requirement_id = asr.get("id")
        if requirement_id:
            conn.execute(
                "INSERT OR REPLACE INTO asr_embeddings (requirement_id, embedding_json) "
                "VALUES (?, ?)",
                (requirement_id, json.dumps(embedding)),
            )
            persisted += 1
    conn.commit()
    conn.close()

    logger.info("Persisted %d ASR embeddings to %s", persisted, _DB_PATH)

    return {"embeddings": embeddings}
