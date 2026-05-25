"""
Per-entity SAAM score calibration engine (Story 2.5).

Pure deterministic engine — no LLM calls, no randomness.
"""
from __future__ import annotations

from raa.utils.constants import (
    SAAM_BASE_SCORE,
    SAAM_BOUNDARY_GROUP_PENALTY,
    SAAM_DEDUP_PENALTY,
    SAAM_PERFECT_SCORE,
)


def _entity_in_boundary_group(entity_id: str, boundary_groups: list[dict]) -> bool:
    """Check whether an entity is a member of any boundary group."""
    for bg in boundary_groups:
        entity_ids = bg.get("entity_ids") or []
        if entity_id in entity_ids:
            return True
    return False


def _get_transitive_sources(entity_id: str, merge_log: list[dict], visited: set[str] | None = None) -> set[str]:
    """Helper to recursively compute all source IDs merged into entity_id."""
    if visited is None:
        visited = set()
    if entity_id in visited:
        return set()
    visited.add(entity_id)

    sources = {entity_id}
    for entry in merge_log:
        merged_id = entry.get("merged_entity_id", "")
        if merged_id == entity_id:
            for s_id in entry.get("source_entity_ids") or []:
                if s_id != entity_id:
                    sources.update(_get_transitive_sources(s_id, merge_log, visited))
    return sources


def _count_merge_events(entity_id: str, merge_log: list[dict]) -> int:
    """Count how many merge events this entity participated in."""
    transitive_sources = _get_transitive_sources(entity_id, merge_log)
    count = 0
    for entry in merge_log:
        merged_id = entry.get("merged_entity_id", "")
        source_ids: list[str] = entry.get("source_entity_ids") or []
        # If the merge event involves any of the transitive source IDs of this entity
        if merged_id in transitive_sources or any(s_id in transitive_sources for s_id in source_ids):
            count += 1
    return count


def _check_perfect_score(
    entity: dict,
    entities: list[dict],
    boundary_groups: list[dict],
    saam_scenarios: list[dict],
) -> bool:
    """Check if an entity qualifies for the perfect SAAM score (1.0).

    Conditions:
    1. c4_type == "component"
    2. No shared requirement_ids with any entity in the same boundary group
    3. All SAAMScenarios for the entity's requirement_ids have satisfaction == "satisfied"
    """
    if entity.get("c4_type") != "component":
        return False

    entity_req_ids = set(entity.get("requirement_ids") or [])
    if not entity_req_ids:
        return False

    # Check functional overlap: no shared requirement_ids with same boundary group entities
    overlapping_entity_ids = set()
    for bg in boundary_groups:
        bg_entity_ids = bg.get("entity_ids") or []
        if entity.get("id") in bg_entity_ids:
            overlapping_entity_ids.update(bg_entity_ids)

    entity_bg_id = (entity.get("metadata") or {}).get("boundary_group_id")
    if entity_bg_id:
        for other in entities:
            if other.get("id") == entity.get("id"):
                continue
            other_bg_id = (other.get("metadata") or {}).get("boundary_group_id")
            if other_bg_id == entity_bg_id:
                overlapping_entity_ids.add(other.get("id"))

    if overlapping_entity_ids:
        for other in entities:
            other_id = other.get("id")
            if other_id == entity.get("id") or other_id not in overlapping_entity_ids:
                continue
            other_req_ids = set(other.get("requirement_ids") or [])
            if entity_req_ids & other_req_ids:
                return False

    # Check all scenarios passing
    entity_req_list = list(entity_req_ids)
    relevant_scenarios = [
        s for s in saam_scenarios
        if set(s.get("requirement_ids") or []) & entity_req_ids
    ]

    if not relevant_scenarios:
        return False

    for scenario in relevant_scenarios:
        if scenario.get("satisfaction") != "satisfied":
            return False

    return True


def calibrate_entity_saam_scores(
    arch_model: dict,
    saam_scenarios: list[dict] | None = None,
    boundary_groups: list[dict] | None = None,
    merge_log: list[dict] | None = None,
) -> dict:
    """Assign a ``saam_score`` to every entity in the arch model.

    Args:
        arch_model: Dict with ``entities`` key. May also carry ``boundary_groups``.
        saam_scenarios: SAAM scenarios from the winning fragment (list of dicts).
        boundary_groups: Override boundary groups. Defaults to model's ``boundary_groups``.
        merge_log: Merge log from deduplication. Each entry has
            ``merged_entity_id``, ``source_entity_ids``, ``merge_type``.

    Returns:
        Updated arch_model dict with ``saam_score`` set on every entity.
    """
    if saam_scenarios is None:
        saam_scenarios = []
    if boundary_groups is None:
        boundary_groups = arch_model.get("boundary_groups") or []
    if merge_log is None:
        merge_log = []

    entities: list[dict] = [dict(e) for e in (arch_model.get("entities") or [])]

    for entity in entities:
        eid = entity.get("id", "")

        if _check_perfect_score(entity, entities, boundary_groups, saam_scenarios):
            entity["saam_score"] = SAAM_PERFECT_SCORE
            continue

        score = SAAM_BASE_SCORE

        # Dedup penalty
        merge_count = _count_merge_events(eid, merge_log)
        score -= SAAM_DEDUP_PENALTY * merge_count

        # Boundary group penalty
        if _entity_in_boundary_group(eid, boundary_groups):
            score -= SAAM_BOUNDARY_GROUP_PENALTY

        # Clamp to [0.0, 1.0]
        entity["saam_score"] = max(0.0, min(1.0, round(score, 4)))

    result = dict(arch_model)
    result["entities"] = entities
    return result
