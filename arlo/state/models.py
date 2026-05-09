"""
Pydantic models for structured LLM output parsing.

Used with `llm.with_structured_output(Model)` to replace
manual JSON parsing from the C# codebase.
"""
from pydantic import BaseModel, Field


class ParsedRequirement(BaseModel):
    """Single requirement classification result from the LLM."""
    id: int
    is_architecturally_significant: bool
    quality_attributes: list[str] = Field(default_factory=list)
    condition_text: str = "under any circumstances"


class ParsedBatch(BaseModel):
    """A batch of parsed requirements returned by the LLM."""
    requirements: list[ParsedRequirement]


class MetricTrigger(BaseModel):
    """A metric–trigger pair extracted from a requirement."""
    metric: str
    trigger: str


class MetricTriggerData(BaseModel):
    """Metric triggers for a single requirement (currently disabled)."""
    id: int
    triggers: list[MetricTrigger]


class SatGroup(BaseModel):
    """Satisfiable group IDs returned by the LLM."""
    group_ids: list[list[int]]   # e.g., [[1,2],[3,4]]
