"""
Quality attribute weight inference from satisfiable groups.
"""
from __future__ import annotations

from arlo.state.schemas import ARLOState


def infer_weights_from_group(satisfiable_group: dict) -> dict[str, int]:
    """Infer quality attribute weights from a single satisfiable group.

    Equivalent to populating C# `Concern.DesiredQualities`: collect the
    requirements contained in this concern's condition groups, then count
    how often each quality attribute appears.
    """
    desired_qualities: dict[str, int] = {}

    for condition_group in satisfiable_group.get("condition_groups", []):
        for requirement in condition_group.get("requirements", []):
            # A malformed LLM output should not let the same quality inflate
            # a single requirement's weight more than once.
            qualities = {
                str(quality).strip()
                for quality in requirement.get("quality_attributes", [])
                if str(quality).strip()
            }

            for quality in qualities:
                desired_qualities[quality] = desired_qualities.get(quality, 0) + 1

    return desired_qualities


def normalize_weights(weights: dict[str, int]) -> dict[str, int]:
    """Normalize quality weights to percentages using C# integer semantics."""
    total_weight = sum(weights.values())
    if total_weight == 0:
        return {}

    return {
        quality: weight * 100 // total_weight
        for quality, weight in weights.items()
    }


def infer_quality_weights(state: ARLOState) -> dict:
    """Node: Produce aggregate quality weights for ARLOOutput/reporting.

    Reads: satisfiable_groups
    Writes: quality_weights

    Optimization uses per-group weights via `infer_weights_from_group`.
    This node aggregates per-group weights so `ARLOOutput.quality_weights`
    has a clear top-level meaning.
    """
    satisfiable_groups = state.get("satisfiable_groups", [])

    quality_weights: dict[str, int] = {}
    for satisfiable_group in satisfiable_groups:
        for quality, weight in infer_weights_from_group(satisfiable_group).items():
            quality_weights[quality] = quality_weights.get(quality, 0) + weight

    return {"quality_weights": quality_weights}
