from pydantic import BaseModel, Field
from typing import Optional, Any

# =========================================================================
# Input Validation Models (Flat JSON structure)
# =========================================================================

class Entity(BaseModel):
    id: str
    name: str
    description: str
    c4_type: str
    technology: str = ""
    parent_system_id: Optional[str] = None
    parent_container_id: Optional[str] = None
    requirement_ids: list[str] = Field(default_factory=list)
    saam_score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)

class Relationship(BaseModel):
    id: str
    source_id: str
    target_id: str
    description: str
    relationship_type: str
    diagram_scope: str
    requirement_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class ArchModel(BaseModel):
    entities: list[Entity]
    relationships: list[Relationship]
    boundary_groups: list[dict[str, Any]] = Field(default_factory=list)
    cross_cutting_candidates: list[Any] = Field(default_factory=list)
    assumption_flags: list[str] = Field(default_factory=list)
    status: str

# =========================================================================
# Internal State Models
# =========================================================================

class DiagramSpec(BaseModel):
    diagram_id: str
    diagram_type: str
    focus_entity_id: str
    focus_entity_label: str = ""
    entities: list[dict[str, Any]] = Field(default_factory=list)
    relationships: list[dict[str, Any]] = Field(default_factory=list)

class CompletedDiagram(BaseModel):
    diagram_id: str
    diagram_type: str
    png_bytes: bytes
    plantuml_source: str
    output_path: str

class FailedDiagram(BaseModel):
    diagram_id: str
    diagram_type: str
    error_message: str
    attempts: int
    last_puml: str = ""

class SessionReport(BaseModel):
    completed_count: int
    failed_count: int
    total_diagrams_expected: int
    planturl_binary: str = ""
    detected_os: str = ""
    plantuml_server_url: str = ""
    wall_clock_seconds: float = 0.0
