"""
Extraction Schemas — Pydantic DTOs for the Ingestion & Extraction layer.

Referenced by: FR-ING-005, FR-ING-015, FR-ING-012/013.
"""

from pydantic import BaseModel, Field


class ExtractedRequirement(BaseModel):
    """A single requirement extracted from an uploaded document."""

    id: str = Field(..., description="Unique ID: 'REQ-[FILE_HASH_PREFIX]-[INCR_ID]'.")
    description: str = Field(..., description="Raw requirement text.")
    source_file: str = Field(..., description="Original filename of the uploaded document.")
    extraction_method: str = Field(..., description="Strategy used: 'Line-by-Line', 'Regex', 'Grammar-Based', 'Hybrid'.")
    confidence_score: float = Field(default=1.0, description="Extraction confidence (0.0–1.0).")


class ExtractionResult(BaseModel):
    """Aggregate result of the extraction phase."""

    requirements: list[ExtractedRequirement] = Field(default_factory=list)
    total_extracted: int = Field(default=0)
    strategy_used: str = Field(default="")
    coverage_percent: float = Field(default=0.0, description="Extracted tokens / total document tokens.")
    csv_bypass: bool = Field(default=False, description="True if CSV schema bypass was triggered.")


class CoverageMetric(BaseModel):
    """Coverage and semantic drift quality metrics (FR-ING-012/013)."""

    coverage_ratio: float = Field(..., description="Extraction coverage (0.0–1.0).")
    drift_flagged_count: int = Field(default=0, description="Number of samples flagged for semantic drift.")
    total_sampled: int = Field(default=0, description="Total samples checked for drift.")
    passed: bool = Field(default=True, description="True if coverage >= 0.80 and drift < 15%.")
