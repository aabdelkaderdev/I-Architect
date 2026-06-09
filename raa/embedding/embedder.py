"""FastEmbed wrapper for local synchronous embedding inference.

Two-phase embedding process runs entirely before the batch loop begins.
A single TextEmbedding instance is created at module level — the underlying
library caches model files internally.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

if TYPE_CHECKING:
    from raa.types import NonASREntry


_MODEL_NAME = "mixedbread-ai/mxbai-embed-large-v1"

# Resolve the project-level models/ cache directory.
# This file lives at raa/embedding/embedder.py → two levels up is the project root.
_CACHE_DIR = str(Path(__file__).resolve().parent.parent.parent / "models")

_embedding_model: object | None = None


def _get_model():
    """Lazy-initialize the FastEmbed model. Cached at module level after first call."""
    global _embedding_model
    if _embedding_model is None:
        try:
            from fastembed import TextEmbedding

            _embedding_model = TextEmbedding(
                model_name=_MODEL_NAME, cache_dir=_CACHE_DIR
            )
        except Exception as exc:
            raise EmbeddingError(
                f"FastEmbed initialisation failed for model {_MODEL_NAME}: {exc}"
            ) from exc
    return _embedding_model


class EmbeddingError(RuntimeError):
    """Raised when FastEmbed initialisation fails or model.embed() raises at runtime."""


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Pre: `texts` may be empty.

    Post: Returns one embedding vector per text, preserving order.
    Side effects: Performs local FastEmbed inference only.
    """
    if not texts:
        return []

    model = _get_model()
    try:
        vectors = list(model.embed(texts))
    except Exception as exc:
        raise EmbeddingError(f"FastEmbed embed() failed: {exc}") from exc

    return [v.tolist() for v in vectors]


def compute_group_vectors(
    condition_groups: list[dict[str, object]],
) -> dict[str, list[float]]:
    """Pre: `condition_groups` contains Phase 1 §2.1 group dictionaries with
         cluster, nominal_condition, and requirements (list of {id, text}).
         Only groups where cluster != -1 are processed.

    Post: Returns mean ASR text vectors keyed by batch ID string
          (e.g. 'concern_batch_1'). Groups are sorted by cluster ascending
          and assigned ordinals, matching BatchConstructor ordering.
    Side effects: Calls `embed_texts()`.
    """
    non_foundation = [
        g for g in condition_groups if int(g.get("cluster", -1)) != -1
    ]
    non_foundation.sort(key=lambda g: int(g["cluster"]))

    group_vectors: dict[str, list[float]] = {}
    for ordinal, group in enumerate(non_foundation, start=1):
        requirements = group["requirements"]
        if not isinstance(requirements, list) or not requirements:
            continue

        texts = [str(req["text"]) for req in requirements if isinstance(req, dict)]
        if not texts:
            continue

        vecs = embed_texts(texts)
        mean_vec = np.mean(np.array(vecs), axis=0)
        group_vectors[f"concern_batch_{ordinal}"] = mean_vec.tolist()

    return group_vectors


def cosine_scores(
    vector: list[float],
    group_vectors: dict[str, list[float]],
) -> dict[str, float]:
    """Pre: `vector` and every group vector have equal dimensionality.

    Post: Returns similarity score by batch ID string.
    Side effects: None.
    """
    if not group_vectors:
        return {}

    batch_ids = list(group_vectors.keys())
    group_matrix = np.array([group_vectors[bid] for bid in batch_ids])

    vec_arr = np.array([vector])
    scores_arr = cosine_similarity(vec_arr, group_matrix)[0]

    return {bid: float(score) for bid, score in zip(batch_ids, scores_arr)}


def assign_non_asrs(
    condition_groups: list[dict],
    non_asrs: list[NonASREntry],
    threshold: float,
) -> tuple[dict[str, list[float]], list[tuple[NonASREntry, str]]]:
    """Pre:
        - `condition_groups` contains groups with cluster, nominal_condition, requirements.
        - `non_asrs` contains enriched functional requirements.
        - `threshold` is SIMILARITY_THRESHOLD from raa/config/defaults.py.

    Process (internal):
        1. Phase A — embed per-group ASR texts, compute np.mean → group vectors
        2. Phase B — batch-embed all non-ASR texts in one model.embed() call
        3. For each (non_asr, vec), compute cosine similarity against stacked group matrix
        4. Assign to best group if above threshold, else to foundation batch

    Post:
        - Returns (group_vectors, assignments).
        - group_vectors: dict[str, list[float]] keyed by batch ID (e.g. 'concern_batch_1').
        - assignments: list[tuple[NonASREntry, batch_id]], exclusive (one batch per non-ASR).

    Side effects:
        - Performs local FastEmbed inference.
        - Does not call LLMs and does not mutate registry or graph state.

    Error contract: raises EmbeddingError if FastEmbed initialisation fails
    (model missing/corrupt) or model.embed() raises at runtime.
    """
    # Phase A: compute group vectors once
    group_vectors = compute_group_vectors(condition_groups)

    # Phase B: batch-embed all non-ASR texts
    if not non_asrs:
        return group_vectors, []

    non_asr_texts = [entry["text"] for entry in non_asrs]
    na_vecs = embed_texts(non_asr_texts)

    batch_ids = list(group_vectors.keys())
    if not batch_ids:
        # No condition groups — all non-ASRs go to foundation
        return group_vectors, [(na, "foundation_batch") for na in non_asrs]

    group_matrix = np.array([group_vectors[bid] for bid in batch_ids])

    assignments: list[tuple[NonASREntry, str]] = []
    for i, non_asr in enumerate(non_asrs):
        vec_arr = np.array([na_vecs[i]])
        scores = cosine_similarity(vec_arr, group_matrix)[0]
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        if best_score > threshold:
            batch_id = batch_ids[best_idx]
        else:
            batch_id = "foundation_batch"

        assignments.append((non_asr, batch_id))

    return group_vectors, assignments
