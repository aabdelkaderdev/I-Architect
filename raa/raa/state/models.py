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
    saam_score: float = Field(default=0.0)
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


class SAAMScenario(BaseModel):
    """A SAAM scenario evaluated against a candidate architecture fragment.

    Each scenario describes a stimulus/context/response, maps to quality
    attributes, and records a satisfaction level.
    """
    id: str
    description: str
    quality_attributes: list[str] = Field(default_factory=list)
    satisfaction: str = "unknown"  # "satisfied", "partial", "unsatisfied", "unknown"
    requirement_ids: list[str] = Field(default_factory=list)
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
    saam_scenarios: list[SAAMScenario] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class FragmentScore(BaseModel):
    """Deterministic score for an ArchFragment produced by a strategy subgraph.

    Records enough metadata for auditable tie-breaking and later merge work.
    """
    batch_id: str
    batch_index: int
    strategy: str
    thread_id: str
    raw_score: float
    multiplier: float
    final_score: float
    scenario_contributions: list[dict] = Field(default_factory=list)
    is_primary: bool = False


# ── Human Review Models (Story 3.1) ──────────────────────────────────────────


class OpenQuestion(BaseModel):
    """A classified open question for human review payload generation.

    Questions are categorized as ``human_preferred`` (requires human judgment)
    or ``judge_resolvable`` (can be auto-resolved by the Judge).
    """
    id: str = Field(description="Unique deterministic identifier for the question.")
    question_type: str = Field(description="The category of question (e.g., contention, hierarchy_conflict).")
    description: str = Field(description="Human-readable description of the issue or conflict.")
    context: dict = Field(default_factory=dict, description="Contextual parameters and C4 entity references.")
    resolution_owner: str = Field(default="human_preferred", description="Determines who/what resolves this ('human_preferred' or 'judge_resolvable').")
    resolution: str | None = Field(default=None, description="Pre-computed suggested resolution for the conflict.")
    assumption_flag: bool = Field(default=False, description="Flag indicating if the suggestion is based on default assumptions.")
    metadata: dict = Field(default_factory=dict, description="Additional system metadata for audit trails.")
