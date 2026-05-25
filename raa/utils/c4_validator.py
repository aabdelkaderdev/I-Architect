"""
Shared C4 metamodel hierarchy enforcement (FR-8).

Validates structural C4 rules across a flat ArchFragment against the running
model: containers must have a valid system parent, components must have a valid
container parent, and relationships must have valid endpoints with correct scope.
"""
from __future__ import annotations

from pydantic import ValidationError

from raa.state.models import ArchFragment, C4Entity, C4Relationship


class C4SchemaValidationException(Exception):
    """Raised when the final C4 model fails metamodel validation checks."""
    pass


def enforce_fragment_hierarchy(
    fragment: ArchFragment,
    running_model: dict,
    *,
    batch_id: str,
    strategy: str,
) -> tuple[ArchFragment, list[dict]]:
    """Validate and clean an ArchFragment against C4 hierarchy rules.

    Returns a cleaned fragment and a list of open-question dicts for
    recoverable violations.
    """
    open_questions: list[dict] = []

    # ── Validate entities (hierarchical passes) ────────────────────────────
    valid_entities: list[C4Entity] = []

    # Pass 1: Collect non-container, non-component entities
    for entity in fragment.entities:
        if entity.c4_type not in ("container", "component"):
            valid_entities.append(entity)

    # Collect valid system IDs from running model and valid fragment entities
    valid_system_ids = _collect_ids(_model_systems(running_model))
    for entity in valid_entities:
        if entity.c4_type == "system":
            valid_system_ids.add(entity.id)

    # Pass 2: Validate containers
    valid_container_entities: list[C4Entity] = []
    for entity in fragment.entities:
        if entity.c4_type == "container":
            if entity.parent_system_id and entity.parent_system_id in valid_system_ids:
                valid_container_entities.append(entity)
            elif entity.parent_system_id and entity.parent_system_id not in valid_system_ids:
                open_questions.append({
                    "type": "hierarchy_conflict",
                    "reason": "orphan_container",
                    "batch_id": batch_id,
                    "strategy": strategy,
                    "entity_id": entity.id,
                    "requirement_ids": entity.requirement_ids,
                    "suggested_resolution": (
                        f"Container '{entity.id}' references missing system "
                        f"'{entity.parent_system_id}'. Add the system to the running model "
                        f"or correct the parent_system_id."
                    ),
                })
            else:
                # Container with no parent_system_id — keep but flag
                valid_container_entities.append(entity)
                open_questions.append({
                    "type": "coverage_gap",
                    "reason": "container_missing_parent_system",
                    "batch_id": batch_id,
                    "strategy": strategy,
                    "entity_id": entity.id,
                    "requirement_ids": entity.requirement_ids,
                    "suggested_resolution": (
                        f"Container '{entity.id}' has no parent_system_id. "
                        f"Assign a parent system."
                    ),
                })
    valid_entities.extend(valid_container_entities)

    # Collect valid container IDs from running model and validated fragment containers
    valid_container_ids = _collect_ids(_model_containers(running_model))
    for entity in valid_container_entities:
        valid_container_ids.add(entity.id)

    # Pass 3: Validate components
    for entity in fragment.entities:
        if entity.c4_type == "component":
            if entity.parent_container_id and entity.parent_container_id in valid_container_ids:
                valid_entities.append(entity)
            elif entity.parent_container_id and entity.parent_container_id not in valid_container_ids:
                open_questions.append({
                    "type": "hierarchy_conflict",
                    "reason": "orphan_component",
                    "batch_id": batch_id,
                    "strategy": strategy,
                    "entity_id": entity.id,
                    "requirement_ids": entity.requirement_ids,
                    "suggested_resolution": (
                        f"Component '{entity.id}' references missing container "
                        f"'{entity.parent_container_id}'. Add the container or correct "
                        f"the parent_container_id."
                    ),
                })
            else:
                valid_entities.append(entity)
                open_questions.append({
                    "type": "coverage_gap",
                    "reason": "component_missing_parent_container",
                    "batch_id": batch_id,
                    "strategy": strategy,
                    "entity_id": entity.id,
                    "requirement_ids": entity.requirement_ids,
                    "suggested_resolution": (
                        f"Component '{entity.id}' has no parent_container_id. "
                        f"Assign a parent container."
                    ),
                })

    # Allow relationship endpoints from either valid fragment entities OR the running model
    valid_entity_ids = {e.id for e in valid_entities}
    valid_entity_ids.update(_model_entities_all_ids(running_model))

    # ── Validate relationships ─────────────────────────────────────────────
    valid_relationships: list[C4Relationship] = []
    for rel in fragment.relationships:
        if rel.source_id not in valid_entity_ids or rel.target_id not in valid_entity_ids:
            open_questions.append({
                "type": "hierarchy_conflict",
                "reason": "unresolved_relationship_endpoint",
                "batch_id": batch_id,
                "strategy": strategy,
                "relationship_id": rel.id,
                "requirement_ids": [],
                "suggested_resolution": (
                    f"Relationship '{rel.id}' ({rel.source_id} -> {rel.target_id}) "
                    f"references an entity not present in the valid fragment or running model. "
                    f"Ensure both endpoints exist."
                ),
            })
        else:
            valid_relationships.append(rel)

    # ── Assign diagram_scope ───────────────────────────────────────────────
    entity_type_map = {e.id: e.c4_type for e in valid_entities}
    entity_type_map.update(_model_entities_all_types(running_model))
    for rel in valid_relationships:
        rel.diagram_scope = _compute_scope(rel, entity_type_map)

    cleaned = ArchFragment(
        entities=valid_entities,
        relationships=valid_relationships,
        cross_cutting_candidates=fragment.cross_cutting_candidates,
        assumption_flags=fragment.assumption_flags,
        metadata=fragment.metadata,
    )
    return cleaned, open_questions


# ── Private helpers ─────────────────────────────────────────────────────────


_SCOPE_TYPE_RANK = {"component": 3, "container": 2, "system": 1, "external_system": 0, "person": 0}


def _compute_scope(rel: C4Relationship, entity_type_map: dict[str, str]) -> str:
    """Assign diagram_scope from the deepest endpoint level."""
    src_type = entity_type_map.get(rel.source_id, "")
    tgt_type = entity_type_map.get(rel.target_id, "")
    src_rank = _SCOPE_TYPE_RANK.get(src_type, 0)
    tgt_rank = _SCOPE_TYPE_RANK.get(tgt_type, 0)
    max_rank = max(src_rank, tgt_rank)
    if max_rank >= 3:
        return "component"
    elif max_rank >= 2:
        return "container"
    return "context"


def _collect_ids(entities: list[C4Entity]) -> set[str]:
    return {e.id for e in entities if e.id}


def _model_entities_all_ids(running_model: dict) -> set[str]:
    """Collect all entity IDs from the running model."""
    ids = set()
    for key in ("systems", "containers", "components", "persons", "external_systems", "entities"):
        items = running_model.get(key) or []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and "id" in item:
                    ids.add(item["id"])
                    if key == "systems":
                        ctrs = item.get("containers") or []
                        if isinstance(ctrs, list):
                            for ctr in ctrs:
                                if isinstance(ctr, dict) and "id" in ctr:
                                    ids.add(ctr["id"])
                                    cmps = ctr.get("components") or []
                                    if isinstance(cmps, list):
                                        for cmp in cmps:
                                            if isinstance(cmp, dict) and "id" in cmp:
                                                ids.add(cmp["id"])
                    elif key == "containers":
                        cmps = item.get("components") or []
                        if isinstance(cmps, list):
                            for cmp in cmps:
                                if isinstance(cmp, dict) and "id" in cmp:
                                    ids.add(cmp["id"])
    return ids


def _model_entities_all_types(running_model: dict) -> dict[str, str]:
    """Collect {entity_id: c4_type} from the running model."""
    types = {}
    for key in ("systems", "containers", "components", "persons", "external_systems", "entities"):
        items = running_model.get(key) or []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and "id" in item:
                    c4_type = item.get("c4_type")
                    if not c4_type:
                        if key == "systems":
                            c4_type = "system"
                        elif key == "containers":
                            c4_type = "container"
                        elif key == "components":
                            c4_type = "component"
                        elif key == "persons":
                            c4_type = "person"
                        elif key == "external_systems":
                            c4_type = "external_system"
                        else:
                            c4_type = "container"
                    types[item["id"]] = c4_type

                    if key == "systems":
                        ctrs = item.get("containers") or []
                        if isinstance(ctrs, list):
                            for ctr in ctrs:
                                if isinstance(ctr, dict) and "id" in ctr:
                                    types[ctr["id"]] = ctr.get("c4_type") or "container"
                                    cmps = ctr.get("components") or []
                                    if isinstance(cmps, list):
                                        for cmp in cmps:
                                            if isinstance(cmp, dict) and "id" in cmp:
                                                types[cmp["id"]] = cmp.get("c4_type") or "component"
                    elif key == "containers":
                        cmps = item.get("components") or []
                        if isinstance(cmps, list):
                            for cmp in cmps:
                                if isinstance(cmp, dict) and "id" in cmp:
                                    types[cmp["id"]] = cmp.get("c4_type") or "component"
    return types


def _model_systems(running_model: dict) -> list[C4Entity]:
    """Extract system-level entities from common running-model shapes."""
    entities: list[C4Entity] = []
    for key in ("systems",):
        items = running_model.get(key) or []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    entities.append(C4Entity(
                        id=item.get("id", ""),
                        name=item.get("name", ""),
                        c4_type="system",
                        metadata=item.get("metadata", {}),
                    ))
    # Also check top-level entities list
    top_entities = running_model.get("entities") or []
    if isinstance(top_entities, list):
        for item in top_entities:
            if isinstance(item, dict) and item.get("c4_type") == "system":
                entities.append(C4Entity(
                    id=item.get("id", ""),
                    name=item.get("name", ""),
                    c4_type="system",
                    metadata=item.get("metadata", {}),
                ))
    return entities


def _model_containers(running_model: dict) -> list[C4Entity]:
    """Extract container-level entities from common running-model shapes."""
    entities: list[C4Entity] = []
    for system in running_model.get("systems") or []:
        if isinstance(system, dict):
            containers = system.get("containers") or []
            if isinstance(containers, list):
                for c in containers:
                    if isinstance(c, dict):
                        entities.append(C4Entity(
                            id=c.get("id", ""),
                            name=c.get("name", ""),
                            c4_type="container",
                            metadata=c.get("metadata", {}),
                        ))
    # Also check top-level containers list
    for key in ("containers",):
        items = running_model.get(key) or []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    entities.append(C4Entity(
                        id=item.get("id", ""),
                        name=item.get("name", ""),
                        c4_type="container",
                        metadata=item.get("metadata", {}),
                    ))
    # Also from entities list
    top_entities = running_model.get("entities") or []
    if isinstance(top_entities, list):
        for item in top_entities:
            if isinstance(item, dict) and item.get("c4_type") == "container":
                entities.append(C4Entity(
                    id=item.get("id", ""),
                    name=item.get("name", ""),
                    c4_type="container",
                    metadata=item.get("metadata", {}),
                ))
    return entities


# ── Full Model Validation (Story 4.4) ────────────────────────────────────────

_SCOPE_RANK: dict[str, int] = {
    "component": 3,
    "container": 2,
    "system": 1,
    "external_system": 0,
    "person": 0,
}


def _scope_from_rank(rank: int) -> str:
    if rank >= 3:
        return "component"
    elif rank >= 2:
        return "container"
    return "context"


def validate_c4_model(arch_model: dict) -> None:
    """Validate the final C4 architecture model against metamodel rules.

    Checks performed:
    1. All entities parse as valid ``C4Entity`` models.
    2. All relationships parse as valid ``C4Relationship`` models.
    3. Every component has a parent container that exists in the model.
    4. Every container has a parent system that exists in the model.
    5. All relationships reference valid entity IDs.
    6. Relationship scope matches the deepest endpoint type.

    Raises:
        C4SchemaValidationException: If any validation check fails.
    """
    entities_raw = arch_model.get("entities") or []
    relationships_raw = arch_model.get("relationships") or []

    # 1. Validate entities
    entities: list[C4Entity] = []
    entity_ids: set[str] = set()
    entity_types: dict[str, str] = {}

    for i, e in enumerate(entities_raw or []):
        if not isinstance(e, dict):
            raise C4SchemaValidationException(
                f"Entity at index {i} is not a dict: {type(e).__name__}"
            )
        try:
            entity = C4Entity.model_validate(e)
        except ValidationError as exc:
            raise C4SchemaValidationException(
                f"Entity '{e.get('id', f'index {i}')}' failed C4Entity validation: {exc}"
            ) from exc
        
        # Enforce valid c4_type
        if entity.c4_type not in ("system", "container", "component", "person", "external_system"):
            raise C4SchemaValidationException(
                f"Entity '{entity.id}' has invalid c4_type '{entity.c4_type}'."
            )
            
        entities.append(entity)
        entity_ids.add(entity.id)
        entity_types[entity.id] = entity.c4_type

    # 2. Validate relationships
    for i, r in enumerate(relationships_raw or []):
        if not isinstance(r, dict):
            raise C4SchemaValidationException(
                f"Relationship at index {i} is not a dict: {type(r).__name__}"
            )
        try:
            C4Relationship.model_validate(r)
        except ValidationError as exc:
            raise C4SchemaValidationException(
                f"Relationship '{r.get('id', f'index {i}')}' failed C4Relationship validation: {exc}"
            ) from exc

    # 3. Component parent container check
    for entity in entities:
        if entity.c4_type == "component":
            if not entity.parent_container_id:
                raise C4SchemaValidationException(
                    f"Component '{entity.id}' has no parent_container_id."
                )
            if entity.parent_container_id not in entity_ids:
                raise C4SchemaValidationException(
                    f"Component '{entity.id}' references missing parent container "
                    f"'{entity.parent_container_id}'."
                )
            if entity_types[entity.parent_container_id] != "container":
                raise C4SchemaValidationException(
                    f"Component '{entity.id}' references parent '{entity.parent_container_id}' "
                    f"which is a '{entity_types[entity.parent_container_id]}', not a 'container'."
                )

    # 4. Container parent system check
    for entity in entities:
        if entity.c4_type == "container":
            if not entity.parent_system_id:
                raise C4SchemaValidationException(
                    f"Container '{entity.id}' has no parent_system_id."
                )
            if entity.parent_system_id not in entity_ids:
                raise C4SchemaValidationException(
                    f"Container '{entity.id}' references missing parent system "
                    f"'{entity.parent_system_id}'."
                )
            if entity_types[entity.parent_system_id] != "system":
                raise C4SchemaValidationException(
                    f"Container '{entity.id}' references parent '{entity.parent_system_id}' "
                    f"which is a '{entity_types[entity.parent_system_id]}', not a 'system'."
                )

    # 5. Relationship endpoint validity
    for i, r in enumerate(relationships_raw or []):
        rel_id = r.get("id", f"index {i}")
        src = r.get("source_id", "")
        tgt = r.get("target_id", "")
        if src and src not in entity_ids:
            raise C4SchemaValidationException(
                f"Relationship '{rel_id}' references unknown source entity '{src}'."
            )
        if tgt and tgt not in entity_ids:
            raise C4SchemaValidationException(
                f"Relationship '{rel_id}' references unknown target entity '{tgt}'."
            )

        # 6. Scope matches endpoint depth
        declared_scope = r.get("diagram_scope", "")
        if declared_scope and src and tgt:
            src_type = entity_types.get(src, "")
            tgt_type = entity_types.get(tgt, "")
            src_rank = _SCOPE_RANK.get(src_type, 0)
            tgt_rank = _SCOPE_RANK.get(tgt_type, 0)
            expected_scope = _scope_from_rank(max(src_rank, tgt_rank))
            if declared_scope != expected_scope:
                raise C4SchemaValidationException(
                    f"Relationship '{rel_id}' has scope '{declared_scope}' but "
                    f"endpoints ({src} [{src_type}], {tgt} [{tgt_type}]) "
                    f"require scope '{expected_scope}'."
                )
