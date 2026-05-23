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
