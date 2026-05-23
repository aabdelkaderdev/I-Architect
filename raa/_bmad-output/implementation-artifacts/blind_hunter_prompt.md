# Blind Hunter Code Review Prompt

You are executing the `bmad-review-adversarial-general` workflow.

## Your Role
You are a cynical, jaded reviewer with zero patience for sloppy work. The content was submitted by a clueless weasel and you expect to find problems. Be skeptical of everything. Look for what's missing, not just what's wrong. Use a precise, professional tone — no profanity or personal attacks.

## Input Diff
Here is the diff output of the changes to review. You have NO project context, NO spec, NO other documentation.

```diff
diff --git a/raa/raa/judge/__init__.py b/raa/raa/judge/__init__.py
index 607f7b0..332210f 100644
--- a/raa/raa/judge/__init__.py
+++ b/raa/raa/judge/__init__.py
@@ -1,5 +1 @@
-"""Judge package — SAAM-first fragment scoring and ranking.
-
-Story 2.3 implements pure deterministic scoring. Later stories add
-deduplication, boundary grouping, and merge into ``arch_model``.
-"""
+"""Judge package — SAAM-first fragment scoring, ranking, deduplication, cross-cutting promotion, SAAM calibration, and merge into ``arch_model``."""
diff --git a/raa/raa/judge/cross_cutting.py b/raa/raa/judge/cross_cutting.py
new file mode 100644
index 0000000..e3e7916
--- /dev/null
+++ b/raa/raa/judge/cross_cutting.py
@@ -0,0 +1,254 @@
+"""
+Cross-cutting concern promotion engine (Story 2.5).
+
+Pure deterministic engine — no LLM calls, no randomness.
+"""
+from __future__ import annotations
+
+from raa.state.models import C4Entity, C4Relationship
+from raa.utils.constants import CROSS_CUTTING_PATTERNS, INFRA_KEYWORDS
+
+
+def detect_cross_cutting_candidates(
+    arch_model: dict,
+    patterns: list[str] | None = None,
+) -> list[dict]:
+    """Scan arch_model for cross-cutting candidates matching known patterns.
+
+    Args:
+        arch_model: Dict with ``entities``, ``relationships``, and optionally
+            ``cross_cutting_candidates`` (list[str] from ArchFragment).
+        patterns: Patterns to match against. Defaults to CROSS_CUTTING_PATTERNS + INFRA_KEYWORDS.
+
+    Returns:
+        List of detection records with ``candidate_pattern``, ``related_entity_ids``,
+        and ``requirement_ids``.
+    """
+    if patterns is None:
+        patterns = list(CROSS_CUTTING_PATTERNS) + list(INFRA_KEYWORDS)
+
+    cross_cutting_candidates: list[str] = arch_model.get("cross_cutting_candidates") or []
+    entities: list[dict] = arch_model.get("entities") or []
+
+    detections: list[dict] = []
+    seen_patterns: set[str] = set()
+
+    for candidate in cross_cutting_candidates:
+        candidate_lower = candidate.lower().strip()
+        for pattern in patterns:
+            pattern_lower = pattern.lower()
+            if pattern_lower not in candidate_lower:
+                continue
+            if pattern_lower in seen_patterns:
+                continue
+            seen_patterns.add(pattern_lower)
+
+            related_entity_ids: list[str] = []
+            collected_req_ids: set[str] = set()
+
+            for entity in entities:
+                eid = entity.get("id", "")
+                name = (entity.get("name") or "").lower()
+                desc = (entity.get("description") or "").lower()
+                tech = (entity.get("technology") or "").lower()
+
+                if pattern_lower in name or pattern_lower in desc or pattern_lower in tech:
+                    if eid:
+                        related_entity_ids.append(eid)
+                    req_ids = entity.get("requirement_ids") or []
+                    collected_req_ids.update(req_ids)
+
+            detections.append({
+                "candidate_pattern": pattern_lower,
+                "related_entity_ids": related_entity_ids,
+                "requirement_ids": sorted(collected_req_ids),
+            })
+
+    # Also detect patterns from entity metadata cross_cutting_candidates
+    for entity in entities:
+        meta = entity.get("metadata") or {}
+        entity_cc = meta.get("cross_cutting_candidates") or []
+        for cc in entity_cc:
+            cc_lower = str(cc).lower().strip()
+            for pattern in patterns:
+                pattern_lower = pattern.lower()
+                if pattern_lower not in cc_lower:
+                    continue
+                if pattern_lower in seen_patterns:
+                    continue
+                seen_patterns.add(pattern_lower)
+
+                related_entity_ids: list[str] = []
+                collected_req_ids: set[str] = set()
+
+                for e2 in entities:
+                    eid2 = e2.get("id", "")
+                    name2 = (e2.get("name") or "").lower()
+                    desc2 = (e2.get("description") or "").lower()
+                    tech2 = (e2.get("technology") or "").lower()
+                    meta2 = e2.get("metadata") or {}
+                    e2_cc = meta2.get("cross_cutting_candidates") or []
+
+                    if pattern_lower in name2 or pattern_lower in desc2 or pattern_lower in tech2 or pattern_lower in [str(c).lower() for c in e2_cc]:
+                        if eid2:
+                            related_entity_ids.append(eid2)
+                        req_ids2 = e2.get("requirement_ids") or []
+                        collected_req_ids.update(req_ids2)
+
+                detections.append({
+                    "candidate_pattern": pattern_lower,
+                    "related_entity_ids": related_entity_ids,
+                    "requirement_ids": sorted(collected_req_ids),
+                })
+
+    return detections
+
+
+def promote_cross_cutting_to_component(
+    detection: dict,
+    arch_model: dict,
+) -> tuple[C4Entity, list[str]]:
+    """Create a promoted component entity for a detected cross-cutting concern.
+
+    Args:
+        detection: Detection record from ``detect_cross_cutting_candidates``.
+        arch_model: Current arch_model dict.
+
+    Returns:
+        Tuple of (promoted C4Entity, list of affected source entity IDs).
+    """
+    pattern = detection["candidate_pattern"]
+    component_id = f"cc_{pattern}"
+    affected_entity_ids = list(detection.get("related_entity_ids") or [])
+    requirement_ids = list(detection.get("requirement_ids") or [])
+
+    # Find parent container — first container whose name/description mentions pattern
+    parent_container_id: str | None = None
+    for entity in arch_model.get("entities") or []:
+        c4_type = entity.get("c4_type", "")
+        if c4_type != "container":
+            continue
+        name = (entity.get("name") or "").lower()
+        desc = (entity.get("description") or "").lower()
+        if pattern in name or pattern in desc:
+            parent_container_id = entity.get("id")
+            break
+
+    promoted = C4Entity(
+        id=component_id,
+        name=f"{pattern.title()} (Cross-Cutting)",
+        description=f"Cross-cutting {pattern} concern promoted to structural component.",
+        c4_type="component",
+        technology="",
+        parent_container_id=parent_container_id,
+        requirement_ids=requirement_ids,
+        saam_score=0.0,
+    )
+
+    return promoted, affected_entity_ids
+
+
+def rewrite_relationships_for_promotion(
+    relationships: list[dict],
+    affected_entity_ids: list[str],
+    promoted_component_id: str,
+    pattern: str,
+) -> list[dict]:
+    """Rewrite relationships that transit through cross-cutting entities to point
+    to the promoted component.
+
+    A relationship is rewritten when its source or target is in the affected set
+    AND the relationship description or metadata mentions the pattern.
+
+    Args:
+        relationships: List of relationship dicts.
+        affected_entity_ids: Entity IDs that previously carried the cross-cutting concern.
+        promoted_component_id: The new component's ID.
+        pattern: The cross-cutting pattern being promoted.
+
+    Returns:
+        New list of relationship dicts (never mutates input).
+    """
+    affected_set = set(affected_entity_ids)
+    pattern_lower = pattern.lower()
+    rewritten: list[dict] = []
+
+    for rel in relationships:
+        rel = dict(rel)
+        src = rel.get("source_id", "")
+        tgt = rel.get("target_id", "")
+        desc = (rel.get("description") or "").lower()
+        meta = rel.get("metadata") or {}
+        meta_str = str(meta).lower()
+
+        mentions_pattern = pattern_lower in desc or pattern_lower in meta_str
+
+        if mentions_pattern:
+            if src in affected_set:
+                rel["source_id"] = promoted_component_id
+            if tgt in affected_set:
+                rel["target_id"] = promoted_component_id
+
+        rewritten.append(rel)
+
+    return rewritten
+
+
+def promote_all_cross_cutting(
+    arch_model: dict,
+) -> tuple[dict, list[dict]]:
+    """Detect and promote all cross-cutting concerns in the arch model.
+
+    Args:
+        arch_model: Dict with ``entities``, ``relationships``, and optionally
+            ``cross_cutting_candidates``.
+
+    Returns:
+        Tuple of (updated_arch_model, open_questions).
+    """
+    model = {
+        "entities": [dict(e) for e in (arch_model.get("entities") or [])],
+        "relationships": [dict(r) for r in (arch_model.get("relationships") or [])],
+        "boundary_groups": list(arch_model.get("boundary_groups") or []),
+        "cross_cutting_candidates": list(arch_model.get("cross_cutting_candidates") or []),
+    }
+
+    detections = detect_cross_cutting_candidates(model)
+    open_questions: list[dict] = []
+
+    for detection in detections:
+        promoted, affected_ids = promote_cross_cutting_to_component(detection, model)
+
+        if promoted.parent_container_id is None:
+            open_questions.append({
+                "question_type": "change_risk",
+                "description": (
+                    f"Cross-cutting '{detection['candidate_pattern']}' promoted to "
+                    f"component '{promoted.id}' but no parent container could be "
+                    "determined. Manual container assignment required."
+                ),
+                "source": "cross_cutting_promotion",
+                "severity": "medium",
+                "promoted_component_id": promoted.id,
+            })
+
+        # Add promoted component to entities
+        model["entities"].append(promoted.model_dump())
+
+        # Rewrite relationships
+        model["relationships"] = rewrite_relationships_for_promotion(
+            model["relationships"],
+            affected_ids,
+            promoted.id,
+            detection["candidate_pattern"],
+        )
+
+        # Remove requirement IDs from affected entities (move to promoted component)
+        promoted_req_ids = set(promoted.requirement_ids)
+        for i, entity in enumerate(model["entities"]):
+            if entity.get("id") in affected_ids:
+                req_ids = entity.get("requirement_ids") or []
+                new_req_ids = [r for r in req_ids if r not in promoted_req_ids]
+                entity["requirement_ids"] = new_req_ids
+
+    return model, open_questions
diff --git a/raa/raa/judge/deduplication.py b/raa/raa/judge/deduplication.py
new file mode 100644
index 0000000..c9b56ae
--- /dev/null
+++ b/raa/raa/judge/deduplication.py
@@ -0,0 +1,433 @@
+"""
+Conservative entity deduplication and C4 boundary grouping (Story 2.4).
+
+Pure deterministic engine — no LLM calls, no LangGraph dependency.
+"""
+from __future__ import annotations
+
+import re
+from typing import Any
+
+from fastembed import TextEmbedding
+from pydantic import ValidationError
+
+from raa.state.models import C4Entity, C4Relationship
+from raa.utils.constants import (
+    DEDUP_GROUP_THRESHOLD_HIGH,
+    DEDUP_GROUP_THRESHOLD_LOW,
+    DEDUP_MERGE_THRESHOLD,
+)
+from raa.utils.embedding_cache import EmbeddingCache, cosine_similarity
+
+# Patterns for ID normalization
+_RE_CAMEL_INSERT = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
+_RE_ACRONYM_SPLIT = re.compile(r"(?<=[A-Z])(?=[A-Z][a-z])")
+_RE_SEPARATORS = re.compile(r"[-.\s]+")
+_RE_MULTI_UNDERSCORE = re.compile(r"_+")
+
+
+def normalize_entity_id(entity_id: str) -> str:
+    """Convert any entity ID format to lowercase snake_case.
+
+    >>> normalize_entity_id("User_Service")
+    'user_service'
+    >>> normalize_entity_id("userService")
+    'user_service'
+    >>> normalize_entity_id("user-service")
+    'user_service'
+    >>> normalize_entity_id("DTOParser")
+    'dto_parser'
+    """
+    s = entity_id.strip()
+    s = _RE_SEPARATORS.sub("_", s)
+    s = _RE_CAMEL_INSERT.sub("_", s)
+    s = _RE_ACRONYM_SPLIT.sub("_", s)
+    s = _RE_MULTI_UNDERSCORE.sub("_", s.lower())
+    s = re.sub(r"[^a-z0-9_]", "_", s)
+    s = _RE_MULTI_UNDERSCORE.sub("_", s)
+    return s.strip("_")
+
+
+def _compute_entity_similarity(
+    entity_a: C4Entity,
+    entity_b: C4Entity,
+    cache: EmbeddingCache,
+    model: TextEmbedding,
+) -> float:
+    """Compute cosine similarity between two entity descriptions.
+
+    Returns 0.0 if either description is empty/whitespace-only.
+    """
+    desc_a = (entity_a.description or "").strip()
+    desc_b = (entity_b.description or "").strip()
+
+    if not desc_a or not desc_b:
+        return 0.0
+
+    hash_a = cache.text_hash(desc_a)
+    hash_b = cache.text_hash(desc_b)
+
+    vec_a = cache.get_cached_vector(entity_a.id, hash_a)
+    if vec_a is None:
+        embeddings = list(model.embed([desc_a]))
+        vec_a = embeddings[0].tolist()
+        cache.store_vector(entity_a.id, hash_a, vec_a)
+
+    vec_b = cache.get_cached_vector(entity_b.id, hash_b)
+    if vec_b is None:
+        embeddings = list(model.embed([desc_b]))
+        vec_b = embeddings[0].tolist()
+        cache.store_vector(entity_b.id, hash_b, vec_b)
+
+    return cosine_similarity(vec_a, vec_b)
+
+
+def _do_ids_overlap(entity_a: C4Entity, entity_b: C4Entity) -> bool:
+    """Check whether two entities share at least one requirement ID."""
+    ids_a = set(entity_a.requirement_ids or [])
+    ids_b = set(entity_b.requirement_ids or [])
+    return bool(ids_a & ids_b)
+
+
+def _union_technology(tech_a: str, tech_b: str) -> str:
+    """Union two technology tag strings with proper formatting.
+
+    Tags are split by comma/semicolon, stripped, deduplicated case-insensitively,
+    sorted, and joined with ", ".
+    """
+    seen: dict[str, str] = {}
+    for tech in (tech_a, tech_b):
+        if tech:
+            for tag in re.split(r"[,;]+", tech):
+                stripped = tag.strip()
+                if stripped:
+                    key = stripped.lower()
+                    if key not in seen:
+                        seen[key] = stripped
+                    elif any(c.isupper() for c in stripped) and not any(c.isupper() for c in seen[key]):
+                        seen[key] = stripped
+    return ", ".join(sorted(seen.values(), key=lambda s: s.lower()))
+
+
+def _merge_entities(entity_a: C4Entity, entity_b: C4Entity) -> C4Entity:
+    """Merge two entities into one.
+
+    Retains the longer description, unions technology tags and requirement IDs.
+    The canonical entity ID is the one with more requirement_ids (tie-break: entity_a).
+    """
+    canonical = (
+        entity_a
+        if len(entity_a.requirement_ids or []) >= len(entity_b.requirement_ids or [])
+        else entity_b
+    )
+
+    description = (
+        entity_a.description
+        if len(entity_a.description or "") >= len(entity_b.description or "")
+        else entity_b.description
+    )
+
+    technology = _union_technology(entity_a.technology or "", entity_b.technology or "")
+
+    requirement_ids = sorted(
+        set(entity_a.requirement_ids or []) | set(entity_b.requirement_ids or [])
+    )
+
+    return C4Entity(
+        id=canonical.id,
+        name=canonical.name,
+        description=description,
+        c4_type=canonical.c4_type,
+        technology=technology,
+        parent_system_id=canonical.parent_system_id,
+        parent_container_id=canonical.parent_container_id,
+        requirement_ids=requirement_ids,
+        metadata={**entity_a.metadata, **entity_b.metadata},
+    )
+
+
+def _rewrite_relationship_ids(
+    relationships: list[C4Relationship],
+    old_id: str,
+    new_id: str,
+) -> list[C4Relationship]:
+    """Rewrite source_id and target_id from old_id to new_id.
+
+    Returns new list — never mutates inputs.
+    """
+    rewritten: list[C4Relationship] = []
+    for rel in relationships:
+        new_source = new_id if rel.source_id == old_id else rel.source_id
+        new_target = new_id if rel.target_id == old_id else rel.target_id
+        meta = dict(rel.metadata) if rel.metadata else {}
+        rewritten.append(
+            C4Relationship(
+                id=rel.id,
+                source_id=new_source,
+                target_id=new_target,
+                description=rel.description,
+                relationship_type=rel.relationship_type,
+                diagram_scope=rel.diagram_scope,
+                metadata=meta,
+            )
+        )
+    return rewritten
+
+
+def _create_boundary_group(
+    entity_a_id: str,
+    entity_b_id: str,
+    similarity: float,
+) -> dict:
+    """Create a boundary group entry for two moderately-similar entities."""
+    return {
+        "group_id": f"bg_{entity_a_id}_{entity_b_id}",
+        "entity_ids": sorted([entity_a_id, entity_b_id]),
+        "similarity": round(similarity, 4),
+        "rationale": (
+            f"Entities have moderate semantic similarity ({similarity:.2f}) "
+            "suggesting shared deployment context but distinct C4 responsibilities."
+        ),
+    }
+
+
+def _check_hierarchy_mismatch(entity_a: C4Entity, entity_b: C4Entity) -> dict | None:
+    """Check if two entities have different parent system or container IDs."""
+    mismatches = []
+    if entity_a.parent_system_id != entity_b.parent_system_id:
+        mismatches.append(f"parent_system_id ('{entity_a.parent_system_id}' vs '{entity_b.parent_system_id}')")
+    if entity_a.parent_container_id != entity_b.parent_container_id:
+        mismatches.append(f"parent_container_id ('{entity_a.parent_container_id}' vs '{entity_b.parent_container_id}')")
+
+    if mismatches:
+        canonical_id = (
+            entity_a.id
+            if len(entity_a.requirement_ids or []) >= len(entity_b.requirement_ids or [])
+            else entity_b.id
+        )
+        return {
+            "question_type": "change_risk",
+            "entity_a_id": entity_a.id,
+            "entity_b_id": entity_b.id,
+            "description": (
+                f"Merged entities '{entity_a.name}' and '{entity_b.name}' have mismatching C4 parent hierarchy: "
+                f"{', '.join(mismatches)}. Canonical entity '{canonical_id}' parent hierarchy will be used."
+            ),
+            "source": "deduplication",
+            "severity": "medium",
+        }
+    return None
+
+
+def _to_entity(obj: Any) -> C4Entity:
+    """Coerce a dict or C4Entity into a C4Entity using Pydantic validation."""
+    if isinstance(obj, C4Entity):
+        return obj
+    if isinstance(obj, dict):
+        try:
+            return C4Entity.model_validate(obj)
+        except ValidationError as e:
+            raise ValueError(f"Failed to validate C4Entity: {e}") from e
+    raise TypeError(f"Cannot coerce {type(obj)} to C4Entity")
+
+
+def _to_relationship(obj: Any) -> C4Relationship:
+    """Coerce a dict or C4Relationship into a C4Relationship using Pydantic validation."""
+    if isinstance(obj, C4Relationship):
+        return obj
+    if isinstance(obj, dict):
+        try:
+            return C4Relationship.model_validate(obj)
+        except ValidationError as e:
+            raise ValueError(f"Failed to validate C4Relationship: {e}") from e
+    raise TypeError(f"Cannot coerce {type(obj)} to C4Relationship")
+
+
+def deduplicate_and_merge_fragment(
+    primary_fragment: dict,
+    running_model: dict,
+    cache: EmbeddingCache | None,
+    model: TextEmbedding | None,
+) -> tuple[dict, list[dict], list[dict]]:
+    """Process primary fragment against running model with dedup, merge, and boundary grouping.
+
+    Args:
+        primary_fragment: Dict with ``entities`` and ``relationships`` (ArchFragment-like).
+        running_model: Current arch_model dict with ``entities``, ``relationships``,
+            and optionally ``boundary_groups``.
+        cache: EmbeddingCache for vector lookup/storage. When ``None``, similarity-based
+            dedup and boundary grouping are skipped; only exact normalized-ID matching is performed.
+        model: FastEmbed TextEmbedding for on-the-fly embedding generation. Only used
+            when ``cache`` is not ``None``.
+
+    Returns:
+        Tuple of (updated_running_model, open_questions, merge_log).
+    """
+    # Parse primary fragment
+    pf_entities = [_to_entity(e) for e in (primary_fragment.get("entities") or [])]
+    pf_relationships = [
+        _to_relationship(r) for r in (primary_fragment.get("relationships") or [])
+    ]
+
+    # Parse running model
+    rm_entities = [_to_entity(e) for e in (running_model.get("entities") or [])]
+    rm_relationships = [
+        _to_relationship(r) for r in (running_model.get("relationships") or [])
+    ]
+
+    boundary_groups: list[dict] = list(running_model.get("boundary_groups") or [])
+    open_questions: list[dict] = []
+    merge_log: list[dict] = []
+
+    # Map old entity ID → canonical entity ID for relationship rewriting
+    id_mapping: dict[str, str] = {}
+
+    has_model = cache is not None and model is not None
+
+    for pf_entity in pf_entities:
+        norm_pf_id = normalize_entity_id(pf_entity.id)
+        merged = False
+
+        temp_boundary_groups: list[dict] = []
+        temp_open_questions: list[dict] = []
+
+        for i, rm_entity in enumerate(rm_entities):
+            norm_rm_id = normalize_entity_id(rm_entity.id)
+
+            # Exact normalized-ID match → merge immediately
+            if norm_pf_id == norm_rm_id:
+                # Check parent hierarchy mismatch
+                hierarchy_q = _check_hierarchy_mismatch(pf_entity, rm_entity)
+                if hierarchy_q:
+                    open_questions.append(hierarchy_q)
+
+                merged_entity = _merge_entities(pf_entity, rm_entity)
+                rm_entities[i] = merged_entity
+                id_mapping[pf_entity.id] = merged_entity.id
+                id_mapping[rm_entity.id] = merged_entity.id
+                merge_log.append({
+                    "merged_entity_id": merged_entity.id,
+                    "source_entity_ids": [pf_entity.id, rm_entity.id],
+                    "merge_type": "exact_id",
+                })
+                merged = True
+                break
+
+            # Similarity-based dedup and boundary grouping — only when model available
+            if not has_model:
+                continue
+
+            similarity = _compute_entity_similarity(pf_entity, rm_entity, cache, model)
+
+            if similarity >= DEDUP_MERGE_THRESHOLD and _do_ids_overlap(
+                pf_entity, rm_entity
+            ):
+                # Check parent hierarchy mismatch
+                hierarchy_q = _check_hierarchy_mismatch(pf_entity, rm_entity)
+                if hierarchy_q:
+                    open_questions.append(hierarchy_q)
+
+                merged_entity = _merge_entities(pf_entity, rm_entity)
+                rm_entities[i] = merged_entity
+                id_mapping[pf_entity.id] = merged_entity.id
+                id_mapping[rm_entity.id] = merged_entity.id
+                merge_log.append({
+                    "merged_entity_id": merged_entity.id,
+                    "source_entity_ids": [pf_entity.id, rm_entity.id],
+                    "merge_type": "similarity",
+                })
+                merged = True
+                break
+
+            if DEDUP_GROUP_THRESHOLD_LOW <= similarity < DEDUP_GROUP_THRESHOLD_HIGH:
+                bg = _create_boundary_group(pf_entity.id, rm_entity.id, similarity)
+                temp_boundary_groups.append(bg)
+
+                # Update metadata
+                bg_id = bg["group_id"]
+                pf_entity.metadata["boundary_group_id"] = bg_id
+
+                new_rm_metadata = dict(rm_entity.metadata)
+                new_rm_metadata["boundary_group_id"] = bg_id
+                rm_entities[i] = C4Entity(
+                    id=rm_entity.id,
+                    name=rm_entity.name,
+                    description=rm_entity.description,
+                    c4_type=rm_entity.c4_type,
+                    technology=rm_entity.technology,
+                    parent_system_id=rm_entity.parent_system_id,
+                    parent_container_id=rm_entity.parent_container_id,
+                    requirement_ids=rm_entity.requirement_ids,
+                    metadata=new_rm_metadata,
+                )
+
+                temp_open_questions.append(
+                    {
+                        "question_type": "change_risk",
+                        "entity_a_id": pf_entity.id,
+                        "entity_b_id": rm_entity.id,
+                        "similarity": round(similarity, 4),
+                        "description": (
+                            f"Entities '{pf_entity.name}' and '{rm_entity.name}' have "
+                            f"moderate semantic similarity ({similarity:.2f}). "
+                            f"They are grouped in C4 boundary group '{bg['group_id']}' "
+                            "but remain separate deployment units."
+                        ),
+                        "source": "deduplication",
+                        "severity": "medium",
+                    }
+                )
+
+        if not merged:
+            rm_entities.append(pf_entity)
+            boundary_groups.extend(temp_boundary_groups)
+            open_questions.extend(temp_open_questions)
+
+    # Rewrite ALL relationships (both running model and primary fragment) using the ID mapping
+    all_relationships: list[C4Relationship] = []
+
+    for rel in rm_relationships:
+        src = id_mapping.get(rel.source_id, rel.source_id)
+        tgt = id_mapping.get(rel.target_id, rel.target_id)
+        meta = dict(rel.metadata) if rel.metadata else {}
+        all_relationships.append(
+            C4Relationship(
+                id=rel.id,
+                source_id=src,
+                target_id=tgt,
+                description=rel.description,
+                relationship_type=rel.relationship_type,
+                diagram_scope=rel.diagram_scope,
+                metadata=meta,
+            )
+        )
+
+    for rel in pf_relationships:
+        src = id_mapping.get(rel.source_id, rel.source_id)
+        tgt = id_mapping.get(rel.target_id, rel.target_id)
+        meta = dict(rel.metadata) if rel.metadata else {}
+        all_relationships.append(
+            C4Relationship(
+                id=rel.id,
+                source_id=src,
+                target_id=tgt,
+                description=rel.description,
+                relationship_type=rel.relationship_type,
+                diagram_scope=rel.diagram_scope,
+                metadata=meta,
+            )
+        )
+
+    # Serialize back to dicts
+    updated_model: dict[str, Any] = {
+        "entities": [
+            e.model_dump() if isinstance(e, C4Entity) else e for e in rm_entities
+        ],
+        "relationships": [
+            r.model_dump() if isinstance(r, C4Relationship) else r
+            for r in all_relationships
+        ],
+        "boundary_groups": boundary_groups,
+    }
+
+    return updated_model, open_questions, merge_log
diff --git a/raa/raa/judge/reconcile.py b/raa/raa/judge/reconcile.py
index c9678e3..ce64469 100644
--- a/raa/raa/judge/reconcile.py
+++ b/raa/raa/judge/reconcile.py
@@ -1,29 +1,34 @@
 """
-Judge reconciliation node (Story 2.3).
+Judge reconciliation node (Story 2.3 + 2.4 + 2.5).
 
-Selects the primary fragment for the current batch via SAAM scoring but
-does NOT merge, deduplicate, or advance ``batch_cursor``.
+Scores and ranks fragments via SAAM, deduplicates and merges the primary
+fragment into the running ``arch_model``, promotes cross-cutting concerns,
+calibrates per-entity SAAM scores, and advances ``batch_cursor``.
 """
 from __future__ import annotations
 
+import os
 from typing import Any
 
 from langchain_core.runnables import RunnableConfig
 
+from raa.judge.cross_cutting import promote_all_cross_cutting
+from raa.judge.deduplication import deduplicate_and_merge_fragment
+from raa.judge.saam_calibration import calibrate_entity_saam_scores
 from raa.judge.scoring import rank_batch_fragments
 from raa.state.schemas import RAAState
+from raa.utils.constants import EMBEDDING_CACHE_DIR, EMBEDDING_MODEL_NAME
+from raa.utils.embedding_cache import EmbeddingCache, get_embedding_model
 
 
 def select_primary_fragment(
     state: RAAState,
     config: RunnableConfig | None = None,
 ) -> dict[str, Any]:
-    """Score and rank fragments for the current batch, selecting a primary.
+    """Score, rank, deduplicate, and merge the primary fragment.
 
-    Does NOT:
-    - Return ``batch_cursor``
-    - Update ``arch_model``
-    - Perform deduplication or boundary grouping
+    Returns partial state update with ``judge_rankings``, ``arch_model``,
+    ``batch_cursor`` (incremented by 1), and any dedup ``open_questions``.
     """
     batch_outputs: list[dict] = state.get("batch_outputs") or []
     batch_cursor = state.get("batch_cursor", 0)
@@ -31,14 +36,105 @@ def select_primary_fragment(
 
     # Filter to records for the current batch_cursor only
     current_batch = [
-        r for r in batch_outputs
+        r
+        for r in batch_outputs
         if isinstance(r, dict) and r.get("batch_index") == batch_cursor
     ]
 
     result = rank_batch_fragments(current_batch, quality_weights)
 
-    # Store auditable ranking results; key is batch_cursor for later lookup
+    # Store auditable ranking results
     existing_rankings = dict(state.get("judge_rankings") or {})
     existing_rankings[batch_cursor] = result
 
-    return {"judge_rankings": existing_rankings}
+    # ── Story 2.4: Dedup and merge primary fragment into arch_model ──────
+    primary = result.get("primary_fragment")
+    open_questions: list[dict] = []
+    merge_log: list[dict] = []
+    current_model = state.get("arch_model") or {}
+
+    # Capture winning fragment's saam_scenarios and cross_cutting_candidates for
+    # downstream cross-cutting promotion (Story 2.5) and SAAM calibration (Story 2.5).
+    winning_saam_scenarios: list[dict] = []
+    winning_cc_candidates: list[str] = []
+
+    if primary is not None:
+        # Locate the winning record
+        winning_record = None
+        for r in current_batch:
+            frag = r.get("arch_fragment") if isinstance(r, dict) else None
+            if (
+                frag
+                and r.get("batch_id") == primary.batch_id
+                and r.get("strategy") == primary.strategy
+            ):
+                winning_record = r
+                break
+
+        if winning_record is not None and winning_record.get("arch_fragment"):
+            pf = winning_record["arch_fragment"]
+            pf_entities = pf.get("entities") or []
+            rm_entities = current_model.get("entities") or []
+
+            # Capture fragment-level annotations for downstream processing
+            winning_saam_scenarios = pf.get("saam_scenarios") or []
+            winning_cc_candidates = pf.get("cross_cutting_candidates") or []
+
+            # Only load the embedding model when both sides have entities to compare.
+            # First batch (empty running model) and empty fragments skip the model load.
+            if pf_entities and rm_entities:
+                cfg = {}
+                if config is not None:
+                    if isinstance(config, dict):
+                        cfg = config.get("configurable") or {}
+                    else:
+                        cfg = getattr(config, "configurable", None) or {}
+
+                db_path = cfg.get(
+                    "non_asr_embeddings_db_path",
+                    os.path.join(EMBEDDING_CACHE_DIR, "non_asr_embeddings.db"),
+                )
+                cache_dir = cfg.get("embedding_cache_dir", EMBEDDING_CACHE_DIR)
+                model_name = cfg.get("embedding_model_name", EMBEDDING_MODEL_NAME)
+
+                model = get_embedding_model(cache_dir, model_name)
+
+                with EmbeddingCache(db_path, model_name) as cache:
+                    new_arch_model, questions, merge_log = deduplicate_and_merge_fragment(
+                        pf,
+                        current_model,
+                        cache,
+                        model,
+                    )
+                open_questions = questions
+            else:
+                # No cross-model dedup needed — merge without embedding comparison
+                new_arch_model, _, merge_log = deduplicate_and_merge_fragment(
+                    pf,
+                    current_model,
+                    None,  # cache
+                    None,  # model
+                )
+        else:
+            new_arch_model = current_model
+    else:
+        new_arch_model = current_model
+
+    # ── Story 2.5: Cross-cutting promotion ────────────────────────────────
+    new_arch_model["cross_cutting_candidates"] = list(winning_cc_candidates)
+    new_arch_model, cc_questions = promote_all_cross_cutting(new_arch_model)
+    open_questions.extend(cc_questions)
+
+    # ── Story 2.5: SAAM score calibration ─────────────────────────────────
+    new_arch_model = calibrate_entity_saam_scores(
+        new_arch_model,
+        saam_scenarios=winning_saam_scenarios,
+        merge_log=merge_log,
+    )
+
+    return {
+        "judge_rankings": existing_rankings,
+        "arch_model": new_arch_model,
+        "batch_cursor": batch_cursor + 1,
+        "open_questions": open_questions,
+    }
diff --git a/raa/raa/judge/saam_calibration.py b/raa/raa/judge/saam_calibration.py
new file mode 100644
index 0000000..3c7b3ea
--- /dev/null
+++ b/raa/raa/judge/saam_calibration.py
@@ -0,0 +1,134 @@
+"""
+Per-entity SAAM score calibration engine (Story 2.5).
+
+Pure deterministic engine — no LLM calls, no randomness.
+"""
+from __future__ import annotations
+
+from raa.utils.constants import (
+    SAAM_BASE_SCORE,
+    SAAM_BOUNDARY_GROUP_PENALTY,
+    SAAM_DEDUP_PENALTY,
+    SAAM_PERFECT_SCORE,
+)
+
+
+def _entity_in_boundary_group(entity_id: str, boundary_groups: list[dict]) -> bool:
+    """Check whether an entity is a member of any boundary group."""
+    for bg in boundary_groups:
+        entity_ids = bg.get("entity_ids") or []
+        if entity_id in entity_ids:
+            return True
+    return False
+
+
+def _count_merge_events(entity_id: str, merge_log: list[dict]) -> int:
+    """Count how many merge events this entity participated in."""
+    count = 0
+    for entry in merge_log:
+        merged_id = entry.get("merged_entity_id", "")
+        source_ids: list[str] = entry.get("source_entity_ids") or []
+        if entity_id == merged_id or entity_id in source_ids:
+            count += 1
+    return count
+
+
+def _check_perfect_score(
+    entity: dict,
+    entities: list[dict],
+    boundary_groups: list[dict],
+    saam_scenarios: list[dict],
+) -> bool:
+    """Check if an entity qualifies for the perfect SAAM score (1.0).
+
+    Conditions:
+    1. c4_type == "component"
+    2. No shared requirement_ids with any entity in the same boundary group
+    3. All SAAMScenarios for the entity's requirement_ids have satisfaction == "satisfied"
+    """
+    if entity.get("c4_type") != "component":
+        return False
+
+    entity_req_ids = set(entity.get("requirement_ids") or [])
+    if not entity_req_ids:
+        return False
+
+    # Check functional overlap: no shared requirement_ids with same boundary group entities
+    entity_bg_id = (entity.get("metadata") or {}).get("boundary_group_id")
+    if entity_bg_id:
+        for other in entities:
+            if other.get("id") == entity.get("id"):
+                continue
+            other_bg_id = (other.get("metadata") or {}).get("boundary_group_id")
+            if other_bg_id == entity_bg_id:
+                other_req_ids = set(other.get("requirement_ids") or [])
+                if entity_req_ids & other_req_ids:
+                    return False
+
+    # Check all scenarios passing
+    entity_req_list = list(entity_req_ids)
+    relevant_scenarios = [
+        s for s in saam_scenarios
+        if set(s.get("requirement_ids") or []) & entity_req_ids
+    ]
+
+    if not relevant_scenarios:
+        return False
+
+    for scenario in relevant_scenarios:
+        if scenario.get("satisfaction") != "satisfied":
+            return False
+
+    return True
+
+
+def calibrate_entity_saam_scores(
+    arch_model: dict,
+    saam_scenarios: list[dict] | None = None,
+    boundary_groups: list[dict] | None = None,
+    merge_log: list[dict] | None = None,
+) -> dict:
+    """Assign a ``saam_score`` to every entity in the arch model.
+
+    Args:
+        arch_model: Dict with ``entities`` key. May also carry ``boundary_groups``.
+        saam_scenarios: SAAM scenarios from the winning fragment (list of dicts).
+        boundary_groups: Override boundary groups. Defaults to model's ``boundary_groups``.
+        merge_log: Merge log from deduplication. Each entry has
+            ``merged_entity_id``, ``source_entity_ids``, ``merge_type``.
+
+    Returns:
+        Updated arch_model dict with ``saam_score`` set on every entity.
+    """
+    if saam_scenarios is None:
+        saam_scenarios = []
+    if boundary_groups is None:
+        boundary_groups = arch_model.get("boundary_groups") or []
+    if merge_log is None:
+        merge_log = []
+
+    entities: list[dict] = [dict(e) for e in (arch_model.get("entities") or [])]
+
+    for entity in entities:
+        eid = entity.get("id", "")
+
+        if _check_perfect_score(entity, entities, boundary_groups, saam_scenarios):
+            entity["saam_score"] = SAAM_PERFECT_SCORE
+            continue
+
+        score = SAAM_BASE_SCORE
+
+        # Dedup penalty
+        merge_count = _count_merge_events(eid, merge_log)
+        score -= SAAM_DEDUP_PENALTY * merge_count
+
+        # Boundary group penalty
+        if _entity_in_boundary_group(eid, boundary_groups):
+            score -= SAAM_BOUNDARY_GROUP_PENALTY
+
+        # Clamp to [0.0, 1.0]
+        entity["saam_score"] = max(0.0, min(1.0, round(score, 4)))
+
+    result = dict(arch_model)
+    result["entities"] = entities
+    return result
diff --git a/raa/raa/state/models.py b/raa/raa/state/models.py
index 8afc344..9ea73c7 100644
--- a/raa/raa/state/models.py
+++ b/raa/raa/state/models.py
@@ -38,6 +38,7 @@ class C4Entity(BaseModel):
     parent_system_id: str | None = None
     parent_container_id: str | None = None
     requirement_ids: list[str] = Field(default_factory=list)
+    saam_score: float = Field(default=0.0)
     metadata: dict = Field(default_factory=dict)
 
 
diff --git a/raa/raa/utils/constants.py b/raa/raa/utils/constants.py
index aa2a047..1d46860 100644
--- a/raa/raa/utils/constants.py
+++ b/raa/raa/utils/constants.py
@@ -35,6 +35,26 @@ INFRA_KEYWORDS = ["all", "every", "always", "any"]
 # ── SAAM scoring multipliers ───────────────────────────────────────────────
 SAAM_REDUCED_CONFIDENCE_MULTIPLIER = 0.5
 
+# ── Cross-cutting concern patterns ─────────────────────────────────────────
+CROSS_CUTTING_PATTERNS = [
+    "security",
+    "compliance",
+    "logging",
+    "monitoring",
+    "authentication",
+    "authorization",
+    "audit",
+    "observability",
+    "rate_limiting",
+    "caching",
+]
+
+# ── SAAM calibration constants ─────────────────────────────────────────────
+SAAM_PERFECT_SCORE = 1.0
+SAAM_BASE_SCORE = 0.70
+SAAM_DEDUP_PENALTY = 0.15
+SAAM_BOUNDARY_GROUP_PENALTY = 0.10
+
 # ── SAAM satisfaction factors ──────────────────────────────────────────────
 SAAM_SATISFACTION_FACTORS: dict[str, float] = {
     "satisfied": 1.0,
diff --git a/raa/tests/raa/unit/test_judge_cross_cutting.py b/raa/tests/raa/unit/test_judge_cross_cutting.py
new file mode 100644
index 0000000..7f29846
--- /dev/null
+++ b/raa/tests/raa/unit/test_judge_cross_cutting.py
@@ -0,0 +1,391 @@
+"""
+Unit tests for cross-cutting concern promotion engine (Story 2.5).
+"""
+from __future__ import annotations
+
+import pytest
+
+from raa.judge.cross_cutting import (
+    detect_cross_cutting_candidates,
+    promote_cross_cutting_to_component,
+    rewrite_relationships_for_promotion,
+    promote_all_cross_cutting,
+)
+from raa.state.models import C4Entity
+
+
+# ── Helpers ─────────────────────────────────────────────────────────────────
+
+
+def _entity_dict(
+    id="entity-1",
+    name="Test Entity",
+    description="Test description",
+    c4_type="container",
+    technology="",
+    requirement_ids=None,
+    metadata=None,
+):
+    return {
+        "id": id,
+        "name": name,
+        "description": description,
+        "c4_type": c4_type,
+        "technology": technology,
+        "parent_system_id": None,
+        "parent_container_id": None,
+        "requirement_ids": requirement_ids or [],
+        "saam_score": 0.0,
+        "metadata": metadata or {},
+    }
+
+
+def _rel_dict(source_id="a", target_id="b", description="uses", metadata=None):
+    return {
+        "id": f"rel-{source_id}-{target_id}",
+        "source_id": source_id,
+        "target_id": target_id,
+        "description": description,
+        "relationship_type": "uses",
+        "diagram_scope": "",
+        "metadata": metadata or {},
+    }
+
+
+# ── Detection ───────────────────────────────────────────────────────────────
+
+
+class TestDetectCrossCuttingCandidates:
+    def test_no_cross_cutting_candidates_returns_empty(self):
+        model = {"entities": [], "relationships": [], "cross_cutting_candidates": []}
+        result = detect_cross_cutting_candidates(model)
+        assert result == []
+
+    def test_no_matching_patterns_returns_empty(self):
+        model = {
+            "entities": [_entity_dict()],
+            "relationships": [],
+            "cross_cutting_candidates": ["unknown_pattern_xyz"],
+        }
+        result = detect_cross_cutting_candidates(model)
+        assert result == []
+
+    def test_detects_security_pattern(self):
+        model = {
+            "entities": [
+                _entity_dict(
+                    id="auth-svc",
+                    name="Authentication Service",
+                    description="Handles security and authentication",
+                    requirement_ids=["R1", "R2"],
+                )
+            ],
+            "relationships": [],
+            "cross_cutting_candidates": ["security_component", "logging_service"],
+        }
+        result = detect_cross_cutting_candidates(model)
+        patterns = {d["candidate_pattern"] for d in result}
+        assert "security" in patterns
+        assert "logging" in patterns
+
+    def test_detects_pattern_from_entity_metadata(self):
+        model = {
+            "entities": [
+                _entity_dict(
+                    id="mon-svc",
+                    name="Monitor",
+                    description="Monitoring service",
+                    metadata={"cross_cutting_candidates": ["monitoring", "logging"]},
+                )
+            ],
+            "relationships": [],
+            "cross_cutting_candidates": [],
+        }
+        result = detect_cross_cutting_candidates(model)
+        patterns = {d["candidate_pattern"] for d in result}
+        assert "monitoring" in patterns
+        assert "logging" in patterns
+
+    def test_deduplicates_same_pattern(self):
+        model = {
+            "entities": [_entity_dict()],
+            "relationships": [],
+            "cross_cutting_candidates": ["security_service", "security_check"],
+        }
+        result = detect_cross_cutting_candidates(model)
+        assert len(result) == 1
+        assert result[0]["candidate_pattern"] == "security"
+
+    def test_collects_related_entity_ids(self):
+        model = {
+            "entities": [
+                _entity_dict(id="auth-1", name="Auth Service", description="Handles authentication"),
+                _entity_dict(id="unrelated", name="Data Store", description="Stores data"),
+            ],
+            "relationships": [],
+            "cross_cutting_candidates": ["authentication_check"],
+        }
+        result = detect_cross_cutting_candidates(model)
+        assert len(result) == 1
+        assert "auth-1" in result[0]["related_entity_ids"]
+        assert "unrelated" not in result[0]["related_entity_ids"]
+
+    def test_collects_requirement_ids_from_related_entities(self):
+        model = {
+            "entities": [
+                _entity_dict(id="auth-1", name="Auth", description="authentication", requirement_ids=["R1", "R2"]),
+                _entity_dict(id="auth-2", name="Login", description="authentication", requirement_ids=["R2", "R3"]),
+            ],
+            "relationships": [],
+            "cross_cutting_candidates": ["authentication"],
+        }
+        result = detect_cross_cutting_candidates(model)
+        assert len(result) == 1
+        assert set(result[0]["requirement_ids"]) == {"R1", "R2", "R3"}
+
+    def test_matches_infra_keywords(self):
+        model = {
+            "entities": [_entity_dict(name="Every", description="all things")],
+            "relationships": [],
+            "cross_cutting_candidates": ["all_things", "every_service"],
+        }
+        result = detect_cross_cutting_candidates(model)
+        patterns = {d["candidate_pattern"] for d in result}
+        assert "all" in patterns
+        assert "every" in patterns
+
+    def test_entity_tech_matches_pattern(self):
+        model = {
+            "entities": [_entity_dict(id="s1", name="Svc", technology="security-library, caching-layer")],
+            "relationships": [],
+            "cross_cutting_candidates": ["security"],
+        }
+        result = detect_cross_cutting_candidates(model)
+        assert len(result) == 1
+        assert "s1" in result[0]["related_entity_ids"]
+
+
+# ── Promotion ───────────────────────────────────────────────────────────────
+
+
+class TestPromoteCrossCuttingToComponent:
+    def test_creates_component_with_correct_c4_type(self):
+        detection = {
+            "candidate_pattern": "security",
+            "related_entity_ids": ["auth-svc"],
+            "requirement_ids": ["R1", "R2"],
+        }
+        model = {"entities": [], "relationships": []}
+        promoted, affected = promote_cross_cutting_to_component(detection, model)
+        assert promoted.c4_type == "component"
+        assert promoted.id == "cc_security"
+        assert promoted.name == "Security (Cross-Cutting)"
+        assert set(promoted.requirement_ids) == {"R1", "R2"}
+
+    def test_returns_affected_entity_ids(self):
+        detection = {
+            "candidate_pattern": "logging",
+            "related_entity_ids": ["log-svc", "audit-svc"],
+            "requirement_ids": [],
+        }
+        model = {"entities": [], "relationships": []}
+        promoted, affected = promote_cross_cutting_to_component(detection, model)
+        assert set(affected) == {"log-svc", "audit-svc"}
+
+    def test_finds_parent_container(self):
+        detection = {
+            "candidate_pattern": "security",
+            "related_entity_ids": [],
+            "requirement_ids": [],
+        }
+        model = {
+            "entities": [
+                _entity_dict(id="api", name="API", c4_type="system"),
+                _entity_dict(id="backend", name="Backend", description="security container", c4_type="container"),
+            ],
+            "relationships": [],
+        }
+        promoted, _ = promote_cross_cutting_to_component(detection, model)
+        assert promoted.parent_container_id == "backend"
+
+    def test_no_parent_container_when_none_match(self):
+        detection = {
+            "candidate_pattern": "monitoring",
+            "related_entity_ids": [],
+            "requirement_ids": [],
+        }
+        model = {
+            "entities": [_entity_dict(id="api", name="API Gateway", c4_type="system")],
+            "relationships": [],
+        }
+        promoted, _ = promote_cross_cutting_to_component(detection, model)
+        assert promoted.parent_container_id is None
+
+
+# ── Relationship Rewriting ──────────────────────────────────────────────────
+
+
+class TestRewriteRelationshipsForPromotion:
+    def test_rewrites_source_when_affected_and_mentions_pattern(self):
+        rels = [
+            _rel_dict(source_id="auth-svc", target_id="db", description="security check"),
+            _rel_dict(source_id="auth-svc", target_id="cache", description="data access"),
+        ]
+        result = rewrite_relationships_for_promotion(
+            rels, affected_entity_ids=["auth-svc"],
+            promoted_component_id="cc_security", pattern="security",
+        )
+        assert result[0]["source_id"] == "cc_security"
+        assert result[0]["target_id"] == "db"
+        assert result[1]["source_id"] == "auth-svc"  # not rewritten — doesn't mention pattern
+
+    def test_rewrites_target_when_affected_and_mentions_pattern(self):
+        rels = [
+            _rel_dict(source_id="client", target_id="auth-svc", description="authentication"),
+        ]
+        result = rewrite_relationships_for_promotion(
+            rels, affected_entity_ids=["auth-svc"],
+            promoted_component_id="cc_authentication", pattern="authentication",
+        )
+        assert result[0]["target_id"] == "cc_authentication"
+
+    def test_no_rewrite_when_not_affected(self):
+        rels = [
+            _rel_dict(source_id="unrelated", target_id="db", description="security audit"),
+        ]
+        result = rewrite_relationships_for_promotion(
+            rels, affected_entity_ids=["auth-svc"],
+            promoted_component_id="cc_security", pattern="security",
+        )
+        assert result[0]["source_id"] == "unrelated"
+        assert result[0]["target_id"] == "db"
+
+    def test_no_rewrite_when_pattern_not_mentioned(self):
+        rels = [
+            _rel_dict(source_id="auth-svc", target_id="db", description="reads data"),
+        ]
+        result = rewrite_relationships_for_promotion(
+            rels, affected_entity_ids=["auth-svc"],
+            promoted_component_id="cc_security", pattern="security",
+        )
+        assert result[0]["source_id"] == "auth-svc"
+
+    def test_pattern_in_metadata_triggers_rewrite(self):
+        rels = [
+            _rel_dict(source_id="auth-svc", target_id="db", description="uses",
+                       metadata={"concern": "security_check"}),
+        ]
+        result = rewrite_relationships_for_promotion(
+            rels, affected_entity_ids=["auth-svc"],
+            promoted_component_id="cc_security", pattern="security",
+        )
+        assert result[0]["source_id"] == "cc_security"
+
+
+# ── Full Pipeline ───────────────────────────────────────────────────────────
+
+
+class TestPromoteAllCrossCutting:
+    def test_no_candidates_returns_model_unchanged(self):
+        model = {
+            "entities": [_entity_dict()],
+            "relationships": [_rel_dict()],
+            "boundary_groups": [],
+            "cross_cutting_candidates": [],
+        }
+        result, questions = promote_all_cross_cutting(model)
+        assert len(result["entities"]) == 1
+        assert len(result["relationships"]) == 1
+        assert questions == []
+
+    def test_promotes_detected_cross_cutting(self):
+        model = {
+            "entities": [
+                _entity_dict(id="auth-svc", name="Auth Service",
+                             description="Handles authentication and authorization",
+                             requirement_ids=["R1", "R2"]),
+            ],
+            "relationships": [
+                _rel_dict(source_id="auth-svc", target_id="db", description="authentication request"),
+            ],
+            "boundary_groups": [],
+            "cross_cutting_candidates": ["authentication"],
+        }
+        result, questions = promote_all_cross_cutting(model)
+        # Promoted component added
+        entity_ids = {e["id"] for e in result["entities"]}
+        assert "cc_authentication" in entity_ids
+        # Relationship rewritten
+        assert result["relationships"][0]["source_id"] == "cc_authentication"
+
+    def test_multiple_cross_cutting_patterns(self):
+        model = {
+            "entities": [
+                _entity_dict(id="svc-1", name="Security Service", description="security", requirement_ids=["R1"]),
+                _entity_dict(id="svc-2", name="Log Service", description="logging", requirement_ids=["R2"]),
+            ],
+            "relationships": [],
+            "boundary_groups": [],
+            "cross_cutting_candidates": ["security", "logging"],
+        }
+        result, questions = promote_all_cross_cutting(model)
+        entity_ids = {e["id"] for e in result["entities"]}
+        assert "cc_security" in entity_ids
+        assert "cc_logging" in entity_ids
+
+    def test_removes_requirement_ids_from_affected_entities(self):
+        model = {
+            "entities": [
+                _entity_dict(id="auth-svc", name="Auth", description="authentication",
+                             requirement_ids=["R1", "R2"]),
+            ],
+            "relationships": [],
+            "boundary_groups": [],
+            "cross_cutting_candidates": ["authentication"],
+        }
+        result, _ = promote_all_cross_cutting(model)
+        auth_entity = next(e for e in result["entities"] if e["id"] == "auth-svc")
+        assert auth_entity["requirement_ids"] == []
+
+    def test_open_question_when_no_parent_container(self):
+        model = {
+            "entities": [
+                _entity_dict(id="svc", name="Service", description="security thing", c4_type="system"),
+            ],
+            "relationships": [],
+            "boundary_groups": [],
+            "cross_cutting_candidates": ["security"],
+        }
+        result, questions = promote_all_cross_cutting(model)
+        assert len(questions) == 1
+        assert questions[0]["source"] == "cross_cutting_promotion"
+        assert "cc_security" in questions[0]["description"]
+
+    def test_deterministic_same_input_same_output(self):
+        model = {
+            "entities": [
+                _entity_dict(id="svc", name="Auth Service", description="security auth",
+                             requirement_ids=["R1"]),
+            ],
+            "relationships": [_rel_dict(source_id="svc", target_id="db")],
+            "boundary_groups": [],
+            "cross_cutting_candidates": ["security"],
+        }
+        r1, q1 = promote_all_cross_cutting(model)
+        r2, q2 = promote_all_cross_cutting(model)
+        assert r1 == r2
+        assert q1 == q2
+
+    def test_entity_without_cross_cutting_is_unchanged(self):
+        model = {
+            "entities": [
+                _entity_dict(id="svc-1", name="Auth Service", description="authentication", requirement_ids=["R1"]),
+                _entity_dict(id="svc-2", name="Data Store", description="stores data", requirement_ids=["R2"]),
+            ],
+            "relationships": [],
+            "boundary_groups": [],
+            "cross_cutting_candidates": ["authentication"],
+        }
+        result, _ = promote_all_cross_cutting(model)
+        data_entity = next(e for e in result["entities"] if e["id"] == "svc-2")
+        assert data_entity["requirement_ids"] == ["R2"]
diff --git a/raa/tests/raa/unit/test_judge_deduplication.py b/raa/tests/raa/unit/test_judge_deduplication.py
new file mode 100644
index 0000000..463c175
--- /dev/null
+++ b/raa/tests/raa/unit/test_judge_deduplication.py
@@ -0,0 +1,466 @@
+"""
+Unit tests for deduplication engine (Story 2.4).
+"""
+from __future__ import annotations
+
+import pytest
+
+from raa.judge.deduplication import (
+    normalize_entity_id,
+    deduplicate_and_merge_fragment,
+    _merge_entities,
+    _union_technology,
+    _do_ids_overlap,
+    _rewrite_relationship_ids,
+    _create_boundary_group,
+    _to_entity,
+    _to_relationship,
+)
+from raa.state.models import C4Entity, C4Relationship
+
+
+# ── ID Normalization ────────────────────────────────────────────────────────
+
+
+@pytest.mark.parametrize(
+    "input_id, expected",
+    [
+        ("User_Service", "user_service"),
+        ("userService", "user_service"),
+        ("user-service", "user_service"),
+        ("UserService", "user_service"),
+        ("DTOParser", "dto_parser"),
+        ("user.service", "user_service"),
+        ("user service", "user_service"),
+        ("user__service", "user_service"),
+        ("_user_service_", "user_service"),
+        ("simple", "simple"),
+        ("UPPERCASE", "uppercase"),
+        ("HTTPClient", "http_client"),
+        ("  spaced  ", "spaced"),
+    ],
+)
+def test_normalize_entity_id(input_id, expected):
+    assert normalize_entity_id(input_id) == expected
+
+
+# ── Technology Union ────────────────────────────────────────────────────────
+
+
+def test_union_technology_basic():
+    result = _union_technology("Python, FastAPI", "FastAPI, Redis")
+    assert result == "FastAPI, Python, Redis"
+
+
+def test_union_technology_semicolons():
+    result = _union_technology("Python;FastAPI", "Redis; Python")
+    assert result == "FastAPI, Python, Redis"
+
+
+def test_union_technology_empty():
+    assert _union_technology("", "") == ""
+    assert _union_technology("Python", "") == "Python"
+
+
+def test_union_technology_whitespace():
+    result = _union_technology("  Python  ,  FastAPI  ", "  FastAPI  ")
+    assert result == "FastAPI, Python"
+
+
+# ── Requirement ID Overlap ──────────────────────────────────────────────────
+
+
+def test_do_ids_overlap_true():
+    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
+    b = C4Entity(id="b", name="B", requirement_ids=["R2", "R3"])
+    assert _do_ids_overlap(a, b) is True
+
+
+def test_do_ids_overlap_false():
+    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
+    b = C4Entity(id="b", name="B", requirement_ids=["R3", "R4"])
+    assert _do_ids_overlap(a, b) is False
+
+
+def test_do_ids_overlap_empty():
+    a = C4Entity(id="a", name="A")
+    b = C4Entity(id="b", name="B")
+    assert _do_ids_overlap(a, b) is False
+
+
+# ── Entity Merging ──────────────────────────────────────────────────────────
+
+
+def test_merge_entities_longest_description_kept():
+    a = C4Entity(id="a", name="A", description="Short", technology="Python",
+                 requirement_ids=["R1"])
+    b = C4Entity(id="b", name="B", description="Much longer description here",
+                 technology="FastAPI", requirement_ids=["R2"])
+    merged = _merge_entities(a, b)
+    assert merged.description == "Much longer description here"
+
+
+def test_merge_entities_canonical_id_from_more_reqs():
+    a = C4Entity(id="a", name="A", requirement_ids=["R1"])
+    b = C4Entity(id="b", name="B", requirement_ids=["R2", "R3"])
+    merged = _merge_entities(a, b)
+    assert merged.id == "b"
+
+
+def test_merge_entities_canonical_id_tie_break_a():
+    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
+    b = C4Entity(id="b", name="B", requirement_ids=["R3", "R4"])
+    merged = _merge_entities(a, b)
+    assert merged.id == "a"  # tie → entity_a wins
+
+
+def test_merge_entities_technology_union():
+    a = C4Entity(id="a", name="A", technology="Python, FastAPI", requirement_ids=["R1"])
+    b = C4Entity(id="b", name="B", technology="FastAPI, Redis", requirement_ids=["R1"])
+    merged = _merge_entities(a, b)
+    assert "Python" in merged.technology
+    assert "FastAPI" in merged.technology
+    assert "Redis" in merged.technology
+
+
+def test_merge_entities_requirement_ids_union():
+    a = C4Entity(id="a", name="A", requirement_ids=["R1", "R2"])
+    b = C4Entity(id="b", name="B", requirement_ids=["R2", "R3"])
+    merged = _merge_entities(a, b)
+    assert merged.requirement_ids == ["R1", "R2", "R3"]
+
+
+def test_merge_entities_metadata_merged():
+    a = C4Entity(id="a", name="A", metadata={"key_a": 1})
+    b = C4Entity(id="b", name="B", metadata={"key_b": 2})
+    merged = _merge_entities(a, b)
+    assert merged.metadata == {"key_a": 1, "key_b": 2}
+
+
+def test_merge_entities_retains_c4_type():
+    a = C4Entity(id="a", name="A", c4_type="container", requirement_ids=["R1", "R2"])
+    b = C4Entity(id="b", name="B", c4_type="component", requirement_ids=["R3"])
+    merged = _merge_entities(a, b)
+    assert merged.c4_type == "container"  # canonical (more reqs) is a
+
+
+# ── Relationship Rewriting ──────────────────────────────────────────────────
+
+
+def test_rewrite_relationship_ids_source():
+    rels = [
+        C4Relationship(
+            id="rel-1", source_id="old_id", target_id="other",
+            description="uses", relationship_type="uses",
+        ),
+    ]
+    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
+    assert result[0].source_id == "new_id"
+    assert result[0].target_id == "other"
+
+
+def test_rewrite_relationship_ids_target():
+    rels = [
+        C4Relationship(
+            id="rel-1", source_id="other", target_id="old_id",
+            description="uses", relationship_type="uses",
+        ),
+    ]
+    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
+    assert result[0].source_id == "other"
+    assert result[0].target_id == "new_id"
+
+
+def test_rewrite_relationship_ids_both():
+    rels = [
+        C4Relationship(
+            id="rel-1", source_id="old_id", target_id="old_id",
+            description="self-ref", relationship_type="uses",
+        ),
+    ]
+    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
+    assert result[0].source_id == "new_id"
+    assert result[0].target_id == "new_id"
+
+
+def test_rewrite_relationship_ids_no_match():
+    rels = [
+        C4Relationship(
+            id="rel-1", source_id="a", target_id="b",
+            description="uses", relationship_type="uses",
+        ),
+    ]
+    result = _rewrite_relationship_ids(rels, "old_id", "new_id")
+    assert result[0].source_id == "a"
+    assert result[0].target_id == "b"
+
+
+def test_rewrite_relationship_ids_does_not_mutate_original():
+    rels = [
+        C4Relationship(
+            id="rel-1", source_id="old_id", target_id="other",
+        ),
+    ]
+    _rewrite_relationship_ids(rels, "old_id", "new_id")
+    assert rels[0].source_id == "old_id"  # unchanged
+
+
+# ── Boundary Group Creation ─────────────────────────────────────────────────
+
+
+def test_create_boundary_group():
+    bg = _create_boundary_group("entity_a", "entity_b", 0.7234)
+    assert bg["group_id"] == "bg_entity_a_entity_b"
+    assert bg["entity_ids"] == ["entity_a", "entity_b"]
+    assert bg["similarity"] == 0.7234
+    assert "rationale" in bg
+
+
+# ── Type Coercion ───────────────────────────────────────────────────────────
+
+
+def test_to_entity_from_dict():
+    d = {"id": "a", "name": "A", "description": "desc"}
+    result = _to_entity(d)
+    assert isinstance(result, C4Entity)
+    assert result.id == "a"
+
+
+def test_to_entity_from_c4entity():
+    e = C4Entity(id="a", name="A")
+    result = _to_entity(e)
+    assert result is e
+
+
+def test_to_entity_bad_type():
+    with pytest.raises(TypeError):
+        _to_entity("not an entity")
+
+
+def test_to_relationship_from_dict():
+    d = {"id": "r1", "source_id": "a", "target_id": "b"}
+    result = _to_relationship(d)
+    assert isinstance(result, C4Relationship)
+    assert result.id == "r1"
+
+
+def test_to_relationship_bad_type():
+    with pytest.raises(TypeError):
+        _to_relationship(42)
+
+
+# ── Deduplicate and Merge Fragment ──────────────────────────────────────────
+
+
+def _entity_dict(**overrides):
+    defaults = {
+        "id": "svc-1",
+        "name": "Service 1",
+        "description": "A backend service for user management",
+        "c4_type": "container",
+        "technology": "Python",
+        "requirement_ids": ["R1"],
+    }
+    defaults.update(overrides)
+    return defaults
+
+
+def _rel_dict(**overrides):
+    defaults = {
+        "id": "rel-1",
+        "source_id": "svc-1",
+        "target_id": "svc-2",
+        "description": "uses",
+        "relationship_type": "uses",
+    }
+    defaults.update(overrides)
+    return defaults
+
+
+class TestDeduplicateAndMergeFragment:
+    """Tests for deduplicate_and_merge_fragment function."""
+
+    def test_empty_fragment_empty_model(self):
+        """Empty fragment into empty model → empty model."""
+        model, questions, _ = deduplicate_and_merge_fragment(
+            {"entities": [], "relationships": []},
+            {},
+            None,
+            None,
+        )
+        assert model["entities"] == []
+        assert model["relationships"] == []
+        assert model["boundary_groups"] == []
+        assert questions == []
+
+    def test_new_entities_added_to_empty_model(self):
+        """First batch: all entities added without dedup."""
+        pf = {
+            "entities": [_entity_dict(id="svc-1"), _entity_dict(id="svc-2")],
+            "relationships": [_rel_dict()],
+        }
+        model, questions, _ = deduplicate_and_merge_fragment(pf, {}, None, None)
+
+        assert len(model["entities"]) == 2
+        assert len(model["relationships"]) == 1
+        assert questions == []
+
+    def test_exact_id_match_merges(self):
+        """Normalized ID match (no model needed)."""
+        pf = {
+            "entities": [_entity_dict(id="user-service", description="New desc",
+                                      technology="FastAPI", requirement_ids=["R1"])],
+            "relationships": [],
+        }
+        running = {
+            "entities": [_entity_dict(id="user_service", description="Old",
+                                      technology="Python", requirement_ids=["R2"])],
+            "relationships": [],
+        }
+
+        model, questions, _ = deduplicate_and_merge_fragment(pf, running, None, None)
+
+        assert len(model["entities"]) == 1
+        merged = model["entities"][0]
+        assert merged["description"] == "New desc"  # longer kept
+        assert "FastAPI" in merged["technology"]
+        assert "Python" in merged["technology"]
+        assert set(merged["requirement_ids"]) == {"R1", "R2"}
+
+    def test_exact_id_match_rewrites_relationships(self):
+        """When entity merged by ID, relationships are rewritten."""
+        pf = {
+            "entities": [_entity_dict(id="user-service")],
+            "relationships": [_rel_dict(source_id="user-service", target_id="payment")],
+        }
+        running = {
+            "entities": [_entity_dict(id="user_service")],
+            "relationships": [],
+        }
+
+        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)
+
+        assert len(model["relationships"]) == 1
+        assert model["relationships"][0]["source_id"] == model["entities"][0]["id"]
+
+    def test_no_model_fallback_adds_as_new(self):
+        """When cache=None, no similarity check — non-matching entities added as new."""
+        pf = {
+            "entities": [_entity_dict(id="svc-new")],
+            "relationships": [],
+        }
+        running = {
+            "entities": [_entity_dict(id="svc-existing")],
+            "relationships": [],
+        }
+
+        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)
+
+        assert len(model["entities"]) == 2
+
+    def test_preserves_existing_boundary_groups(self):
+        """Existing boundary_groups in running model are preserved."""
+        existing_bg = [{"group_id": "bg_old", "entity_ids": ["a", "b"], "similarity": 0.7}]
+        pf = {"entities": [_entity_dict()], "relationships": []}
+        running = {"entities": [], "relationships": [], "boundary_groups": existing_bg}
+
+        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)
+
+        assert len(model["boundary_groups"]) == 1
+        assert model["boundary_groups"][0]["group_id"] == "bg_old"
+
+    def test_returns_serialized_dicts(self):
+        """Output should contain plain dicts, not Pydantic models."""
+        pf = {"entities": [_entity_dict()], "relationships": [_rel_dict()]}
+        model, _, _ = deduplicate_and_merge_fragment(pf, {}, None, None)
+
+        assert isinstance(model["entities"][0], dict)
+        assert isinstance(model["relationships"][0], dict)
+
+    def test_no_id_match_no_model(self):
+        """Different IDs, no model → entities added separately."""
+        pf = {
+            "entities": [_entity_dict(id="svc-a")],
+            "relationships": [],
+        }
+        running = {
+            "entities": [_entity_dict(id="svc-b")],
+            "relationships": [],
+        }
+
+        model, _, _ = deduplicate_and_merge_fragment(pf, running, None, None)
+
+        assert len(model["entities"]) == 2
+        ids = {e["id"] for e in model["entities"]}
+        assert ids == {"svc-a", "svc-b"}
+
+    def test_union_technology_case_insensitive_dedup(self):
+        """Technology union should deduplicate case-insensitively."""
+        result = _union_technology("python, fastapi", "Python, FastAPI")
+        assert result == "FastAPI, Python"
+
+    def test_merge_hierarchy_mismatch_creates_open_question(self):
+        """Hierarchy mismatch during merge should create a change_risk open question."""
+        pf = {
+            "entities": [_entity_dict(id="user-service", parent_system_id="system-a")],
+            "relationships": [],
+        }
+        running = {
+            "entities": [_entity_dict(id="user_service", parent_system_id="system-b")],
+            "relationships": [],
+        }
+        model, questions, _ = deduplicate_and_merge_fragment(pf, running, None, None)
+        assert len(questions) == 1
+        assert questions[0]["question_type"] == "change_risk"
+        assert "mismatching C4 parent hierarchy" in questions[0]["description"]
+
+    # ── Merge Log (Story 2.5) ──────────────────────────────────────────
+
+    def test_returns_3_tuple_with_merge_log(self):
+        """deduplicate_and_merge_fragment returns 3-tuple: (model, questions, merge_log)."""
+        pf = {"entities": [_entity_dict()], "relationships": []}
+        result = deduplicate_and_merge_fragment(pf, {}, None, None)
+        assert len(result) == 3
+        model, questions, merge_log = result
+        assert isinstance(model, dict)
+        assert isinstance(questions, list)
+        assert isinstance(merge_log, list)
+
+    def test_merge_log_empty_when_no_merges(self):
+        pf = {"entities": [_entity_dict(id="svc-new")], "relationships": []}
+        running = {"entities": [_entity_dict(id="svc-existing")], "relationships": []}
+        _, _, merge_log = deduplicate_and_merge_fragment(pf, running, None, None)
+        assert merge_log == []
+
+    def test_merge_log_records_exact_id_merge(self):
+        pf = {
+            "entities": [_entity_dict(id="user-service")],
+            "relationships": [],
+        }
+        running = {
+            "entities": [_entity_dict(id="user_service")],
+            "relationships": [],
+        }
+        _, _, merge_log = deduplicate_and_merge_fragment(pf, running, None, None)
+        assert len(merge_log) == 1
+        entry = merge_log[0]
+        assert "merged_entity_id" in entry
+        assert "source_entity_ids" in entry
+        assert len(entry["source_entity_ids"]) == 2
+        assert entry["merge_type"] == "exact_id"
+
+    def test_merge_log_entry_structure(self):
+        pf = {
+            "entities": [_entity_dict(id="user-service")],
+            "relationships": [],
+        }
+        running = {
+            "entities": [_entity_dict(id="user_service")],
+            "relationships": [],
+        }
+        _, _, merge_log = deduplicate_and_merge_fragment(pf, running, None, None)
+        entry = merge_log[0]
+        assert isinstance(entry["merged_entity_id"], str)
+        assert isinstance(entry["source_entity_ids"], list)
+        assert all(isinstance(eid, str) for eid in entry["source_entity_ids"])
+        assert entry["merge_type"] in ("exact_id", "similarity")
diff --git a/raa/tests/raa/unit/test_judge_reconcile.py b/raa/tests/raa/unit/test_judge_reconcile.py
index b72c9cb..eac88bd 100644
--- a/raa/tests/raa/unit/test_judge_reconcile.py
+++ b/raa/tests/raa/unit/test_judge_reconcile.py
@@ -1,12 +1,12 @@
 """
-Unit tests for Judge reconciliation node (Story 2.3).
+Unit tests for Judge reconciliation node (Story 2.3 + 2.4).
 """
 from __future__ import annotations
 
 import pytest
 
 from raa.judge.reconcile import select_primary_fragment
-from raa.state.models import ArchFragment, SAAMScenario
+from raa.state.models import ArchFragment, C4Entity, C4Relationship, SAAMScenario
 
 
 def _make_fragment():
@@ -19,7 +19,37 @@ def _make_fragment():
     return ArchFragment(saam_scenarios=[scenario])
 
 
-def _make_state(batch_outputs=None, batch_cursor=0, quality_weights=None):
+def _make_fragment_with_entities():
+    """Create a fragment with entities for merge testing."""
+    scenario = SAAMScenario(
+        id="S1",
+        description="Test scenario",
+        quality_attributes=["Performance Efficiency"],
+        satisfaction="satisfied",
+    )
+    entity = C4Entity(
+        id="user_service",
+        name="User Service",
+        description="Handles user authentication and authorization",
+        c4_type="container",
+        technology="Python, FastAPI",
+        requirement_ids=["R1", "R2"],
+    )
+    relationship = C4Relationship(
+        id="rel-1",
+        source_id="user_service",
+        target_id="payment_service",
+        description="Uses",
+        relationship_type="uses",
+    )
+    return ArchFragment(
+        entities=[entity],
+        relationships=[relationship],
+        saam_scenarios=[scenario],
+    )
+
+
+def _make_state(batch_outputs=None, batch_cursor=0, quality_weights=None, arch_model=None):
     return {
         "batch_cursor": batch_cursor,
         "quality_weights": quality_weights or {"Performance Efficiency": 5},
@@ -34,6 +64,7 @@ def _make_state(batch_outputs=None, batch_cursor=0, quality_weights=None):
         "batch_outputs": batch_outputs or [],
         "open_questions": [],
         "incoherent_batches": [],
+        "arch_model": arch_model or {},
     }
 
 
@@ -96,25 +127,21 @@ def test_select_primary_fragment_filters_by_batch_cursor():
     assert rankings[1]["scored_fragments"][0].batch_index == 1
 
 
-def test_select_primary_fragment_returns_only_state_updates():
-    """Node must return only state updates, not the full state."""
+def test_select_primary_fragment_increments_batch_cursor():
+    """Story 2.4: Node must increment batch_cursor by 1."""
     frag = _make_fragment()
     records = [
         _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
     ]
-    state = _make_state(batch_outputs=records, batch_cursor=0)
+    state = _make_state(batch_outputs=records, batch_cursor=3)
 
     result = select_primary_fragment(state)
 
-    # Should be a partial update dict, not contain the full state keys
-    assert "judge_rankings" in result
-    assert "batch_cursor" not in result
-    assert "arch_model" not in result
-    assert "batch_outputs" not in result
+    assert result["batch_cursor"] == 4
 
 
-def test_select_primary_fragment_does_not_advance_batch_cursor():
-    """Node must not return batch_cursor in the update."""
+def test_select_primary_fragment_returns_arch_model():
+    """Story 2.4: Node must return arch_model in state update."""
     frag = _make_fragment()
     records = [
         _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
@@ -123,7 +150,9 @@ def test_select_primary_fragment_does_not_advance_batch_cursor():
 
     result = select_primary_fragment(state)
 
-    assert "batch_cursor" not in result
+    assert "arch_model" in result
+    assert "entities" in result["arch_model"]
+    assert "relationships" in result["arch_model"]
 
 
 def test_select_primary_fragment_empty_batch():
@@ -135,6 +164,9 @@ def test_select_primary_fragment_empty_batch():
     assert "judge_rankings" in result
     rankings = result["judge_rankings"]
     assert rankings[0]["primary_fragment"] is None
+    # Story 2.4: still advances cursor and returns arch_model
+    assert result["batch_cursor"] == 1
+    assert "arch_model" in result
 
 
 def test_select_primary_fragment_preserves_existing_rankings():
@@ -157,8 +189,10 @@ def test_select_primary_fragment_preserves_existing_rankings():
     state2 = _make_state(
         batch_outputs=records0 + records1,
         batch_cursor=1,
+        arch_model=intermediate.get("arch_model"),
     )
     state2["judge_rankings"] = intermediate["judge_rankings"]
+    state2["open_questions"] = []
 
     result = select_primary_fragment(state2)
 
@@ -167,3 +201,148 @@ def test_select_primary_fragment_preserves_existing_rankings():
     assert 1 in rankings  # new
     assert rankings[0]["primary_fragment"].strategy == "raa_a"
     assert rankings[1]["primary_fragment"].strategy == "raa_b"
+
+
+def test_select_primary_fragment_merges_entities():
+    """Story 2.4: Primary fragment entities should be merged into arch_model."""
+    frag = _make_fragment_with_entities()
+    records = [
+        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
+    ]
+    state = _make_state(batch_outputs=records, batch_cursor=0)
+
+    result = select_primary_fragment(state)
+
+    assert len(result["arch_model"]["entities"]) == 1
+    assert result["arch_model"]["entities"][0]["name"] == "User Service"
+    assert len(result["arch_model"]["relationships"]) == 1
+    assert "open_questions" in result
+
+
+# ── Story 2.5 Integration Tests ─────────────────────────────────────────────
+
+
+def test_reconcile_entities_carry_saam_score():
+    """Story 2.5: C4Entity objects in returned arch_model must carry saam_score."""
+    frag = _make_fragment_with_entities()
+    records = [
+        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
+    ]
+    state = _make_state(batch_outputs=records, batch_cursor=0)
+
+    result = select_primary_fragment(state)
+
+    for entity in result["arch_model"]["entities"]:
+        assert "saam_score" in entity
+        assert isinstance(entity["saam_score"], float)
+        assert 0.0 <= entity["saam_score"] <= 1.0
+
+
+def test_reconcile_calls_cross_cutting_promotion():
+    """Story 2.5: Cross-cutting candidates in fragment trigger promotion."""
+    entity = C4Entity(
+        id="auth_service",
+        name="Authentication Service",
+        description="Handles security and authentication",
+        c4_type="container",
+        technology="Python",
+        requirement_ids=["R1", "R2"],
+    )
+    frag = ArchFragment(
+        entities=[entity],
+        relationships=[],
+        cross_cutting_candidates=["security", "logging"],
+        saam_scenarios=[],
+    )
+    records = [
+        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
+    ]
+    state = _make_state(batch_outputs=records, batch_cursor=0)
+
+    result = select_primary_fragment(state)
+
+    entity_ids = {e["id"] for e in result["arch_model"]["entities"]}
+    assert "cc_security" in entity_ids
+    assert "cc_logging" in entity_ids
+
+
+def test_reconcile_no_cross_cutting_when_no_candidates():
+    """Story 2.5: No cross-cutting candidates → no promoted components."""
+    frag = _make_fragment_with_entities()
+    records = [
+        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
+    ]
+    state = _make_state(batch_outputs=records, batch_cursor=0)
+
+    result = select_primary_fragment(state)
+
+    entity_ids = {e["id"] for e in result["arch_model"]["entities"]}
+    assert not any(eid.startswith("cc_") for eid in entity_ids)
+
+
+def test_reconcile_passes_merge_log_to_calibration():
+    """Story 2.5: merge_log from dedup flows into calibration (scores reflect merge state)."""
+    entity = C4Entity(
+        id="auth_service",
+        name="Auth",
+        description="Authentication service",
+        c4_type="container",
+        requirement_ids=["R1"],
+    )
+    frag = ArchFragment(
+        entities=[entity],
+        relationships=[],
+        saam_scenarios=[],
+    )
+    records = [
+        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
+    ]
+    state = _make_state(batch_outputs=records, batch_cursor=0)
+
+    # Run first batch to add entity to arch_model
+    result1 = select_primary_fragment(state)
+    assert len(result1["arch_model"]["entities"]) == 1
+
+    # Run second batch with same entity (different ID casing → exact_id merge)
+    entity2 = C4Entity(
+        id="auth_service",  # same normalized ID
+        name="Auth v2",
+        description="Updated authentication service",
+        c4_type="container",
+        requirement_ids=["R2"],
+    )
+    frag2 = ArchFragment(
+        entities=[entity2],
+        relationships=[],
+        saam_scenarios=[],
+    )
+    records2 = [
+        _make_record(batch_id="batch-2", batch_index=1, strategy="raa_a",
+                     arch_fragment=frag2.model_dump()),
+    ]
+    state2 = _make_state(
+        batch_outputs=records2,
+        batch_cursor=1,
+        arch_model=result1["arch_model"],
+    )
+    state2["judge_rankings"] = result1.get("judge_rankings", {})
+    state2["open_questions"] = []
+
+    result2 = select_primary_fragment(state2)
+    # Entity merged → saam_score should be below base (dedup penalty applied)
+    merged = result2["arch_model"]["entities"][0]
+    from raa.utils.constants import SAAM_BASE_SCORE, SAAM_DEDUP_PENALTY
+    assert merged["saam_score"] < SAAM_BASE_SCORE
+
+
+def test_reconcile_boundary_groups_preserved():
+    """Story 2.5: boundary_groups in arch_model are preserved through calibration."""
+    frag = _make_fragment_with_entities()
+    records = [
+        _make_record(strategy="raa_a", arch_fragment=frag.model_dump()),
+    ]
+    state = _make_state(batch_outputs=records, batch_cursor=0)
+
+    result = select_primary_fragment(state)
+
+    assert "boundary_groups" in result["arch_model"]
diff --git a/raa/tests/raa/unit/test_judge_saam_calibration.py b/raa/tests/raa/unit/test_judge_saam_calibration.py
new file mode 100644
index 0000000..7c1e940
--- /dev/null
+++ b/raa/tests/raa/unit/test_judge_saam_calibration.py
@@ -0,0 +1,399 @@
+"""
+Unit tests for SAAM score calibration engine (Story 2.5).
+"""
+from __future__ import annotations
+
+import pytest
+
+from raa.judge.saam_calibration import calibrate_entity_saam_scores
+from raa.utils.constants import (
+    SAAM_BASE_SCORE,
+    SAAM_BOUNDARY_GROUP_PENALTY,
+    SAAM_DEDUP_PENALTY,
+    SAAM_PERFECT_SCORE,
+)
+
+
+# ── Helpers ─────────────────────────────────────────────────────────────────
+
+
+def _entity_dict(
+    id="entity-1",
+    name="Test",
+    description="Test",
+    c4_type="container",
+    requirement_ids=None,
+    metadata=None,
+):
+    return {
+        "id": id,
+        "name": name,
+        "description": description,
+        "c4_type": c4_type,
+        "technology": "",
+        "parent_system_id": None,
+        "parent_container_id": None,
+        "requirement_ids": requirement_ids or [],
+        "saam_score": 0.0,
+        "metadata": metadata or {},
+    }
+
+
+def _scenario(satisfaction="satisfied", requirement_ids=None):
+    return {
+        "id": "scenario-1",
+        "description": "Test scenario",
+        "quality_attributes": ["Performance Efficiency"],
+        "satisfaction": satisfaction,
+        "requirement_ids": requirement_ids or [],
+        "metadata": {},
+    }
+
+
+# ── Base Score ──────────────────────────────────────────────────────────────
+
+
+class TestBaseScore:
+    def test_base_score_applied_to_non_component_entity(self):
+        model = {"entities": [_entity_dict(c4_type="container")]}
+        result = calibrate_entity_saam_scores(model)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+    def test_base_score_applied_to_system_entity(self):
+        model = {"entities": [_entity_dict(c4_type="system")]}
+        result = calibrate_entity_saam_scores(model)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+    def test_base_score_applied_when_no_scenarios(self):
+        model = {"entities": [_entity_dict(c4_type="component", requirement_ids=["R1"])]}
+        result = calibrate_entity_saam_scores(model, saam_scenarios=[])
+        # No scenarios means not qualified for perfect → gets base score
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+
+# ── Perfect Score ───────────────────────────────────────────────────────────
+
+
+class TestPerfectScore:
+    def test_perfect_score_for_qualifying_component(self):
+        model = {
+            "entities": [
+                _entity_dict(
+                    id="comp-1",
+                    c4_type="component",
+                    requirement_ids=["R1", "R2"],
+                )
+            ]
+        }
+        scenarios = [
+            _scenario(satisfaction="satisfied", requirement_ids=["R1"]),
+            _scenario(satisfaction="satisfied", requirement_ids=["R2"]),
+        ]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        assert result["entities"][0]["saam_score"] == SAAM_PERFECT_SCORE
+
+    def test_not_perfect_when_requirements_shared_in_boundary_group(self):
+        """Entities in same boundary group with shared requirement IDs can't both be perfect."""
+        model = {
+            "entities": [
+                _entity_dict(
+                    id="comp-1",
+                    c4_type="component",
+                    requirement_ids=["R1", "R2"],
+                    metadata={"boundary_group_id": "bg-1"},
+                ),
+                _entity_dict(
+                    id="comp-2",
+                    c4_type="component",
+                    requirement_ids=["R2", "R3"],
+                    metadata={"boundary_group_id": "bg-1"},
+                ),
+            ]
+        }
+        scenarios = [
+            _scenario(satisfaction="satisfied", requirement_ids=["R1", "R2", "R3"]),
+        ]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        assert result["entities"][0]["saam_score"] != SAAM_PERFECT_SCORE
+        assert result["entities"][1]["saam_score"] != SAAM_PERFECT_SCORE
+
+    def test_not_perfect_when_scenario_unsatisfied(self):
+        model = {
+            "entities": [
+                _entity_dict(
+                    id="comp-1",
+                    c4_type="component",
+                    requirement_ids=["R1"],
+                )
+            ]
+        }
+        scenarios = [
+            _scenario(satisfaction="partial", requirement_ids=["R1"]),
+        ]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        assert result["entities"][0]["saam_score"] != SAAM_PERFECT_SCORE
+
+    def test_not_perfect_for_non_component(self):
+        model = {
+            "entities": [
+                _entity_dict(
+                    id="cont-1",
+                    c4_type="container",
+                    requirement_ids=["R1"],
+                )
+            ]
+        }
+        scenarios = [
+            _scenario(satisfaction="satisfied", requirement_ids=["R1"]),
+        ]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+    def test_not_perfect_when_no_requirement_ids(self):
+        model = {
+            "entities": [
+                _entity_dict(id="comp-1", c4_type="component", requirement_ids=[]),
+            ]
+        }
+        result = calibrate_entity_saam_scores(model)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+
+# ── Dedup Penalty ───────────────────────────────────────────────────────────
+
+
+class TestDedupPenalty:
+    def test_dedup_penalty_reduces_score(self):
+        model = {"entities": [_entity_dict(id="merged-1")]}
+        merge_log = [
+            {
+                "merged_entity_id": "merged-1",
+                "source_entity_ids": ["entity-a", "entity-b"],
+                "merge_type": "similarity",
+            }
+        ]
+        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
+        expected = SAAM_BASE_SCORE - SAAM_DEDUP_PENALTY
+        assert result["entities"][0]["saam_score"] == round(expected, 4)
+
+    def test_multiple_merges_stack_penalty(self):
+        model = {"entities": [_entity_dict(id="multi-merged")]}
+        merge_log = [
+            {
+                "merged_entity_id": "multi-merged",
+                "source_entity_ids": ["e1", "e2"],
+                "merge_type": "exact_id",
+            },
+            {
+                "merged_entity_id": "multi-merged",
+                "source_entity_ids": ["multi-merged", "e3"],
+                "merge_type": "similarity",
+            },
+        ]
+        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
+        expected = SAAM_BASE_SCORE - (SAAM_DEDUP_PENALTY * 2)
+        assert result["entities"][0]["saam_score"] == round(expected, 4)
+
+    def test_source_entity_ids_count_as_merge_event(self):
+        """Entity appearing in source_entity_ids also counts as merge participation."""
+        model = {"entities": [_entity_dict(id="source-e1")]}
+        merge_log = [
+            {
+                "merged_entity_id": "other",
+                "source_entity_ids": ["source-e1", "e2"],
+                "merge_type": "similarity",
+            }
+        ]
+        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
+        expected = SAAM_BASE_SCORE - SAAM_DEDUP_PENALTY
+        assert result["entities"][0]["saam_score"] == round(expected, 4)
+
+    def test_no_penalty_without_merge_log(self):
+        model = {"entities": [_entity_dict(id="clean")]}
+        result = calibrate_entity_saam_scores(model, merge_log=[])
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+
+# ── Boundary Group Penalty ──────────────────────────────────────────────────
+
+
+class TestBoundaryGroupPenalty:
+    def test_boundary_group_penalty_reduces_score(self):
+        model = {
+            "entities": [_entity_dict(id="bg-entity")],
+        }
+        boundary_groups = [
+            {"group_id": "bg-1", "entity_ids": ["bg-entity", "other"], "similarity": 0.7}
+        ]
+        result = calibrate_entity_saam_scores(model, boundary_groups=boundary_groups)
+        expected = SAAM_BASE_SCORE - SAAM_BOUNDARY_GROUP_PENALTY
+        assert result["entities"][0]["saam_score"] == round(expected, 4)
+
+    def test_no_penalty_for_non_member(self):
+        model = {
+            "entities": [_entity_dict(id="loner")],
+        }
+        boundary_groups = [
+            {"group_id": "bg-1", "entity_ids": ["other-1", "other-2"], "similarity": 0.7}
+        ]
+        result = calibrate_entity_saam_scores(model, boundary_groups=boundary_groups)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+    def test_uses_model_boundary_groups_by_default(self):
+        model = {
+            "entities": [_entity_dict(id="bg-entity")],
+            "boundary_groups": [
+                {"group_id": "bg-1", "entity_ids": ["bg-entity", "other"], "similarity": 0.7}
+            ],
+        }
+        result = calibrate_entity_saam_scores(model)
+        expected = SAAM_BASE_SCORE - SAAM_BOUNDARY_GROUP_PENALTY
+        assert result["entities"][0]["saam_score"] == round(expected, 4)
+
+
+# ── Combined Penalties ──────────────────────────────────────────────────────
+
+
+class TestCombinedPenalties:
+    def test_both_penalties_apply(self):
+        model = {
+            "entities": [_entity_dict(id="penalized")],
+        }
+        boundary_groups = [
+            {"group_id": "bg-1", "entity_ids": ["penalized", "other"], "similarity": 0.7}
+        ]
+        merge_log = [
+            {
+                "merged_entity_id": "penalized",
+                "source_entity_ids": ["penalized", "e1"],
+                "merge_type": "similarity",
+            }
+        ]
+        result = calibrate_entity_saam_scores(
+            model, boundary_groups=boundary_groups, merge_log=merge_log
+        )
+        expected = SAAM_BASE_SCORE - SAAM_DEDUP_PENALTY - SAAM_BOUNDARY_GROUP_PENALTY
+        assert result["entities"][0]["saam_score"] == round(expected, 4)
+
+
+# ── Score Clamping ──────────────────────────────────────────────────────────
+
+
+class TestScoreClamping:
+    def test_score_clamped_to_zero(self):
+        model = {"entities": [_entity_dict(id="overpenalized")]}
+        # Stack enough penalties to go below 0
+        merge_log = [
+            {"merged_entity_id": "overpenalized", "source_entity_ids": ["overpenalized", f"e{i}"], "merge_type": "similarity"}
+            for i in range(10)
+        ]
+        result = calibrate_entity_saam_scores(model, merge_log=merge_log)
+        assert result["entities"][0]["saam_score"] == 0.0
+
+    def test_score_clamped_to_one(self):
+        model = {
+            "entities": [
+                _entity_dict(id="comp", c4_type="component", requirement_ids=["R1"]),
+            ]
+        }
+        scenarios = [_scenario(satisfaction="satisfied", requirement_ids=["R1"])]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        assert result["entities"][0]["saam_score"] == SAAM_PERFECT_SCORE
+
+
+# ── Empty/Edge Cases ────────────────────────────────────────────────────────
+
+
+class TestEdgeCases:
+    def test_empty_model_returns_empty_model(self):
+        model = {"entities": []}
+        result = calibrate_entity_saam_scores(model)
+        assert result["entities"] == []
+
+    def test_all_defaults_handled(self):
+        """Call with no optional args should work."""
+        model = {"entities": [_entity_dict()]}
+        result = calibrate_entity_saam_scores(model)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+    def test_preserves_non_entity_keys(self):
+        model = {
+            "entities": [_entity_dict()],
+            "boundary_groups": [{"group_id": "bg-1", "entity_ids": ["a", "b"]}],
+            "cross_cutting_candidates": ["security"],
+        }
+        result = calibrate_entity_saam_scores(model)
+        assert "boundary_groups" in result
+        assert "cross_cutting_candidates" in result
+
+    def test_multiple_entities_scored(self):
+        model = {
+            "entities": [
+                _entity_dict(id="e1", c4_type="component", requirement_ids=["R1"]),
+                _entity_dict(id="e2", c4_type="container"),
+                _entity_dict(id="e3", c4_type="system"),
+            ]
+        }
+        scenarios = [_scenario(satisfaction="satisfied", requirement_ids=["R1"])]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        scores = {e["id"]: e["saam_score"] for e in result["entities"]}
+        assert scores["e1"] == SAAM_PERFECT_SCORE
+        assert scores["e2"] == SAAM_BASE_SCORE
+        assert scores["e3"] == SAAM_BASE_SCORE
+
+    def test_deterministic_same_input_same_output(self):
+        model = {
+            "entities": [
+                _entity_dict(id="e1", c4_type="component", requirement_ids=["R1"]),
+                _entity_dict(id="e2"),
+            ]
+        }
+        scenarios = [_scenario(satisfaction="satisfied", requirement_ids=["R1"])]
+        merge_log = [
+            {"merged_entity_id": "e2", "source_entity_ids": ["e2", "e_old"], "merge_type": "exact_id"}
+        ]
+        r1 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
+        r2 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
+        assert r1 == r2
+
+    def test_scenario_with_unknown_satisfaction_not_perfect(self):
+        model = {
+            "entities": [
+                _entity_dict(id="comp", c4_type="component", requirement_ids=["R1"]),
+            ]
+        }
+        scenarios = [_scenario(satisfaction="unknown", requirement_ids=["R1"])]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+    def test_scenario_with_unsatisfied_not_perfect(self):
+        model = {
+            "entities": [
+                _entity_dict(id="comp", c4_type="component", requirement_ids=["R1"]),
+            ]
+        }
+        scenarios = [_scenario(satisfaction="unsatisfied", requirement_ids=["R1"])]
+        result = calibrate_entity_saam_scores(model, saam_scenarios=scenarios)
+        assert result["entities"][0]["saam_score"] == SAAM_BASE_SCORE
+
+    def test_deterministic(self):
+        """Same input → same output (dedicated determinism test)."""
+        model = {
+            "entities": [
+                _entity_dict(id="e1", c4_type="component", requirement_ids=["R1"]),
+                _entity_dict(id="e2", c4_type="container", requirement_ids=["R2"]),
+            ],
+            "boundary_groups": [
+                {"group_id": "bg-1", "entity_ids": ["e1", "e2"], "similarity": 0.7}
+            ],
+        }
+        scenarios = [
+            _scenario(satisfaction="satisfied", requirement_ids=["R1"]),
+            _scenario(satisfaction="partial", requirement_ids=["R2"]),
+        ]
+        merge_log = [
+            {"merged_entity_id": "e1", "source_entity_ids": ["e1", "e_old"], "merge_type": "exact_id"}
+        ]
+        r1 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
+        r2 = calibrate_entity_saam_scores(model, saam_scenarios=scenarios, merge_log=merge_log)
+        assert r1 == r2

```

## Execution Instructions
Review the diff with extreme skepticism — assume problems exist. Find at least ten issues to fix or improve in the provided content.

## Output Format
Output findings as a Markdown list (descriptions only). No preamble, no postamble.
