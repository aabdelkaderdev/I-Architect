"""
Conservative entity deduplication and C4 boundary grouping (Story 2.4).

Pure deterministic engine — no LLM calls, no LangGraph dependency.
"""
from __future__ import annotations

import re
from typing import Any

from fastembed import TextEmbedding
from pydantic import ValidationError

from raa.state.models import C4Entity, C4Relationship
from raa.utils.constants import (
    DEDUP_GROUP_THRESHOLD_HIGH,
    DEDUP_GROUP_THRESHOLD_LOW,
    DEDUP_MERGE_THRESHOLD,
)
from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity

# Patterns for ID normalization
_RE_CAMEL_INSERT = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_RE_ACRONYM_SPLIT = re.compile(r"(?<=[A-Z])(?=[A-Z][a-z])")
_RE_SEPARATORS = re.compile(r"[-.\s]+")
_RE_MULTI_UNDERSCORE = re.compile(r"_+")


def normalize_entity_id(entity_id: str) -> str:
    """Convert any entity ID format to lowercase snake_case.

    >>> normalize_entity_id("User_Service")
    'user_service'
    >>> normalize_entity_id("userService")
    'user_service'
    >>> normalize_entity_id("user-service")
    'user_service'
    >>> normalize_entity_id("DTOParser")
    'dto_parser'
    """
    s = entity_id.strip()
    s = _RE_SEPARATORS.sub("_", s)
    s = _RE_CAMEL_INSERT.sub("_", s)
    s = _RE_ACRONYM_SPLIT.sub("_", s)
    s = _RE_MULTI_UNDERSCORE.sub("_", s.lower())
    s = re.sub(r"[^a-z0-9_]", "_", s)
    s = _RE_MULTI_UNDERSCORE.sub("_", s)
    return s.strip("_")


def _compute_entity_similarity(
    entity_a: C4Entity,
    entity_b: C4Entity,
    cache: EmbeddingCache,
    model: TextEmbedding,
) -> float:
    """Compute cosine similarity between two entity descriptions.

    Returns 0.0 if either description is empty/whitespace-only.
    """
    desc_a = (entity_a.description or "").strip()
    desc_b = (entity_b.description or "").strip()

    if not desc_a or not desc_b:
        return 0.0

    hash_a = cache.text_hash(desc_a)
    hash_b = cache.text_hash(desc_b)

    vec_a = cache.get_cached_vector(entity_a.id, hash_a)
    if vec_a is None:
        embeddings = list(model.embed([desc_a]))
        vec_a = embeddings[0].tolist()
        cache.store_vector(entity_a.id, hash_a, vec_a)

    vec_b = cache.get_cached_vector(entity_b.id, hash_b)
    if vec_b is None:
        embeddings = list(model.embed([desc_b]))
        vec_b = embeddings[0].tolist()
        cache.store_vector(entity_b.id, hash_b, vec_b)

    return cosine_similarity(vec_a, vec_b)


def _do_ids_overlap(entity_a: C4Entity, entity_b: C4Entity) -> bool:
    """Check whether two entities share at least one requirement ID."""
    ids_a = set(entity_a.requirement_ids or [])
    ids_b = set(entity_b.requirement_ids or [])
    return bool(ids_a & ids_b)


def _union_technology(tech_a: str, tech_b: str) -> str:
    """Union two technology tag strings with proper formatting.

    Tags are split by comma/semicolon, stripped, deduplicated case-insensitively,
    sorted, and joined with ", ".
    """
    seen: dict[str, str] = {}
    for tech in (tech_a, tech_b):
        if tech:
            for tag in re.split(r"[,;]+", tech):
                stripped = tag.strip()
                if stripped:
                    key = stripped.lower()
                    if key not in seen:
                        seen[key] = stripped
                    elif any(c.isupper() for c in stripped) and not any(c.isupper() for c in seen[key]):
                        seen[key] = stripped
    return ", ".join(sorted(seen.values(), key=lambda s: s.lower()))


def _merge_entities(entity_a: C4Entity, entity_b: C4Entity) -> C4Entity:
    """Merge two entities into one.

    Retains the longer description, unions technology tags and requirement IDs.
    The canonical entity ID is the one with more requirement_ids (tie-break: entity_a).
    """
    canonical = (
        entity_a
        if len(entity_a.requirement_ids or []) >= len(entity_b.requirement_ids or [])
        else entity_b
    )

    description = (
        entity_a.description
        if len(entity_a.description or "") >= len(entity_b.description or "")
        else entity_b.description
    )

    technology = _union_technology(entity_a.technology or "", entity_b.technology or "")

    requirement_ids = sorted(
        set(entity_a.requirement_ids or []) | set(entity_b.requirement_ids or [])
    )

    return C4Entity(
        id=canonical.id,
        name=canonical.name,
        description=description,
        c4_type=canonical.c4_type,
        technology=technology,
        parent_system_id=canonical.parent_system_id,
        parent_container_id=canonical.parent_container_id,
        requirement_ids=requirement_ids,
        metadata={**entity_a.metadata, **entity_b.metadata},
    )


def _rewrite_relationship_ids(
    relationships: list[C4Relationship],
    old_id: str,
    new_id: str,
) -> list[C4Relationship]:
    """Rewrite source_id and target_id from old_id to new_id.

    Returns new list — never mutates inputs.
    """
    rewritten: list[C4Relationship] = []
    for rel in relationships:
        new_source = new_id if rel.source_id == old_id else rel.source_id
        new_target = new_id if rel.target_id == old_id else rel.target_id
        meta = dict(rel.metadata) if rel.metadata else {}
        rewritten.append(
            C4Relationship(
                id=rel.id,
                source_id=new_source,
                target_id=new_target,
                description=rel.description,
                relationship_type=rel.relationship_type,
                diagram_scope=rel.diagram_scope,
                requirement_ids=list(rel.requirement_ids or []),
                metadata=meta,
            )
        )
    return rewritten


def _create_boundary_group(
    entity_a_id: str,
    entity_b_id: str,
    similarity: float,
) -> dict:
    """Create a boundary group entry for two moderately-similar entities."""
    return {
        "group_id": f"bg_{entity_a_id}_{entity_b_id}",
        "entity_ids": sorted([entity_a_id, entity_b_id]),
        "similarity": round(similarity, 4),
        "rationale": (
            f"Entities have moderate semantic similarity ({similarity:.2f}) "
            "suggesting shared deployment context but distinct C4 responsibilities."
        ),
    }


def _check_hierarchy_mismatch(entity_a: C4Entity, entity_b: C4Entity) -> dict | None:
    """Check if two entities have different parent system or container IDs."""
    mismatches = []
    if entity_a.parent_system_id != entity_b.parent_system_id:
        mismatches.append(f"parent_system_id ('{entity_a.parent_system_id}' vs '{entity_b.parent_system_id}')")
    if entity_a.parent_container_id != entity_b.parent_container_id:
        mismatches.append(f"parent_container_id ('{entity_a.parent_container_id}' vs '{entity_b.parent_container_id}')")

    if mismatches:
        canonical_id = (
            entity_a.id
            if len(entity_a.requirement_ids or []) >= len(entity_b.requirement_ids or [])
            else entity_b.id
        )
        return {
            "question_type": "change_risk",
            "entity_a_id": entity_a.id,
            "entity_b_id": entity_b.id,
            "description": (
                f"Merged entities '{entity_a.name}' and '{entity_b.name}' have mismatching C4 parent hierarchy: "
                f"{', '.join(mismatches)}. Canonical entity '{canonical_id}' parent hierarchy will be used."
            ),
            "source": "deduplication",
            "severity": "medium",
        }
    return None


def _to_entity(obj: Any) -> C4Entity:
    """Coerce a dict or C4Entity into a C4Entity using Pydantic validation."""
    if isinstance(obj, C4Entity):
        return obj
    if isinstance(obj, dict):
        try:
            return C4Entity.model_validate(obj)
        except ValidationError as e:
            raise ValueError(f"Failed to validate C4Entity: {e}") from e
    raise TypeError(f"Cannot coerce {type(obj)} to C4Entity")


def _to_relationship(obj: Any) -> C4Relationship:
    """Coerce a dict or C4Relationship into a C4Relationship using Pydantic validation."""
    if isinstance(obj, C4Relationship):
        return obj
    if isinstance(obj, dict):
        try:
            return C4Relationship.model_validate(obj)
        except ValidationError as e:
            raise ValueError(f"Failed to validate C4Relationship: {e}") from e
    raise TypeError(f"Cannot coerce {type(obj)} to C4Relationship")

def _rewrite_entity_parent_ids(
    entities: list[C4Entity], id_mapping: dict[str, str]
) -> list[C4Entity]:
    if not id_mapping:
        return entities
    rewritten = []
    for e in entities:
        new_parent_container_id = id_mapping.get(
            e.parent_container_id, e.parent_container_id
        )
        new_parent_system_id = id_mapping.get(
            e.parent_system_id, e.parent_system_id
        )
        if (
            new_parent_container_id == e.parent_container_id
            and new_parent_system_id == e.parent_system_id
        ):
            rewritten.append(e)
            continue
        rewritten.append(C4Entity(
            id=e.id,
            name=e.name,
            description=e.description,
            c4_type=e.c4_type,
            technology=e.technology,
            parent_system_id=new_parent_system_id,
            parent_container_id=new_parent_container_id,
            requirement_ids=e.requirement_ids,
            metadata=e.metadata,
        ))
    return rewritten

def deduplicate_and_merge_fragment(
    primary_fragment: dict,
    running_model: dict,
    cache: EmbeddingCache | None,
    model: TextEmbedding | None,
) -> tuple[dict, list[dict], list[dict]]:
    """Process primary fragment against running model with dedup, merge, and boundary grouping.

    Args:
        primary_fragment: Dict with ``entities`` and ``relationships`` (ArchFragment-like).
        running_model: Current arch_model dict with ``entities``, ``relationships``,
            and optionally ``boundary_groups``.
        cache: EmbeddingCache for vector lookup/storage. When ``None``, similarity-based
            dedup and boundary grouping are skipped; only exact normalized-ID matching is performed.
        model: FastEmbed TextEmbedding for on-the-fly embedding generation. Only used
            when ``cache`` is not ``None``.

    Returns:
        Tuple of (updated_running_model, open_questions, merge_log).
    """
    # Parse primary fragment
    pf_entities = [_to_entity(e) for e in (primary_fragment.get("entities") or [])]
    pf_relationships = [
        _to_relationship(r) for r in (primary_fragment.get("relationships") or [])
    ]

    # Parse running model
    rm_entities = [_to_entity(e) for e in (running_model.get("entities") or [])]
    rm_relationships = [
        _to_relationship(r) for r in (running_model.get("relationships") or [])
    ]

    boundary_groups: list[dict] = list(running_model.get("boundary_groups") or [])
    open_questions: list[dict] = []
    merge_log: list[dict] = []

    # Map old entity ID → canonical entity ID for relationship rewriting
    id_mapping: dict[str, str] = {}

    has_model = cache is not None and model is not None

    for pf_entity in pf_entities:
        norm_pf_id = normalize_entity_id(pf_entity.id)
        merged = False

        temp_boundary_groups: list[dict] = []
        temp_open_questions: list[dict] = []

        for i, rm_entity in enumerate(rm_entities):
            norm_rm_id = normalize_entity_id(rm_entity.id)

            # Exact normalized-ID match → merge immediately
            if norm_pf_id == norm_rm_id:
                if pf_entity.c4_type != rm_entity.c4_type:
                    break  # same id, different type — treat as separate entity

                # Check parent hierarchy mismatch
                hierarchy_q = _check_hierarchy_mismatch(pf_entity, rm_entity)
                if hierarchy_q:
                    open_questions.append(hierarchy_q)

                merged_entity = _merge_entities(pf_entity, rm_entity)
                rm_entities[i] = merged_entity
                id_mapping[pf_entity.id] = merged_entity.id
                id_mapping[rm_entity.id] = merged_entity.id
                merge_log.append({
                    "merged_entity_id": merged_entity.id,
                    "source_entity_ids": [pf_entity.id, rm_entity.id],
                    "merge_type": "exact_id",
                })
                merged = True
                break

            # Similarity-based dedup and boundary grouping — only when model available
            if not has_model:
                continue

            similarity = _compute_entity_similarity(pf_entity, rm_entity, cache, model)

            if similarity >= DEDUP_MERGE_THRESHOLD and _do_ids_overlap(
                pf_entity, rm_entity
            ):
                if pf_entity.c4_type != rm_entity.c4_type:
                    continue  # semantically close but structurally different — keep separate

                # Check parent hierarchy mismatch
                hierarchy_q = _check_hierarchy_mismatch(pf_entity, rm_entity)
                if hierarchy_q:
                    open_questions.append(hierarchy_q)

                merged_entity = _merge_entities(pf_entity, rm_entity)
                rm_entities[i] = merged_entity
                id_mapping[pf_entity.id] = merged_entity.id
                id_mapping[rm_entity.id] = merged_entity.id
                merge_log.append({
                    "merged_entity_id": merged_entity.id,
                    "source_entity_ids": [pf_entity.id, rm_entity.id],
                    "merge_type": "similarity",
                })
                merged = True
                break

            if DEDUP_GROUP_THRESHOLD_LOW <= similarity < DEDUP_GROUP_THRESHOLD_HIGH:
                bg = _create_boundary_group(pf_entity.id, rm_entity.id, similarity)
                temp_boundary_groups.append(bg)

                # Update metadata
                bg_id = bg["group_id"]
                pf_entity.metadata["boundary_group_id"] = bg_id

                new_rm_metadata = dict(rm_entity.metadata)
                new_rm_metadata["boundary_group_id"] = bg_id
                rm_entities[i] = C4Entity(
                    id=rm_entity.id,
                    name=rm_entity.name,
                    description=rm_entity.description,
                    c4_type=rm_entity.c4_type,
                    technology=rm_entity.technology,
                    parent_system_id=rm_entity.parent_system_id,
                    parent_container_id=rm_entity.parent_container_id,
                    requirement_ids=rm_entity.requirement_ids,
                    metadata=new_rm_metadata,
                )

                temp_open_questions.append(
                    {
                        "question_type": "change_risk",
                        "entity_a_id": pf_entity.id,
                        "entity_b_id": rm_entity.id,
                        "similarity": round(similarity, 4),
                        "description": (
                            f"Entities '{pf_entity.name}' and '{rm_entity.name}' have "
                            f"moderate semantic similarity ({similarity:.2f}). "
                            f"They are grouped in C4 boundary group '{bg['group_id']}' "
                            "but remain separate deployment units."
                        ),
                        "source": "deduplication",
                        "severity": "medium",
                    }
                )

        if not merged:
            rm_entities.append(pf_entity)
            boundary_groups.extend(temp_boundary_groups)
            open_questions.extend(temp_open_questions)

    # Rewrite parent hierarchy IDs on entities (mirrors relationship rewrite below)
    rm_entities = _rewrite_entity_parent_ids(rm_entities, id_mapping)
    # Rewrite ALL relationships (both running model and primary fragment) using the ID mapping
    all_relationships: list[C4Relationship] = []

    for rel in rm_relationships:
        src = id_mapping.get(rel.source_id, rel.source_id)
        tgt = id_mapping.get(rel.target_id, rel.target_id)
        meta = dict(rel.metadata) if rel.metadata else {}
        all_relationships.append(
            C4Relationship(
                id=rel.id,
                source_id=src,
                target_id=tgt,
                description=rel.description,
                relationship_type=rel.relationship_type,
                diagram_scope=rel.diagram_scope,
                requirement_ids=list(rel.requirement_ids or []),
                metadata=meta,
            )
        )

    for rel in pf_relationships:
        src = id_mapping.get(rel.source_id, rel.source_id)
        tgt = id_mapping.get(rel.target_id, rel.target_id)
        meta = dict(rel.metadata) if rel.metadata else {}
        all_relationships.append(
            C4Relationship(
                id=rel.id,
                source_id=src,
                target_id=tgt,
                description=rel.description,
                relationship_type=rel.relationship_type,
                diagram_scope=rel.diagram_scope,
                requirement_ids=list(rel.requirement_ids or []),
                metadata=meta,
            )
        )

    # Serialize back to dicts
    updated_model: dict[str, Any] = {
        "entities": [
            e.model_dump() if isinstance(e, C4Entity) else e for e in rm_entities
        ],
        "relationships": [
            r.model_dump() if isinstance(r, C4Relationship) else r
            for r in all_relationships
        ],
        "boundary_groups": boundary_groups,
    }

    return updated_model, open_questions, merge_log
