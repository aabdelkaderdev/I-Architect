"""
Human review gate node (Story 3.1).

Classifies open questions and builds a detailed human review payload
with categorized questions, conflicting elements, model statistics,
and pre-computed suggested resolutions for judge-resolvable questions.
"""
from __future__ import annotations

from typing import Any
from raa.state.models import OpenQuestion
from raa.state.schemas import RAAState

# ── Classification mapping ──────────────────────────────────────────────────

_HUMAN_PREFERRED_TYPES = frozenset({"change_risk", "high_coupling", "coverage_gap"})
_JUDGE_RESOLVABLE_TYPES = frozenset({"contention", "tie", "hierarchy_conflict", "scope_conflict"})

# ── Suggested resolutions for judge-resolvable question types ───────────────

_SUGGESTED_RESOLUTIONS: dict[str, str] = {
    "hierarchy_conflict": "Use parent hierarchy from canonical entity.",
    "scope_conflict": "Apply fallback constraints to adjust relationship scope.",
    "tie": "Resolve tie by selecting the proposal from primary strategy (RAA-A SAAM-First).",
    "contention": "Consolidate entities using the primary strategy's structure as the ground truth.",
}


def _make_json_serializable(val: Any) -> Any:
    """Recursively coerce non-serializable objects into basic JSON-serializable types."""
    if isinstance(val, dict):
        return {str(k): _make_json_serializable(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple, set, frozenset)):
        return [_make_json_serializable(item) for item in val]
    elif isinstance(val, (str, int, float, bool)) or val is None:
        return val
    else:
        # Default fallback: cast to string
        return str(val)


def _classify_question_type(question_type: str) -> str:
    """Map a raw question_type to its resolution_owner category.

    Returns:
        ``"human_preferred"`` or ``"judge_resolvable"``.
    """
    if question_type in _HUMAN_PREFERRED_TYPES:
        return "human_preferred"
    if question_type in _JUDGE_RESOLVABLE_TYPES:
        return "judge_resolvable"
    # Default: unknown types go to human review
    return "human_preferred"


def _generate_deterministic_id(index: int, question: dict) -> str:
    """Generate a deterministic question ID from its index and content."""
    q_type = question.get("question_type") or question.get("type") or "unknown"
    if not isinstance(q_type, str):
        q_type = str(q_type)
    return f"q_{index}_{q_type}"


def _normalize_question(raw: dict, index: int) -> OpenQuestion:
    """Normalize a raw question dict into an OpenQuestion model.

    Handles legacy keys (``type`` → ``question_type``).
    """
    question_type = raw.get("question_type") or raw.get("type") or "unknown"
    if not isinstance(question_type, str):
        question_type = str(question_type)
    resolution_owner = _classify_question_type(question_type)

    suggested: str | None = None
    if resolution_owner == "judge_resolvable":
        suggested = _SUGGESTED_RESOLUTIONS.get(question_type)

    fallback_desc = f"Open question of type {question_type}"
    description = raw.get("description") or raw.get("summary") or fallback_desc

    # Ensure nested values in context and metadata are JSON-serializable primitives
    raw_context = {
        k: v
        for k, v in raw.items()
        if k not in ("question_type", "type", "description", "summary")
    }
    clean_context = _make_json_serializable(raw_context)
    clean_metadata = _make_json_serializable(raw.get("metadata", {}))

    return OpenQuestion(
        id=_generate_deterministic_id(index, raw),
        question_type=question_type,
        description=description,
        context=clean_context,
        resolution_owner=resolution_owner,
        resolution=suggested,
        assumption_flag=False,
        metadata=clean_metadata,
    )


def _gather_conflicting_elements(
    open_questions: list[dict],
    arch_model: dict,
) -> list[dict]:
    """Collect entity details from arch_model for entities referenced in open questions.

    Scans entity IDs from keys: ``entity_a_id``, ``entity_b_id``, ``entity_id``,
    and ``promoted_component_id`` at both the root level and within nested ``context``.
    """
    entity_map: dict[str, dict] = {}
    for entity in arch_model.get("entities") or []:
        if isinstance(entity, dict):
            eid = entity.get("id", "")
            if eid:
                entity_map[eid] = entity

    referenced_ids: set[str] = set()
    id_keys = ("entity_a_id", "entity_b_id", "entity_id", "promoted_component_id")

    for q in open_questions:
        if not isinstance(q, dict):
            continue
        # Scan root level keys
        for key in id_keys:
            val = q.get(key)
            if val and isinstance(val, str):
                referenced_ids.add(val)
        # Scan nested context dictionary if present
        context = q.get("context")
        if isinstance(context, dict):
            for key in id_keys:
                val = context.get(key)
                if val and isinstance(val, str):
                    referenced_ids.add(val)

    conflicting: list[dict] = []
    for eid in sorted(referenced_ids):
        if eid in entity_map:
            conflicting.append(entity_map[eid])

    return conflicting


def _calculate_model_statistics(arch_model: dict) -> dict:
    """Count entities by C4 type and count relationships."""
    entities: list[dict] = arch_model.get("entities") or []
    relationships: list[dict] = arch_model.get("relationships") or []

    type_counts: dict[str, int] = {}
    for e in entities:
        if isinstance(e, dict):
            c4_type = e.get("c4_type", "unknown")
            type_counts[c4_type] = type_counts.get(c4_type, 0) + 1

    return {
        "system_count": type_counts.get("system", 0),
        "external_system_count": type_counts.get("external_system", 0),
        "container_count": type_counts.get("container", 0),
        "component_count": type_counts.get("component", 0),
        "relationship_count": len(relationships),
        "total_entities": len(entities),
    }


def prepare_human_review_payload(state: RAAState) -> dict:
    """Classify open questions and build a human review payload.

    Reads ``open_questions`` from state, normalizes and classifies each question,
    auto-generates suggested resolutions for judge-resolvable types, gathers
    conflicting C4 elements from ``arch_model``, and computes model statistics.

    Args:
        state: Full RAA state with ``open_questions`` and ``arch_model`` channels.

    Returns:
        dict with key ``human_review_payload`` containing categorized questions,
        conflicting elements, model statistics, and pre-computed resolutions.
    """
    raw_questions: list[dict] = list(state.get("open_questions") or [])
    arch_model: dict = state.get("arch_model") or {}

    classified: list[OpenQuestion] = []
    for i, raw in enumerate(raw_questions):
        if not isinstance(raw, dict):
            continue
        classified.append(_normalize_question(raw, i))

    # Build pre-computed resolutions map
    pre_computed_resolutions: dict[str, str] = {}
    for q in classified:
        if q.resolution_owner == "judge_resolvable" and q.resolution is not None:
            pre_computed_resolutions[q.id] = q.resolution

    conflicting_elements = _gather_conflicting_elements(raw_questions, arch_model)
    model_statistics = _calculate_model_statistics(arch_model)

    payload = {
        "open_questions": [q.model_dump() for q in classified],
        "conflicting_elements": conflicting_elements,
        "model_statistics": model_statistics,
        "pre_computed_resolutions": pre_computed_resolutions,
    }

    return {"human_review_payload": payload}
