"""Type definitions for the AGA subgraph.

Three groups:
1. RAA-boundary types — Python representations of the RAA output dict.
2. Internal work types — DiagramSpec and supporting records.
3. LangGraph state schemas — TypedDicts parameterising the StateGraph.
"""

from __future__ import annotations

import operator
from typing import Literal, TypedDict

from pydantic import BaseModel, Field
from typing_extensions import Annotated

# ── RAA Boundary Types ──────────────────────────────────────────────────────


class RAAActorEntry(BaseModel):
    """One actor from l1_description["actors"]."""

    canonical_id: str
    name: str
    description: str
    source_requirements: list[str]


class RAAExternalSystemEntry(BaseModel):
    """One entry from l1_description["external_systems"]."""

    canonical_id: str
    name: str
    description: str
    source_requirements: list[str]


class RAARelationshipEntry(BaseModel):
    """One relationship from any relationship list (L1, L2, or L3)."""

    source_id: str
    target_id: str
    label: str
    description: str


class RAAContainerEntry(BaseModel):
    """One container from an l2_descriptions[i]["containers"] list."""

    canonical_id: str
    name: str
    description: str
    source_requirements: list[str]


class RAAComponentEntry(BaseModel):
    """One component from an l3_descriptions[i]["components"] list."""

    canonical_id: str
    name: str
    description: str
    responsibilities: list[str]
    interfaces: list[str] = Field(default_factory=list)
    source_requirements: list[str]


class RAAL1Description(BaseModel):
    """Top-level L1 block from raa_output["l1_description"]."""

    system_name: str
    system_description: str
    system_boundary_description: str
    actors: list[RAAActorEntry]
    external_systems: list[RAAExternalSystemEntry]
    relationships: list[RAARelationshipEntry]
    source_requirements: list[str]


class RAAL2Description(BaseModel):
    """One entry from raa_output["l2_descriptions"]."""

    concern_id: str
    condition: str
    containers: list[RAAContainerEntry]
    relationships: list[RAARelationshipEntry]
    source_requirements: list[str]


class RAAL3Description(BaseModel):
    """One entry from raa_output["l3_descriptions"]."""

    parent_container_id: str
    concern_id: str
    components: list[RAAComponentEntry]
    relationships: list[RAARelationshipEntry]
    source_requirements: list[str]


class RAAEntityRegistryEntry(BaseModel):
    """One entry from raa_output["entity_registry"] (keyed by ENT-NNN)."""

    canonical_id: str
    canonical_name: str
    c4_level: str  # "system", "container", or "component"
    c4_type: str  # e.g. "service", "database", "gateway", "actor"
    description: str
    source_requirements: list[str]
    authority: str  # "asr" or "non_asr"
    variants: dict[str, dict]  # keyed by batch/concern ID


class RAAOutput(BaseModel):
    """Fully-typed representation of the RAA output dict."""

    l1_description: RAAL1Description
    l2_descriptions: list[RAAL2Description]
    l3_descriptions: list[RAAL3Description]
    entity_registry: dict[str, RAAEntityRegistryEntry]
    coverage_gaps: list[dict]  # passed through unmodified
    conflicts: list[dict]  # passed through unmodified


# ── Internal Work Types ─────────────────────────────────────────────────────

DiagramType = Literal["context", "container", "component"]


class DiagramSpec(BaseModel):
    """Unit of work for one diagram. Produced by the queue builder (Phase 3)."""

    diagram_id: str
    diagram_type: DiagramType
    label: str
    output_filename: str
    source_l1: RAAL1Description | None = None
    source_l2: RAAL2Description | None = None
    source_l3: RAAL3Description | None = None


class CompletedDiagram(BaseModel):
    """Successfully rendered diagram record."""

    diagram_id: str
    diagram_type: DiagramType
    output_path: str
    plantuml_source: str
    retry_count: int


class FailedDiagram(BaseModel):
    """Diagram that exhausted max_retries without successful rendering."""

    diagram_id: str
    diagram_type: DiagramType
    last_puml_code: str
    last_error: str
    retry_count: int


class SessionReport(BaseModel):
    """Summary record assembled at graph exit."""

    completed_count: int
    failed_count: int
    total_diagrams_expected: int
    output_dir: str
    plantuml_base_url: str
    wall_clock_seconds: float


# ── LangGraph State Schemas ─────────────────────────────────────────────────


class AGAInputState(TypedDict):
    """What the Orchestrator passes to .invoke()."""

    raa_output: dict


class AGAOutputState(TypedDict):
    """What .invoke() returns to the Orchestrator."""

    completed_diagrams: list[CompletedDiagram]
    failed_diagrams: list[FailedDiagram]
    session_report: SessionReport


class AGAInternalState(AGAInputState):
    """Full working state of the graph. All nodes read/write this schema."""

    parsed_raa: RAAOutput | None
    diagram_queue: list[DiagramSpec]
    current_diagram: DiagramSpec | None
    current_puml_code: str
    retry_count: int
    completed_diagrams: Annotated[list[CompletedDiagram], operator.add]
    failed_diagrams: Annotated[list[FailedDiagram], operator.add]
    session_start_time: float
    session_report: SessionReport
