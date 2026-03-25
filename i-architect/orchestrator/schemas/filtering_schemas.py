"""
Filtering Agent Schemas — Pydantic DTOs for noise classification.

Referenced by: FR-FILT-003, FR-FILT-007, FR-FILT-008.
"""

from pydantic import BaseModel, Field


class FilteringInput(BaseModel):
    """Input payload for a single filtering batch item."""

    id: str = Field(..., description="Requirement ID.")
    text: str = Field(..., description="Raw requirement description.")


class FilteringOutput(BaseModel):
    """LLM output for a single requirement's noise classification."""

    id: str = Field(..., description="Requirement ID.")
    is_noisy: bool = Field(..., description="True if classified as noise.")
    confidence: float = Field(..., description="Classification confidence (0.0–1.0).")


class FilteringDetailedOutput(BaseModel):
    """Extended filtering output with reasoning (internal use only)."""

    id: str = Field(..., description="Requirement ID.")
    is_noisy: bool = Field(..., description="True if classified as noise.")
    confidence_score: float = Field(..., description="Classification confidence.")
    primary_pattern_detected: str = Field(default="", description="Matched pattern type (e.g., 'Stack Trace', 'Meeting Logistics').")
    reasoning: str = Field(default="", description="1–2 sentence justification (discarded from CSV output).")


class FilteringBatchResult(BaseModel):
    """Aggregate result for a filtering batch."""

    batch_index: int = Field(..., description="Batch sequence number.")
    input_count: int = Field(..., description="Number of items sent to LLM.")
    output_count: int = Field(..., description="Number of items returned by LLM.")
    results: list[FilteringOutput] = Field(default_factory=list)
    method: str = Field(default="LLM", description="'LLM', 'Regex', or 'Fallback'.")
