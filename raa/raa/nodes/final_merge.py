"""
Final merge node (Story 4.1).

Merges all batch outputs globally into a single C4 structure,
runs global entity deduplication, and resolves all outstanding
open questions so the final output contains no unresolved conflicts.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field, ValidationError

from raa.judge.deduplication import (
    _check_hierarchy_mismatch,
    _do_ids_overlap,
    _merge_entities,
    _rewrite_relationship_ids,
    _to_entity,
    _to_relationship,
    _union_technology,
    deduplicate_and_merge_fragment,
    normalize_entity_id,
)
from raa.nodes.conflict_resolution import (
    _apply_answer_overrides,
    _map_answers_to_questions,
    _normalize_answers,
)
from raa.nodes.human_review_gate import (
    _SUGGESTED_RESOLUTIONS,
    _classify_question_type,
)
from raa.state.models import C4Entity, C4Relationship, OpenQuestion
from raa.state.schemas import RAAState
from raa.utils.constants import (
    DEDUP_MERGE_THRESHOLD,
    EMBEDDING_CACHE_DIR,
    EMBEDDING_MODEL_NAME,
)
from raa.utils.embedding_cache import (
    EmbeddingCache,
    ModelNonExistentException,
    cosine_similarity,
    get_embedding_model,
)
from raa.utils.prompt_loader import load_prompt

logger = logging.getLogger(__name__)


# ── Structured assumption output for LLM ────────────────────────────────────


class DocumentedAssumption(BaseModel):
    assumption: str = Field(description="The documented assumption text")
    rationale: str = Field(description="Why this assumption is reasonable")


# ── Embedding initialization ────────────────────────────────────────────────


def _init_embeddings(config: RunnableConfig | None = None):
    """Try to initialize embedding cache and model for similarity-based dedup.

    Returns (cache, model) or (None, None) if unavailable.
    """
    cfg = {}
    if config is not None:
        if isinstance(config, dict):
            cfg = config.get("configurable") or {}
        else:
            cfg = getattr(config, "configurable", None) or {}

    db_path = cfg.get(
        "non_asr_embeddings_db_path",
        os.path.join(EMBEDDING_CACHE_DIR, "non_asr_embeddings.db"),
    )
    cache_dir = cfg.get("embedding_cache_dir", EMBEDDING_CACHE_DIR)
    model_name = cfg.get("embedding_model_name", EMBEDDING_MODEL_NAME)

    try:
        cache = EmbeddingCache(db_path=db_path, model_name=model_name)
        model = get_embedding_model(cache_dir, model_name)
        return cache, model
    except (ModelNonExistentException, Exception) as e:
        logger.warning("Embedding model unavailable, skipping similarity dedup: %s", e)
        return None, None


# ── Global merge ────────────────────────────────────────────────────────────


def _normalize_merge_questions(questions: list[dict]) -> list[dict]:
    """Post-process merge questions to align question types with AC requirements.

    Hierarchy-related issues from dedup become ``hierarchy_conflict``
    with owner ``judge_resolvable``.
    """
    normalized_qs = []
    for q in questions:
        if not isinstance(q, dict):
            continue
        q_copy = dict(q)
        reason = q_copy.get("reason", "")
        desc = q_copy.get("description", "") or ""

        if reason in (
            "orphan_container",
            "orphan_component",
            "unresolved_relationship_endpoint",
        ):
            q_copy["question_type"] = "hierarchy_conflict"
            q_copy["resolution_owner"] = "judge_resolvable"
            q_copy["resolution"] = _SUGGESTED_RESOLUTIONS.get("hierarchy_conflict", "")
            q_copy["assumption_flag"] = False

        elif "mismatching C4 parent hierarchy" in desc:
            q_copy["question_type"] = "hierarchy_conflict"
            q_copy["resolution_owner"] = "judge_resolvable"
            q_copy["resolution"] = _SUGGESTED_RESOLUTIONS.get("hierarchy_conflict", "")
            q_copy["assumption_flag"] = False

        normalized_qs.append(q_copy)

    return normalized_qs


def _global_merge(
    arch_model: dict,
    batch_outputs: list[dict],
    cache,
    model,
) -> tuple[dict, list[dict]]:
    """Merge all batch outputs into a single unified arch_model.

    Each batch_output is processed against the running arch_model using
    ``deduplicate_and_merge_fragment``. All merge-related open questions
    are collected and normalized.
    """
    all_questions: list[dict] = []
    running_model = {
        "entities": list(arch_model.get("entities") or []),
        "relationships": list(arch_model.get("relationships") or []),
        "boundary_groups": list(arch_model.get("boundary_groups") or []),
    }

    for batch_output in batch_outputs:
        if not batch_output:
            continue
        running_model, questions, _ = deduplicate_and_merge_fragment(
            batch_output, running_model, cache, model,
        )
        if questions:
            all_questions.extend([dict(q) for q in questions if isinstance(q, dict)])

    all_questions = _normalize_merge_questions(all_questions)

    # Preserve other model keys from the original arch_model
    for key in ("cross_cutting_candidates", "assumption_flags"):
        if key in arch_model:
            running_model[key] = list(arch_model[key] or [])

    return running_model, all_questions


# ── Question resolution ─────────────────────────────────────────────────────


def _get_resolution_owner(question: dict) -> str:
    """Determine resolution owner from a question dict.

    Uses ``resolution_owner`` field if present, otherwise classifies
    by ``question_type``.
    """
    owner = question.get("resolution_owner")
    if owner:
        return owner
    qt = question.get("question_type") or question.get("type") or "unknown"
    return _classify_question_type(qt)


def _get_default_suggestion(question: dict) -> str:
    """Get the default suggestion template for a judge_resolvable question type."""
    qt = question.get("question_type") or question.get("type") or ""
    return _SUGGESTED_RESOLUTIONS.get(
        qt,
        "Resolve using the primary strategy's output as the canonical reference.",
    )


def _collect_entity_ids(question: dict) -> set[str]:
    """Collect all entity IDs referenced in a question (root and context)."""
    ids: set[str] = set()
    id_keys = ("entity_a_id", "entity_b_id", "entity_id", "promoted_component_id")
    for key in id_keys:
        val = question.get(key)
        if val and isinstance(val, str):
            ids.add(val)
    ctx = question.get("context") or {}
    if isinstance(ctx, dict):
        for key in id_keys:
            val = ctx.get(key)
            if val and isinstance(val, str):
                ids.add(val)
    return ids


def _generate_assumption(
    question: dict,
    arch_model: dict,
    requirements: dict[str, str],
    config: RunnableConfig | None,
) -> str:
    """Generate a documented assumption for a human_preferred question.

    Uses ``judge_llm`` from config if available; falls back to a standard
    template referencing the original issue description.
    """
    qt = question.get("question_type", "unknown")
    desc = question.get("description")
    if not desc:
        desc = "No description provided."

    # Try judge LLM from config
    judge_llm = None
    if config is not None:
        cfg = (
            config.get("configurable") or {}
            if isinstance(config, dict)
            else getattr(config, "configurable", None) or {}
        )
        judge_llm = cfg.get("judge_llm")

    if judge_llm is not None:
        try:
            reqs_text = "\n".join(f"- {rid}: {rdesc}" for rid, rdesc in requirements.items())
            prompt = load_prompt("generate_assumption.md", {
                "question_type": qt,
                "description": desc,
                "requirements": reqs_text or "No requirements specified.",
            })
            structured_llm = judge_llm.with_structured_output(DocumentedAssumption)
            result = structured_llm.invoke(prompt)
            if isinstance(result, dict):
                assumption = result.get("assumption", "")
                rationale = result.get("rationale", "")
            else:
                assumption = getattr(result, "assumption", "")
                rationale = getattr(result, "rationale", "")
            return f"{assumption} (Rationale: {rationale})"
        except (ValidationError, Exception) as e:
            logger.debug("LLM assumption generation failed, using fallback template: %s", e)

    # Fallback template
    return (
        f"Assumed default resolution for {qt} concern. "
        f"Issue: {desc[:300]}. "
        f"Architecture maintains current structure; no structural changes applied. "
        f"Review recommended before production deployment."
    )


def _resolve_all_questions(
    open_questions: list[dict],
    human_answers: dict,
    arch_model: dict,
    requirements: dict[str, str],
    config: RunnableConfig | None,
) -> dict:
    """Resolve all outstanding open questions.

    1. Apply human answers to matching questions (resets assumption flags).
    2. For unresolved ``judge_resolvable`` questions, apply pre-computed
       suggestion or default template, with ``assumption_flag = False``.
    3. For unresolved ``human_preferred`` questions, generate a documented
       assumption (LLM or fallback), with ``assumption_flag = True``.

    Mutates ``open_questions`` in place. Returns the updated ``arch_model``.
    """
    # 1. Apply human answers
    answers = _normalize_answers(human_answers)
    if answers:
        open_questions, resolved_entity_ids = _map_answers_to_questions(
            answers, open_questions,
        )
        arch_model = dict(arch_model)
        arch_model = _apply_answer_overrides(arch_model, resolved_entity_ids)

    # Clone arch_model lists & dicts to avoid direct state mutation
    arch_model = dict(arch_model)
    arch_model["entities"] = [dict(e) for e in (arch_model.get("entities") or [])]
    arch_model["relationships"] = [dict(r) for r in (arch_model.get("relationships") or [])]
    arch_model["boundary_groups"] = list(arch_model.get("boundary_groups") or [])
    arch_model["cross_cutting_candidates"] = list(arch_model.get("cross_cutting_candidates") or [])
    arch_model["assumption_flags"] = list(arch_model.get("assumption_flags") or [])

    for q in open_questions:
        if not isinstance(q, dict):
            continue
        # Skip already-resolved questions
        if q.get("resolution") is not None:
            continue

        owner = _get_resolution_owner(q)

        if owner == "judge_resolvable":
            resolution = _get_default_suggestion(q)
            q["resolution"] = resolution
            q["assumption_flag"] = False

        elif owner == "human_preferred":
            assumption = _generate_assumption(q, arch_model, requirements, config)
            q["resolution"] = assumption
            q["assumption_flag"] = True

            # Track assumption flags on entities
            entity_ids = _collect_entity_ids(q)
            assumption_flags: list[str] = list(
                arch_model.get("assumption_flags") or []
            )
            for eid in entity_ids:
                if eid not in assumption_flags:
                    assumption_flags.append(eid)
            arch_model["assumption_flags"] = assumption_flags

            for entity in arch_model["entities"]:
                if entity.get("id") in entity_ids:
                    meta = dict(entity.get("metadata") or {})
                    meta["assumption_flag"] = True
                    meta["assumed"] = True
                    entity["metadata"] = meta

    return arch_model


# ── Main Node ───────────────────────────────────────────────────────────────


def final_merge(
    state: RAAState,
    config: RunnableConfig | None = None,
) -> dict:
    """Merge all batch outputs globally and resolve all outstanding questions.

    1. Combines all batch fragments from ``state["batch_outputs"]`` and the
       running ``state["arch_model"]`` into a single unified C4 structure.
    2. Runs global entity deduplication (normalized ID match + cosine
       similarity when embedding model is available).
    3. Resolves every open question so no question has a ``null`` resolution:
       human answers applied authoritatively, judge_resolvable questions
       resolved with pre-computed suggestions or defaults, and
       human_preferred questions documented with assumptions.

    Args:
        state: Full RAA state with ``batch_outputs``, ``arch_model``,
            open_questions, and human_answers channels.
        config: LangGraph RunnableConfig with optional ``judge_llm`` in
            configurable.

    Returns:
        dict with keys: ``arch_model``, ``open_questions`` (merge-generated).
    """
    arch_model: dict = state.get("arch_model") or {}
    batch_outputs: list[dict] = list(state.get("batch_outputs") or [])
    open_questions: list[dict] = [
        dict(q) for q in (state.get("open_questions") or []) if isinstance(q, dict)
    ]
    human_answers: dict = state.get("human_answers") or {}
    requirements: dict[str, str] = state.get("requirements") or {}

    # 1. Initialize embeddings for similarity-based dedup
    cache, model = _init_embeddings(config)

    # 2. Global merge of all batch outputs
    arch_model, merge_questions = _global_merge(
        arch_model, batch_outputs, cache, model,
    )

    # 3. Resolve all open questions
    arch_model = _resolve_all_questions(
        open_questions, human_answers, arch_model, requirements, config,
    )

    # Return all resolved questions plus any new merge-generated questions
    # to be merged and persisted correctly in the state checkpoint.
    return {
        "arch_model": arch_model,
        "open_questions": open_questions + merge_questions,
    }
