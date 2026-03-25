"""
TOON IR Schema — Trade-off Optimized Option Notation.

Pydantic models defining the intermediate representation used to pass
architectural blueprints between ARLO → RAA → AGA → SA.
Referenced by: FR-RAA-012, FR-ARLO-019, IR-AGA-001.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ToonEntity(BaseModel):
    """A single architectural entity in the TOON IR.

    Maps to components, containers, databases, or external systems
    identified by the RAA from requirements analysis.
    """

    id: str = Field(..., description="Unique entity identifier (e.g., 'container_001').")
    type: str = Field(..., description="Entity type: 'Container', 'Component', 'Database', 'ExternalSystem', 'Actor'.")
    name: str = Field(..., description="Human-readable entity name.")
    tech: str = Field(..., description="Technology stack (e.g., 'React', 'PostgreSQL'). Never null.")
    rationale: str = Field(default="", description="Reasoning for this entity's inclusion.")
    mapped_requirements: list[str] = Field(default_factory=list, description="List of Requirement IDs this entity satisfies.")


class ToonRelationship(BaseModel):
    """A data flow or dependency between two TOON entities."""

    source: str = Field(..., description="Source entity ID.")
    target: str = Field(..., description="Target entity ID.")
    action: str = Field(..., description="Verb describing the interaction (e.g., 'sends data to').")
    type: str = Field(..., description="Interaction type: 'Synchronous' or 'Asynchronous'.")
    protocol: str = Field(..., description="Communication protocol (e.g., 'HTTPS', 'gRPC', 'REST'). Never null.")


class ToonLayoutHints(BaseModel):
    """Layout hints for diagram generation by the AGA."""

    grouping: list[dict[str, list[str]]] = Field(default_factory=list, description="Boundary groupings for system partitions.")
    alignment: str = Field(default="Top-Down", description="Layout direction: 'Top-Down' or 'Left-to-Right'.")
    focus_node: Optional[str] = Field(default=None, description="Primary entity to center the diagram around.")


class ToonMetadata(BaseModel):
    """Metadata block for the TOON IR payload."""

    target_framework: str = Field(..., description="'C4_Container' or 'UML_Component'.")
    arlo_reference: Optional[str] = Field(default=None, description="ARLO reference ID: 'EXP-{SystemName}-{BatchID}'.")
    logic_priority: str = Field(default="Requirements-First", description="Logic priority mode.")
    agent_mode: str = Field(default="Standalone", description="'ARLO-Downstream' or 'Standalone'.")


class ToonIR(BaseModel):
    """Complete TOON Intermediate Representation payload.

    This is the primary data contract between RAA output and AGA input.
    Also consumed by the SA for structural fidelity checking.
    """

    metadata: ToonMetadata
    system_boundary: str = Field(..., description="Top-level system name/boundary.")
    entities: list[ToonEntity] = Field(default_factory=list)
    flow_logic: list[ToonRelationship] = Field(default_factory=list)
    layout_hints: ToonLayoutHints = Field(default_factory=ToonLayoutHints)
