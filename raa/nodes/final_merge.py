"""
Final merge node (Story 4.1).

Merges all batch outputs globally into a single C4 structure,
runs global entity deduplication, and resolves all outstanding
open questions so the final output contains no unresolved conflicts.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Any,TypedDict, Callable
logger = logging.getLogger(__name__)

from langchain_core.runnables import RunnableConfig
from langgraph.config import get_stream_writer
from pydantic import BaseModel, Field, ValidationError

from raa.judge.deduplication import (
    deduplicate_and_merge_fragment,
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
from raa.state.models import ArchFragment, C4Entity, C4Relationship, OpenQuestion
from raa.state.schemas import RAAState
from raa.utils.constants import (
    DEDUP_MERGE_THRESHOLD,
    EMBEDDING_CACHE_DIR,
    EMBEDDING_MODEL_NAME,
    RESIDUAL_HIGH_THRESHOLD,
    RESIDUAL_MID_LOW,
)
from raa.utils.embedding_cache import (
    EmbeddingCache,
    ModelNonExistentException,
    cosine_similarity,
    get_embedding_model,
)
from raa.utils.c4_validator import (
    C4SchemaValidationException,
    enforce_fragment_hierarchy,
    validate_c4_model,
    _scope_from_rank
)
from raa.utils.prompt_loader import load_prompt

from raa.utils.id_utils import to_r_id

logger = logging.getLogger(__name__)


class TraceabilityAuditException(Exception):
    """Raised when the 100% requirements traceability audit fails."""
    pass


class MergeTimeoutError(Exception):
    """Raised when final_merge exceeds the configured wall-clock timeout."""


class HumanInputRequiredException(Exception):
    """Raised when interactive final merge needs explicit human answers."""


# ── Progress helper ─────────────────────────────────────────────────────────


def _get_configurable(config: RunnableConfig | None) -> dict:
    """Return the configurable dict from a LangChain/LangGraph config object."""
    if config is None:
        return {}
    if isinstance(config, dict):
        return config.get("configurable") or {}
    return getattr(config, "configurable", None) or {}


# ── Typed event structure ────────────────────────────────────────────────────
 
class ProgressEvent(TypedDict, total=False):
    event: str
    phase: str
    message: str
    processed: int | None
    total: int | None
    current_item_id: str
 
 
# ── Private helpers ──────────────────────────────────────────────────────────
 
def _build_progress_event(
    phase: str,
    message: str,
    processed: int | None,
    total: int | None,
    current_item_id: str | None,
) -> ProgressEvent:
    event: ProgressEvent = {
        "event": "final_merge_progress",
        "phase": phase,
        "message": message,
        "processed": processed,
        "total": total,
    }
    if current_item_id is not None:
        event["current_item_id"] = current_item_id
    return event
 
 
def _progress_detail(
    processed: int | None,
    total: int | None,
    current_item_id: str | None,
) -> str:
    """Return a compact progress suffix, e.g. ' [3/10] current=abc'."""
    parts: list[str] = []
    if processed is not None and total is not None:
        parts.append(f"[{processed}/{total}]")
    if current_item_id is not None:
        parts.append(f"current={current_item_id}")
    return (" " + " ".join(parts)) if parts else ""
 
 
def _check_timeout(
    start_time: float,
    timeout_s: float,
    phase: str,
    message: str,
    processed: int | None,
    total: int | None,
    current_item_id: str | None,
) -> None:
    """Raise MergeTimeoutError if the wall-clock deadline has been exceeded."""
    if time.monotonic() - start_time <= timeout_s:
        return
 
    detail = _progress_detail(processed, total, current_item_id).strip()
    suffix = f" ({detail})" if detail else ""
    raise MergeTimeoutError(
        f"final_merge timeout ({timeout_s}s) in phase '{phase}': {message}{suffix}"
    )
 
 
def _try_stream_write(event: ProgressEvent) -> None:
    """Write to the LangGraph stream writer, silently no-op outside streaming contexts."""
    try:
        writer = get_stream_writer()
        writer(event)
    except RuntimeError:
        pass
 
 
# ── Public function ──────────────────────────────────────────────────────────
 
def _emit_progress(
    phase: str,
    message: str,
    config: RunnableConfig | None = None,
    metrics: dict | None = None,
    processed: int | None = None,
    total: int | None = None,
    start_time: float | None = None,
    timeout_s: float | None = None,
    current_item_id: str | None = None,
) -> None:
    """Emit a progress event via LangGraph stream writer, callback, stdout, and logger.
 
    Uses ``get_stream_writer()`` so callers consuming ``stream_mode="custom"``
    receive structured progress events. Direct notebook callers can pass
    ``final_merge_progress_to_stdout=True`` or ``final_merge_progress_callback``.
 
    Also logs at INFO level and checks the wall-clock timeout when
    ``start_time`` and ``timeout_s`` are both provided.
    """
    cfg = _get_configurable(config)
    event = _build_progress_event(phase, message, processed, total, current_item_id)
 
    # 1. Structured log
    logger.info(
        "[final_merge] phase=%s | %s | current=%s processed=%s total=%s",
        phase,
        message,
        current_item_id or "-",
        processed if processed is not None else "-",
        total if total is not None else "-",
    )
 
    # 2. Update caller-supplied metrics dict in-place
    if metrics is not None:
        metrics.update(
            last_progress_phase=phase,
            last_progress_message=message,
            **({"last_progress_item_id": current_item_id} if current_item_id else {}),
        )
 
    # 3. Optional user-supplied callback
    callback = cfg.get("final_merge_progress_callback")
    if callback is not None:
        try:
            callback(dict(event))
        except Exception as exc:
            logger.debug("final_merge progress callback failed: %s", exc)
 
    # 4. Optional stdout (e.g. notebook usage)
    if cfg.get("final_merge_progress_to_stdout"):
        detail = _progress_detail(processed, total, current_item_id)
        print(f"[final_merge] {phase}: {message}{detail}", flush=True)
 
    # 5. LangGraph streaming
    _try_stream_write(event)
 
    # 6. Timeout guard — checked last so all outputs are flushed before raising
    if start_time is not None and timeout_s is not None:
        _check_timeout(start_time, timeout_s, phase, message, processed, total, current_item_id)



# ── LLM invocation helper ───────────────────────────────────────────────────


def _invoke_llm(
    invoke_fn: Callable[[], Any],
    config: RunnableConfig | None,
    metrics: dict,
    label: str = "llm_call",
) -> Any | None:
    """Invoke an LLM callable synchronously when explicitly enabled.

    ``final_merge_use_llm`` defaults to False so notebook finalization stays
    deterministic and bounded. ``final_merge_llm_timeout_s`` is retained as an
    advisory setting for callers, but direct synchronous calls cannot be safely
    cancelled in-process.
    """
    cfg = _get_configurable(config)

    if not cfg.get("final_merge_use_llm", False):
        metrics["llm_calls_skipped"] = metrics.get("llm_calls_skipped", 0) + 1
        metrics["llm_fallbacks_used"] = metrics.get("llm_fallbacks_used", 0) + 1
        logger.info("Skipping LLM call '%s'; final_merge_use_llm is false", label)
        return None

    timeout_s = cfg.get("final_merge_llm_timeout_s", 60)
    metrics["llm_calls_attempted"] = metrics.get("llm_calls_attempted", 0) + 1
    logger.info(
        "Running LLM call '%s' synchronously; final_merge_llm_timeout_s=%s is advisory only",
        label,
        timeout_s,
    )

    try:
        return invoke_fn()
    except Exception as e:
        metrics["llm_calls_failed"] = metrics.get("llm_calls_failed", 0) + 1
        metrics["llm_fallbacks_used"] = metrics.get("llm_fallbacks_used", 0) + 1
        logger.debug("LLM call '%s' failed: %s", label, e)
        return None


# ── Structured assumption output for LLM ────────────────────────────────────


class DocumentedAssumption(BaseModel):
    assumption: str = Field(description="The documented assumption text")
    rationale: str = Field(description="Why this assumption is reasonable")


class ResidualCouplingCheck(BaseModel):
    """LLM output: coupling evaluation for moderate-similarity residuals."""

    is_coupled: bool = Field(
        description="Whether the requirement is coupled to the candidate container"
    )


class ResidualArchitecturalCheck(BaseModel):
    """LLM output: architectural relevance evaluation for low-similarity residuals."""

    implies_architectural_structure: bool = Field(
        description="Whether the requirement implies new architectural structure"
    )
    new_entity: dict | None = Field(
        default=None,
        description="Proposed minimal C4 entity with id, name, description, c4_type, technology",
    )
    new_relationships: list[dict] = Field(
        default_factory=list,
        description="Proposed relationships with id, source_id, target_id, description, relationship_type",
    )
    non_architectural_rationale: str = Field(
        default="",
        description="One-sentence rationale for non-architectural classification",
    )


# ── Fallback heuristics for coupling / architectural checks ──────────────────

# Keywords suggesting shared actors or data flows for coupling detection
_COUPLING_ACTOR_FLOW_KEYWORDS: set[str] = {
    "actor", "user", "admin", "customer", "client", "consumer",
    "producer", "publisher", "subscriber", "caller", "callee",
    "data", "flow", "request", "response", "event", "message",
    "api", "call", "invoke", "trigger", "integrate", "integration",
    "payload", "stream", "notify", "callback", "endpoint",
}

# Keywords suggesting architectural structure
_STRUCTURAL_KEYWORDS: set[str] = {
    "system", "service", "component", "container", "database",
    "queue", "api", "gateway", "module", "microservice",
    "server", "client", "broker", "cache", "proxy",
    "load balancer", "pipeline", "architecture", "infrastructure",
    "deploy", "cluster", "node", "ingress", "egress",
}


def _keyword_overlap_coupling(req_text: str, container_desc: str) -> bool:
    """Check if req and container share actor/flow keywords (fallback heuristic)."""
    req_lower = req_text.lower()
    cont_lower = container_desc.lower()
    for kw in _COUPLING_ACTOR_FLOW_KEYWORDS:
        if kw in req_lower and kw in cont_lower:
            return True
    # Also check for shared significant words (> 3 chars) as a looser signal
    req_words = {w for w in req_lower.split() if len(w) > 3}
    cont_words = {w for w in cont_lower.split() if len(w) > 3}
    if not req_words:
        return False
    return len(req_words & cont_words) / max(len(req_words), 1) > 0.25


def _has_structural_keywords(text: str) -> bool:
    """Check if text contains structural/architectural keywords (fallback heuristic)."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in _STRUCTURAL_KEYWORDS)


# ── Embedding initialization ────────────────────────────────────────────────


def _init_embeddings(config: RunnableConfig | None = None):
    """Try to initialize embedding cache and model for similarity-based dedup.

    Returns (cache, model) or (None, None) if unavailable.

    Config keys (priority order):
    - ``non_asr_db_path`` / ``non_asr_embeddings_db_path`` (legacy alias)
    - ``cache_dir`` / ``embedding_cache_dir`` (legacy alias)
    - ``final_merge_require_embeddings``: if True, raise on failure.
    """
    cfg = _get_configurable(config)

    db_path = cfg.get(
        "non_asr_db_path",
        cfg.get(
            "non_asr_embeddings_db_path",
            os.path.join(EMBEDDING_CACHE_DIR, "non_asr_embeddings.db"),
        ),
    )
    cache_dir = cfg.get(
        "cache_dir",
        cfg.get("embedding_cache_dir", EMBEDDING_CACHE_DIR),
    )
    model_name = cfg.get("embedding_model_name", EMBEDDING_MODEL_NAME)

    logger.debug("Embedding init: db_path=%s cache_dir=%s model=%s", db_path, cache_dir, model_name)

    try:
        cache = EmbeddingCache(db_path=db_path, model_name=model_name)
        model = get_embedding_model(cache_dir, model_name)
        return cache, model
    except ModelNonExistentException as e:
        logger.warning("Embedding model not found, disabling similarity dedup: %s", e)
        if cfg.get("final_merge_require_embeddings"):
            raise
        return None, None
    except Exception as e:
        logger.warning("Embedding init failed (%s: %s), disabling similarity dedup", type(e).__name__, e)
        if cfg.get("final_merge_require_embeddings"):
            raise
        return None, None


# ── Global merge ────────────────────────────────────────────────────────────


def _normalize_merge_questions(questions: list[dict], start_index: int = 0) -> list[dict]:
    """Post-process merge questions to align question types with AC requirements.

    Hierarchy-related issues from dedup become ``hierarchy_conflict``
    with owner ``judge_resolvable``.
    """
    normalized_qs = []
    for idx, q in enumerate(questions):
        if not isinstance(q, dict):
            continue
        q_copy = dict(q)
        reason = q_copy.get("reason", "")
        desc = q_copy.get("description", "") or ""

        # Map type -> question_type
        if "type" in q_copy and "question_type" not in q_copy:
            q_copy["question_type"] = q_copy.pop("type")

        # Set question_type to string
        question_type = q_copy.get("question_type") or "unknown"
        if not isinstance(question_type, str):
            question_type = str(question_type)
        q_copy["question_type"] = question_type

        # Apply specific classification rules for hierarchy mismatch
        if reason in (
            "orphan_container",
            "orphan_component",
            "unresolved_relationship_endpoint",
        ) or "mismatching C4 parent hierarchy" in desc:
            q_copy["question_type"] = "hierarchy_conflict"
            q_copy["resolution_owner"] = "judge_resolvable"
            q_copy["resolution"] = _SUGGESTED_RESOLUTIONS.get("hierarchy_conflict", "")
            q_copy["assumption_flag"] = False
        else:
            # Set owner if not present
            if "resolution_owner" not in q_copy:
                q_copy["resolution_owner"] = _classify_question_type(question_type)

        # Ensure ID exists
        if "id" not in q_copy or not q_copy["id"]:
            q_copy["id"] = f"q_{start_index + idx}_{question_type}"

        # Set default values for standard OpenQuestion fields
        q_copy.setdefault("description", f"Open question of type {question_type}")
        q_copy.setdefault("context", {})
        q_copy.setdefault("resolution", None)
        q_copy.setdefault("assumption_flag", False)
        q_copy.setdefault("metadata", {})

        normalized_qs.append(q_copy)

    return normalized_qs


def _global_merge(
    arch_model: dict,
    batch_outputs: list[dict],
    cache,
    model,
    config: RunnableConfig | None = None,
    start_time: float | None = None,
    timeout_s: float | None = None,
    metrics: dict | None = None,
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

    total = len(batch_outputs)
    for idx, batch_output in enumerate(batch_outputs, start=1):
        batch_id = ""
        if isinstance(batch_output, dict):
            batch_id = str(batch_output.get("batch_id") or batch_output.get("id") or idx)
        else:
            batch_id = str(idx)
        _emit_progress(
            "global_merge",
            "Merging batch output",
            config=config,
            metrics=metrics,
            processed=idx - 1,
            total=total,
            start_time=start_time,
            timeout_s=timeout_s,
            current_item_id=batch_id,
        )
        fragment = _extract_batch_fragment(batch_output)
        if fragment is None:
            _emit_progress(
                "global_merge",
                "Skipping batch output without an architecture fragment",
                config=config,
                metrics=metrics,
                processed=idx,
                total=total,
                start_time=start_time,
                timeout_s=timeout_s,
                current_item_id=batch_id,
            )
            continue
        running_model, questions, _ = deduplicate_and_merge_fragment(
            fragment, running_model, cache, model,
        )
        if metrics is not None:
            metrics["batch_outputs_merged"] = metrics.get("batch_outputs_merged", 0) + 1
        if questions:
            all_questions.extend([dict(q) for q in questions if isinstance(q, dict)])
        _emit_progress(
            "global_merge",
            "Batch output merged",
            config=config,
            metrics=metrics,
            processed=idx,
            total=total,
            start_time=start_time,
            timeout_s=timeout_s,
            current_item_id=batch_id,
        )

    all_questions = _normalize_merge_questions(all_questions)

    # Preserve other model keys from the original arch_model
    for key in ("cross_cutting_candidates", "assumption_flags"):
        if key in arch_model:
            running_model[key] = list(arch_model[key] or [])

    return running_model, all_questions


def _extract_batch_fragment(batch_output: dict) -> dict | None:
    """Return a C4 fragment from either a raw fragment or execution output record."""
    if not isinstance(batch_output, dict) or batch_output.get("skipped"):
        return None
    fragment = batch_output.get("arch_fragment")
    if isinstance(fragment, dict):
        return fragment
    if "entities" in batch_output or "relationships" in batch_output:
        return batch_output
    return None


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
    metrics: dict,
) -> str:
    """Generate a documented assumption for a human_preferred question.

    Uses ``judge_llm`` from config if available; falls back to a standard
    template referencing the original issue description.
    """
    qt = question.get("question_type", "unknown")
    desc = question.get("description")
    if not desc:
        desc = "No description provided."

    judge_llm = None
    cfg = _get_configurable(config)
    judge_llm = cfg.get("judge_llm")

    if judge_llm is not None:
        def _call() -> Any:
            reqs_text = "\n".join(f"- {rid}: {rdesc}" for rid, rdesc in requirements.items())
            prompt = load_prompt("generate_assumption.md", {
                "question_type": qt,
                "description": desc,
                "requirements": reqs_text or "No requirements specified.",
            })
            structured_llm = judge_llm.with_structured_output(DocumentedAssumption)
            return structured_llm.invoke(prompt)

        result = _invoke_llm(_call, config, metrics, label="generate_assumption")
        if result is not None:
            try:
                if isinstance(result, dict):
                    assumption = result.get("assumption", "")
                    rationale = result.get("rationale", "")
                else:
                    assumption = getattr(result, "assumption", "")
                    rationale = getattr(result, "rationale", "")
                return f"{assumption} (Rationale: {rationale})"
            except (ValidationError, Exception) as e:
                metrics["llm_fallbacks_used"] = metrics.get("llm_fallbacks_used", 0) + 1
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
    metrics: dict,
) -> dict:
    """Resolve all outstanding open questions.

    1. Apply human answers to matching questions (resets assumption flags).
    2. For unresolved ``judge_resolvable`` questions, apply pre-computed
       suggestion or default template, with ``assumption_flag = False``.
    3. For unresolved ``human_preferred`` questions, generate a documented
       assumption (LLM or fallback), with ``assumption_flag = True``.

    Mutates ``open_questions`` in place. Returns the updated ``arch_model``.

    In ``review_mode="interactive"``, raises an exception for unanswered
    human_preferred questions unless ``final_merge_allow_assumptions`` is set.
    """
    cfg = _get_configurable(config)

    # 1. Apply human answers
    answers = _normalize_answers(human_answers)
    if answers:
        open_questions, resolved_entity_ids = _map_answers_to_questions(
            answers, open_questions,
        )
        arch_model = dict(arch_model)
        arch_model = _apply_answer_overrides(arch_model, resolved_entity_ids)

    # Mark answered questions with metadata
    answered_ids = {a.get("question_id", "") for a in answers.values() if isinstance(a, dict)}
    for q in open_questions:
        if q.get("id") in answered_ids:
            meta = dict(q.get("metadata") or {})
            meta["resolution_status"] = "answered"
            meta["resolved_by"] = "human"
            q["metadata"] = meta

    # Clone arch_model lists & dicts to avoid direct state mutation
    arch_model = dict(arch_model)
    arch_model["entities"] = [dict(e) for e in (arch_model.get("entities") or [])]
    arch_model["relationships"] = [dict(r) for r in (arch_model.get("relationships") or [])]
    arch_model["boundary_groups"] = list(arch_model.get("boundary_groups") or [])
    arch_model["cross_cutting_candidates"] = list(arch_model.get("cross_cutting_candidates") or [])
    arch_model["assumption_flags"] = list(arch_model.get("assumption_flags") or [])

    review_mode = cfg.get("review_mode", "")
    unresolved_interactive_ids: list[str] = []
    if review_mode == "interactive" and not cfg.get("final_merge_allow_assumptions"):
        for q in open_questions:
            if (
                isinstance(q, dict)
                and q.get("resolution") is None
                and _get_resolution_owner(q) == "human_preferred"
            ):
                unresolved_interactive_ids.append(str(q.get("id") or "<missing-id>"))
        if unresolved_interactive_ids:
            raise HumanInputRequiredException(
                "Interactive final merge requires human answers for unresolved "
                f"question IDs: {', '.join(unresolved_interactive_ids)}"
            )

    for q in open_questions:
        if not isinstance(q, dict):
            continue
        # Skip already-resolved questions
        if q.get("resolution") is not None:
            continue

        owner = _get_resolution_owner(q)
        meta = dict(q.get("metadata") or {})

        if owner == "judge_resolvable":
            resolution = _get_default_suggestion(q)
            q["resolution"] = resolution
            q["assumption_flag"] = False
            meta["resolution_status"] = "auto_resolved"
            meta["resolved_by"] = "judge"
            q["metadata"] = meta

        elif owner == "human_preferred":
            assumption = _generate_assumption(q, arch_model, requirements, config, metrics)
            q["resolution"] = assumption
            q["assumption_flag"] = True
            meta["resolution_status"] = "assumed"
            meta["resolved_by"] = "final_merge"
            q["metadata"] = meta

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
                    ent_meta = dict(entity.get("metadata") or {})
                    ent_meta["assumption_flag"] = True
                    ent_meta["assumed"] = True
                    entity["metadata"] = ent_meta

    return arch_model


# ── Residual Requirements Decision Ladder (Story 4.2) ────────────────────────


def _extract_requirement_text(req: dict) -> str:
    """Extract the best text representation from a requirement dict.

    Uses ``condition_text`` for ASRs, ``description`` for non-ASRs.
    """
    text = (req.get("condition_text") or "").strip()
    if not text:
        text = (req.get("description") or "").strip()
    return text


def _check_coupling(
    req_id: str,
    req_text: str,
    is_asr: bool,
    best_container: dict,
    similarity: float,
    judge_llm,
    config: RunnableConfig | None,
    metrics: dict,
) -> bool:
    """Determine if a residual requirement is coupled to a candidate container.

    Uses judge LLM with ``judge_residual.md`` prompt when available;
    falls back to actor/flow keyword overlap heuristic.
    """
    if judge_llm is not None:
        def _call() -> Any:
            prompt = load_prompt("judge_residual.md", {
                "req_id": req_id,
                "req_description": req_text,
                "is_asr": str(is_asr),
                "has_target_container": True,
                "similarity": f"{similarity:.4f}",
                "container_id": best_container.get("id", ""),
                "container_name": best_container.get("name", ""),
                "container_description": best_container.get("description", ""),
            })
            structured_llm = judge_llm.with_structured_output(ResidualCouplingCheck)
            return structured_llm.invoke(prompt)

        result = _invoke_llm(_call, config, metrics, label="check_coupling")
        if result is not None:
            try:
                if isinstance(result, dict):
                    return bool(result.get("is_coupled", False))
                return bool(getattr(result, "is_coupled", False))
            except (ValidationError, Exception) as e:
                metrics["llm_fallbacks_used"] = metrics.get("llm_fallbacks_used", 0) + 1
                logger.debug("LLM coupling check failed, using fallback heuristic: %s", e)

    return _keyword_overlap_coupling(req_text, best_container.get("description", ""))


def _check_architectural(
    req_id: str,
    req_text: str,
    is_asr: bool,
    arch_model: dict,
    judge_llm,
    config: RunnableConfig | None,
    metrics: dict,
) -> tuple[bool, dict | None, list[dict] | None, str]:
    """Determine if a low-similarity residual implies architectural structure.

    Uses judge LLM with ``judge_residual.md`` prompt when available;
    falls back to structural keyword heuristic.

    Returns:
        (is_architectural, new_entity_dict, new_relationships, rationale)
    """
    if judge_llm is not None:
        def _call() -> Any:
            prompt = load_prompt("judge_residual.md", {
                "req_id": req_id,
                "req_description": req_text,
                "is_asr": str(is_asr),
                "has_target_container": False,
            })
            structured_llm = judge_llm.with_structured_output(ResidualArchitecturalCheck)
            return structured_llm.invoke(prompt)

        result = _invoke_llm(_call, config, metrics, label="check_architectural")
        if result is not None:
            try:
                if isinstance(result, dict):
                    return (
                        bool(result.get("implies_architectural_structure", False)),
                        result.get("new_entity"),
                        result.get("new_relationships") or [],
                        result.get("non_architectural_rationale", ""),
                    )
                return (
                    bool(getattr(result, "implies_architectural_structure", False)),
                    getattr(result, "new_entity", None),
                    getattr(result, "new_relationships", None) or [],
                    getattr(result, "non_architectural_rationale", ""),
                )
            except (ValidationError, Exception) as e:
                metrics["llm_fallbacks_used"] = metrics.get("llm_fallbacks_used", 0) + 1
                logger.debug("LLM architectural check failed, using fallback heuristic: %s", e)

    # Fallback: structural keyword heuristic
    if _has_structural_keywords(req_text):
        return (True, None, None, "")
    return (
        False,
        None,
        None,
        f"Requirement '{req_id}' is non-architectural: {req_text[:200]}",
    )


def _process_residual_requirements(
    unprocessed_requirements: list[dict],
    arch_model: dict,
    requirements: dict[str, str],
    cache,
    model,
    config: RunnableConfig | None,
    metrics: dict,
    start_time: float | None = None,
    timeout_s: float | None = None,
) -> tuple[dict, list[dict]]:
    """Process leftover requirements using the multi-step decision ladder.

    Each leftover requirement is evaluated sequentially against the merged
    C4 model. Based on cosine similarity to the best-matching container:

    - **> 0.75**: auto-enrich container description, append requirement ID.
    - **0.50–0.75**: check coupling (LLM or keyword heuristic); enrich with
      assumption flags if coupled, else add ``residual_coupling`` question.
    - **< 0.50**: check if architectural (LLM or structural keyword heuristic);
      propose and validate a minimal C4 entity if architectural, else add a
      ``coverage_gap`` question.

    Returns (updated_arch_model, residual_questions).
    """
    questions: list[dict] = []
    if not unprocessed_requirements:
        return arch_model, questions

    # Get judge_llm from config
    judge_llm = None
    cfg = _get_configurable(config)
    judge_llm = cfg.get("judge_llm")

    running_model = dict(arch_model)
    running_model["entities"] = list(running_model.get("entities") or [])
    running_model["relationships"] = list(running_model.get("relationships") or [])
    running_model["assumption_flags"] = list(running_model.get("assumption_flags") or [])

    # Local cache for container description embeddings
    container_embeddings: dict[str, list[float]] = {}

    total_requirements = len(unprocessed_requirements)
    for req_idx, req in enumerate(unprocessed_requirements, start=1):
        req_id = req.get("id", "")
        is_asr = req.get("is_asr", False)
        req_text = _extract_requirement_text(req)
        if not req_text:
            req_text = requirements.get(req_id, "")
        if not req_text:
            _emit_progress(
                "residual_processing",
                "Skipping residual requirement without text",
                config=config,
                metrics=metrics,
                processed=req_idx,
                total=total_requirements,
                start_time=start_time,
                timeout_s=timeout_s,
                current_item_id=req_id,
            )
            continue

        _emit_progress(
            "residual_processing",
            "Processing residual requirement",
            config=config,
            metrics=metrics,
            processed=req_idx - 1,
            total=total_requirements,
            start_time=start_time,
            timeout_s=timeout_s,
            current_item_id=req_id,
        )

        # ── Embed the requirement ──────────────────────────────────────────
        req_vec = None
        if cache is not None and model is not None:
            try:
                text_hash = cache.text_hash(req_text)
                req_vec = cache.get_cached_vector(req_id, text_hash)
                if req_vec is None:
                    embeddings = list(model.embed([req_text]))
                    req_vec = embeddings[0].tolist()
                    cache.store_vector(req_id, text_hash, req_vec)
            except Exception as e:
                logger.debug("Failed to embed requirement %s: %s", req_id, e)

        # ── Find best-matching container ────────────────────────────────────
        best_similarity = 0.0
        best_container: dict | None = None

        entities = running_model["entities"]
        for entity_idx, entity in enumerate(entities, start=1):
            entity_desc = (entity.get("description") or "").strip()
            if not entity_desc:
                continue
            entity_id = entity.get("id", "")
            _emit_progress(
                "residual_similarity_scan",
                "Scanning entity for residual similarity",
                config=config,
                metrics=metrics,
                processed=entity_idx,
                total=len(entities),
                start_time=start_time,
                timeout_s=timeout_s,
                current_item_id=f"{req_id}:{entity_id}",
            )

            similarity = 0.0
            if req_vec is not None and cache is not None and model is not None:
                try:
                    cont_vec = container_embeddings.get(entity_id)
                    if cont_vec is None:
                        cont_hash = cache.text_hash(entity_desc)
                        cont_vec = cache.get_cached_vector(entity_id, cont_hash)
                        if cont_vec is None:
                            cont_embeds = list(model.embed([entity_desc]))
                            cont_vec = cont_embeds[0].tolist()
                            cache.store_vector(entity_id, cont_hash, cont_vec)
                        container_embeddings[entity_id] = cont_vec
                    similarity = cosine_similarity(req_vec, cont_vec)
                except Exception as e:
                    logger.debug(
                        "Failed to compute similarity for %s vs %s: %s",
                        req_id, entity_id, e,
                    )

            if similarity > best_similarity:
                best_similarity = similarity
                best_container = entity

        # ── Decision ladder ─────────────────────────────────────────────────

        # When embeddings are disabled, skip similarity tiers.
        # Create one deterministic coverage_gap per residual unless structural
        # keywords identify an architectural entity.
        if cache is None or model is None:
            if _has_structural_keywords(req_text):
                _try_merge_residual_entity(
                    req_id, req_text, None, None,
                    running_model, questions, cache, model,
                )
            else:
                questions.append({
                    "id": f"coverage_gap_{req_id}",
                    "question_type": "coverage_gap",
                    "description": (
                        f"Requirement '{req_id}' ({req_text[:120]}) could not be "
                        f"evaluated: embeddings disabled."
                    ),
                    "resolution_owner": "human_preferred",
                    "resolution": None,
                    "assumption_flag": False,
                    "context": {"req_id": req_id},
                    "metadata": {"embedding_disabled": True},
                })
            _emit_progress(
                "residual_processing",
                "Residual requirement processed",
                config=config,
                metrics=metrics,
                processed=req_idx,
                total=total_requirements,
                start_time=start_time,
                timeout_s=timeout_s,
                current_item_id=req_id,
            )
            continue

        if best_similarity > RESIDUAL_HIGH_THRESHOLD and best_container is not None:
            # AC #2: High similarity — auto-enrich
            suffix = f" (Supports {req_id}: {req_text})"
            best_container["description"] = (
                (best_container.get("description") or "") + suffix
            )
            req_ids = list(best_container.get("requirement_ids") or [])
            if req_id not in req_ids:
                req_ids.append(req_id)
            best_container["requirement_ids"] = req_ids

        elif (
            RESIDUAL_MID_LOW <= best_similarity <= RESIDUAL_HIGH_THRESHOLD
            and best_container is not None
        ):
            # AC #3: Moderate similarity — coupling check
            is_coupled = _check_coupling(
                req_id, req_text, is_asr, best_container, best_similarity,
                judge_llm, config, metrics,
            )
            if is_coupled:
                suffix = f" (Supports {req_id}: {req_text})"
                best_container["description"] = (
                    (best_container.get("description") or "") + suffix
                )
                req_ids = list(best_container.get("requirement_ids") or [])
                if req_id not in req_ids:
                    req_ids.append(req_id)
                best_container["requirement_ids"] = req_ids

                meta = dict(best_container.get("metadata") or {})
                meta["assumption_flag"] = True
                meta["assumed"] = True
                best_container["metadata"] = meta

                cid = best_container.get("id", "")
                assumption_flags: list[str] = running_model.get("assumption_flags") or []
                if cid not in assumption_flags:
                    assumption_flags.append(cid)
                running_model["assumption_flags"] = assumption_flags
            else:
                questions.append({
                    "id": f"residual_coupling_{req_id}",
                    "question_type": "residual_coupling",
                    "description": (
                        f"Requirement '{req_id}' ({req_text[:120]}) has moderate "
                        f"similarity ({best_similarity:.2f}) to container "
                        f"'{best_container.get('id')}' but coupling was not confirmed. "
                        f"Manual review needed to determine integration approach."
                    ),
                    "resolution_owner": "human_preferred",
                    "resolution": None,
                    "assumption_flag": False,
                    "context": {
                        "req_id": req_id,
                        "container_id": best_container.get("id"),
                        "similarity": round(best_similarity, 4),
                    },
                })

        else:
            # AC #4/#5: Low similarity — architectural check
            is_arch, new_entity, new_rels, rationale = _check_architectural(
                req_id, req_text, is_asr, running_model, judge_llm, config, metrics,
            )
            if is_arch:
                # AC #4: Propose, validate, and merge a minimal C4 entity
                try:
                    _try_merge_residual_entity(
                        req_id, req_text, new_entity, new_rels,
                        running_model, questions, cache, model,
                    )
                except Exception as e:
                    logger.warning(
                        "Failed to process architectural residual %s: %s", req_id, e,
                    )
                    questions.append({
                        "id": f"coverage_gap_{req_id}",
                        "question_type": "coverage_gap",
                        "description": (
                            f"Requirement '{req_id}' ({req_text[:120]}) implies "
                            f"architectural structure but entity merge failed: {e}"
                        ),
                        "resolution_owner": "human_preferred",
                        "resolution": None,
                        "assumption_flag": False,
                        "context": {"req_id": req_id},
                    })
            else:
                # AC #5: Non-architectural — coverage gap
                questions.append({
                    "id": f"coverage_gap_{req_id}",
                    "question_type": "coverage_gap",
                    "description": rationale or (
                        f"Requirement '{req_id}' ({req_text[:120]}) is "
                        f"non-architectural and excluded from the model."
                    ),
                    "resolution_owner": "human_preferred",
                    "resolution": None,
                    "assumption_flag": False,
                    "context": {"req_id": req_id},
                })

        _emit_progress(
            "residual_processing",
            "Residual requirement processed",
            config=config,
            metrics=metrics,
            processed=req_idx,
            total=total_requirements,
            start_time=start_time,
            timeout_s=timeout_s,
            current_item_id=req_id,
        )

    return running_model, _normalize_merge_questions(questions, start_index=1000)


def _try_merge_residual_entity(
    req_id: str,
    req_text: str,
    new_entity: dict | None,
    new_rels: list[dict] | None,
    running_model: dict,
    questions: list[dict],
    cache,
    model,
) -> None:
    """Propose and validate a residual architectural entity.

    Wraps the LLM-proposed entity in an ``ArchFragment``, validates via
    ``enforce_fragment_hierarchy``, and merges via ``deduplicate_and_merge_fragment``.
    Falls back to a generated minimal entity when the LLM provides no proposal.
    """
    if new_entity is None:
        # Generate a minimal container entity as fallback
        safe_id = req_id.lower().replace("-", "_").replace(" ", "_")
        new_entity = {
            "id": f"residual_{safe_id}",
            "name": req_id,
            "description": req_text,
            "c4_type": "container",
            "technology": "",
        }

    # Ensure required fields
    new_entity.setdefault("id", f"residual_{req_id}")
    new_entity.setdefault("name", req_id)
    new_entity.setdefault("description", req_text)
    new_entity.setdefault("c4_type", "container")
    new_entity.setdefault("technology", "")
    new_entity.setdefault("requirement_ids", [req_id])

    # Assign default parent system/container to satisfy C4 metamodel validation
    if new_entity.get("c4_type") == "container" and not new_entity.get("parent_system_id"):
        systems = [e for e in running_model.get("entities", []) if e.get("c4_type") == "system"]
        if systems:
            new_entity["parent_system_id"] = systems[0]["id"]

    if new_entity.get("c4_type") == "component" and not new_entity.get("parent_container_id"):
        containers = [e for e in running_model.get("entities", []) if e.get("c4_type") == "container"]
        if containers:
            new_entity["parent_container_id"] = containers[0]["id"]

    new_entities = [C4Entity.model_validate(new_entity)]

    # Build relationships, preserving LLM-proposed requirement_ids.
    # If missing, default to [req_id] for relationships created for this residual.
    new_relationships: list[C4Relationship] = []
    for r in (new_rels or []):
        rel_dict = dict(r)
        if not rel_dict.get("requirement_ids"):
            rel_dict["requirement_ids"] = [req_id]
        new_relationships.append(C4Relationship.model_validate(rel_dict))

    fragment = ArchFragment(
        entities=new_entities,
        relationships=new_relationships,
    )

    # Validate hierarchy
    cleaned_fragment, hierarchy_qs = enforce_fragment_hierarchy(
        fragment,
        running_model,
        batch_id=f"residual_{req_id}",
        strategy="residual",
    )
    if hierarchy_qs:
        questions.extend(hierarchy_qs)

    # Merge into running model
    updated_model, merge_qs, _ = deduplicate_and_merge_fragment(
        cleaned_fragment.model_dump(), running_model, cache, model,
    )
    if merge_qs:
        questions.extend([dict(q) for q in merge_qs if isinstance(q, dict)])

    # Update running model in-place
    running_model["entities"] = updated_model.get("entities") or []
    running_model["relationships"] = updated_model.get("relationships") or []
    if "boundary_groups" in updated_model:
        existing_bgs = running_model.get("boundary_groups") or []
        new_bgs = updated_model.get("boundary_groups") or []
        existing_bgs.extend(new_bgs)
        running_model["boundary_groups"] = existing_bgs


# ── Traceability gap detection helpers ──────────────────────────────────────


def _collect_input_requirement_ids(state: RAAState) -> set[str]:
    """Collect all canonical input requirement IDs from state sources."""
    input_ids: set[str] = set()
    for rid in (state.get("requirements") or {}).keys():
        input_ids.add(to_r_id(rid))
    for req in (state.get("normalized_asrs") or []):
        if "id" in req:
            input_ids.add(to_r_id(req["id"]))
    for req in (state.get("normalized_non_asr") or []):
        if "id" in req:
            input_ids.add(to_r_id(req["id"]))
    for req in (state.get("unprocessed_requirements") or []):
        if "id" in req:
            input_ids.add(to_r_id(req["id"]))
    return input_ids


def _collect_execution_assigned_ids(
    state: RAAState, input_ids: set[str],
) -> tuple[set[str], dict[str, list[str]]]:
    """Collect requirement IDs assigned to execution batches, restricted to known inputs.

    Returns (assigned_ids, rid_to_batch_ids) where rid_to_batch_ids maps each
    assigned requirement ID to the list of batch IDs that reference it.
    """
    assigned: set[str] = set()
    rid_to_batches: dict[str, list[str]] = {}
    for batch in (state.get("execution_queue") or []):
        if not isinstance(batch, dict):
            continue
        batch_id = str(batch.get("batch_id") or batch.get("id") or "")
        for key in ("asr_ids", "non_asr_ids"):
            for raw in (batch.get(key) or []):
                norm = to_r_id(str(raw))
                if norm in input_ids:
                    assigned.add(norm)
                    rid_to_batches.setdefault(norm, []).append(batch_id)
    return assigned, rid_to_batches


def _collect_traced_ids(
    arch_model: dict,
    all_questions: list[dict],
    input_ids: set[str],
) -> set[str]:
    """Collect requirement IDs already traced via model elements or questions."""
    traced: set[str] = set()
    for entity in (arch_model.get("entities") or []):
        for rid in (entity.get("requirement_ids") or []):
            norm = to_r_id(str(rid))
            if norm in input_ids:
                traced.add(norm)
    for rel in (arch_model.get("relationships") or []):
        for rid in (rel.get("requirement_ids") or []):
            norm = to_r_id(str(rid))
            if norm in input_ids:
                traced.add(norm)
    for q in all_questions:
        traced.update(_extract_question_requirement_ids(q, input_ids))
    return traced


def _generate_batch_trace_gap_questions(
    state: RAAState,
    arch_model: dict,
    all_questions: list[dict],
    config: RunnableConfig | None = None,
    metrics: dict | None = None,
    start_time: float | None = None,
    timeout_s: float | None = None,
) -> list[dict]:
    """Generate coverage_gap questions for batch-assigned but untraced requirements.

    This is the pre-audit safety net: requirements assigned to execution batches
    but omitted from all merged C4 trace locations become explicit per-requirement
    coverage_gap questions before the traceability audit.
    """
    input_ids = _collect_input_requirement_ids(state)
    if not input_ids:
        return []

    assigned_ids, rid_to_batches = _collect_execution_assigned_ids(state, input_ids)
    if not assigned_ids:
        return []

    traced_ids = _collect_traced_ids(arch_model, all_questions, input_ids)
    missing_ids = assigned_ids - traced_ids

    if metrics is not None:
        metrics["batch_assigned_trace_gaps_created"] = len(missing_ids)

    _emit_progress(
        "traceability_gap_detection",
        f"Detected {len(missing_ids)} batch-assigned requirements without trace",
        config=config,
        metrics=metrics,
        processed=0,
        total=len(missing_ids),
        start_time=start_time,
        timeout_s=timeout_s,
    )

    gap_questions: list[dict] = []
    for idx, rid in enumerate(sorted(missing_ids), start=1):
        batch_ids = rid_to_batches.get(rid, [])
        gap_questions.append({
            "id": f"coverage_gap_{rid}",
            "question_type": "coverage_gap",
            "description": (
                f"Requirement '{rid}' was assigned to execution batch(es) "
                f"{batch_ids} but no merged model element or prior question "
                f"preserved traceability."
            ),
            "resolution_owner": "human_preferred",
            "resolution": None,
            "assumption_flag": False,
            "context": {"req_id": rid},
            "requirement_ids": [rid],
            "metadata": {
                "source": "final_merge_untraced_batch_requirement",
                "batch_ids": batch_ids,
            },
        })
        _emit_progress(
            "traceability_gap_detection",
            f"Created coverage_gap for {rid}",
            config=config,
            metrics=metrics,
            processed=idx,
            total=len(missing_ids),
            start_time=start_time,
            timeout_s=timeout_s,
            current_item_id=rid,
        )

    return gap_questions


# ── Main Node ───────────────────────────────────────────────────────────────


def _normalize_requirement_id_values(value: Any, input_ids: set[str]) -> set[str]:
    """Normalize a scalar/list requirement ID value against known input IDs."""
    values = value if isinstance(value, list) else [value]
    found: set[str] = set()
    for raw in values:
        if raw is None:
            continue
        norm = to_r_id(str(raw))
        if norm in input_ids:
            found.add(norm)
    return found


def _extract_question_requirement_ids(question: dict, input_ids: set[str]) -> set[str]:
    """Extract normalized requirement IDs explicitly referenced by a question."""
    if not isinstance(question, dict):
        return set()

    found: set[str] = set()
    ctx = question.get("context") if isinstance(question.get("context"), dict) else {}
    if ctx:
        found.update(_normalize_requirement_id_values(ctx.get("req_id"), input_ids))
        found.update(_normalize_requirement_id_values(ctx.get("requirement_ids"), input_ids))
    found.update(_normalize_requirement_id_values(question.get("requirement_ids"), input_ids))

    q_id = str(question.get("id") or "")
    q_type = str(question.get("question_type") or question.get("type") or "")
    standard_prefixes = ("coverage_gap_", "residual_coupling_")
    if q_type in ("coverage_gap", "residual_coupling") or q_id.startswith(standard_prefixes):
        for norm_req_id in input_ids:
            stripped = norm_req_id.lstrip("Rr")
            if q_id in (
                f"coverage_gap_{norm_req_id}",
                f"residual_coupling_{norm_req_id}",
                f"coverage_gap_{stripped}",
                f"residual_coupling_{stripped}",
            ):
                found.add(norm_req_id)

    return found


def _value_contains_requirement_id(value: Any, rid: str) -> bool:
    """Best-effort recursive diagnostic search for a normalized requirement ID."""
    if value is None:
        return False
    if isinstance(value, dict):
        return any(_value_contains_requirement_id(v, rid) for v in value.values())
    if isinstance(value, (list, tuple, set)):
        return any(_value_contains_requirement_id(v, rid) for v in value)
    if isinstance(value, str):
        if to_r_id(value) == rid:
            return True
        stripped = rid.lstrip("Rr")
        return bool(
            re.search(rf'(?<![A-Za-z0-9_-]){re.escape(rid)}(?![A-Za-z0-9_-])', value)
            or re.search(rf'(?<![A-Za-z0-9_-]){re.escape(stripped)}(?![A-Za-z0-9_-])', value)
        )
    return False


def _traceability_missing_diagnostics(
    rid: str,
    state: RAAState,
    arch_model: dict,
    all_questions: list[dict],
    input_ids: set[str],
) -> dict:
    """Build diagnostics for missing traceability without treating them as coverage."""
    entity_ids = [
        e.get("id", "")
        for e in arch_model.get("entities", [])
        if _value_contains_requirement_id(e.get("requirement_ids", []), rid)
    ]
    relationship_ids = [
        r.get("id", "")
        for r in arch_model.get("relationships", [])
        if _value_contains_requirement_id(r.get("requirement_ids", []), rid)
    ]
    candidate_question_ids = [
        q.get("id", "")
        for q in all_questions
        if rid in _extract_question_requirement_ids(q, input_ids)
    ]
    return {
        "appeared_in_batches": _value_contains_requirement_id(state.get("batch_outputs") or [], rid),
        "appeared_in_execution_queue": _value_contains_requirement_id(
            state.get("execution_queue") or [],
            rid,
        ),
        "appeared_in_unprocessed_requirements": _value_contains_requirement_id(
            state.get("unprocessed_requirements") or [],
            rid,
        ),
        "model_entity_ids": entity_ids,
        "relationship_ids": relationship_ids,
        "candidate_question_ids": candidate_question_ids,
    }


def _run_traceability_audit(
    state: RAAState,
    arch_model: dict,
    all_questions: list[dict],
) -> dict:
    """Execute a final traceability audit on all input requirement IDs.

    Every requirement must be traceable to exactly one location:
    - model locations from entity or relationship ``requirement_ids``
    - question locations from per-requirement ``coverage_gap`` or
      ``residual_coupling`` questions

    Batch membership alone is NOT a valid final trace location.
    All IDs are normalized via ``to_r_id()`` for comparison.

    Raises:
        TraceabilityAuditException: If any requirement is unmapped, missing,
            mapped to multiple locations, or if bulk rejection is detected.
    """
    # 1. Collect all input requirement IDs (normalized)
    input_ids: set[str] = set()
    for rid in (state.get("requirements") or {}).keys():
        input_ids.add(to_r_id(rid))
    for req in (state.get("normalized_asrs") or []):
        if "id" in req:
            input_ids.add(to_r_id(req["id"]))
    for req in (state.get("normalized_non_asr") or []):
        if "id" in req:
            input_ids.add(to_r_id(req["id"]))
    for req in (state.get("unprocessed_requirements") or []):
        if "id" in req:
            input_ids.add(to_r_id(req["id"]))

    # 2. Build trace registry — model locations only (entity + relationship)
    trace_map: dict[str, list[dict]] = {rid: [] for rid in input_ids}

    for entity in arch_model.get("entities", []):
        entity_id = entity.get("id", "")
        for req_id in entity.get("requirement_ids", []):
            norm_req_id = to_r_id(req_id)
            if norm_req_id in trace_map:
                trace_map[norm_req_id].append({
                    "type": "model",
                    "id": entity_id,
                    "description": f"Mapped to C4 entity '{entity_id}'",
                })

    for rel in arch_model.get("relationships", []):
        rel_id = rel.get("id", "")
        for req_id in rel.get("requirement_ids", []):
            norm_req_id = to_r_id(req_id)
            if norm_req_id in trace_map:
                trace_map[norm_req_id].append({
                    "type": "model",
                    "id": rel_id,
                    "description": f"Mapped to C4 relationship '{rel_id}'",
                })

    # 3. Check open questions for coverage_gap / residual_coupling
    for q in all_questions:
        q_id = q.get("id", "")
        q_type = q.get("question_type", "")
        if q_type not in ("coverage_gap", "residual_coupling"):
            continue
        for norm_req_id in _extract_question_requirement_ids(q, input_ids):
            if not any(
                loc["type"] == "question" and loc["id"] == q_id
                for loc in trace_map[norm_req_id]
            ):
                trace_map[norm_req_id].append({
                    "type": "question",
                    "id": q_id,
                    "description": f"Logged as open question '{q_id}' of type '{q_type}'",
                })

    # 4. Bulk rejection detection — primary: structured context
    for rid, locations in trace_map.items():
        for loc in locations:
            if loc["type"] != "question":
                continue
            q = next((x for x in all_questions if x.get("id") == loc["id"]), None)
            if q is None:
                continue
            extracted_ids = _extract_question_requirement_ids(q, input_ids)
            if len(extracted_ids) > 1:
                raise TraceabilityAuditException(
                    f"Bulk rejection prohibited: Question '{q.get('id')}' "
                    f"contains multiple requirement IDs, indicating bulk rejection."
                )

    # A requirement can legitimately be represented at several C4 levels
    # (for example system, container, component, and relationship). Keep the
    # final manifest one-to-one by selecting a canonical model location while
    # retaining the related model locations as diagnostics. Question locations
    # remain separate, so model+question still fails below.
    for rid, locations in list(trace_map.items()):
        model_locations = [loc for loc in locations if loc["type"] == "model"]
        question_locations = [loc for loc in locations if loc["type"] == "question"]
        if len(model_locations) > 1:
            primary = dict(model_locations[0])
            related = [
                {"type": loc["type"], "id": loc["id"], "description": loc["description"]}
                for loc in model_locations[1:]
            ]
            primary["related_locations"] = related
            related_ids = ", ".join(loc["id"] for loc in related)
            primary["description"] = (
                f"{primary['description']}; also mapped to related C4 model "
                f"locations: {related_ids}"
            )
            trace_map[rid] = [primary] + question_locations

    # 5. Verify 100% accounting — exactly one location per requirement
    manifest: dict[str, dict] = {}
    for rid, locations in trace_map.items():
        if len(locations) == 0:
            diagnostics = _traceability_missing_diagnostics(
                rid,
                state,
                arch_model,
                all_questions,
                input_ids,
            )
            raise TraceabilityAuditException(
                f"Traceability audit failed: Requirement '{rid}' is unmapped or missing "
                f"(silent drop). Diagnostics: {json.dumps(diagnostics, sort_keys=True)}"
            )
        elif len(locations) > 1:
            loc_descriptions = ", ".join(f"{loc['type']}:{loc['id']}" for loc in locations)
            raise TraceabilityAuditException(
                f"Traceability audit failed: Requirement '{rid}' is mapped to multiple locations: {loc_descriptions}."
            )
        else:
            loc = locations[0]
            manifest[rid] = {
                "location_type": loc["type"],
                "location_id": loc["id"],
                "description": loc["description"],
            }
            if "related_locations" in loc:
                manifest[rid]["related_locations"] = loc["related_locations"]

    return manifest


# ── Diagram Manifest & Output (Story 4.4) ──────────────────────────────────


def _compile_diagram_manifest(arch_model: dict) -> list[dict]:
    """Compile the diagram manifest from the final C4 model.

    Manifest length = ``(2 * number of systems) + total containers across all systems``.

    Each system gets a context diagram and a container diagram.
    Each container gets a component diagram.
    """
    entities = arch_model.get("entities") or []

    systems = [e for e in entities if e.get("c4_type") == "system"]
    containers = [e for e in entities if e.get("c4_type") == "container"]

    manifest: list[dict] = []

    for system in systems:
        sid = system.get("id", "")
        sname = system.get("name", sid)
        manifest.append({
            "type": "context",
            "system_id": sid,
            "name": f"{sname} - System Context",
        })
        manifest.append({
            "type": "container",
            "system_id": sid,
            "name": f"{sname} - Container Diagram",
        })

    for container in containers:
        cid = container.get("id", "")
        cname = container.get("name", cid)
        manifest.append({
            "type": "component",
            "container_id": cid,
            "name": f"{cname} - Component Diagram",
        })

    expected_len = (2 * len(systems)) + len(containers)
    if len(manifest) != expected_len:
        logger.error(
            "Diagram manifest length mismatch: expected %d, got %d",
            expected_len, len(manifest),
        )

    return manifest


def _write_output_files(
    arch_model: dict,
    open_questions: list[dict],
    diagram_manifest: list[dict],
    config: RunnableConfig | None,
) -> bool:
    """Write finalized JSON output files to the output directory.

    Writes ``arch_model.json``, ``open_questions.json``, and
    ``diagram_manifest.json`` atomically (write to .tmp, then ``os.replace``).
    Output directory comes from config or defaults to
    ``_bmad-output/implementation-artifacts/``.

    Respects ``final_merge_write_outputs`` config key (default True).
    When False, skips file writes but still returns True.

    Returns True if writes succeeded or were skipped intentionally.
    """
    cfg = _get_configurable(config)

    if cfg.get("final_merge_write_outputs", True) is False:
        logger.info("Output file writes disabled via config.")
        return True

    output_dir = cfg.get(
        "output_dir",
        os.path.join(os.getcwd(), "_bmad-output", "implementation-artifacts"),
    )
    arch_path = os.path.join(output_dir, "arch_model.json")
    questions_path = os.path.join(output_dir, "open_questions.json")
    manifest_path = os.path.join(output_dir, "diagram_manifest.json")

    files_to_write = [
        (arch_model, arch_path),
        (open_questions, questions_path),
        (diagram_manifest, manifest_path),
    ]

    try:
        os.makedirs(output_dir, exist_ok=True)
        for data, path in files_to_write:
            tmp_path = path + ".tmp"
            with open(tmp_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
            os.replace(tmp_path, path)
        logger.info("Output files written to %s", output_dir)
        return True
    except OSError as e:
        logger.warning("Failed to write output files to %s: %s", output_dir, e)
        return False


_C4_TYPE_RANK = {
    "person": 1,
    "system": 1,
    "external_system": 1,
    "container": 2,
    "component": 3,
}

def _fix_relationship_scopes(arch_model: dict) -> dict:
    """Auto-correct diagram_scope on relationships to match the C4 rank
    of their endpoints, using the same logic as validate_c4_model."""
    entity_types = {
        e["id"]: e["c4_type"]
        for e in (arch_model.get("entities") or [])
    }

    corrected = []
    for rel in (arch_model.get("relationships") or []):
        src_type = entity_types.get(rel.get("source_id"))
        tgt_type = entity_types.get(rel.get("target_id"))

        if src_type is None or tgt_type is None:
            # Can't correct without both endpoints — leave as-is
            corrected.append(rel)
            continue

        src_rank = _C4_TYPE_RANK.get(src_type, 1)
        tgt_rank = _C4_TYPE_RANK.get(tgt_type, 1)
        expected_scope = _scope_from_rank(max(src_rank, tgt_rank))

        if rel.get("diagram_scope") != expected_scope:
            rel = dict(rel)
            rel["diagram_scope"] = expected_scope
        corrected.append(rel)

    arch_model = dict(arch_model)
    arch_model["relationships"] = corrected
    return arch_model

def _sanitize_arch_model(arch_model: dict) -> dict:
    """
    Pre-validation sanitization pass. Fixes all structural inconsistencies
    that the LLM may introduce across batch outputs:
      1. Remove relationships whose source or target entity doesn't exist
      2. Remove components whose parent_container_id doesn't exist or isn't a container
      3. Remove containers whose parent_system_id doesn't exist or isn't a system/external_system
      4. Fix diagram_scope to match endpoint depth
    """
    entities = list(arch_model.get("entities") or [])
    relationships = list(arch_model.get("relationships") or [])

    entity_ids = {e["id"] for e in entities}
    entity_types = {e["id"]: e["c4_type"] for e in entities}

    SYSTEM_TYPES = {"system", "external_system"}
    CONTAINER_TYPES = {"container"}
    C4_TYPE_RANK = {
        "person": 1, "system": 1, "external_system": 1,
        "container": 2, "component": 3,
    }

    def scope_from_rank(rank: int) -> str:
        if rank >= 3:
            return "component"
        elif rank >= 2:
            return "container"
        return "context"

    # 1. Drop components with missing or wrong-typed parent_container_id
    clean_entities = []
    for e in entities:
        if e["c4_type"] == "component":
            pid = e.get("parent_container_id")
            if not pid or pid not in entity_ids:
                print(f"[sanitize] Dropping component '{e['id']}': "
                      f"parent_container_id '{pid}' not in model")
                continue
            if entity_types[pid] not in CONTAINER_TYPES:
                print(f"[sanitize] Dropping component '{e['id']}': "
                      f"parent '{pid}' is '{entity_types[pid]}', not a container")
                continue
        elif e["c4_type"] == "container":
            pid = e.get("parent_system_id")
            if pid and pid not in entity_ids:
                print(f"[sanitize] Clearing parent_system_id '{pid}' "
                      f"from container '{e['id']}': not in model")
                e = dict(e)
                e["parent_system_id"] = None
            elif pid and entity_types.get(pid) not in SYSTEM_TYPES:
                print(f"[sanitize] Clearing parent_system_id '{pid}' "
                      f"from container '{e['id']}': type is '{entity_types.get(pid)}'")
                e = dict(e)
                e["parent_system_id"] = None
        clean_entities.append(e)

    # Rebuild lookup after entity cleanup
    entity_ids = {e["id"] for e in clean_entities}
    entity_types = {e["id"]: e["c4_type"] for e in clean_entities}

    # 2. Drop relationships with unknown source or target, fix scopes on the rest
    clean_relationships = []
    for r in relationships:
        src = r.get("source_id")
        tgt = r.get("target_id")
        if src and src not in entity_ids:
            print(f"[sanitize] Dropping rel '{r.get('id')}': "
                  f"unknown source '{src}'")
            continue
        if tgt and tgt not in entity_ids:
            print(f"[sanitize] Dropping rel '{r.get('id')}': "
                  f"unknown target '{tgt}'")
            continue
        # Fix scope
        src_rank = C4_TYPE_RANK.get(entity_types.get(src), 1)
        tgt_rank = C4_TYPE_RANK.get(entity_types.get(tgt), 1)
        expected_scope = scope_from_rank(max(src_rank, tgt_rank))
        if r.get("diagram_scope") != expected_scope:
            r = dict(r)
            r["diagram_scope"] = expected_scope
        clean_relationships.append(r)

    result = dict(arch_model)
    result["entities"] = clean_entities
    result["relationships"] = clean_relationships
    return result

def final_merge(
    state: RAAState,
    config: RunnableConfig | None = None,
) -> dict:
    """Merge all batch outputs globally, validate, and produce final output files.

    1. Combines all batch fragments via global entity deduplication.
    2. Processes residual unprocessed requirements (Story 4.2 decision ladder).
    3. Resolves every open question so no question has a ``null`` resolution.
    4. Runs the 100% requirements traceability audit (Story 4.3).
    5. Validates the final model against C4 metamodel rules (Story 4.4).
    6. Compiles the diagram manifest and writes output files (Story 4.4).

    Progress events are emitted via ``get_stream_writer()`` (LangGraph
    ``stream_mode="custom"``). Notebook callers can also set
    ``final_merge_progress_to_stdout=True`` in configurable for stdout output.

    Config keys under ``configurable``:

    - ``final_merge_timeout_s``: wall-clock timeout; raises ``MergeTimeoutError``.
    - ``final_merge_progress_to_stdout``: print progress with flush (bool).
    - ``final_merge_llm_timeout_s``: per-LLM-call timeout (default 60).
    - ``final_merge_require_embeddings``: raise on embedding failure.
    - ``final_merge_allow_assumptions``: allow auto-assumptions in interactive mode.
    - ``final_merge_write_outputs``: write output files (default True).

    Returns:
        dict with keys: ``arch_model``, ``open_questions``,
        ``traceability_manifest``, ``diagram_manifest``,
        ``final_merge_metrics``.
    """
    cfg = _get_configurable(config)

    start_time = time.monotonic()
    timeout_s = cfg.get("final_merge_timeout_s")

    arch_model: dict = state.get("arch_model") or {}
    batch_outputs: list[dict] = list(state.get("batch_outputs") or [])
    open_questions: list[dict] = [
        dict(q) for q in (state.get("open_questions") or []) if isinstance(q, dict)
    ]
    human_answers: dict = state.get("human_answers") or {}
    requirements: dict[str, str] = state.get("requirements") or {}
    unprocessed_requirements: list[dict] = list(
        state.get("unprocessed_requirements") or []
    )

    # Metrics collected throughout the run
    metrics: dict[str, Any] = {
        "batch_outputs_seen": len(batch_outputs),
        "batch_outputs_merged": 0,
        "residual_requirements_seen": len(unprocessed_requirements),
        "residual_questions_created": 0,
        "open_questions_resolved": 0,
        "embedding_enabled": False,
        "llm_calls_attempted": 0,
        "llm_calls_skipped": 0,
        "llm_calls_failed": 0,
        "llm_fallbacks_used": 0,
        "llm_calls_timed_out": 0,
    }

    # 1. Initialize embeddings for similarity-based dedup
    _emit_progress(
        "embedding_init", "Initializing embeddings",
        config=config, metrics=metrics,
        start_time=start_time, timeout_s=timeout_s,
    )
    cache, model = _init_embeddings(config)
    metrics["embedding_enabled"] = cache is not None and model is not None

    # 2. Global merge of all batch outputs
    _emit_progress(
        "global_merge", "Starting global merge",
        config=config, metrics=metrics,
        start_time=start_time, timeout_s=timeout_s,
    )
    arch_model, merge_questions = _global_merge(
        arch_model, batch_outputs, cache, model,
        config=config, start_time=start_time, timeout_s=timeout_s, metrics=metrics,
    )
    _emit_progress("global_merge", "Global merge complete",
                   config=config, metrics=metrics,
                   processed=metrics["batch_outputs_merged"],
                   total=metrics["batch_outputs_seen"],
                   start_time=start_time, timeout_s=timeout_s)

    # 3. Process residual unprocessed requirements (Story 4.2 decision ladder)
    _emit_progress("residual_processing", "Processing residual requirements",
                   config=config, metrics=metrics,
                   total=metrics["residual_requirements_seen"],
                   start_time=start_time, timeout_s=timeout_s)
    arch_model, residual_questions = _process_residual_requirements(
        unprocessed_requirements, arch_model, requirements, cache, model, config, metrics,
        start_time=start_time, timeout_s=timeout_s,
    )
    metrics["residual_questions_created"] = len(residual_questions)
    _emit_progress("residual_processing", "Residual processing complete",
                   config=config, metrics=metrics,
                   processed=metrics["residual_requirements_seen"],
                   total=metrics["residual_requirements_seen"],
                   start_time=start_time, timeout_s=timeout_s)

    # Combine all open questions to resolve them together
    all_questions = open_questions + merge_questions + residual_questions

    # 3b. Pre-audit safety net: generate coverage_gap questions for
    #     batch-assigned requirements that are missing from all trace locations.
    batch_gap_questions = _generate_batch_trace_gap_questions(
        state, arch_model, all_questions,
        config=config, metrics=metrics,
        start_time=start_time, timeout_s=timeout_s,
    )
    if batch_gap_questions:
        all_questions.extend(batch_gap_questions)

    # 4. Resolve all open questions (including merge and residual questions)
    _emit_progress("question_resolution", "Resolving open questions",
                   config=config, metrics=metrics,
                   total=len(all_questions),
                   start_time=start_time, timeout_s=timeout_s)
    arch_model = _resolve_all_questions(
        all_questions, human_answers, arch_model, requirements, config, metrics,
    )
    metrics["open_questions_resolved"] = sum(
        1 for q in all_questions if isinstance(q, dict) and q.get("resolution") is not None
    )
    _emit_progress("question_resolution", "Questions resolved",
                   config=config, metrics=metrics,
                   processed=metrics["open_questions_resolved"],
                   total=len(all_questions),
                   start_time=start_time, timeout_s=timeout_s)

    # 5. Run the 100% requirements traceability audit (Story 4.3)
    _emit_progress("traceability_audit", "Running traceability audit",
                   config=config, metrics=metrics,
                   start_time=start_time, timeout_s=timeout_s)
    traceability_manifest = _run_traceability_audit(
        state, arch_model, all_questions,
    )
    _emit_progress("traceability_audit", "Traceability audit complete",
                   config=config, metrics=metrics,
                   start_time=start_time, timeout_s=timeout_s)

    # 5b. Auto-correct relationship scopes before validation
    arch_model = _sanitize_arch_model(arch_model)

    # TEMPORARY DIAGNOSTIC v2
    entity_ids_raw = {e['id'] for e in arch_model.get('entities', [])}
    from raa.judge.deduplication import normalize_entity_id
    entity_ids_norm = {normalize_entity_id(e['id']) for e in arch_model.get('entities', [])}
    
    for e in arch_model.get('entities', []):
        if e['c4_type'] == 'component':
            pid = e.get('parent_container_id')
            if pid:
                in_raw = pid in entity_ids_raw
                in_norm = normalize_entity_id(pid) in entity_ids_norm
                if not in_raw or not in_norm:
                    print(f"component '{e['id']}' -> '{pid}' | in_raw={in_raw} in_norm={in_norm}")
    # END DIAGNOSTIC

    # 6. Validate the final model against C4 metamodel rules (Story 4.4, AC #1)
    _emit_progress("validation", "Validating C4 model",
                   config=config, metrics=metrics,
                   start_time=start_time, timeout_s=timeout_s)
    validate_c4_model(arch_model)

    # 7. Set status to "final" (Story 4.4, AC #4)
    arch_model["status"] = "final"

    # 8. Compile diagram manifest (Story 4.4, AC #2)
    diagram_manifest = _compile_diagram_manifest(arch_model)

    # 9. Write finalized JSON files (Story 4.4, AC #3)
    _emit_progress("output", "Writing output files",
                   config=config, metrics=metrics,
                   start_time=start_time, timeout_s=timeout_s)
    _write_output_files(arch_model, all_questions, diagram_manifest, config)

    _emit_progress("complete", "final_merge complete",
                   config=config, metrics=metrics,
                   start_time=start_time, timeout_s=timeout_s)

    return {
        "arch_model": arch_model,
        "open_questions": all_questions,
        "traceability_manifest": traceability_manifest,
        "diagram_manifest": diagram_manifest,
        "final_merge_metrics": metrics,
    }
