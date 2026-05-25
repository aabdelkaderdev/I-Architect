"""
Embedding cache abstraction (AR4) — encapsulates all SQLite read/write for
dense vector storage and provides the FastEmbed model loader.

Nodes never call ``sqlite3`` or ``fastembed`` directly. They use this module.
"""
from __future__ import annotations

import hashlib
import logging
import sqlite3
import struct
import threading
from pathlib import Path

import math
from fastembed import TextEmbedding

from raa.utils.constants import EMBEDDING_DIM

logger = logging.getLogger(__name__)

# ── Exception ────────────────────────────────────────────────────────────────


class ModelNonExistentException(Exception):
    """Raised when FastEmbed model files are absent from cache_dir."""

    def __init__(self, cache_dir: str, model_name: str) -> None:
        model_dir = Path(cache_dir) / _model_dir_name(model_name)
        super().__init__(
            f"Embedding model files not found at {model_dir}. "
            f"Download {model_name} first or place it in {cache_dir}."
        )
        self.cache_dir = cache_dir
        self.model_name = model_name


# ── Standalone cosine similarity (Task 1.3) ──────────────────────────────────

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute the cosine similarity between two flat vectors.

    If either vector has a norm of 0, returns 0.0.
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


# ── Model loader (singleton, mirrors arlo/nodes/embedding.py) ────────────────

_embedding_model: TextEmbedding | None = None
_loaded_cache_dir: str | None = None
_loaded_model_name: str | None = None
_model_lock = threading.Lock()


def _model_dir_name(model_name: str) -> str:
    """FastEmbed's on-disk directory name for a model."""
    return "models--" + model_name.replace("/", "--")


def _get_embedding_model(cache_dir: str, model_name: str) -> TextEmbedding:
    """Lazy-initialize the FastEmbed TextEmbedding model singleton.

    Verifies the model directory exists on disk before initializing.
    Raises ``ModelNonExistentException`` if absent.
    """
    global _embedding_model, _loaded_cache_dir, _loaded_model_name
    
    with _model_lock:
        if _embedding_model is not None:
            if _loaded_cache_dir != cache_dir or _loaded_model_name != model_name:
                raise RuntimeError(
                    f"Model already loaded with name {_loaded_model_name} and cache_dir {_loaded_cache_dir}. "
                    f"Mismatched request: model_name={model_name}, cache_dir={cache_dir}"
                )
            return _embedding_model

        model_dir = Path(cache_dir) / _model_dir_name(model_name)
        if not model_dir.is_dir():
            raise ModelNonExistentException(cache_dir, model_name)
        
        try:
            _embedding_model = TextEmbedding(
                model_name=model_name,
                cache_dir=cache_dir,
            )
            _loaded_cache_dir = cache_dir
            _loaded_model_name = model_name
        except Exception:
            _embedding_model = None
            _loaded_cache_dir = None
            _loaded_model_name = None
            raise
        
        logger.info("FastEmbed model loaded: %s (cache=%s)", model_name, cache_dir)
        return _embedding_model


def get_embedding_model(cache_dir: str, model_name: str) -> TextEmbedding:
    """Public wrapper to lazy-initialize and retrieve the TextEmbedding model singleton."""
    return _get_embedding_model(cache_dir, model_name)


def _reset_singleton() -> None:
    """Reset the singleton state (used only for unit testing)."""
    global _embedding_model, _loaded_cache_dir, _loaded_model_name
    with _model_lock:
        _embedding_model = None
        _loaded_cache_dir = None
        _loaded_model_name = None


# ── Embedding cache ──────────────────────────────────────────────────────────

class EmbeddingCache:
    """SQLite-backed cache for 1024-dim dense embedding vectors (D2).

    Schema: ``(req_id TEXT PRIMARY KEY, embedding BLOB, text_hash TEXT, model_name TEXT)``
    """

    def __init__(self, db_path: str, model_name: str) -> None:
        self._db_path = db_path
        self._model_name = model_name
        self._conn = None
        
        try:
            self._conn = sqlite3.connect(db_path)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute(
                "CREATE TABLE IF NOT EXISTS embeddings ("
                "  req_id TEXT PRIMARY KEY,"
                "  embedding BLOB NOT NULL,"
                "  text_hash TEXT NOT NULL,"
                "  model_name TEXT NOT NULL"
                ")"
            )
            self._conn.commit()
        except Exception as e:
            if self._conn is not None:
                try:
                    self._conn.close()
                except Exception:
                    pass
            raise RuntimeError(f"Cannot initialize cache DB at {db_path}: {e}") from e

    # ── Public API ───────────────────────────────────────────────────────

    @staticmethod
    def text_hash(text: str) -> str:
        """SHA-256 hex digest of ``text.encode('utf-8')``."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Maintain compute_hash as an alias for backward compatibility.
    compute_hash = text_hash

    def get_cached_vector(self, req_id: str, text_hash: str) -> list[float] | None:
        """Return deserialized 1024-dim vector if (req_id, text_hash) matches.

        Returns ``None`` when the requirement is missing or the hash is stale.
        """
        if self._conn is None:
            raise RuntimeError("EmbeddingCache is closed.")
        row = self._conn.execute(
            "SELECT embedding FROM embeddings WHERE req_id = ? AND text_hash = ?",
            (req_id, text_hash),
        ).fetchone()
        if row is None:
            return None
        blob = row[0]
        expected_len = EMBEDDING_DIM * 4
        if len(blob) != expected_len:
            logger.warning(
                "Corrupt or incorrect length BLOB for req_id %s: expected %d bytes, got %d",
                req_id, expected_len, len(blob)
            )
            return None
        return list(struct.unpack(f"<{EMBEDDING_DIM}f", blob))

    def store_vector(self, req_id: str, text_hash: str, vector: list[float]) -> None:
        """Serialize vector to BLOB and INSERT OR REPLACE into the DB."""
        if self._conn is None:
            raise RuntimeError("EmbeddingCache is closed.")
        if len(vector) != EMBEDDING_DIM:
            raise ValueError(f"Expected vector of length {EMBEDDING_DIM}, got {len(vector)}")
        blob = struct.pack(f"<{EMBEDDING_DIM}f", *vector)
        try:
            self._conn.execute(
                "INSERT OR REPLACE INTO embeddings (req_id, embedding, text_hash, model_name) "
                "VALUES (?, ?, ?, ?)",
                (req_id, blob, text_hash, self._model_name),
            )
            self._conn.commit()
        except Exception:
            try:
                self._conn.rollback()
            except sqlite3.Error:
                pass
            raise

    def store_vectors(self, records: list[tuple[str, str, list[float]]]) -> None:
        """Serialize and insert multiple vectors in a single transaction."""
        if self._conn is None:
            raise RuntimeError("EmbeddingCache is closed.")
        if not records:
            return
        try:
            for req_id, text_hash, vector in records:
                if len(vector) != EMBEDDING_DIM:
                    raise ValueError(f"Expected vector of length {EMBEDDING_DIM}, got {len(vector)}")
                blob = struct.pack(f"<{EMBEDDING_DIM}f", *vector)
                self._conn.execute(
                    "INSERT OR REPLACE INTO embeddings (req_id, embedding, text_hash, model_name) "
                    "VALUES (?, ?, ?, ?)",
                    (req_id, blob, text_hash, self._model_name),
                )
            self._conn.commit()
        except Exception:
            try:
                self._conn.rollback()
            except sqlite3.Error:
                pass
            raise

    # ── Raw vector access (for centroid / nearest-neighbor queries) ─────

    def get_vector(self, req_id: str) -> list[float] | None:
        """Retrieve a raw embedding vector by requirement ID (no hash check)."""
        if self._conn is None:
            raise RuntimeError("EmbeddingCache is closed.")
        row = self._conn.execute(
            "SELECT embedding FROM embeddings WHERE req_id = ?", (req_id,)
        ).fetchone()
        if row is None:
            return None
        blob = row[0]
        expected_len = EMBEDDING_DIM * 4
        if len(blob) != expected_len:
            logger.warning(
                "Corrupt BLOB for req_id %s: expected %d bytes, got %d",
                req_id, expected_len, len(blob),
            )
            return None
        return list(struct.unpack(f"<{EMBEDDING_DIM}f", blob))

    def iter_all_vectors(self):
        """Generator yielding (req_id, vector) for every stored embedding.

        Returns each vector as a ``list[float]`` of length ``EMBEDDING_DIM``.
        """
        if self._conn is None:
            raise RuntimeError("EmbeddingCache is closed.")
        rows = self._conn.execute("SELECT req_id, embedding FROM embeddings")
        for req_id, blob in rows:
            if len(blob) == EMBEDDING_DIM * 4:
                yield req_id, list(struct.unpack(f"<{EMBEDDING_DIM}f", blob))
            else:
                logger.warning("Skipping corrupt BLOB for req_id %s", req_id)

    # ── Context Manager ──────────────────────────────────────────────────

    def __enter__(self) -> EmbeddingCache:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # ── Test / teardown helpers ──────────────────────────────────────────

    def __repr__(self) -> str:
        return f"EmbeddingCache(db_path={self._db_path!r}, model_name={self._model_name!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @property
    def db_path(self) -> str:
        return self._db_path

