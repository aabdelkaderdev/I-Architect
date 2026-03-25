"""
ARLO Schemas — Pydantic DTOs for the ARLO optimization pipeline.

Migrated from legacy C# models (Requirement.cs, Decision.cs, Matrix.cs,
Concern.cs, SatisfiableGroup.cs) with extensions for v2.3 pipeline integration.

Referenced by: FR-ARLO-001–022, IR-ARLO-001/002.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class QualityAttribute(str, Enum):
    """Fixed taxonomy of 8 quality attributes (FR-ARLO-007).

    Maps to legacy QA acronyms: PE, CO, US, RE, SE, MA, PO, CE.
    """

    PERFORMANCE_EFFICIENCY = "PE"
    COMPATIBILITY = "CO"
    USABILITY = "US"
    RELIABILITY = "RE"
    SECURITY = "SE"
    MAINTAINABILITY = "MA"
    PORTABILITY = "PO"
    COST_EFFICIENCY = "CE"


class ArloRequirement(BaseModel):
    """ARLO internal requirement model.

    Migrated from legacy Requirement.cs. Key changes in v2.3:
    - `id` is now a pipeline string ID (e.g., 'REQ-a1b2c3-001'), not auto-int.
    - Added `user_override` and `source_context` fields.
    - Removed legacy: `Parsed`, `CreatedDate`, `LastModifiedDate`, `IsNFR`.
    """

    id: str = Field(..., description="Pipeline-provided Requirement ID (e.g., 'REQ-a1b2c3-001').")
    description: str = Field(..., description="Raw requirement description text.")
    source_context: str = Field(default="", description="Extraction metadata for traceability.")
    user_override: bool = Field(default=False, description="If True, ARLO never drops this requirement (FR-ARLO-003).")
    is_noisy: bool = Field(default=False, description="Filtering Agent's noise classification.")
    confidence_score: float = Field(default=1.0, description="Filtering confidence (0.0–1.0).")
    is_architecturally_significant: Optional[bool] = Field(default=None, description="LLM classification result.")
    quality_attributes: list[QualityAttribute] = Field(default_factory=list, description="Extracted QAs from the fixed taxonomy.")
    condition_text: str = Field(default="under any circumstances", description="Conditional statement or default.")
    condition_embeddings: list[float] = Field(default_factory=list, description="Vector embeddings for condition grouping.")


class ArloDecision(BaseModel):
    """An architectural decision selected by the optimizer.

    Migrated from legacy Decision.cs. Now includes scored trade-offs.
    """

    category: str = Field(..., description="Architectural decision category (e.g., 'Database Management').")
    selected_pattern: str = Field(..., description="Selected architectural pattern name.")
    weighted_score: float = Field(..., description="Weighted score from the optimization.")
    satisfied_qas: list[dict[str, float]] = Field(default_factory=list, description="QAs positively impacted [{qa, score}].")
    trade_offs: list[dict[str, float]] = Field(default_factory=list, description="QAs negatively impacted [{qa, score}].")
    primary_driver_ids: list[str] = Field(default_factory=list, description="Requirement IDs that primarily drove this decision.")


class ConditionGroup(BaseModel):
    """A group of semantically similar conditions (FR-ARLO-011)."""

    group_id: int = Field(..., description="Unique group identifier.")
    condition_texts: list[str] = Field(default_factory=list, description="Condition strings in this group.")
    requirement_ids: list[str] = Field(default_factory=list, description="Requirement IDs sharing this condition.")


class SatisfiableGroup(BaseModel):
    """A set of requirements that must be satisfied simultaneously."""

    group_id: int = Field(..., description="Unique satisfiable group identifier.")
    requirement_ids: list[str] = Field(default_factory=list, description="IDs of requirements in this group.")
    condition_group_ids: list[int] = Field(default_factory=list, description="Condition groups included in this satisfiable group.")


class InfluentialSet(BaseModel):
    """An Architecturally Influential Set from sensitivity analysis (FR-ARLO-018)."""

    rank: int = Field(..., description="Sensitivity rank (1 = most influential).")
    target_qa: str = Field(..., description="The quality attribute most affected.")
    impacted_decisions: list[str] = Field(default_factory=list, description="Decision categories that changed.")
    ais_requirement_ids: list[str] = Field(default_factory=list, description="Requirement IDs in this influential set.")


class ArloExecutionMetadata(BaseModel):
    """Metadata for an ARLO execution run."""

    system_name: str = Field(..., description="Name of the analyzed system.")
    optimization_strategy: str = Field(..., description="'ILP' or 'Greedy'.")
    arlo_reference: str = Field(..., description="Reference ID: 'EXP-{SystemName}-{BatchID}'.")
    batch_size: int = Field(default=10, description="Number of requirements per batch.")


class ArloToonPayload(BaseModel):
    """Complete ARLO output payload in TOON format (FR-ARLO-019).

    Contains Alpha (decisions), Beta (influential sets), Gamma (ASR registry).
    """

    arlo_execution_metadata: ArloExecutionMetadata
    alpha_decisions: list[ArloDecision] = Field(default_factory=list, description="Selected patterns per category.")
    beta_influential_sets: list[InfluentialSet] = Field(default_factory=list, description="Sensitivity analysis results.")
    gamma_asr_registry: dict = Field(
        default_factory=lambda: {
            "total_input_requirements": 0,
            "total_asrs": 0,
            "asr_ids": [],
            "discarded_ids": [],
        },
        description="ASR identification summary.",
    )


class ArloConfig(BaseModel):
    """Configuration for an ARLO run, set from the UI (FR-ARLO-017)."""

    optimization_strategy: str = Field(default="ILP", description="'ILP' or 'Greedy'.")
    batch_size: int = Field(default=10, description="Requirements per LLM batch.")
    ilp_timeout_seconds: int = Field(default=120, description="ILP solver wall-clock timeout.")
