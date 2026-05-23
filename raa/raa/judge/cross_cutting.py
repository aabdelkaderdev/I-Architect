"""
Cross-cutting concern promotion engine (Story 2.5).

Pure deterministic engine — no LLM calls, no randomness.
"""
from __future__ import annotations

from raa.state.models import C4Entity, C4Relationship
from raa.utils.constants import CROSS_CUTTING_PATTERNS, INFRA_KEYWORDS


def detect_cross_cutting_candidates(
    arch_model: dict,
    patterns: list[str] | None = None,
) -> list[dict]:
    """Scan arch_model for cross-cutting candidates matching known patterns.

    Args:
        arch_model: Dict with ``entities``, ``relationships``, and optionally
            ``cross_cutting_candidates`` (list[str] from ArchFragment).
        patterns: Patterns to match against. Defaults to CROSS_CUTTING_PATTERNS + INFRA_KEYWORDS.

    Returns:
        List of detection records with ``candidate_pattern``, ``related_entity_ids``,
        and ``requirement_ids``.
    """
    if patterns is None:
        patterns = list(CROSS_CUTTING_PATTERNS) + list(INFRA_KEYWORDS)

    cross_cutting_candidates: list[str] = arch_model.get("cross_cutting_candidates") or []
    entities: list[dict] = arch_model.get("entities") or []

    active_patterns = set()
    for candidate in cross_cutting_candidates:
        candidate_lower = candidate.lower().strip()
        for pattern in patterns:
            pattern_lower = pattern.lower()
            if pattern_lower in candidate_lower:
                active_patterns.add(pattern_lower)

    for entity in entities:
        meta = entity.get("metadata") or {}
        entity_cc = meta.get("cross_cutting_candidates") or []
        for cc in entity_cc:
            cc_lower = str(cc).lower().strip()
            for pattern in patterns:
                pattern_lower = pattern.lower()
                if pattern_lower in cc_lower:
                    active_patterns.add(pattern_lower)

    detections: list[dict] = []
    for pattern_lower in sorted(active_patterns):
        related_entity_ids: list[str] = []
        collected_req_ids: set[str] = set()

        for entity in entities:
            eid = entity.get("id", "")
            name = (entity.get("name") or "").lower()
            desc = (entity.get("description") or "").lower()
            tech = (entity.get("technology") or "").lower()
            meta = entity.get("metadata") or {}
            entity_cc = meta.get("cross_cutting_candidates") or []
            entity_cc_lower = [str(c).lower().strip() for c in entity_cc]

            if (
                pattern_lower in name
                or pattern_lower in desc
                or pattern_lower in tech
                or any(pattern_lower in c for c in entity_cc_lower)
            ):
                if eid:
                    related_entity_ids.append(eid)
                req_ids = entity.get("requirement_ids") or []
                collected_req_ids.update(req_ids)

        detections.append({
            "candidate_pattern": pattern_lower,
            "related_entity_ids": related_entity_ids,
            "requirement_ids": sorted(collected_req_ids),
        })

    return detections


def promote_cross_cutting_to_component(
    detection: dict,
    arch_model: dict,
) -> tuple[C4Entity, list[str]]:
    """Create a promoted component entity for a detected cross-cutting concern.

    Args:
        detection: Detection record from ``detect_cross_cutting_candidates``.
        arch_model: Current arch_model dict.

    Returns:
        Tuple of (promoted C4Entity, list of affected source entity IDs).
    """
    pattern = detection["candidate_pattern"]
    component_id = f"cc_{pattern}"
    affected_entity_ids = list(detection.get("related_entity_ids") or [])
    requirement_ids = list(detection.get("requirement_ids") or [])

    # Find parent container — first container whose name/description mentions pattern
    parent_container_id: str | None = None
    for entity in arch_model.get("entities") or []:
        c4_type = entity.get("c4_type", "")
        if c4_type != "container":
            continue
        name = (entity.get("name") or "").lower()
        desc = (entity.get("description") or "").lower()
        if pattern in name or pattern in desc:
            parent_container_id = entity.get("id")
            break

    promoted = C4Entity(
        id=component_id,
        name=f"{pattern.title()} (Cross-Cutting)",
        description=f"Cross-cutting {pattern} concern promoted to structural component.",
        c4_type="component",
        technology="",
        parent_container_id=parent_container_id,
        requirement_ids=requirement_ids,
        saam_score=0.0,
    )

    return promoted, affected_entity_ids


def rewrite_relationships_for_promotion(
    relationships: list[dict],
    affected_entity_ids: list[str],
    promoted_component_id: str,
    pattern: str,
) -> list[dict]:
    """Rewrite relationships that transit through cross-cutting entities to point
    to the promoted component.

    A relationship is rewritten when its source or target is in the affected set
    AND the relationship description or metadata mentions the pattern.

    Args:
        relationships: List of relationship dicts.
        affected_entity_ids: Entity IDs that previously carried the cross-cutting concern.
        promoted_component_id: The new component's ID.
        pattern: The cross-cutting pattern being promoted.

    Returns:
        New list of relationship dicts (never mutates input).
    """
    affected_set = set(affected_entity_ids)
    pattern_lower = pattern.lower()
    rewritten: list[dict] = []

    for rel in relationships:
        rel = dict(rel)
        src = rel.get("source_id", "")
        tgt = rel.get("target_id", "")
        desc = (rel.get("description") or "").lower()
        meta = rel.get("metadata") or {}
        meta_str = str(meta).lower()

        mentions_pattern = pattern_lower in desc or pattern_lower in meta_str

        if mentions_pattern:
            new_src = promoted_component_id if src in affected_set else src
            new_tgt = promoted_component_id if tgt in affected_set else tgt
            if new_src == new_tgt:
                continue
            rel["source_id"] = new_src
            rel["target_id"] = new_tgt

        rewritten.append(rel)

    return rewritten


def promote_all_cross_cutting(
    arch_model: dict,
) -> tuple[dict, list[dict]]:
    """Detect and promote all cross-cutting concerns in the arch model.

    Args:
        arch_model: Dict with ``entities``, ``relationships``, and optionally
            ``cross_cutting_candidates``.

    Returns:
        Tuple of (updated_arch_model, open_questions).
    """
    model = {
        "entities": [dict(e) for e in (arch_model.get("entities") or [])],
        "relationships": [dict(r) for r in (arch_model.get("relationships") or [])],
        "boundary_groups": list(arch_model.get("boundary_groups") or []),
        "cross_cutting_candidates": list(arch_model.get("cross_cutting_candidates") or []),
    }

    detections = detect_cross_cutting_candidates(model)
    open_questions: list[dict] = []

    for detection in detections:
        promoted, affected_ids = promote_cross_cutting_to_component(detection, model)

        if promoted.parent_container_id is None:
            open_questions.append({
                "question_type": "change_risk",
                "description": (
                    f"Cross-cutting '{detection['candidate_pattern']}' promoted to "
                    f"component '{promoted.id}' but no parent container could be "
                    "determined. Manual container assignment required."
                ),
                "source": "cross_cutting_promotion",
                "severity": "medium",
                "promoted_component_id": promoted.id,
            })

        # Add promoted component to entities
        model["entities"].append(promoted.model_dump())

        # Rewrite relationships
        model["relationships"] = rewrite_relationships_for_promotion(
            model["relationships"],
            affected_ids,
            promoted.id,
            detection["candidate_pattern"],
        )

        # Remove requirement IDs from affected entities (move to promoted component)
        promoted_req_ids = set(promoted.requirement_ids)
        for i, entity in enumerate(model["entities"]):
            if entity.get("id") in affected_ids:
                req_ids = entity.get("requirement_ids") or []
                new_req_ids = [r for r in req_ids if r not in promoted_req_ids]
                entity["requirement_ids"] = new_req_ids

    return model, open_questions
