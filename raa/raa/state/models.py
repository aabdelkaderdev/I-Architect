"""
Pydantic models for structured LLM output parsing.

Used with `llm.with_structured_output(Model, include_raw=True)` to replace
manual JSON parsing. All downstream nodes consume these canonical models.
"""
from pydantic import BaseModel, Field


class NormalizedRequirement(BaseModel):
    """Standardized requirement record used across all RAA phases.

    All RAA-internal requirement IDs carry the "R" prefix (e.g. "R5").
    ARLO-internal integer IDs are normalized during Phase 1 ingestion.
    """
    id: str                                          # "R5" format
    description: str
    is_asr: bool
    quality_attributes: list[str] = Field(default_factory=list)
    condition_text: str | None = None


# ── C4 Architecture Fragment Models (Story 2.1) ───────────────────────────


class C4Entity(BaseModel):
    """A C4 entity node — person, system, external_system, container, or component.

    Parent references enforce C4 hierarchy:
    - Containers must declare ``parent_system_id``.
    - Components must declare ``parent_container_id``.
    """
    id: str
    name: str
    description: str = ""
    c4_type: str = "container"
    technology: str = ""
    parent_system_id: str | None = None
    parent_container_id: str | None = None
    requirement_ids: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class C4Relationship(BaseModel):
    """A directed relationship between two C4 entities.

    ``diagram_scope`` reflects endpoint hierarchy depth:
    ``context`` for person/system/external_system endpoints,
    ``container`` for container endpoints, ``component`` for component endpoints.
    """
    id: str
    source_id: str
    target_id: str
    description: str = ""
    relationship_type: str = "uses"
    diagram_scope: str = ""
    metadata: dict = Field(default_factory=dict)


class ArchFragment(BaseModel):
    """Output from a single strategy subgraph (RAA-A, RAA-B, or RAA-C).

    Permissive by design for Story 2.1 — strict C4 hierarchy validation
    belongs to Story 2.2.
    """
    entities: list[C4Entity] = Field(default_factory=list)
    relationships: list[C4Relationship] = Field(default_factory=list)
    cross_cutting_candidates: list[str] = Field(default_factory=list)
    assumption_flags: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
