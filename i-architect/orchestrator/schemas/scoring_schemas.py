"""
Scoring Agent Schemas — Pydantic DTOs for architectural evaluation.

Referenced by: FR-SA-008, FR-SA-009, FR-SA-011.
Matches the SRS §9.6 JSON output schema exactly.
"""

from pydantic import BaseModel, Field
from typing import Optional


class SAScores(BaseModel):
    """Score breakdown across the 4 evaluation pillars."""

    total_percent_correct: float = Field(..., description="Weighted average: Syntax(20%) + Trace(20%) + Fidelity(30%) + SAAM(30%).")
    syntax_health: float = Field(..., description="Pillar 1: Syntactic & rendering validation (0–100).")
    traceability_score: float = Field(..., description="Pillar 2: Requirement ID traceability audit (0–100).")
    structural_fidelity: float = Field(..., description="Pillar 3: Entity/edge parity check (0–100).")
    saam_alignment: float = Field(..., description="Pillar 4: SAAM/ATAM quality attribute alignment (0–100).")


class SADrawback(BaseModel):
    """A single drawback/issue identified during evaluation."""

    severity: str = Field(..., description="'Critical', 'High', 'Medium', or 'Low'.")
    category: str = Field(..., description="Issue category (e.g., 'Missing Entity', 'Cyclic Dependency').")
    description: str = Field(..., description="Human-readable description of the issue.")
    affected_entities: list[str] = Field(default_factory=list, description="Entity names/IDs affected.")


class SAEvaluationMetadata(BaseModel):
    """Metadata for the scoring context."""

    target_framework: str = Field(..., description="'C4_Container' or 'UML_Component'.")
    arlo_reference_id: Optional[str] = Field(default=None, description="ARLO reference ID if ARLO was enabled.")


class SAStatus(BaseModel):
    """Rendering and regeneration status flags."""

    is_renderable: bool = Field(default=True, description="True if diagram compiled successfully.")
    recommend_regeneration: bool = Field(default=False, description="True if total_percent_correct < 70% or any pillar < 50%.")


class SADivergenceWarning(BaseModel):
    """Divergence warning for Workflow 3 parallel scoring (FR-SA-011)."""

    pillar_name: str = Field(..., description="Name of the divergent pillar.")
    scores: dict[str, float] = Field(default_factory=dict, description="Instance → score mapping.")
    range_percent: float = Field(..., description="Max - Min score difference.")
    outlier_instance: str = Field(..., description="Name of the outlier LLM instance.")
    median_score: float = Field(..., description="Computed median score.")


class SAEvaluation(BaseModel):
    """Complete SA evaluation output (FR-SA-008).

    This is the primary output contract of the Scoring Agent.
    """

    evaluation_metadata: SAEvaluationMetadata
    scores: SAScores
    status: SAStatus = Field(default_factory=SAStatus)
    drawbacks: list[SADrawback] = Field(default_factory=list)
    adjustments_needed: list[str] = Field(default_factory=list, description="Imperative fix commands.")
    divergence_warning: Optional[SADivergenceWarning] = Field(default=None, description="Workflow 3 only.")
