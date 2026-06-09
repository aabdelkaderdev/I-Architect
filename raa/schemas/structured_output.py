"""Pydantic models used only for LangChain structured-output binding.

These models intentionally keep business validation light. The RAA validators
remain the source of truth for naming rules, C4 literals, and merge invariants.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RawEntityProposalOutput(BaseModel):
    """Entity proposal emitted by ASR and Non-ASR LLM calls."""

    model_config = ConfigDict(extra="allow")

    proposed_name: str = Field(default="", description="PascalCase entity name.")
    c4_level: str = Field(
        default="container",
        description="system, container, or component.",
    )
    c4_type: str = Field(
        default="service",
        description="service, database, gateway, queue, store, external, or actor.",
    )
    description: str = Field(
        default="",
        description="One-to-two sentence entity description.",
    )
    responsibilities: list[str] = Field(
        default_factory=list,
        description="Entity responsibilities.",
    )
    source_requirements: list[str] = Field(
        default_factory=list,
        description="Requirement IDs justifying the proposal.",
    )
    proposing_subgraph: str = Field(default="", description="asr or non_asr.")
    concern_technology: str | None = Field(
        default=None,
        description="Optional concern-scoped technology.",
    )
    justification: str = Field(
        default="",
        description="Reasoning for the proposed entity.",
    )


class EntityProposalListOutput(BaseModel):
    """Wrapper for lists of entity proposals."""

    proposals: list[RawEntityProposalOutput] = Field(default_factory=list)


class RawJudgedProposalOutput(BaseModel):
    """Judge annotation for a proposal.

    Judge outputs intentionally do not carry a nested proposal object. The
    Judge annotates trusted proposals supplied by the ASR/Non-ASR nodes; code in
    judge_node.py reattaches these annotations by proposal_ref/name/index.
    """

    model_config = ConfigDict(extra="allow")

    proposal_ref: str = Field(
        default="",
        description="Stable proposal reference from the prompt, e.g. P001.",
    )
    proposed_name: str = Field(
        default="",
        description="Proposal name, used as a fallback matching key.",
    )
    scenario_classification: str = Field(default="direct")
    satisfied_requirements: list[str] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)


class RawCoverageGapOutput(BaseModel):
    """Coverage gap emitted by the Judge."""

    model_config = ConfigDict(extra="allow")

    requirement_id: str = Field(default="")
    requirement_text: str = Field(default="")
    batch_id: str = Field(default="")
    gap_reason: str = Field(default="")


class RawConflictRecordOutput(BaseModel):
    """Conflict record emitted by the Judge."""

    model_config = ConfigDict(extra="allow")

    requirement_ids: list[str] = Field(default_factory=list)
    entity_name: str = Field(default="")
    conflict_description: str = Field(default="")
    batch_id: str = Field(default="")
    resolution: str = Field(default="unresolved")


class JudgeClassificationOutput(BaseModel):
    """Structured output for SAAM Step 3."""

    classified: list[RawJudgedProposalOutput]


class JudgeCoverageOutput(BaseModel):
    """Structured output for SAAM Step 4."""

    judged: list[RawJudgedProposalOutput]
    coverage_gaps: list[RawCoverageGapOutput] = Field(default_factory=list)


class JudgeInteractionOutput(BaseModel):
    """Structured output for SAAM Step 5."""

    judged: list[RawJudgedProposalOutput]
    conflicts: list[RawConflictRecordOutput] = Field(default_factory=list)


def dump_structured_response(response: object) -> Any:
    """Convert Pydantic structured-output responses to plain Python containers."""
    if isinstance(response, BaseModel):
        return response.model_dump()
    return response
