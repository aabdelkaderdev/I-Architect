"""Per-batch judge node — SAAM scoring, deterministic merge, and
running_arch_model update (RAA_Plan.md Section 13).

Reads batch_outputs[batch_cursor], scores fragments via llm_judge from
runtime context, runs the 4-step deterministic merge algorithm, and
updates best_batch_output, running_arch_model, open_questions, and
batch_cursor.
"""

from __future__ import annotations

import json
from typing import Any

from typing_extensions import TypedDict

from raa.state.types import (
    ArchComponent,
    ArchContainer,
    ArchExternalSystem,
    ArchFragment,
    ArchModel,
    ArchPerson,
    ArchRelationship,
    ArchSystem,
    OpenQuestion,
)

# ---- Constants ---------------------------------------------------------------

LLM_JUDGE_KEY = "llm_judge"

_FRAGMENT_TIE_ORDER: dict[str, int] = {
    "raa_a": 0,
    "raa_b": 1,
    "raa_c": 2,
}

# C4 entity type names for scope resolution
_CONTEXT_TYPES = frozenset({"system", "person", "external_system"})
_CONTAINER_TYPES = frozenset({"container"})
_COMPONENT_TYPES = frozenset({"component"})

_SCOPE_TABLE: dict[str, frozenset[str]] = {
    "context": _CONTEXT_TYPES,
    "container": _CONTAINER_TYPES,
    "component": _COMPONENT_TYPES,
}

# ---- Internal score structure ------------------------------------------------


class JudgeScore(TypedDict, total=False):
    """Per-fragment SAAM score metadata produced during scoring phase."""

    source_fragment: str
    base_score: float
    weighted_score: float
    covered_entity_ids: list[str]
    covered_relationship_keys: list[str]
    reduced_confidence: bool


# =============================================================================
# T020 — Context and LLM helpers
# =============================================================================


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


# =============================================================================
# T021 — SAAM scoring prompt and response parsing
# =============================================================================


def _fragment_summary(fragment: ArchFragment, name: str) -> str:
    """Build a compact text summary of fragment contents for the SAAM prompt."""
    lines = [f"Fragment {name}:"]
    for s in fragment.systems:
        lines.append(f"  System: {s.id} ({s.label}) — {s.description}")
    for c in fragment.containers:
        lines.append(f"  Container: {c.id} ({c.label}) parent={c.parent_system_id} — {c.description}")
    for comp in fragment.components:
        lines.append(f"  Component: {comp.id} ({comp.label}) parent={comp.parent_container_id} — {comp.description}")
    for p in fragment.persons:
        lines.append(f"  Person: {p.id} ({p.label})")
    for e in fragment.external_systems:
        lines.append(f"  ExternalSystem: {e.id} ({e.label})")
    for r in fragment.relationships:
        lines.append(f"  Relationship: {r.source_id} -> {r.target_id} [{r.interaction_type}] scope={r.diagram_scope}")
    return "\n".join(lines)


def _build_saam_prompt(
    batch: dict,
    quality_weights: dict[str, int],
    fragments: list[ArchFragment],
    fragment_names: list[str],
) -> str:
    """Assemble the SAAM scoring prompt with batch context and fragment summaries."""
    parts: list[str] = []

    parts.append("You are a SAAM (Scenario-Based Architecture Analysis Method) evaluator.\n")

    # Batch requirements
    requirements = batch.get("requirements", [])
    req_text = "\n".join(
        f"- {r.get('id', '?')}: {r.get('text', r.get('content', ''))}"
        for r in requirements
    )
    parts.append(f"## Requirements\n{req_text}\n")

    # Quality weights
    if quality_weights:
        parts.append(f"## Quality Weights\n{json.dumps(quality_weights)}\n")

    # Fragment summaries
    parts.append("## Candidate Fragments\n")
    for frag, name in zip(fragments, fragment_names):
        parts.append(_fragment_summary(frag, name))
        parts.append("")

    # Output format instruction
    parts.append(
        "## Required Output Format\n"
        "Return a JSON object with a 'scores' array. Each score entry must contain:\n"
        "- source_fragment: str (fragment name)\n"
        "- base_score: float (0-10 SAAM score)\n"
        "- covered_entity_ids: list[str] (entity IDs this fragment covers well)\n"
        "- covered_relationship_keys: list[str] (relationship keys in 'source->target:type' format)\n"
    )

    return "\n".join(parts)


def _parse_saam_response(
    data: dict,
    fragment_names: list[str],
    reduced_confidence: bool,
) -> list[JudgeScore]:
    """Parse SAAM scores from LLM response and apply confidence weighting."""
    raw_scores: list[dict] = data.get("scores", [])

    scores: list[JudgeScore] = []
    for entry in raw_scores:
        base = float(entry.get("base_score", 0))
        weighted = base * 0.5 if reduced_confidence else base
        scores.append(
            JudgeScore(
                source_fragment=entry.get("source_fragment", ""),
                base_score=base,
                weighted_score=weighted,
                covered_entity_ids=list(entry.get("covered_entity_ids", [])),
                covered_relationship_keys=list(entry.get("covered_relationship_keys", [])),
                reduced_confidence=reduced_confidence,
            )
        )

    # Fill in any missing fragment names
    for name in fragment_names:
        if not any(s.get("source_fragment") == name for s in scores):
            scores.append(
                JudgeScore(
                    source_fragment=name,
                    base_score=0.0,
                    weighted_score=0.0,
                    covered_entity_ids=[],
                    covered_relationship_keys=[],
                    reduced_confidence=reduced_confidence,
                )
            )

    return scores


def _score_fragments(
    llm_judge: object,
    batch: dict,
    quality_weights: dict[str, int],
    fragments: list[ArchFragment],
    fragment_names: list[str],
    reduced_confidence: bool,
) -> list[JudgeScore]:
    """Run SAAM scoring pipeline: prompt → invoke → parse → apply weighting."""
    prompt = _build_saam_prompt(batch, quality_weights, fragments, fragment_names)
    raw = _invoke_llm(llm_judge, prompt)
    data = _response_to_dict(raw)
    return _parse_saam_response(data, fragment_names, reduced_confidence)


# =============================================================================
# T023 — Canonical ID and relationship-key normalization
# =============================================================================


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


def _rel_key_str(source_id: str, target_id: str, interaction_type: str) -> str:
    """String form of relationship key for SAAM coverage matching."""
    return f"{source_id}->{target_id}:{interaction_type}"


# =============================================================================
# T024 — Primary fragment selection
# =============================================================================


def _select_primary(
    scores: list[JudgeScore],
    fragments: list[ArchFragment],
    fragment_names: list[str],
) -> tuple[int, ArchFragment, str]:
    """Select the highest-scoring fragment. Break ties deterministically."""
    best_idx = 0
    best_score = -1.0

    for i, score in enumerate(scores):
        ws = score.get("weighted_score", 0.0)
        if ws > best_score:
            best_score = ws
            best_idx = i
        elif ws == best_score:
            # Tie-break: prefer earlier in FRAGMENT_TIE_ORDER
            name_i = score.get("source_fragment", fragment_names[i])
            name_best = scores[best_idx].get("source_fragment", fragment_names[best_idx])
            tie_i = _FRAGMENT_TIE_ORDER.get(name_i, 99)
            tie_best = _FRAGMENT_TIE_ORDER.get(name_best, 99)
            if tie_i < tie_best:
                best_idx = i

    return best_idx, fragments[best_idx], fragment_names[best_idx]


# =============================================================================
# T025 — Entity deduplication
# =============================================================================


def _deduplicate_entities(
    primary: ArchFragment,
    residual_fragments: list[tuple[ArchFragment, str, JudgeScore]],
    open_questions: list[OpenQuestion],
) -> ArchFragment:
    """Merge entities from residual fragments into primary with deduplication.

    Same canonical ID → keep longer description, flag hierarchy conflicts.
    New ID → add directly.
    """
    # Build merged result starting from primary
    result = ArchFragment(
        systems=list(primary.systems),
        containers=list(primary.containers),
        components=list(primary.components),
        persons=list(primary.persons),
        external_systems=list(primary.external_systems),
        relationships=list(primary.relationships),
        patterns=list(primary.patterns),
        rationale=dict(primary.rationale),
    )

    # Index primary entities by canonical ID for O(1) lookup
    sys_by_id: dict[str, ArchSystem] = {_canonical_id(s.id): s for s in result.systems}
    cont_by_id: dict[str, ArchContainer] = {_canonical_id(c.id): c for c in result.containers}
    comp_by_id: dict[str, ArchComponent] = {_canonical_id(c.id): c for c in result.components}
    person_by_id: dict[str, ArchPerson] = {_canonical_id(p.id): p for p in result.persons}
    ext_by_id: dict[str, ArchExternalSystem] = {_canonical_id(e.id): e for e in result.external_systems}

    for fragment, frag_name, score in residual_fragments:
        _merge_systems(result, fragment, frag_name, sys_by_id, open_questions)
        _merge_containers(result, fragment, frag_name, cont_by_id, open_questions)
        _merge_components(result, fragment, frag_name, comp_by_id, open_questions)
        _merge_persons(result, fragment, frag_name, person_by_id, open_questions)
        _merge_external_systems(result, fragment, frag_name, ext_by_id, open_questions)

    return result


def _merge_systems(
    result: ArchFragment,
    fragment: ArchFragment,
    frag_name: str,
    index: dict[str, ArchSystem],
    open_questions: list[OpenQuestion],
) -> None:
    for entity in fragment.systems:
        cid = _canonical_id(entity.id)
        if cid in index:
            existing = index[cid]
            if len(entity.description) > len(existing.description):
                existing.description = entity.description
        else:
            result.systems.append(entity)
            index[cid] = entity


def _merge_containers(
    result: ArchFragment,
    fragment: ArchFragment,
    frag_name: str,
    index: dict[str, ArchContainer],
    open_questions: list[OpenQuestion],
) -> None:
    for entity in fragment.containers:
        cid = _canonical_id(entity.id)
        if cid in index:
            existing = index[cid]
            # T026 — hierarchy conflict detection
            if entity.parent_system_id and existing.parent_system_id:
                if _canonical_id(entity.parent_system_id) != _canonical_id(existing.parent_system_id):
                    open_questions.append(
                        OpenQuestion(
                            entity_id=entity.id,
                            type="hierarchy_conflict",
                            description=(
                                f"Container '{entity.id}' has conflicting parent_system_id: "
                                f"'{entity.parent_system_id}' (from {frag_name}) vs "
                                f"'{existing.parent_system_id}' (existing)"
                            ),
                        )
                    )
            if len(entity.description) > len(existing.description):
                existing.description = entity.description
            # Retain available technology if not set
            if entity.technology and not existing.technology:
                existing.technology = entity.technology
        else:
            result.containers.append(entity)
            index[cid] = entity


def _merge_components(
    result: ArchFragment,
    fragment: ArchFragment,
    frag_name: str,
    index: dict[str, ArchComponent],
    open_questions: list[OpenQuestion],
) -> None:
    for entity in fragment.components:
        cid = _canonical_id(entity.id)
        if cid in index:
            existing = index[cid]
            # T026 — hierarchy conflict detection
            if entity.parent_container_id and existing.parent_container_id:
                if _canonical_id(entity.parent_container_id) != _canonical_id(existing.parent_container_id):
                    open_questions.append(
                        OpenQuestion(
                            entity_id=entity.id,
                            type="hierarchy_conflict",
                            description=(
                                f"Component '{entity.id}' has conflicting parent_container_id: "
                                f"'{entity.parent_container_id}' (from {frag_name}) vs "
                                f"'{existing.parent_container_id}' (existing)"
                            ),
                        )
                    )
            if len(entity.description) > len(existing.description):
                existing.description = entity.description
            if entity.technology and not existing.technology:
                existing.technology = entity.technology
        else:
            result.components.append(entity)
            index[cid] = entity


def _merge_persons(
    result: ArchFragment,
    fragment: ArchFragment,
    frag_name: str,
    index: dict[str, ArchPerson],
    open_questions: list[OpenQuestion],
) -> None:
    for entity in fragment.persons:
        cid = _canonical_id(entity.id)
        if cid in index:
            existing = index[cid]
            if len(entity.description) > len(existing.description):
                existing.description = entity.description
        else:
            result.persons.append(entity)
            index[cid] = entity


def _merge_external_systems(
    result: ArchFragment,
    fragment: ArchFragment,
    frag_name: str,
    index: dict[str, ArchExternalSystem],
    open_questions: list[OpenQuestion],
) -> None:
    for entity in fragment.external_systems:
        cid = _canonical_id(entity.id)
        if cid in index:
            existing = index[cid]
            if len(entity.description) > len(existing.description):
                existing.description = entity.description
            if entity.technology and not existing.technology:
                existing.technology = entity.technology
        else:
            result.external_systems.append(entity)
            index[cid] = entity


# =============================================================================
# T027-T029 — Relationship deduplication, scope resolution, scope conflicts
# =============================================================================


def _build_entity_type_index(fragment: ArchFragment, running_model: ArchModel | None = None) -> dict[str, str]:
    """Build {canonical_entity_id: entity_type} index for scope resolution."""
    index: dict[str, str] = {}

    for s in fragment.systems:
        index[_canonical_id(s.id)] = "system"
    for c in fragment.containers:
        index[_canonical_id(c.id)] = "container"
    for comp in fragment.components:
        index[_canonical_id(comp.id)] = "component"
    for p in fragment.persons:
        index[_canonical_id(p.id)] = "person"
    for e in fragment.external_systems:
        index[_canonical_id(e.id)] = "external_system"

    if running_model is not None:
        for s in running_model.systems:
            index[_canonical_id(s.id)] = "system"
            for c in s.containers:
                index[_canonical_id(c.id)] = "container"
                for comp in c.components:
                    index[_canonical_id(comp.id)] = "component"
        for p in running_model.persons:
            index[_canonical_id(p.id)] = "person"
        for e in running_model.external_systems:
            index[_canonical_id(e.id)] = "external_system"

    return index


def _resolve_scope(source_type: str, target_type: str) -> str:
    """Determine the correct diagram_scope from two entity type names."""
    for scope, type_set in _SCOPE_TABLE.items():
        if source_type in type_set and target_type in type_set:
            return scope
    return "context"


def _deduplicate_relationships(
    merged: ArchFragment,
    residual_fragments: list[tuple[ArchFragment, str, JudgeScore]],
    open_questions: list[OpenQuestion],
    all_scores: list[JudgeScore] | None = None,
    running_model: ArchModel | None = None,
) -> ArchFragment:
    """Merge relationships from residual fragments with deduplication.

    Key: (canonical source_id, canonical target_id, canonical interaction_type).
    Same key → higher weighted_score fragment wins for conflicting descriptions.
    Different diagram_scope → scope_conflict, choose endpoint-consistent scope.
    """
    # Build score lookup: source_fragment → weighted_score (all fragments)
    score_by_fragment: dict[str, float] = {}
    if all_scores:
        for score in all_scores:
            score_by_fragment[score.get("source_fragment", "")] = score.get("weighted_score", 0.0)
    else:
        for _, frag_name, score in residual_fragments:
            score_by_fragment[frag_name] = score.get("weighted_score", 0.0)

    # Index merged relationships by key
    rel_index: dict[tuple, tuple[int, ArchRelationship]] = {}
    for i, rel in enumerate(merged.relationships):
        rk = _rel_key(rel.source_id, rel.target_id, rel.interaction_type)
        rel_index[rk] = (i, rel)

    # Build type index for scope resolution
    type_index = _build_entity_type_index(merged, running_model)

    for fragment, frag_name, score in residual_fragments:
        for rel in fragment.relationships:
            rk = _rel_key(rel.source_id, rel.target_id, rel.interaction_type)

            if rk in rel_index:
                idx, existing = rel_index[rk]

                # T029 — scope conflict detection
                if rel.diagram_scope != existing.diagram_scope:
                    src_type = type_index.get(_canonical_id(rel.source_id), "system")
                    tgt_type = type_index.get(_canonical_id(rel.target_id), "system")
                    resolved = _resolve_scope(src_type, tgt_type)

                    open_questions.append(
                        OpenQuestion(
                            entity_id=f"{rel.source_id}->{rel.target_id}",
                            type="scope_conflict",
                            description=(
                                f"Relationship {rel.source_id}->{rel.target_id} [{rel.interaction_type}] "
                                f"has conflicting diagram_scope: '{rel.diagram_scope}' (from {frag_name}) vs "
                                f"'{existing.diagram_scope}' (existing). "
                                f"Resolved to '{resolved}' based on endpoint types ({src_type}, {tgt_type})."
                            ),
                        )
                    )
                    # Use the endpoint-consistent scope
                    existing.diagram_scope = resolved

                # T027 — higher-scored fragment wins for conflicting descriptions
                fragment_score = score.get("weighted_score", 0.0)
                existing_fragment = existing.source_fragment or ""
                existing_score = score_by_fragment.get(existing_fragment, 0.0)
                if fragment_score > existing_score:
                    existing.technology = rel.technology or existing.technology
                    existing.source_fragment = frag_name
            else:
                merged.relationships.append(rel)
                rel_index[rk] = (len(merged.relationships) - 1, rel)

    return merged


# =============================================================================
# T030-T032 — Residual scan, coverage union, orphan prevention, coverage gaps
# =============================================================================


def _collect_covered_ids(all_scores: list[JudgeScore]) -> set[str]:
    """Collect all entity IDs covered by positive SAAM scores."""
    covered: set[str] = set()
    for score in all_scores:
        for eid in score.get("covered_entity_ids", []):
            covered.add(_canonical_id(eid))
    return covered


def _collect_covered_rel_keys(all_scores: list[JudgeScore]) -> set[str]:
    """Collect all relationship keys covered by positive SAAM scores."""
    covered: set[str] = set()
    for score in all_scores:
        for rk in score.get("covered_relationship_keys", []):
            covered.add(rk.strip().lower())
    return covered


def _resolve_parent(
    parent_id: str,
    merged: ArchFragment,
    running_model: ArchModel | None,
    adopted_ids: set[str],
) -> bool:
    """Check if a parent ID is resolvable in merged output, running model, or newly adopted."""
    cid = _canonical_id(parent_id)
    if cid in adopted_ids:
        return True
    # Check merged fragment
    for s in merged.systems:
        if _canonical_id(s.id) == cid:
            return True
    for c in merged.containers:
        if _canonical_id(c.id) == cid:
            return True
    # Check running model (hierarchical: systems → containers → components)
    if running_model is not None:
        for s in running_model.systems:
            if _canonical_id(s.id) == cid:
                return True
            for c in s.containers:
                if _canonical_id(c.id) == cid:
                    return True
    return False


def _coverage_union(
    merged: ArchFragment,
    residual_fragments: list[tuple[ArchFragment, str, JudgeScore]],
    all_scores: list[JudgeScore],
    open_questions: list[OpenQuestion],
    running_model: ArchModel | None = None,
) -> ArchFragment:
    """Add non-conflicting entities/relationships from losing fragments.

    Only considers entities/relationships present in that fragment's
    positive SAAM coverage metadata. Rejects orphans and records
    coverage_gap entries.
    """
    covered_ids = _collect_covered_ids(all_scores)
    covered_rel_keys = _collect_covered_rel_keys(all_scores)

    # Track entity IDs already in merged result
    existing_system_ids = {_canonical_id(s.id) for s in merged.systems}
    existing_container_ids = {_canonical_id(c.id) for c in merged.containers}
    existing_component_ids = {_canonical_id(c.id) for c in merged.components}
    existing_person_ids = {_canonical_id(p.id) for p in merged.persons}
    existing_ext_ids = {_canonical_id(e.id) for e in merged.external_systems}
    existing_rel_keys = {
        _rel_key(r.source_id, r.target_id, r.interaction_type)
        for r in merged.relationships
    }

    # Track newly adopted IDs for cross-residual parent resolution
    adopted_system_ids: set[str] = set()
    adopted_container_ids: set[str] = set()

    for fragment, frag_name, score in residual_fragments:
        frag_covered_ids = {_canonical_id(eid) for eid in score.get("covered_entity_ids", [])}
        frag_covered_rel_keys = {rk.strip().lower() for rk in score.get("covered_relationship_keys", [])}

        # Adopt covered systems
        for entity in fragment.systems:
            cid = _canonical_id(entity.id)
            if cid in existing_system_ids or cid in adopted_system_ids:
                continue
            if cid in covered_ids and cid in frag_covered_ids:
                merged.systems.append(entity)
                existing_system_ids.add(cid)
                adopted_system_ids.add(cid)

        # Adopt covered containers (with orphan check)
        for entity in fragment.containers:
            cid = _canonical_id(entity.id)
            if cid in existing_container_ids or cid in adopted_container_ids:
                continue
            if cid in covered_ids and cid in frag_covered_ids:
                # T031 — orphan prevention
                parent_ok = _resolve_parent(
                    entity.parent_system_id, merged, running_model,
                    adopted_system_ids,
                )
                if not parent_ok:
                    open_questions.append(
                        OpenQuestion(
                            entity_id=entity.id,
                            type="coverage_gap",
                            description=(
                                f"Orphan container '{entity.id}': parent_system_id "
                                f"'{entity.parent_system_id}' not found in merged output, "
                                f"running model, or newly adopted systems (from {frag_name})."
                            ),
                        )
                    )
                    continue
                merged.containers.append(entity)
                existing_container_ids.add(cid)
                adopted_container_ids.add(cid)

        # Adopt covered components (with orphan check)
        for entity in fragment.components:
            cid = _canonical_id(entity.id)
            if cid in existing_component_ids:
                continue
            if cid in covered_ids and cid in frag_covered_ids:
                # T031 — orphan prevention
                parent_ok = _resolve_parent(
                    entity.parent_container_id, merged, running_model,
                    adopted_container_ids,
                )
                if not parent_ok:
                    open_questions.append(
                        OpenQuestion(
                            entity_id=entity.id,
                            type="coverage_gap",
                            description=(
                                f"Orphan component '{entity.id}': parent_container_id "
                                f"'{entity.parent_container_id}' not found in merged output, "
                                f"running model, or newly adopted containers (from {frag_name})."
                            ),
                        )
                    )
                    continue
                merged.components.append(entity)
                existing_component_ids.add(cid)

        # Adopt covered persons (no parent check — leaf entities)
        for entity in fragment.persons:
            cid = _canonical_id(entity.id)
            if cid in existing_person_ids:
                continue
            if cid in covered_ids and cid in frag_covered_ids:
                merged.persons.append(entity)
                existing_person_ids.add(cid)

        # Adopt covered external systems (no parent check — leaf entities)
        for entity in fragment.external_systems:
            cid = _canonical_id(entity.id)
            if cid in existing_ext_ids:
                continue
            if cid in covered_ids and cid in frag_covered_ids:
                merged.external_systems.append(entity)
                existing_ext_ids.add(cid)

        # Adopt covered relationships
        for rel in fragment.relationships:
            rk = _rel_key(rel.source_id, rel.target_id, rel.interaction_type)
            if rk in existing_rel_keys:
                continue
            rk_str = _rel_key_str(rel.source_id, rel.target_id, rel.interaction_type)
            if rk_str in covered_rel_keys and rk_str in frag_covered_rel_keys:
                merged.relationships.append(rel)
                existing_rel_keys.add(rk)

    return merged


# =============================================================================
# T034 — Tree assembly
# =============================================================================


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
            # Attach to source if it's a system, or find the owning system
            src_cid = _canonical_id(rel.source_id)
            if src_cid in sys_map:
                sys_map[src_cid].context_relationships.append(rel)
            else:
                # Source is person/external_system — attach to target system
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


# =============================================================================
# T035 — Running model update
# =============================================================================


def _update_running_model(
    running: ArchModel,
    contribution: ArchFragment,
    open_questions: list[OpenQuestion],
) -> ArchModel:
    """Merge assembled batch contribution into running_arch_model.

    Avoids duplicating existing entities. Preserves unrelated tree branches.
    Records hierarchy and scope conflicts against existing model.
    """
    # Index existing top-level entities
    # Containers/components are nested inside systems — indexed via recursive merge
    existing_sys = {_canonical_id(s.id): s for s in running.systems}
    existing_person = {_canonical_id(p.id): p for p in running.persons}
    existing_ext = {_canonical_id(e.id): e for e in running.external_systems}

    # Merge systems
    for s in contribution.systems:
        cid = _canonical_id(s.id)
        if cid in existing_sys:
            existing = existing_sys[cid]
            if len(s.description) > len(existing.description):
                existing.description = s.description
            # Merge containers recursively
            _merge_sys_containers(existing, s, open_questions)
        else:
            running.systems.append(s)
            existing_sys[cid] = s

    # Merge persons
    for p in contribution.persons:
        cid = _canonical_id(p.id)
        if cid in existing_person:
            existing = existing_person[cid]
            if len(p.description) > len(existing.description):
                existing.description = p.description
        else:
            running.persons.append(p)

    # Merge external systems
    for e in contribution.external_systems:
        cid = _canonical_id(e.id)
        if cid in existing_ext:
            existing = existing_ext[cid]
            if len(e.description) > len(existing.description):
                existing.description = e.description
        else:
            running.external_systems.append(e)

    # Merge patterns
    existing_pattern_names = {p.name for p in running.patterns}
    for p in contribution.patterns:
        if p.name not in existing_pattern_names:
            running.patterns.append(p)

    return running


def _merge_sys_containers(
    existing_sys: ArchSystem,
    contrib_sys: ArchSystem,
    open_questions: list[OpenQuestion],
) -> None:
    """Merge containers from contribution into existing system."""
    existing_cont = {_canonical_id(c.id): c for c in existing_sys.containers}

    for c in contrib_sys.containers:
        cid = _canonical_id(c.id)
        if cid in existing_cont:
            ec = existing_cont[cid]
            if len(c.description) > len(ec.description):
                ec.description = c.description
            # Merge components recursively
            _merge_cont_components(ec, c, open_questions)
        else:
            existing_sys.containers.append(c)

    # Merge context relationships
    existing_rel_keys = {
        _rel_key(r.source_id, r.target_id, r.interaction_type)
        for r in existing_sys.context_relationships
    }
    for r in contrib_sys.context_relationships:
        rk = _rel_key(r.source_id, r.target_id, r.interaction_type)
        if rk not in existing_rel_keys:
            existing_sys.context_relationships.append(r)


def _merge_cont_components(
    existing_cont: ArchContainer,
    contrib_cont: ArchContainer,
    open_questions: list[OpenQuestion],
) -> None:
    """Merge components from contribution into existing container."""
    existing_comp = {_canonical_id(c.id): c for c in existing_cont.components}

    for comp in contrib_cont.components:
        cid = _canonical_id(comp.id)
        if cid in existing_comp:
            ec = existing_comp[cid]
            if len(comp.description) > len(ec.description):
                ec.description = comp.description
        else:
            existing_cont.components.append(comp)

    # Merge container relationships
    existing_rel_keys = {
        _rel_key(r.source_id, r.target_id, r.interaction_type)
        for r in existing_cont.container_relationships
    }
    for r in contrib_cont.container_relationships:
        rk = _rel_key(r.source_id, r.target_id, r.interaction_type)
        if rk not in existing_rel_keys:
            existing_cont.container_relationships.append(r)


# =============================================================================
# T033 — LLM-backed conflict description helpers
# =============================================================================


def _describe_conflicts(
    llm_judge: object,
    open_questions: list[OpenQuestion],
) -> list[OpenQuestion]:
    """Use llm_judge only to phrase conflict descriptions.

    LLM is never used to choose merged entities or tree structure —
    only to produce human-readable descriptions of already-detected issues.
    """
    if not open_questions:
        return open_questions

    # Build a prompt listing all detected conflicts
    conflict_lines = []
    for i, oq in enumerate(open_questions):
        conflict_lines.append(
            f"{i}: [{oq.type}] entity={oq.entity_id} — {oq.description}"
        )

    prompt = (
        "You are an architecture conflict analyst. Below are detected merge conflicts "
        "and coverage gaps from a batch architecture merge. For each one, provide a "
        "concise, human-readable description (1-2 sentences). Keep the descriptions "
        "technical and actionable. Do NOT suggest resolutions — just describe what "
        "the conflict or gap is.\n\n"
        + "\n".join(conflict_lines)
        + "\n\nReturn a JSON object with a 'descriptions' array of strings, "
        "one per conflict in the same order."
    )

    try:
        raw = _invoke_llm(llm_judge, prompt)
        data = _response_to_dict(raw)
        descriptions = data.get("descriptions", [])
        for i, desc in enumerate(descriptions):
            if i < len(open_questions):
                open_questions[i].description = str(desc)
    except Exception:
        # If LLM description fails, keep the original auto-generated descriptions
        pass

    return open_questions


# =============================================================================
# T036 — Main orchestration
# =============================================================================


def _entity_count(fragment: ArchFragment) -> int:
    """Count total C4 entities in a fragment."""
    return (
        len(fragment.systems)
        + len(fragment.containers)
        + len(fragment.components)
        + len(fragment.persons)
        + len(fragment.external_systems)
    )


def _extract_fragment_names(fragments: list[ArchFragment]) -> list[str]:
    """Extract source_fragment names from a list of fragments."""
    names: list[str] = []
    for f in fragments:
        name = None
        if f.systems:
            name = f.systems[0].source_fragment
        elif f.containers:
            name = f.containers[0].source_fragment
        elif f.components:
            name = f.components[0].source_fragment
        elif f.persons:
            name = f.persons[0].source_fragment
        elif f.external_systems:
            name = f.external_systems[0].source_fragment
        names.append(name or "unknown")
    return names


def judge_batch(state: dict[str, Any], config: dict | None = None) -> dict[str, Any]:
    """Evaluate parallel subgraph outputs, merge, and update running model.

    Args:
        state: RAAState dict with batch_outputs, batch_cursor, running_arch_model, etc.
        config: LangGraph config dict with config['context']['llm_judge'].

    Returns:
        State update dict with best_batch_output, running_arch_model,
        open_questions, and batch_cursor. Never includes LLM objects.
    """
    # 1. Extract context and llm_judge from config (never from state)
    ctx = _context_dict(config)
    llm_judge = _require_llm_judge(ctx)

    # 2. Read current batch position
    batch_cursor: int = state.get("batch_cursor", 0)
    batch_outputs: dict[int, list[ArchFragment]] = state.get("batch_outputs", {})
    batch_queue: list[dict] = state.get("batch_queue", [])
    quality_weights: dict[str, int] = state.get("quality_weights", {})

    # Guard: empty batch queue
    if not batch_queue or batch_cursor >= len(batch_queue):
        return {"batch_cursor": batch_cursor}

    batch = batch_queue[batch_cursor]
    fragments = batch_outputs.get(batch_cursor, [])

    # Guard: no fragments for this batch
    if not fragments:
        return {
            "best_batch_output": {batch_cursor: ArchFragment()},
            "batch_cursor": batch_cursor + 1,
        }

    fragment_names = _extract_fragment_names(fragments)
    reduced = batch.get("reduced_confidence", False)

    # 3. SAAM scoring via llm_judge
    scores = _score_fragments(
        llm_judge, batch, quality_weights, fragments, fragment_names, reduced,
    )

    # 4. Select primary fragment (highest weighted_score)
    primary_idx, primary, primary_name = _select_primary(scores, fragments, fragment_names)

    # 5. Build residual list (losing fragments with their scores)
    residual: list[tuple[ArchFragment, str, JudgeScore]] = [
        (fragments[i], fragment_names[i], scores[i])
        for i in range(len(fragments))
        if i != primary_idx
    ]

    # 6. Entity deduplication (primary + residuals)
    open_questions: list[OpenQuestion] = []
    merged = _deduplicate_entities(primary, residual, open_questions)

    # 7. Relationship deduplication with scope conflict detection
    running: ArchModel = state.get("running_arch_model", ArchModel())
    if isinstance(running, dict):
        running = ArchModel()
    merged = _deduplicate_relationships(merged, residual, open_questions, scores, running)

    # 8. Coverage union (residual scan with orphan prevention)
    merged = _coverage_union(merged, residual, scores, open_questions, running)

    # 9. LLM-backed conflict description phrasing (LLM only for descriptions)
    open_questions = _describe_conflicts(llm_judge, open_questions)

    # 10. Tree assembly — nest into C4 hierarchy
    assembled = _assemble_tree(merged)

    # 11. Update running model
    updated_model = _update_running_model(running, assembled, open_questions)

    # 12. Build state update — must NOT include any LLM object
    # open_questions channel uses Annotated[list, add] reducer — new items append automatically
    return {
        "best_batch_output": {batch_cursor: assembled},
        "running_arch_model": updated_model,
        "open_questions": open_questions,
        "batch_cursor": batch_cursor + 1,
    }
