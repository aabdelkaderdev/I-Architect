"""Final merge and output node — global deterministic merge, scoped reconciliation,
C4 schema validation, diagram manifest generation, and filesystem output
(RAA_Plan.md Section 16).

Reads best_batch_output, running_arch_model, open_questions, and
incoherent_batches from state. Runs the 4-step deterministic merge
algorithm globally, reconciles unresolved questions via llm_judge,
validates against C4 schema, generates the diagram manifest, and
writes arch_model.json to the orchestrator-provided output path.
"""

from __future__ import annotations

import copy
import json
import logging
from pathlib import Path
from typing import Any

from raa.state.types import (
    ArchComponent,
    ArchContainer,
    ArchExternalSystem,
    ArchFragment,
    ArchModel,
    ArchPerson,
    ArchRelationship,
    ArchSystem,
    ConfidenceRecord,
    DiagramManifestEntry,
    IncoherentBatchRecord,
    OpenQuestion,
)

logger = logging.getLogger(__name__)

LLM_JUDGE_KEY = "llm_judge"

# ---------------------------------------------------------------------------
# T016 — Context and LLM helpers
# ---------------------------------------------------------------------------


def _context_dict(config: dict | None) -> dict[str, Any]:
    """Extract runtime context dict from graph config without reading state."""
    if config is None:
        return {}
    return config.get("context", {})


def _require_llm_judge(context: dict[str, Any]) -> object:
    """Get llm_judge from context by key; raise if missing."""
    llm = context.get(LLM_JUDGE_KEY)
    if llm is None:
        raise RuntimeError(
            f"Required LLM context key '{LLM_JUDGE_KEY}' is missing. "
            f"Ensure the config dict includes config['context']['{LLM_JUDGE_KEY}'] "
            f"with a ChatModel instance."
        )
    return llm


def _invoke_llm(llm: object, prompt: str) -> object:
    """Invoke an LLM with a prompt string. Supports .invoke(prompt) interface."""
    return llm.invoke(prompt)


def _response_to_dict(raw_response: object) -> dict[str, Any]:
    """Convert an LLM response to a plain dict."""
    if isinstance(raw_response, dict):
        return raw_response
    if hasattr(raw_response, "content"):
        content = raw_response.content
        if isinstance(content, dict):
            return content
        if isinstance(content, str):
            return json.loads(content)
    if isinstance(raw_response, str):
        return json.loads(raw_response)
    raise TypeError(f"Cannot convert LLM response type {type(raw_response)} to dict")


# ---------------------------------------------------------------------------
# T017 — Global fragment collection
# ---------------------------------------------------------------------------


def _collect_global_fragments(
    best_batch_output: dict[int, ArchFragment],
    running_arch_model: ArchModel,
) -> list[ArchFragment]:
    """Collect fragments in sorted batch-index order.

    Includes the running model as a baseline fragment so its entities
    participate in deduplication.
    """
    fragments: list[ArchFragment] = []

    # Add running model as baseline
    baseline = ArchFragment()
    for s in running_arch_model.systems:
        baseline.systems.append(s)
        for c in s.containers:
            baseline.containers.append(c)
            for comp in c.components:
                baseline.components.append(comp)
    for p in running_arch_model.persons:
        baseline.persons.append(p)
    for e in running_arch_model.external_systems:
        baseline.external_systems.append(e)
    fragments.append(baseline)

    # Add batch outputs in index order
    for idx in sorted(best_batch_output.keys()):
        fragments.append(best_batch_output[idx])

    return fragments


# ---------------------------------------------------------------------------
# T018-T019 — Global deterministic merge
# ---------------------------------------------------------------------------


def _canonical_id(entity_id: str) -> str:
    """Normalize entity ID to canonical form for deduplication."""
    return entity_id.strip().lower()


def _rel_key(source_id: str, target_id: str, interaction_type: str) -> tuple[str, str, str]:
    """Build canonical relationship key for deduplication."""
    return (
        _canonical_id(source_id),
        _canonical_id(target_id),
        interaction_type.strip().lower(),
    )


def _global_merge_fragments(
    fragments: list[ArchFragment],
) -> tuple[ArchFragment, list[OpenQuestion]]:
    """Apply 4-step deterministic merge algorithm globally across all fragments.

    1. Entity deduplication per type (longest description wins)
    2. Relationship deduplication by (source, target, interaction_type)
    3. Coverage union and orphan prevention
    4. Tree assembly (nest systems -> containers -> components)
    """
    open_questions: list[OpenQuestion] = []
    merged = ArchFragment()

    # Indices for canonical ID dedup
    sys_by_id: dict[str, tuple[int, ArchSystem]] = {}
    cont_by_id: dict[str, tuple[int, ArchContainer]] = {}
    comp_by_id: dict[str, tuple[int, ArchComponent]] = {}
    person_by_id: dict[str, tuple[int, ArchPerson]] = {}
    ext_by_id: dict[str, tuple[int, ArchExternalSystem]] = {}

    # --- Step 1: Entity deduplication (per type) ---
    for frag_idx, fragment in enumerate(fragments):
        # Systems
        for entity in fragment.systems:
            cid = _canonical_id(entity.id)
            if cid in sys_by_id:
                _, existing = sys_by_id[cid]
                if len(entity.description) > len(existing.description):
                    existing.description = entity.description
            else:
                merged.systems.append(entity)
                sys_by_id[cid] = (frag_idx, entity)

        # Containers
        for entity in fragment.containers:
            cid = _canonical_id(entity.id)
            if cid in cont_by_id:
                _, existing = cont_by_id[cid]
                # Hierarchy conflict detection
                if entity.parent_system_id and existing.parent_system_id:
                    if _canonical_id(entity.parent_system_id) != _canonical_id(existing.parent_system_id):
                        open_questions.append(
                            OpenQuestion(
                                entity_id=entity.id,
                                type="hierarchy_conflict",
                                description=(
                                    f"Container '{entity.id}' has conflicting parent_system_id: "
                                    f"'{entity.parent_system_id}' vs "
                                    f"'{existing.parent_system_id}' (existing)"
                                ),
                            )
                        )
                if len(entity.description) > len(existing.description):
                    existing.description = entity.description
                if entity.technology and not existing.technology:
                    existing.technology = entity.technology
            else:
                merged.containers.append(entity)
                cont_by_id[cid] = (frag_idx, entity)

        # Components
        for entity in fragment.components:
            cid = _canonical_id(entity.id)
            if cid in comp_by_id:
                _, existing = comp_by_id[cid]
                if entity.parent_container_id and existing.parent_container_id:
                    if _canonical_id(entity.parent_container_id) != _canonical_id(existing.parent_container_id):
                        open_questions.append(
                            OpenQuestion(
                                entity_id=entity.id,
                                type="hierarchy_conflict",
                                description=(
                                    f"Component '{entity.id}' has conflicting parent_container_id: "
                                    f"'{entity.parent_container_id}' vs "
                                    f"'{existing.parent_container_id}' (existing)"
                                ),
                            )
                        )
                if len(entity.description) > len(existing.description):
                    existing.description = entity.description
                if entity.technology and not existing.technology:
                    existing.technology = entity.technology
            else:
                merged.components.append(entity)
                comp_by_id[cid] = (frag_idx, entity)

        # Persons
        for entity in fragment.persons:
            cid = _canonical_id(entity.id)
            if cid in person_by_id:
                _, existing = person_by_id[cid]
                if len(entity.description) > len(existing.description):
                    existing.description = entity.description
            else:
                merged.persons.append(entity)
                person_by_id[cid] = (frag_idx, entity)

        # External systems
        for entity in fragment.external_systems:
            cid = _canonical_id(entity.id)
            if cid in ext_by_id:
                _, existing = ext_by_id[cid]
                if len(entity.description) > len(existing.description):
                    existing.description = entity.description
                if entity.technology and not existing.technology:
                    existing.technology = entity.technology
            else:
                merged.external_systems.append(entity)
                ext_by_id[cid] = (frag_idx, entity)

    # --- Step 2: Relationship deduplication ---
    rel_index: dict[tuple, ArchRelationship] = {}
    for fragment in fragments:
        for rel in fragment.relationships:
            rk = _rel_key(rel.source_id, rel.target_id, rel.interaction_type)
            if rk in rel_index:
                existing = rel_index[rk]
                if len(rel.technology or "") > len(existing.technology or ""):
                    existing.technology = rel.technology
            else:
                merged.relationships.append(rel)
                rel_index[rk] = rel

    # --- Step 3: Orphan prevention ---
    # Build set of valid parent IDs
    system_ids = {_canonical_id(s.id) for s in merged.systems}
    container_ids = {_canonical_id(c.id) for c in merged.containers}

    # Check containers have valid system parents
    for c in merged.containers:
        if _canonical_id(c.parent_system_id) not in system_ids:
            open_questions.append(
                OpenQuestion(
                    entity_id=c.id,
                    type="coverage_gap",
                    description=(
                        f"Orphan container '{c.id}': parent_system_id "
                        f"'{c.parent_system_id}' not found in merged systems"
                    ),
                )
            )

    # Check components have valid container parents
    for comp in merged.components:
        if _canonical_id(comp.parent_container_id) not in container_ids:
            open_questions.append(
                OpenQuestion(
                    entity_id=comp.id,
                    type="coverage_gap",
                    description=(
                        f"Orphan component '{comp.id}': parent_container_id "
                        f"'{comp.parent_container_id}' not found in merged containers"
                    ),
                )
            )

    # --- Step 4: Tree assembly ---
    merged = _assemble_tree(merged)

    return merged, open_questions


def _assemble_tree(fragment: ArchFragment) -> ArchFragment:
    """Build nested C4 hierarchy from flat entity lists.

    Systems receive their containers. Containers receive their components.
    Relationships are distributed to the correct level by diagram_scope.
    """
    # Index systems by canonical ID
    sys_map: dict[str, ArchSystem] = {}
    for s in fragment.systems:
        s.containers = []
        s.context_relationships = []
        sys_map[_canonical_id(s.id)] = s

    # Index containers by canonical ID, attach to parent system
    cont_map: dict[str, ArchContainer] = {}
    for c in fragment.containers:
        c.components = []
        c.container_relationships = []
        cont_map[_canonical_id(c.id)] = c
        parent_cid = _canonical_id(c.parent_system_id)
        if parent_cid in sys_map:
            sys_map[parent_cid].containers.append(c)

    # Index components by canonical ID, attach to parent container
    comp_map: dict[str, ArchComponent] = {}
    for comp in fragment.components:
        comp.component_relationships = []
        comp_map[_canonical_id(comp.id)] = comp
        parent_cid = _canonical_id(comp.parent_container_id)
        if parent_cid in cont_map:
            cont_map[parent_cid].components.append(comp)

    # Build full type index for relationship routing
    type_index: dict[str, str] = {}
    for s in fragment.systems:
        type_index[_canonical_id(s.id)] = "system"
    for c in fragment.containers:
        type_index[_canonical_id(c.id)] = "container"
    for comp in fragment.components:
        type_index[_canonical_id(comp.id)] = "component"
    for p in fragment.persons:
        type_index[_canonical_id(p.id)] = "person"
    for e in fragment.external_systems:
        type_index[_canonical_id(e.id)] = "external_system"

    # Distribute relationships to correct level
    for rel in fragment.relationships:
        scope = rel.diagram_scope
        if scope == "context":
            src_cid = _canonical_id(rel.source_id)
            if src_cid in sys_map:
                sys_map[src_cid].context_relationships.append(rel)
            else:
                tgt_cid = _canonical_id(rel.target_id)
                if tgt_cid in sys_map:
                    sys_map[tgt_cid].context_relationships.append(rel)
        elif scope == "container":
            src_cid = _canonical_id(rel.source_id)
            if src_cid in cont_map:
                cont_map[src_cid].container_relationships.append(rel)
        elif scope == "component":
            src_cid = _canonical_id(rel.source_id)
            if src_cid in comp_map:
                comp_map[src_cid].component_relationships.append(rel)

    return fragment


# ---------------------------------------------------------------------------
# T020 — Confidence metadata
# ---------------------------------------------------------------------------


def _build_confidence_metadata(
    model: ArchModel,
    best_batch_output: dict[int, ArchFragment],
    incoherent_batches: list[IncoherentBatchRecord],
) -> dict[str, ConfidenceRecord]:
    """Build per-entity confidence metadata keyed by entity ID.

    Entities from incoherent batches get reduced_confidence=True
    and their source batch recorded.
    """
    # Build set of batch indices with reduced confidence
    reduced_batches: set[int] = set()
    for record in incoherent_batches:
        if record.reduced_confidence:
            reduced_batches.add(record.batch_id)

    # Map canonical entity ID to source batch ID
    entity_to_batch: dict[str, int] = {}
    for batch_id, fragment in best_batch_output.items():
        for system in fragment.systems:
            entity_to_batch[_canonical_id(system.id)] = batch_id
            for container in system.containers:
                entity_to_batch[_canonical_id(container.id)] = batch_id
                for component in container.components:
                    entity_to_batch[_canonical_id(component.id)] = batch_id
        for person in fragment.persons:
            entity_to_batch[_canonical_id(person.id)] = batch_id
        for ext in fragment.external_systems:
            entity_to_batch[_canonical_id(ext.id)] = batch_id

    metadata: dict[str, ConfidenceRecord] = {}

    # Walk all entities in the model and check their source batch
    for system in model.systems:
        _record_confidence(system.id, system.confidence, reduced_batches, entity_to_batch, metadata)

    for container in _all_containers(model):
        _record_confidence(container.id, container.confidence, reduced_batches, entity_to_batch, metadata)

    for component in _all_components(model):
        _record_confidence(component.id, component.confidence, reduced_batches, entity_to_batch, metadata)

    for person in model.persons:
        _record_confidence(person.id, person.confidence, reduced_batches, entity_to_batch, metadata)

    for ext in model.external_systems:
        _record_confidence(ext.id, ext.confidence, reduced_batches, entity_to_batch, metadata)

    return metadata


def _record_confidence(
    entity_id: str,
    confidence: float | None,
    reduced_batches: set[int],
    entity_to_batch: dict[str, int],
    metadata: dict[str, ConfidenceRecord],
) -> None:
    """Record confidence metadata for a single entity."""
    cid = _canonical_id(entity_id)
    source_batch = entity_to_batch.get(cid, -1)
    reduced = (confidence is not None and confidence < 0.5) or (source_batch in reduced_batches)
    metadata[cid] = ConfidenceRecord(
        reduced_confidence=reduced,
        source_batch=source_batch,
        saam_score=confidence if confidence is not None else 1.0,
    )


def _all_containers(model: ArchModel):
    """Yield all containers from all systems in the model."""
    for s in model.systems:
        yield from s.containers


def _all_components(model: ArchModel):
    """Yield all components from all containers in the model."""
    for c in _all_containers(model):
        yield from c.components


# ---------------------------------------------------------------------------
# T021 — Reconciliation prompt
# ---------------------------------------------------------------------------


def _build_reconciliation_prompt(
    open_questions: list[OpenQuestion],
    merged_model: ArchModel,
) -> str:
    """Build a tightly scoped reconciliation prompt forbidding full re-analysis.

    The prompt lists only the unresolved open_questions and a compact
    summary of the merged model structure, instructing llm_judge to
    resolve only the listed questions.
    """
    parts: list[str] = []

    parts.append(
        "You are an architecture reconciliation specialist. "
        "Below is a compact summary of a merged C4 architecture model "
        "and a list of unresolved conflicts or gaps. "
        "Resolve ONLY the listed questions. Do NOT perform a full re-analysis "
        "or suggest changes beyond the listed items.\n"
    )

    # Compact model summary
    parts.append("## Merged Model Summary")
    parts.append(f"Systems: {len(merged_model.systems)}")
    for s in merged_model.systems:
        parts.append(f"  - {s.id} ({s.label}): {len(s.containers)} containers")
        for c in s.containers:
            parts.append(f"    - {c.id} ({c.label}): {len(c.components)} components")
    parts.append(f"Persons: {len(merged_model.persons)}")
    for p in merged_model.persons:
        parts.append(f"  - {p.id} ({p.label})")
    parts.append(f"External Systems: {len(merged_model.external_systems)}")
    for e in merged_model.external_systems:
        parts.append(f"  - {e.id} ({e.label})")
    parts.append("")

    # Open questions
    parts.append("## Unresolved Questions")
    for i, oq in enumerate(open_questions):
        parts.append(
            f"{i}: [{oq.type}] entity={oq.entity_id} — {oq.description}"
        )
    parts.append("")

    # Output format
    parts.append(
        "## Required Output Format\n"
        "Return a JSON object with a 'resolutions' array. Each resolution must contain:\n"
        "- question_index: int (the index of the question being resolved)\n"
        "- resolution_type: str (one of: 'select_parent', 'assign_scope', 'merge_entities', 'keep_unresolved')\n"
        "- resolved_value: object (the resolved value, e.g. parent_id for select_parent, scope for assign_scope)\n"
        "- rationale: str (brief explanation of the resolution)\n"
    )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# T022-T023 — Reconciliation application and failure handling
# ---------------------------------------------------------------------------


def _apply_reconciliation_response(
    merged_model: ArchModel,
    open_questions: list[OpenQuestion],
    response: dict[str, Any],
) -> tuple[ArchModel, list[OpenQuestion]]:
    """Apply structured reconciliation operations to the merged model.

    Only accepts structured, validated operations that resolve listed
    OpenQuestion items. Returns updated (model, remaining_questions).
    """
    resolutions = response.get("resolutions", [])
    resolved_indices: set[int] = set()
    remaining: list[OpenQuestion] = []

    for i, oq in enumerate(open_questions):
        resolved = False
        for res in resolutions:
            qi = res.get("question_index", -1)
            if qi != i:
                continue

            rtype = res.get("resolution_type", "")
            value = res.get("resolved_value")

            if rtype == "select_parent" and oq.type == "hierarchy_conflict":
                _apply_parent_resolution(merged_model, oq, value)
                resolved_indices.add(i)
                resolved = True
            elif rtype == "assign_scope" and oq.type == "scope_conflict":
                _apply_scope_resolution(merged_model, oq, value)
                resolved_indices.add(i)
                resolved = True
            elif rtype == "keep_unresolved":
                # Explicitly keep — stays in remaining
                pass
            break

        if not resolved:
            remaining.append(oq)

    return merged_model, remaining


def _apply_parent_resolution(
    model: ArchModel,
    question: OpenQuestion,
    parent_id: object,
) -> None:
    """Apply a parent ID resolution to the appropriate entity."""
    if question.entity_id is None or parent_id is None:
        return
    eid = _canonical_id(question.entity_id)
    pid = _canonical_id(str(parent_id))

    # Check containers
    for s in model.systems:
        for c in s.containers:
            if _canonical_id(c.id) == eid:
                c.parent_system_id = pid
                return

    # Check components
    for s in model.systems:
        for c in s.containers:
            for comp in c.components:
                if _canonical_id(comp.id) == eid:
                    comp.parent_container_id = pid
                    return


def _apply_scope_resolution(
    model: ArchModel,
    question: OpenQuestion,
    scope: object,
) -> None:
    """Apply a diagram_scope resolution to the relationship."""
    if question.entity_id is None or scope is None:
        return
    # entity_id for scope conflicts is "source->target"
    parts = question.entity_id.split("->")
    if len(parts) != 2:
        return
    source_id = _canonical_id(parts[0])
    target_id = _canonical_id(parts[1])
    new_scope = str(scope)

    for s in model.systems:
        for r in s.context_relationships:
            if _canonical_id(r.source_id) == source_id and _canonical_id(r.target_id) == target_id:
                r.diagram_scope = new_scope
                return
        for c in s.containers:
            for r in c.container_relationships:
                if _canonical_id(r.source_id) == source_id and _canonical_id(r.target_id) == target_id:
                    r.diagram_scope = new_scope
                    return
            for comp in c.components:
                for r in comp.component_relationships:
                    if _canonical_id(r.source_id) == source_id and _canonical_id(r.target_id) == target_id:
                        r.diagram_scope = new_scope
                        return


# ---------------------------------------------------------------------------
# T033 — C4 entity indexing
# ---------------------------------------------------------------------------


def _index_c4_entities(model: ArchModel) -> dict[str, str]:
    """Traverse nested systems, containers, components, persons, external systems.

    Returns: {canonical_entity_id: entity_type} for all entities.
    """
    index: dict[str, str] = {}

    for s in model.systems:
        sid = _canonical_id(s.id)
        index[sid] = "system"
        for c in s.containers:
            cid = _canonical_id(c.id)
            index[cid] = "container"
            for comp in c.components:
                comp_id = _canonical_id(comp.id)
                index[comp_id] = "component"

    for p in model.persons:
        index[_canonical_id(p.id)] = "person"

    for e in model.external_systems:
        index[_canonical_id(e.id)] = "external_system"

    return index


# ---------------------------------------------------------------------------
# T034 — Relationship collection from model hierarchy
# ---------------------------------------------------------------------------


def _collect_model_relationships(model: ArchModel) -> list[ArchRelationship]:
    """Gather all relationships from the nested hierarchy."""
    rels: list[ArchRelationship] = []

    for s in model.systems:
        rels.extend(s.context_relationships)
        for c in s.containers:
            rels.extend(c.container_relationships)
            for comp in c.components:
                rels.extend(comp.component_relationships)

    return rels


# ---------------------------------------------------------------------------
# T035-T036 — C4 schema validation
# ---------------------------------------------------------------------------


def _expected_relationship_scope(source_type: str, target_type: str) -> str:
    """Determine correct diagram_scope from two entity type names.

    Section 12 rules:
    - context: system/person/external_system ↔ system/person/external_system
    - container: at least one endpoint is container
    - component: at least one endpoint is component
    """
    types = {source_type, target_type}

    # If any endpoint is a component, scope is component
    if "component" in types:
        return "component"
    # If any endpoint is a container, scope is container
    if "container" in types:
        return "container"
    # Default: context (system, person, external_system)
    return "context"


def validate_c4_model(model: ArchModel) -> list[str]:
    """Validate the merged model against C4 structural criteria.

    Returns a list of validation error messages. Empty list = valid.
    """
    errors: list[str] = []

    # 1. Index all entities with duplicate ID detection
    entity_index: dict[str, str] = {}
    for s in model.systems:
        sid = _canonical_id(s.id)
        if sid in entity_index:
            errors.append(f"Duplicate entity ID '{s.id}' used as both system and {entity_index[sid]}")
        else:
            entity_index[sid] = "system"
        for c in s.containers:
            cid = _canonical_id(c.id)
            if cid in entity_index:
                errors.append(f"Duplicate entity ID '{c.id}' used as both container and {entity_index[cid]}")
            else:
                entity_index[cid] = "container"
            for comp in c.components:
                comp_id = _canonical_id(comp.id)
                if comp_id in entity_index:
                    errors.append(f"Duplicate entity ID '{comp.id}' used as both component and {entity_index[comp_id]}")
                else:
                    entity_index[comp_id] = "component"

    for p in model.persons:
        pid = _canonical_id(p.id)
        if pid in entity_index:
            errors.append(f"Duplicate entity ID '{p.id}' used as both person and {entity_index[pid]}")
        else:
            entity_index[pid] = "person"

    for e in model.external_systems:
        eid = _canonical_id(e.id)
        if eid in entity_index:
            errors.append(f"Duplicate entity ID '{e.id}' used as both external_system and {entity_index[eid]}")
        else:
            entity_index[eid] = "external_system"

    # 2. Check hierarchy: containers have valid system parents
    system_ids = {_canonical_id(s.id) for s in model.systems}
    for s in model.systems:
        for c in s.containers:
            cid = _canonical_id(c.id)
            pcid = _canonical_id(c.parent_system_id)
            if pcid != _canonical_id(s.id):
                errors.append(
                    f"Container '{c.id}' parent_system_id '{c.parent_system_id}' "
                    f"does not match owning system '{s.id}'"
                )
            if pcid not in system_ids:
                errors.append(
                    f"Orphan container '{c.id}': parent_system_id "
                    f"'{c.parent_system_id}' not found in systems"
                )

            # 4. Check components have valid container parents
            container_ids_in_sys = {_canonical_id(cc.id) for cc in s.containers}
            for comp in c.components:
                comp_id = _canonical_id(comp.id)
                pcid = _canonical_id(comp.parent_container_id)
                if pcid != cid:
                    errors.append(
                        f"Component '{comp.id}' parent_container_id "
                        f"'{comp.parent_container_id}' does not match owning container '{c.id}'"
                    )
                if pcid not in container_ids_in_sys and pcid != cid:
                    errors.append(
                        f"Orphan component '{comp.id}': parent_container_id "
                        f"'{comp.parent_container_id}' not found in containers"
                    )

    # 5. Check no duplicate IDs across entity types
    # Already enforced — index keys are canonical IDs per type

    # 6. Check all relationship endpoints exist
    all_relationships = _collect_model_relationships(model)
    for rel in all_relationships:
        src_cid = _canonical_id(rel.source_id)
        tgt_cid = _canonical_id(rel.target_id)
        if src_cid not in entity_index:
            errors.append(
                f"Relationship source '{rel.source_id}' not found in model entities"
            )
        if tgt_cid not in entity_index:
            errors.append(
                f"Relationship target '{rel.target_id}' not found in model entities"
            )

        # 7. Check diagram_scope matches endpoint types
        if src_cid in entity_index and tgt_cid in entity_index:
            src_type = entity_index[src_cid]
            tgt_type = entity_index[tgt_cid]
            expected = _expected_relationship_scope(src_type, tgt_type)
            if rel.diagram_scope != expected:
                errors.append(
                    f"Relationship {rel.source_id}->{rel.target_id} "
                    f"[{rel.interaction_type}] has diagram_scope "
                    f"'{rel.diagram_scope}' but expected '{expected}' "
                    f"based on endpoint types ({src_type}, {tgt_type})"
                )

    return errors


# ---------------------------------------------------------------------------
# T037 — Diagram manifest generation
# ---------------------------------------------------------------------------


def generate_diagram_manifest(model: ArchModel) -> list[DiagramManifestEntry]:
    """Generate deterministic diagram manifest work queue for AGA.

    One ctx-{system_id} and cnt-{system_id} per system, plus one
    cmp-{container_id} per container.
    """
    manifest: list[DiagramManifestEntry] = []

    for system in model.systems:
        manifest.append(
            DiagramManifestEntry(
                diagram_id=f"ctx-{system.id}",
                diagram_type="context",
                focus_entity_id=system.id,
                label=f"System Context — {system.label}",
            )
        )
        manifest.append(
            DiagramManifestEntry(
                diagram_id=f"cnt-{system.id}",
                diagram_type="container",
                focus_entity_id=system.id,
                label=f"System Container — {system.label}",
            )
        )
        for container in system.containers:
            manifest.append(
                DiagramManifestEntry(
                    diagram_id=f"cmp-{container.id}",
                    diagram_type="component",
                    focus_entity_id=container.id,
                    label=f"Component Diagram — {container.label}",
                )
            )

    return manifest


# ---------------------------------------------------------------------------
# T038 — Handoff JSON construction
# ---------------------------------------------------------------------------


def _build_c4_handoff_dict(model: ArchModel) -> dict[str, Any]:
    """Serialize the final C4 JSON fields exactly as the Section 16 output schema requires.

    Uses dataclass_to_dict from serialization.py for consistent output.
    """
    from raa.state.serialization import dataclass_to_dict

    return {
        "systems": dataclass_to_dict(model.systems),
        "persons": dataclass_to_dict(model.persons),
        "external_systems": dataclass_to_dict(model.external_systems),
        "patterns": dataclass_to_dict(model.patterns),
        "diagram_manifest": dataclass_to_dict(model.diagram_manifest),
        "confidence_metadata": {
            k: dataclass_to_dict(v)
            for k, v in model.confidence_metadata.items()
        },
        "open_questions": dataclass_to_dict(model.open_questions),
    }


# ---------------------------------------------------------------------------
# T045 — Output directory resolution
# ---------------------------------------------------------------------------


def _require_output_dir(context: dict[str, Any]) -> Path:
    """Read the orchestrator-provided output directory from runtime context.

    Does not fall back to hardcoded paths.
    """
    output_dir = context.get("output_dir")
    if output_dir is None:
        raise RuntimeError(
            "Required config key 'output_dir' is missing from context. "
            "The orchestrator must provide config['context']['output_dir']."
        )
    return Path(output_dir)


# ---------------------------------------------------------------------------
# T046 — File writing
# ---------------------------------------------------------------------------


def _write_arch_model_json(output_dir: Path, handoff_dict: dict[str, Any]) -> None:
    """Write arch_model.json with deterministic key ordering and indentation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "arch_model.json"
    output_path.write_text(json.dumps(handoff_dict, indent=2, sort_keys=True), encoding="utf-8")
    logger.info("Wrote arch_model.json to %s", output_path)


def _validate_batch_completeness(
    batch_queue: list[dict],
    best_batch_output: dict[int, ArchFragment],
) -> set[int]:
    """Validate completeness of batch outputs."""
    expected_indices = set(range(len(batch_queue)))
    actual_indices = set(best_batch_output.keys())
    missing_indices = expected_indices - actual_indices

    # Also iterate best_batch_output values to detect None or empty fragments
    for idx in actual_indices:
        frag = best_batch_output[idx]
        if frag is None:
            missing_indices.add(idx)
        elif (not frag.systems and
              not frag.persons and
              not frag.external_systems and
              not frag.patterns and
              not frag.relationships and
              not frag.components):
            # empty fragment
            missing_indices.add(idx)

    return missing_indices


# ---------------------------------------------------------------------------
# T024 + T039 + T047 — Main orchestration
# ---------------------------------------------------------------------------


def final_merge(state: dict[str, Any], config: dict | None = None) -> dict[str, Any]:
    """Execute final global merge, reconciliation, validation, and output.

    Args:
        state: RAAState dict with best_batch_output, running_arch_model,
               open_questions, incoherent_batches.
        config: LangGraph config dict with config['context']['llm_judge']
                and config['context']['output_dir'].

    Returns:
        State update dict with running_arch_model, diagram_manifest,
        confidence_metadata, and open_questions. Never includes LLM
        objects or filesystem-only artifacts.
    """
    # 1. Extract context and llm_judge from config (never from state)
    ctx = _context_dict(config)

    # 2. Read state channels
    best_batch_output: dict[int, ArchFragment] = state.get("best_batch_output", {})
    running_arch_model: ArchModel = state.get("running_arch_model", ArchModel())
    if isinstance(running_arch_model, dict):
        running_arch_model = ArchModel()
    existing_open_questions: list[OpenQuestion] = list(
        state.get("open_questions", [])
    )
    incoherent_batches: list[IncoherentBatchRecord] = list(
        state.get("incoherent_batches", [])
    )
    batch_queue: list[dict] = state.get("batch_queue", [])

    # 2b. Desync Check
    missing_indices = _validate_batch_completeness(batch_queue, best_batch_output)
    if missing_indices:
        rollback_cursor = min(missing_indices)
        logger.warning(
            "Desync detected: missing batch outputs for indices %s. Rolling back batch_cursor to %d for targeted re-run.",
            sorted(missing_indices),
            rollback_cursor,
        )
        return {"batch_cursor": rollback_cursor}

    # 3. Global merge — deterministic, no LLM
    fragments = _collect_global_fragments(best_batch_output, running_arch_model)
    merged_fragment, merge_questions = _global_merge_fragments(fragments)

    # Combine merge questions with existing open questions
    all_questions = existing_open_questions + merge_questions

    # 4. Build initial merged model from fragment tree
    merged_model = ArchModel(
        systems=list(merged_fragment.systems),
        persons=list(merged_fragment.persons),
        external_systems=list(merged_fragment.external_systems),
        patterns=list(merged_fragment.patterns),
    )

    # 5. Scoped LLM reconciliation (only if open_questions remain)
    llm_judge = _require_llm_judge(ctx)
    if all_questions:
        try:
            pre_reconcile_model = copy.deepcopy(merged_model)
            pre_errors = validate_c4_model(pre_reconcile_model)

            prompt = _build_reconciliation_prompt(all_questions, merged_model)
            raw = _invoke_llm(llm_judge, prompt)
            data = _response_to_dict(raw)
            reconciled_model, unresolved = _apply_reconciliation_response(
                merged_model, all_questions, data
            )

            # Validate reconciled model against C4 schema
            post_errors = validate_c4_model(reconciled_model)
            if len(post_errors) > len(pre_errors):
                logger.warning(
                    "Reconciliation introduced new C4 violations; reverting to pre-reconciliation model."
                )
                merged_model = pre_reconcile_model
                unresolved = all_questions
            else:
                merged_model = reconciled_model
        except Exception as exc:
            logger.warning(
                "Reconciliation failed: %s. Preserving unresolved open_questions.",
                exc,
            )
            unresolved = all_questions
    else:
        unresolved = all_questions

    # 6. Build confidence metadata
    confidence_metadata = _build_confidence_metadata(
        merged_model, best_batch_output, incoherent_batches
    )

    # 7. Generate diagram manifest
    manifest = generate_diagram_manifest(merged_model)

    # 8. C4 validation
    validation_errors = validate_c4_model(merged_model)
    if validation_errors:
        error_msg = "C4 validation failed:\n" + "\n".join(
            f"  - {e}" for e in validation_errors
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # 9. Attach manifest and confidence to model
    merged_model.diagram_manifest = manifest
    merged_model.confidence_metadata = confidence_metadata
    merged_model.open_questions = unresolved

    # 10. Filesystem output (only after validation passes)
    output_dir = _require_output_dir(ctx)
    handoff_dict = _build_c4_handoff_dict(merged_model)
    _write_arch_model_json(output_dir, handoff_dict)

    # 11. Build state update — must NOT include any LLM object.
    # diagram_manifest and confidence_metadata are embedded in running_arch_model.
    return {
        "running_arch_model": merged_model,
        "open_questions": unresolved,
    }
