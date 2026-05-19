"""Shared types, constants, reference loading, prompt assembly, LLM invocation,
output parsing, and validation for RAA parallel subgraphs (Section 12)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from typing_extensions import TypedDict

from raa.state.types import (
    ArchComponent,
    ArchContainer,
    ArchExternalSystem,
    ArchFragment,
    ArchModel,
    ArchPattern,
    ArchPerson,
    ArchRelationship,
    ArchSystem,
)

# ---- Strategy names ---------------------------------------------------------

SubgraphStrategy = Literal["saam_first", "pattern_driven", "entity_driven"]

STRATEGY_SAAM_FIRST: SubgraphStrategy = "saam_first"
STRATEGY_PATTERN_DRIVEN: SubgraphStrategy = "pattern_driven"
STRATEGY_ENTITY_DRIVEN: SubgraphStrategy = "entity_driven"

# ---- LLM context keys -------------------------------------------------------

LLM_RAA_A_KEY = "llm_raa_a"
LLM_RAA_B_KEY = "llm_raa_b"
LLM_RAA_C_KEY = "llm_raa_c"

# ---- Send target node names -------------------------------------------------

SEND_TARGET_RAA_A = "raa_a"
SEND_TARGET_RAA_B = "raa_b"
SEND_TARGET_RAA_C = "raa_c"

ALL_SEND_TARGETS: list[str] = [
    SEND_TARGET_RAA_A,
    SEND_TARGET_RAA_B,
    SEND_TARGET_RAA_C,
]

TARGET_LLM_KEY_MAP: dict[str, str] = {
    SEND_TARGET_RAA_A: LLM_RAA_A_KEY,
    SEND_TARGET_RAA_B: LLM_RAA_B_KEY,
    SEND_TARGET_RAA_C: LLM_RAA_C_KEY,
}


# ---- Send payload -----------------------------------------------------------

class SubgraphPayload(TypedDict, total=False):
    """Payload carried by each LangGraph Send into a strategy subgraph."""

    batch: dict
    batch_index: int
    quality_weights: dict[str, int]
    running_arch_model: dict | None
    bridge_requirements: dict[tuple, list[str]]
    strategy: str
    llm: object
    model_constraints: str


# ---- Per-strategy reference manifests (Section 12) --------------------------

REFERENCE_DIR = "Skills/RAA/references"

REF_C4 = "C4.md"
REF_C4_LEVEL_MAPPING = "C4_Level_Mapping.md"
REF_ENTITY_EXTRACTION = "Entity_Extraction.md"
REF_RELATIONSHIP_EXTRACTION = "Relationship_Extraction.md"
REF_TECHNOLOGY_INFERENCE = "Technology_Inference.md"
REF_QUALITY_ATTRIBUTES = "Quality_Attributes.md"
REF_SAAM = "SAAM.md"
REF_PATTERN_SELECTION = "Pattern_Selection.md"

RAA_A_REFERENCES: list[str] = [
    REF_SAAM, REF_QUALITY_ATTRIBUTES, REF_ENTITY_EXTRACTION,
    REF_RELATIONSHIP_EXTRACTION, REF_TECHNOLOGY_INFERENCE, REF_C4, REF_C4_LEVEL_MAPPING,
]

RAA_B_REFERENCES: list[str] = [
    REF_PATTERN_SELECTION, REF_QUALITY_ATTRIBUTES, REF_ENTITY_EXTRACTION,
    REF_RELATIONSHIP_EXTRACTION, REF_TECHNOLOGY_INFERENCE, REF_C4, REF_C4_LEVEL_MAPPING,
]

RAA_C_REFERENCES: list[str] = [
    REF_ENTITY_EXTRACTION, REF_RELATIONSHIP_EXTRACTION, REF_TECHNOLOGY_INFERENCE,
    REF_C4, REF_C4_LEVEL_MAPPING,
]

STRATEGY_REFERENCE_MANIFEST: dict[str, list[str]] = {
    STRATEGY_SAAM_FIRST: RAA_A_REFERENCES,
    STRATEGY_PATTERN_DRIVEN: RAA_B_REFERENCES,
    STRATEGY_ENTITY_DRIVEN: RAA_C_REFERENCES,
}


# ---- Relationship scope table (Section 12) -----------------------------------

_CONTEXT_ENDPOINT_TYPES = frozenset({"system", "person", "external_system"})
_CONTAINER_ENDPOINT_TYPES = frozenset({"container"})
_COMPONENT_ENDPOINT_TYPES = frozenset({"component"})

RELATIONSHIP_SCOPE_TABLE: dict[str, frozenset[str]] = {
    "context": _CONTEXT_ENDPOINT_TYPES,
    "container": _CONTAINER_ENDPOINT_TYPES,
    "component": _COMPONENT_ENDPOINT_TYPES,
}

VALID_DIAGRAM_SCOPES = frozenset(RELATIONSHIP_SCOPE_TABLE.keys())

# Type name → scope classification (mapping of __class__.__name__.lower())
_TYPE_NAME_TO_SCOPE: dict[str, frozenset[str]] = {
    "archsystem": _CONTEXT_ENDPOINT_TYPES,
    "archperson": _CONTEXT_ENDPOINT_TYPES,
    "archexternalsystem": _CONTEXT_ENDPOINT_TYPES,
    "archcontainer": _CONTAINER_ENDPOINT_TYPES,
    "archcomponent": _COMPONENT_ENDPOINT_TYPES,
}

# Class-name-based lookup for dict-based running_arch_model entities
_DICT_ENTITY_SCOPE_HINTS: dict[str, str] = {
    "systems": "system",
    "containers": "container",
    "components": "component",
    "persons": "person",
    "external_systems": "external_system",
}


# ---- T041: Reference loading -------------------------------------------------


def load_reference_file(filename: str) -> str:
    """Read a reference file from Skills/RAA/references/."""
    ref_path = Path(REFERENCE_DIR) / filename
    if not ref_path.is_file():
        raise FileNotFoundError(f"Reference file not found: {ref_path}")
    return ref_path.read_text(encoding="utf-8")


def load_strategy_references(strategy: str) -> dict[str, str]:
    """Load all reference files for a given strategy into {filename: content}."""
    manifest = STRATEGY_REFERENCE_MANIFEST.get(strategy, [])
    return {filename: load_reference_file(filename) for filename in manifest}


# ---- T043: Model serialization -----------------------------------------------


def serialize_running_arch_model(
    running_arch_model: ArchModel | dict | None,
) -> dict[str, Any]:
    """Expose existing system/container/component/actor IDs for prompt constraints."""
    if running_arch_model is None:
        return {"systems": [], "containers": [], "components": [],
                "persons": [], "external_systems": []}
    if isinstance(running_arch_model, dict):
        return running_arch_model
    # ArchModel dataclass — extract list of dicts for each entity type
    return {
        "systems": [_entity_to_dict(s) for s in getattr(running_arch_model, "systems", [])],
        "containers": [_entity_to_dict(c) for c in getattr(running_arch_model, "containers", [])],
        "components": [_entity_to_dict(c) for c in getattr(running_arch_model, "components", [])],
        "persons": [_entity_to_dict(p) for p in getattr(running_arch_model, "persons", [])],
        "external_systems": [_entity_to_dict(e) for e in getattr(running_arch_model, "external_systems", [])],
    }


def _entity_to_dict(entity: Any) -> dict[str, Any]:
    """Minimal dict serialization of a dataclass entity {id, label, ...}."""
    if hasattr(entity, "__dataclass_fields__"):
        from dataclasses import asdict
        return asdict(entity)
    if isinstance(entity, dict):
        return entity
    return {"id": str(getattr(entity, "id", entity)), "label": str(entity)}


# ---- T044: Prompt assembly ---------------------------------------------------


def build_subgraph_prompt(
    payload: SubgraphPayload,
    strategy: str,
    references: dict[str, str],
) -> str:
    """Assemble the full subgraph prompt from batch context, references, and strategy."""
    parts: list[str] = []

    parts.append("You are an architecture analysis subgraph agent.\n")

    # Batch requirements
    batch = payload.get("batch", {})
    requirements = batch.get("requirements", [])
    req_text = "\n".join(
        f"- {r.get('id', '?')}: {r.get('text', r.get('content', ''))}"
        for r in requirements
    )
    parts.append(f"## Requirements\n{req_text}\n")

    # Quality weights
    qw = payload.get("quality_weights", {})
    if qw:
        parts.append(f"## Quality Weights\n{json.dumps(qw)}\n")

    # Bridge requirements
    br = payload.get("bridge_requirements", {})
    if br:
        parts.append(f"## Bridge Requirements\n{json.dumps(br)}\n")

    # Running model constraints (pre-serialized by fan-out routing)
    model_constraints = payload.get("model_constraints", "")
    if model_constraints:
        parts.append(f"## Existing Architecture Model\n{model_constraints}\n")
    else:
        parts.append("## Existing Architecture Model\nNo existing architecture model yet.\n")

    # Strategy focus
    strategy_focus = {
        "saam_first": "Prioritize SAAM-based scenario evaluation. Identify quality attribute trade-offs.",
        "pattern_driven": "Identify applicable architectural patterns. Justify pattern selection.",
        "entity_driven": "Extract entities and relationships from requirements. Focus on C4 element discovery.",
    }
    parts.append(f"## Strategy: {strategy}\n{strategy_focus.get(strategy, strategy)}\n")

    # Orphan prevention rules
    parts.append(
        "## Hard Rules\n"
        "- Every container MUST have a parent_system_id that resolves to an existing system "
        "(in this fragment or the running model).\n"
        "- Every component MUST have a parent_container_id that resolves to an existing container "
        "(in this fragment or the running model).\n"
        "- Every relationship MUST have a diagram_scope of 'context', 'container', or 'component' "
        "matching the endpoint types per the C4 model.\n"
    )

    # Relationship scoping rules
    parts.append(
        "## Relationship Scoping Rules\n"
        "- system/person/external_system endpoints → context scope\n"
        "- container endpoints → container scope\n"
        "- component endpoints → component scope\n"
    )

    # Reference documents
    parts.append("## Reference Documents\n")
    for filename, content in references.items():
        parts.append(f"### {filename}\n{content}\n")

    # Output format
    parts.append(
        "## Output Format\n"
        "Return a JSON object with: systems, containers, components, persons, "
        "external_systems, relationships, patterns, rationale.\n"
    )

    return "\n".join(parts)


# ---- T045: LLM invocation ----------------------------------------------------


def _invoke_llm(llm: object, prompt: str) -> object:
    """Invoke an LLM with a prompt string. Supports .invoke(prompt) interface."""
    return llm.invoke(prompt)


# ---- T046: Response parsing --------------------------------------------------


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


# ---- T047: Dataclass construction from dict ----------------------------------


def arch_fragment_from_dict(data: dict[str, Any], source_fragment: str) -> ArchFragment:
    """Build a typed ArchFragment from a dict/JSON LLM response."""
    return ArchFragment(
        systems=[
            ArchSystem(
                id=s["id"], label=s.get("label", s["id"]),
                description=s.get("description", ""),
                source_fragment=source_fragment,
            )
            for s in data.get("systems", [])
        ],
        containers=[
            ArchContainer(
                id=c["id"], label=c.get("label", c["id"]),
                description=c.get("description", ""),
                parent_system_id=c.get("parent_system_id", ""),
                source_fragment=source_fragment,
            )
            for c in data.get("containers", [])
        ],
        components=[
            ArchComponent(
                id=c["id"], label=c.get("label", c["id"]),
                description=c.get("description", ""),
                parent_container_id=c.get("parent_container_id", ""),
                source_fragment=source_fragment,
            )
            for c in data.get("components", [])
        ],
        persons=[
            ArchPerson(
                id=p["id"], label=p.get("label", p["id"]),
                description=p.get("description", ""),
                source_fragment=source_fragment,
            )
            for p in data.get("persons", [])
        ],
        external_systems=[
            ArchExternalSystem(
                id=e["id"], label=e.get("label", e["id"]),
                description=e.get("description", ""),
                source_fragment=source_fragment,
            )
            for e in data.get("external_systems", [])
        ],
        relationships=[
            ArchRelationship(
                source_id=r["source_id"], target_id=r["target_id"],
                interaction_type=r.get("interaction_type", ""),
                technology=r.get("technology"),
                diagram_scope=r.get("diagram_scope", "context"),
                source_fragment=source_fragment,
            )
            for r in data.get("relationships", [])
        ],
        patterns=[
            ArchPattern(
                name=p.get("name", p.get("pattern_name", "")),
                rationale=p.get("rationale", ""),
                quality_attributes=p.get("quality_attributes", []),
            )
            for p in data.get("patterns", [])
        ],
        rationale=data.get("rationale", {}),
    )


# ---- T048: ID index helpers --------------------------------------------------


def _running_system_ids(running_arch_model: ArchModel | dict | None) -> set[str]:
    """Collect all system IDs from the running architecture model."""
    ids: set[str] = set()
    if running_arch_model is None:
        return ids
    if isinstance(running_arch_model, dict):
        for sys in running_arch_model.get("systems", []):
            sid = sys.get("id") if isinstance(sys, dict) else getattr(sys, "id", None)
            if sid:
                ids.add(sid)
    elif hasattr(running_arch_model, "systems"):
        for sys in running_arch_model.systems:
            ids.add(sys.id)
    return ids


def _running_container_ids(running_arch_model: ArchModel | dict | None) -> set[str]:
    """Collect all container IDs from the running architecture model."""
    ids: set[str] = set()
    if running_arch_model is None:
        return ids
    if isinstance(running_arch_model, dict):
        for cont in running_arch_model.get("containers", []):
            cid = cont.get("id") if isinstance(cont, dict) else getattr(cont, "id", None)
            if cid:
                ids.add(cid)
    elif hasattr(running_arch_model, "containers"):
        for cont in running_arch_model.containers:
            ids.add(cont.id)
    return ids


# ---- T049: Parent-link validation --------------------------------------------


def validate_parent_links(
    fragment: ArchFragment,
    running_arch_model: ArchModel | dict | None = None,
) -> None:
    """Enforce: no container without resolvable parent_system_id;
    no component without resolvable parent_container_id."""
    system_ids: set[str] = {s.id for s in fragment.systems}
    system_ids |= _running_system_ids(running_arch_model)

    container_ids: set[str] = {c.id for c in fragment.containers}
    container_ids |= _running_container_ids(running_arch_model)

    for container in fragment.containers:
        if container.parent_system_id not in system_ids:
            raise ValueError(
                f"Orphan container '{container.id}': parent_system_id "
                f"'{container.parent_system_id}' not found in fragment or running model"
            )

    for component in fragment.components:
        if component.parent_container_id not in container_ids:
            raise ValueError(
                f"Orphan component '{component.id}': parent_container_id "
                f"'{component.parent_container_id}' not found in fragment or running model"
            )


# ---- T050: Entity type index -------------------------------------------------


def _entity_type_index(
    fragment: ArchFragment,
    running_arch_model: ArchModel | dict | None = None,
) -> dict[str, str]:
    """Build {entity_id: entity_type_name} index from fragment and running model."""
    index: dict[str, str] = {}

    for sys in fragment.systems:
        index[sys.id] = "system"
    for cont in fragment.containers:
        index[cont.id] = "container"
    for comp in fragment.components:
        index[comp.id] = "component"
    for person in fragment.persons:
        index[person.id] = "person"
    for ext in fragment.external_systems:
        index[ext.id] = "external_system"

    if running_arch_model is not None:
        if isinstance(running_arch_model, dict):
            for scope, hint in _DICT_ENTITY_SCOPE_HINTS.items():
                for entity in running_arch_model.get(scope, []):
                    eid = entity.get("id") if isinstance(entity, dict) else getattr(entity, "id", None)
                    if eid:
                        index[eid] = hint
        elif hasattr(running_arch_model, "systems"):
            for sys in getattr(running_arch_model, "systems", []):
                index[sys.id] = "system"
            for cont in getattr(running_arch_model, "containers", []):
                index[cont.id] = "container"
            for comp in getattr(running_arch_model, "components", []):
                index[comp.id] = "component"
            for person in getattr(running_arch_model, "persons", []):
                index[person.id] = "person"
            for ext in getattr(running_arch_model, "external_systems", []):
                index[ext.id] = "external_system"

    return index


# ---- T051: Expected diagram_scope from endpoint types ------------------------


def _expected_diagram_scope(source_type: str, target_type: str) -> str:
    """Determine the expected diagram_scope from two entity type names."""
    for scope, type_set in RELATIONSHIP_SCOPE_TABLE.items():
        if source_type in type_set and target_type in type_set:
            return scope
    return "context"


# ---- T052: Relationship scope validation -------------------------------------


def validate_relationship_scopes(
    fragment: ArchFragment,
    running_arch_model: ArchModel | dict | None = None,
) -> None:
    """Enforce: every ArchRelationship has a valid diagram_scope matching endpoint types."""
    type_index = _entity_type_index(fragment, running_arch_model)

    for rel in fragment.relationships:
        scope = rel.diagram_scope
        if not scope or scope not in VALID_DIAGRAM_SCOPES:
            raise ValueError(
                f"Relationship {rel.source_id}->{rel.target_id}: "
                f"invalid or missing diagram_scope '{scope}'"
            )

        src_type = type_index.get(rel.source_id, "system")
        tgt_type = type_index.get(rel.target_id, "system")
        expected = _expected_diagram_scope(src_type, tgt_type)

        if scope != expected:
            raise ValueError(
                f"Relationship {rel.source_id}({src_type})->{rel.target_id}({tgt_type}): "
                f"diagram_scope '{scope}' does not match expected '{expected}'"
            )


# ---- T053: Full subgraph execution pipeline ----------------------------------


def execute_strategy_subgraph(
    payload: SubgraphPayload,
    strategy: str,
    source_fragment: str,
) -> dict[str, Any]:
    """Load references, build prompt, invoke LLM, parse, validate, return batch_outputs."""
    references = load_strategy_references(strategy)
    prompt = build_subgraph_prompt(payload, strategy, references)
    raw = _invoke_llm(payload["llm"], prompt)
    data = _response_to_dict(raw)
    fragment = arch_fragment_from_dict(data, source_fragment)

    running = payload.get("running_arch_model")
    validate_parent_links(fragment, running)
    validate_relationship_scopes(fragment, running)

    return {"batch_outputs": {payload["batch_index"]: [fragment]}}
