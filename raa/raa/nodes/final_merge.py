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
from typing import Any

from langchain_core.runnables import RunnableConfig
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
)
from raa.utils.prompt_loader import load_prompt

from raa.utils.id_utils import to_r_id

logger = logging.getLogger(__name__)


class TraceabilityAuditException(Exception):
    """Raised when the 100% requirements traceability audit fails."""
    pass


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
) -> bool:
    """Determine if a residual requirement is coupled to a candidate container.

    Uses judge LLM with ``judge_residual.md`` prompt when available;
    falls back to actor/flow keyword overlap heuristic.
    """
    if judge_llm is not None:
        try:
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
            result = structured_llm.invoke(prompt)
            if isinstance(result, dict):
                return bool(result.get("is_coupled", False))
            return bool(getattr(result, "is_coupled", False))
        except (ValidationError, Exception) as e:
            logger.debug("LLM coupling check failed, using fallback heuristic: %s", e)

    return _keyword_overlap_coupling(req_text, best_container.get("description", ""))


def _check_architectural(
    req_id: str,
    req_text: str,
    is_asr: bool,
    arch_model: dict,
    judge_llm,
) -> tuple[bool, dict | None, list[dict] | None, str]:
    """Determine if a low-similarity residual implies architectural structure.

    Uses judge LLM with ``judge_residual.md`` prompt when available;
    falls back to structural keyword heuristic.

    Returns:
        (is_architectural, new_entity_dict, new_relationships, rationale)
    """
    if judge_llm is not None:
        try:
            prompt = load_prompt("judge_residual.md", {
                "req_id": req_id,
                "req_description": req_text,
                "is_asr": str(is_asr),
                "has_target_container": False,
            })
            structured_llm = judge_llm.with_structured_output(ResidualArchitecturalCheck)
            result = structured_llm.invoke(prompt)
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
    if config is not None:
        cfg = (
            config.get("configurable") or {}
            if isinstance(config, dict)
            else getattr(config, "configurable", None) or {}
        )
        judge_llm = cfg.get("judge_llm")

    running_model = dict(arch_model)
    running_model["entities"] = list(running_model.get("entities") or [])
    running_model["relationships"] = list(running_model.get("relationships") or [])
    running_model["assumption_flags"] = list(running_model.get("assumption_flags") or [])

    # Local cache for container description embeddings
    container_embeddings: dict[str, list[float]] = {}

    for req in unprocessed_requirements:
        req_id = req.get("id", "")
        is_asr = req.get("is_asr", False)
        req_text = _extract_requirement_text(req)
        if not req_text:
            req_text = requirements.get(req_id, "")
        if not req_text:
            continue

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

        for entity in running_model["entities"]:
            entity_desc = (entity.get("description") or "").strip()
            if not entity_desc:
                continue
            entity_id = entity.get("id", "")

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
                req_id, req_text, is_asr, best_container, best_similarity, judge_llm,
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
                req_id, req_text, is_asr, running_model, judge_llm,
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
    new_relationships = [
        C4Relationship.model_validate(r)
        for r in (new_rels or [])
    ]

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


# ── Main Node ───────────────────────────────────────────────────────────────


def _run_traceability_audit(
    state: RAAState,
    arch_model: dict,
    all_questions: list[dict],
) -> dict:
    """Execute a final traceability audit on all input requirement IDs.

    Verifies that every single input requirement ID is traceable to exactly
    one location: either a processed batch, a mapped container/component,
    or a coverage_gap/residual_coupling question.

    Note:
        Bulk rejection detection (AC #3) uses heuristic matching on question
        IDs and descriptions. It reliably prevents bulk rejection via standard
        question ID formats but cannot guarantee detection for non-standard
        LLM-generated question IDs.

    Raises:
        TraceabilityAuditException: If any requirement is unmapped, missing,
            or mapped to multiple locations, or if bulk acceptance/rejection
            is detected.
    """
    # 1. Collect all input requirement IDs (normalized)
    input_ids = set()
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

    # 2. Collect processed batches
    execution_queue = state.get("execution_queue") or state.get("batches") or []

    # 3. Build a trace registry mapping requirement ID -> list of locations
    trace_map: dict[str, list[dict]] = {rid: [] for rid in input_ids}

    # A. Check processed batches
    for batch in execution_queue:
        batch_id = batch.get("group_id", "")
        batch_reqs = batch.get("asr_ids", []) + batch.get("non_asr_ids", [])
        for req_id in batch_reqs:
            norm_req_id = to_r_id(req_id)
            if norm_req_id in trace_map:
                trace_map[norm_req_id].append({
                    "type": "batch",
                    "id": batch_id,
                    "description": f"Processed in batch '{batch_id}'",
                })

    # B. Check final arch_model (entities and relationships)
    for entity in arch_model.get("entities", []):
        entity_id = entity.get("id", "")
        for req_id in entity.get("requirement_ids", []):
            norm_req_id = to_r_id(req_id)
            if norm_req_id in trace_map:
                if not any(loc["type"] in ("batch", "model") for loc in trace_map[norm_req_id]):
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
                if not any(loc["type"] in ("batch", "model") for loc in trace_map[norm_req_id]):
                    trace_map[norm_req_id].append({
                        "type": "model",
                        "id": rel_id,
                        "description": f"Mapped to C4 relationship '{rel_id}'",
                    })

    # C. Check open questions for coverage gap or residual coupling
    for q in all_questions:
        q_id = q.get("id", "")
        q_type = q.get("question_type", "")
        q_req_id = q.get("context", {}).get("req_id") if isinstance(q.get("context"), dict) else None

        for norm_req_id in input_ids:
            is_match = False
            if q_id in (f"coverage_gap_{norm_req_id}", f"residual_coupling_{norm_req_id}"):
                is_match = True
            elif q_type in ("coverage_gap", "residual_coupling") and (
                q_req_id == norm_req_id or q_id.endswith(f"_{norm_req_id}")
            ):
                is_match = True

            if is_match:
                if not any(loc["type"] == "batch" for loc in trace_map[norm_req_id]):
                    if not any(loc["type"] == "question" and loc["id"] == q_id for loc in trace_map[norm_req_id]):
                        trace_map[norm_req_id].append({
                            "type": "question",
                            "id": q_id,
                            "description": f"Logged as open question '{q_id}' of type '{q_type}'",
                        })

    # 4. Prohibit bulk acceptance/rejection of leftovers
    leftovers = [rid for rid in input_ids if not any(loc["type"] == "batch" for loc in trace_map[rid])]
    for rid in leftovers:
        locs = trace_map[rid]
        question_locs = [loc for loc in locs if loc["type"] == "question"]
        for loc in question_locs:
            q_id = loc["id"]
            q = next((x for x in all_questions if x.get("id") == q_id), None)
            if q:
                other_ids = [other_id for other_id in input_ids if other_id != rid]
                desc = q.get("description", "")
                if any(
                    re.search(rf'(?<![A-Za-z0-9]){re.escape(oid)}(?![A-Za-z0-9])', desc)
                    or q_id.endswith(f"_{oid}")
                    for oid in other_ids
                ):
                    raise TraceabilityAuditException(
                        f"Bulk rejection prohibited: Question '{q_id}' contains multiple requirement IDs, "
                        f"indicating bulk rejection."
                    )

    # 5. Verify 100% accounting and exactly one location per requirement
    manifest = {}
    for rid, locations in trace_map.items():
        if len(locations) == 0:
            raise TraceabilityAuditException(
                f"Traceability audit failed: Requirement '{rid}' is unmapped or missing (silent drop)."
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
) -> None:
    """Write finalized JSON output files to the output directory.

    Writes ``arch_model.json``, ``open_questions.json``, and
    ``diagram_manifest.json``. Output directory comes from config
    or defaults to ``_bmad-output/implementation-artifacts/``.
    """

    cfg: dict = {}
    if config is not None:
        if isinstance(config, dict):
            cfg = config.get("configurable") or {}
        else:
            cfg = getattr(config, "configurable", None) or {}

    output_dir = cfg.get(
        "output_dir",
        os.path.join(os.getcwd(), "_bmad-output", "implementation-artifacts"),
    )
    arch_path = os.path.join(output_dir, "arch_model.json")
    questions_path = os.path.join(output_dir, "open_questions.json")
    manifest_path = os.path.join(output_dir, "diagram_manifest.json")

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(arch_path, "w") as f:
            json.dump(arch_model, f, indent=2, default=str)
        with open(questions_path, "w") as f:
            json.dump(open_questions, f, indent=2, default=str)
        with open(manifest_path, "w") as f:
            json.dump(diagram_manifest, f, indent=2, default=str)
        logger.info("Output files written to %s", output_dir)
    except OSError as e:
        logger.warning("Failed to write output files to %s: %s", output_dir, e)


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

    Args:
        state: Full RAA state.
        config: LangGraph RunnableConfig with optional ``judge_llm`` and
            ``output_dir`` in configurable.

    Returns:
        dict with keys: ``arch_model``, ``open_questions``,
        ``traceability_manifest``, ``diagram_manifest``.
    """
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

    # 1. Initialize embeddings for similarity-based dedup
    cache, model = _init_embeddings(config)

    # 2. Global merge of all batch outputs
    arch_model, merge_questions = _global_merge(
        arch_model, batch_outputs, cache, model,
    )

    # 3. Process residual unprocessed requirements (Story 4.2 decision ladder)
    arch_model, residual_questions = _process_residual_requirements(
        unprocessed_requirements, arch_model, requirements, cache, model, config,
    )

    # Combine all open questions to resolve them together
    all_questions = open_questions + merge_questions + residual_questions

    # 4. Resolve all open questions (including merge and residual questions)
    arch_model = _resolve_all_questions(
        all_questions, human_answers, arch_model, requirements, config,
    )

    # 5. Run the 100% requirements traceability audit (Story 4.3)
    traceability_manifest = _run_traceability_audit(
        state, arch_model, all_questions,
    )

    # 6. Validate the final model against C4 metamodel rules (Story 4.4, AC #1)
    validate_c4_model(arch_model)

    # 7. Set status to "final" (Story 4.4, AC #4)
    arch_model["status"] = "final"

    # 8. Compile diagram manifest (Story 4.4, AC #2)
    diagram_manifest = _compile_diagram_manifest(arch_model)

    # 9. Write finalized JSON files (Story 4.4, AC #3)
    _write_output_files(arch_model, all_questions, diagram_manifest, config)

    return {
        "arch_model": arch_model,
        "open_questions": all_questions,
        "traceability_manifest": traceability_manifest,
        "diagram_manifest": diagram_manifest,
    }

