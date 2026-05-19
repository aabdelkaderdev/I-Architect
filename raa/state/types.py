"""
RAA state dataclasses and type definitions.

All types defined in RAA_Plan.md Section 4 (State Schema / State Channel Type Definitions).
Uses @dataclass (stdlib) for native JsonPlusSerializer compatibility.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


# ---------------------------------------------------------------------------
# Leaf / Simple Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ArchPattern:
    """Pattern selected by the ILP or Greedy optimizer."""

    name: str
    rationale: str
    quality_attributes: list[str] = field(default_factory=list)


@dataclass
class OpenQuestion:
    """Unresolved or conflicting item flagged during graph runs.

    type must be one of: change_risk, high_coupling, contention, tie,
    coverage_gap, hierarchy_conflict, scope_conflict.
    """

    entity_id: str | None
    type: str
    description: str
    scenario_ids: list[str] = field(default_factory=list)


@dataclass
class IncoherentBatchRecord:
    """Batch that failed the coherence gate after splitting."""

    batch_id: int
    coherence_score: float
    reduced_confidence: bool


@dataclass
class ConfidenceRecord:
    """Per-entity confidence metadata from batch execution."""

    reduced_confidence: bool
    source_batch: int
    saam_score: float


@dataclass
class DiagramManifestEntry:
    """Work-queue entry for AGA diagram generation.

    diagram_type must be one of: context, container, component.
    """

    diagram_id: str
    diagram_type: str
    focus_entity_id: str
    label: str


# ---------------------------------------------------------------------------
# Batch TypedDict
# ---------------------------------------------------------------------------

class SortingMetadata(TypedDict, total=False):
    """Per-batch ordering metadata written by the queue ordering node.

    Fields: score (float), strategy (str), tie_breaker (str).
    """

    score: float
    strategy: str
    tie_breaker: str


class Batch(TypedDict, total=False):
    """Ordered batch of requirements for one RAA execution unit.

    Extended per RAA_Plan.md Section 8 with cluster labels, full normalized
    requirement payloads, similarity scores, and non-ASR candidate records.
    """

    batch_id: int
    group_id: int
    requirement_ids: list[str]
    group_centroid: list[float] | None
    reduced_confidence: bool
    cluster: list[str]
    requirements: list[dict]
    similarity_scores: dict[str, float]
    non_asr_candidates: list[dict]
    coherence_score: float
    is_split: bool
    source_batch_id: int
    sorting_metadata: SortingMetadata


# ---------------------------------------------------------------------------
# Relationship
# ---------------------------------------------------------------------------

@dataclass
class ArchRelationship:
    """Directed relationship between C4 elements.

    diagram_scope must be one of: context, container, component.
    Scope is determined by endpoint types per RAA_Plan.md Section 12.
    """

    source_id: str
    target_id: str
    interaction_type: str
    technology: str | None
    requirement_ids: list[int] = field(default_factory=list)
    source_fragment: str | None = None
    diagram_scope: str = "context"


# ---------------------------------------------------------------------------
# Actor Dataclasses (flat leaf entities)
# ---------------------------------------------------------------------------

@dataclass
class ArchPerson:
    """Human actor. Flat leaf entity; always referenced by ID from relationships."""

    id: str
    label: str
    description: str
    requirement_ids: list[int] = field(default_factory=list)
    source_fragment: str | None = None
    confidence: float | None = None


@dataclass
class ArchExternalSystem:
    """External software system. Flat leaf entity; always referenced by ID."""

    id: str
    label: str
    description: str
    technology: str | None = None
    requirement_ids: list[int] = field(default_factory=list)
    source_fragment: str | None = None
    confidence: float | None = None


# ---------------------------------------------------------------------------
# C4 Hierarchy Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ArchComponent:
    """Internal building block within a container."""

    id: str
    label: str
    description: str
    parent_container_id: str
    technology: str | None = None
    requirement_ids: list[int] = field(default_factory=list)
    source_fragment: str | None = None
    confidence: float | None = None
    component_relationships: list[ArchRelationship] = field(default_factory=list)


@dataclass
class ArchContainer:
    """Deployable unit within a system."""

    id: str
    label: str
    description: str
    parent_system_id: str
    technology: str | None = None
    requirement_ids: list[int] = field(default_factory=list)
    source_fragment: str | None = None
    confidence: float | None = None
    container_relationships: list[ArchRelationship] = field(default_factory=list)
    components: list[ArchComponent] = field(default_factory=list)


@dataclass
class ArchSystem:
    """Software system under design. Root of the C4 hierarchy branch."""

    id: str
    label: str
    description: str
    requirement_ids: list[int] = field(default_factory=list)
    source_fragment: str | None = None
    confidence: float | None = None
    context_relationships: list[ArchRelationship] = field(default_factory=list)
    containers: list[ArchContainer] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Aggregate Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ArchFragment:
    """Partial output from a single RAA subgraph run.

    Uses semi-flat structure with explicit parent ID fields for easier
    inter-fragment deduplication and merge. The judge constructs the fully
    nested ArchModel after merge.
    """

    systems: list[ArchSystem] = field(default_factory=list)
    containers: list[ArchContainer] = field(default_factory=list)
    components: list[ArchComponent] = field(default_factory=list)
    persons: list[ArchPerson] = field(default_factory=list)
    external_systems: list[ArchExternalSystem] = field(default_factory=list)
    relationships: list[ArchRelationship] = field(default_factory=list)
    patterns: list[ArchPattern] = field(default_factory=list)
    rationale: dict = field(default_factory=dict)


@dataclass
class ArchModel:
    """Accumulated architecture model in hierarchical form.

    Systems contain containers, which contain components. Persons and
    external systems are global, shared actors referenced by ID from
    relationships. Structurally identical to C4JsonModel at the AGA boundary.
    """

    systems: list[ArchSystem] = field(default_factory=list)
    persons: list[ArchPerson] = field(default_factory=list)
    external_systems: list[ArchExternalSystem] = field(default_factory=list)
    patterns: list[ArchPattern] = field(default_factory=list)
    diagram_manifest: list[DiagramManifestEntry] = field(default_factory=list)
    confidence_metadata: dict[str, ConfidenceRecord] = field(default_factory=dict)
    open_questions: list[OpenQuestion] = field(default_factory=list)


@dataclass
class FailureRegisterEntry:
    """Represents a monitored runtime risk and its active mitigation."""

    risk_id: str
    description: str
    mitigation_strategy: str
    section_ref: str
    verified_node: str

