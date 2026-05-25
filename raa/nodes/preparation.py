"""
Phase 1 node: Input normalization and enrichment (FR-1).

Normalizes raw ARLO outputs into standardized RAA-internal requirement records.
All requirement IDs are converted to "R{id}" string format.
Non-ASR requirements are enriched with default field values.
"""
from langchain_core.runnables import RunnableConfig

from raa.state.schemas import RAAState
from raa.utils.id_utils import to_r_id


# ── Sentinel ─────────────────────────────────────────────────────────────
_UNSET = object()


def normalize_requirements(state: RAAState, config: RunnableConfig) -> dict:
    """Normalize and enrich raw ARLO requirements into standardized records.

    Description resolution precedence for ASRs:
    1. Orchestrator-provided ``requirements`` dict (raw and normalized key forms)
    2. ARLO-provided ASR description text (fallback only)

    Non-ASR description resolution:
    1. Orchestrator-provided ``requirements`` dict (raw and normalized key forms)

    Args:
        state: Full RAA state with ``requirements``, ``asrs``, and ``non_asr`` channels.
        config: LangGraph RunnableConfig (unused by this node — no LLM calls).

    Returns:
        dict with keys: normalized_asrs, normalized_non_asr, embeddings_ready.
    """
    requirements = state["requirements"]
    raw_asrs = state["asrs"]
    raw_non_asr_ids = state["non_asr"]
    seen_ids: dict[str, str] = {}

    # ── Normalize ASR records ──────────────────────────────────────────
    normalized_asrs = []
    for asr in raw_asrs:
        asr_id = asr["id"]
        normalized_id = to_r_id(asr_id)
        _register_canonical_id(seen_ids, normalized_id, f"ASR {asr_id!r}")
        description = _resolve_asr_description(asr_id, normalized_id, asr, requirements)
        qa = _coerce_quality_attributes(asr.get("quality_attributes", _UNSET))

        normalized_asrs.append({
            "id": normalized_id,
            "description": description,
            "is_asr": True,
            "quality_attributes": qa,
            "condition_text": asr.get("condition_text"),
        })

    # ── Normalize Non-ASR records ──────────────────────────────────────
    normalized_non_asr = []
    for req_id in raw_non_asr_ids:
        normalized_id = to_r_id(req_id)
        _register_canonical_id(seen_ids, normalized_id, f"Non-ASR {req_id!r}")
        description = _resolve_non_asr_description(req_id, normalized_id, requirements)

        normalized_non_asr.append({
            "id": normalized_id,
            "description": description,
            "is_asr": False,
            "quality_attributes": [],
            "condition_text": None,
        })

    return {
        "normalized_asrs": normalized_asrs,
        "normalized_non_asr": normalized_non_asr,
        "embeddings_ready": False,
    }


# ── Private helpers (not node functions — co-located with sole consumer) ─


def _resolve_asr_description(
    raw_id,
    normalized_id: str,
    asr: dict,
    requirements: dict[str, str],
) -> str:
    """Resolve ASR description with precedence:
    1. requirements[raw_id]
    2. requirements[normalized_id]
    3. asr["description"] (ARLO-provided, fallback only)
    4. "" (empty string)
    """
    desc = _lookup_requirements(requirements, raw_id, normalized_id)
    if desc is not None:
        return desc
    if _description_is_usable(asr.get("description")):
        return asr["description"]
    return ""


def _resolve_non_asr_description(
    raw_id: str,
    normalized_id: str,
    requirements: dict[str, str],
) -> str:
    """Resolve non-ASR description from requirements dict.

    Tries raw ID, then normalized ID, then empty string.
    """
    desc = _lookup_requirements(requirements, raw_id, normalized_id)
    return desc if desc is not None else ""


def _lookup_requirements(
    requirements: dict[str, str],
    raw_id,
    normalized_id: str,
) -> str | None:
    """Try raw and normalized ID forms in requirements dict. Returns None if missing."""
    for key in _candidate_requirement_keys(raw_id, normalized_id):
        if key in requirements and _description_is_usable(requirements[key]):
            return requirements[key]
    return None


def _coerce_quality_attributes(value) -> list[str]:
    """Coerce ARLO quality_attributes to clean ``list[str]``."""
    import logging
    logger = logging.getLogger(__name__)

    if value is None or value is _UNSET:
        return []
    if not isinstance(value, list):
        logger.warning("Quality attributes is not a list: %r", value)
        return []
    
    coerced = []
    for v in value:
        if isinstance(v, str):
            coerced.append(v)
        else:
            logger.warning("Dropping non-string quality attribute: %r", v)
    return coerced


def _candidate_requirement_keys(raw_id, normalized_id: str) -> list[str]:
    """Return lookup keys from the raw, stripped, and canonical forms."""
    keys: list[str] = []
    raw_text = str(raw_id).strip()

    for key in (raw_text, normalized_id):
        if key and key not in keys:
            keys.append(key)

    if normalized_id.startswith("R") and len(normalized_id) > 1:
        stripped = normalized_id[1:]
        if stripped and stripped not in keys:
            keys.append(stripped)

    return keys


def _description_is_usable(value) -> bool:
    """Treat empty strings as authoritative, but reject whitespace-only text."""
    if value is None:
        return False
    if not isinstance(value, str):
        value = str(value)
    if value == "":
        return True
    return bool(value.strip())


def _register_canonical_id(seen_ids: dict[str, str], normalized_id: str, source: str) -> None:
    """Reject duplicate canonical IDs across normalized ASR / Non-ASR inputs."""
    previous = seen_ids.get(normalized_id)
    if previous is not None:
        raise ValueError(
            f"Duplicate canonical requirement ID {normalized_id!r} encountered in {previous} and {source}"
        )
    seen_ids[normalized_id] = source


# ── Phase 1b node: Embedding verification (FR-2) ─────────────────────────


def verify_embeddings(state: RAAState, config: RunnableConfig) -> dict:
    """Verify or generate dense embeddings for normalized requirements.

    Reads ``normalized_asrs`` and ``normalized_non_asr`` from state.
    For each requirement, checks the SQLite embedding cache for a matching
    text hash. Only computes new embeddings on cache miss (new or stale text).

    Config keys expected in ``config["configurable"]``:
        ``asr_db_path``, ``non_asr_db_path``, ``cache_dir``,
        and optionally ``embedding_model_name``.

    Returns:
        dict with key ``embeddings_ready`` set to ``True``.
    """
    from raa.utils.embedding_cache import EmbeddingCache, get_embedding_model
    from raa.utils.constants import EMBEDDING_MODEL_NAME

    configurable = config.get("configurable")
    if configurable is None:
        raise KeyError("RunnableConfig is missing 'configurable' key")
    
    missing = [key for key in ("asr_db_path", "non_asr_db_path", "cache_dir") if key not in configurable]
    if missing:
        raise KeyError(f"Missing required configurable paths: {', '.join(missing)}")

    asr_db_path = configurable["asr_db_path"]
    non_asr_db_path = configurable["non_asr_db_path"]
    cache_dir = configurable["cache_dir"]
    model_name = configurable.get("embedding_model_name", EMBEDDING_MODEL_NAME)

    model = get_embedding_model(cache_dir, model_name)
    
    asr_cache = None
    non_asr_cache = None
    try:
        asr_cache = EmbeddingCache(asr_db_path, model_name)
        non_asr_cache = EmbeddingCache(non_asr_db_path, model_name)

        # ── ASR embeddings (embed condition_text) ───────────────────────
        _embed_requirements(
            records=state.get("normalized_asrs") or [],
            text_key="condition_text",
            cache=asr_cache,
            model=model,
        )

        # ── Non-ASR embeddings (embed description) ──────────────────────
        _embed_requirements(
            records=state.get("normalized_non_asr") or [],
            text_key="description",
            cache=non_asr_cache,
            model=model,
        )
    finally:
        if asr_cache is not None:
            asr_cache.close()
        if non_asr_cache is not None:
            non_asr_cache.close()

    return {"embeddings_ready": True}


def _embed_requirements(
    records: list[dict],
    text_key: str,
    cache,
    model,
) -> None:
    """Hash-check-embed loop shared by ASR and Non-ASR embedding passes."""
    from raa.utils.embedding_cache import EmbeddingCache

    miss_records = []
    miss_texts = []

    for rec in records:
        rec_id = rec.get("id")
        if not rec_id:
            raise ValueError(f"Record is missing 'id' key: {rec}")
            
        text = rec.get(text_key)
        if text is None:
            text = ""
        else:
            text = str(text)

        text_hash = EmbeddingCache.text_hash(text)
        cached = cache.get_cached_vector(rec_id, text_hash)
        if cached is None:
            miss_records.append((rec_id, text_hash))
            miss_texts.append(text)

    if miss_texts:
        results = list(model.embed(miss_texts))
        if len(results) != len(miss_texts):
            raise RuntimeError(
                f"FastEmbed model returned {len(results)} embeddings, expected {len(miss_texts)}"
            )

        vectors_to_store = []
        for (rec_id, text_hash), result in zip(miss_records, results):
            vector = result.tolist() if hasattr(result, 'tolist') else list(result)
            vectors_to_store.append((rec_id, text_hash, vector))

        cache.store_vectors(vectors_to_store)

