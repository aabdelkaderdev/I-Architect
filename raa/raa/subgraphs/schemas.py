"""
Private TypedDict schemas for strategy subgraphs (Story 2.1).

Each subgraph receives a controlled subset of parent RAAState so that
the full parent state is never exposed to strategy execution.
"""
from __future__ import annotations

from typing import NotRequired

from typing_extensions import TypedDict

from raa.state.models import ArchFragment


class StrategySubgraphInput(TypedDict):
    """Private input mapped from parent RAAState before subgraph invocation."""
    batch: dict
    quality_weights: dict[str, int]
    running_model: dict
    bridge_requirements: list[dict]
    strategy: str
    reduced_confidence: bool


class StrategySubgraphState(StrategySubgraphInput):
    """Private state accumulated during subgraph execution."""
    arch_fragment: NotRequired[ArchFragment]
    open_questions: NotRequired[list[dict]]
    intermediate: NotRequired[dict]
    error: NotRequired[str]


class StrategySubgraphOutput(TypedDict):
    """Normalized output returned to the parent after subgraph execution."""
    arch_fragment: ArchFragment
    open_questions: NotRequired[list[dict]]
