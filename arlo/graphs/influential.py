"""
InfluentialSets experiment graph.

Extends the core pipeline with sensitivity analysis over each baseline
concern. The implementation mirrors the C# experiment at graph level:
run ARLO once, then for each concern repeatedly lower quality weights for
candidate requirements and re-run optimization against the same satisfiable
group to find requirement sets that change decisions.
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from arlo.nodes.clustering import cluster_conditions
from arlo.nodes.embedding import generate_embeddings
from arlo.nodes.grouping import (
    build_condition_groups,
    check_condition_equivalence,
    generate_satisfiable_groups,
)
from arlo.nodes.optimization import (
    _run_optimizer,
    assign_concern_workers,
    concern_worker,
)
from arlo.nodes.parsing import parse_requirements
from arlo.nodes.weights import (
    infer_quality_weights,
    infer_weights_from_group,
    normalize_weights,
)
from arlo.state.config import ExperimentConfig
from arlo.state.schemas import ARLOContext, ARLOInput, ARLOOutput, ARLOState


class InfluentialState(ARLOState, total=False):
    """Internal state for the InfluentialSets experiment."""
    influential_sets: list[dict]


def _prepare_influential_fan_out(state: InfluentialState) -> dict:
    """Finalize baseline stats before Send API fan-out."""
    parsing_stats = state.get("parsing_stats", {})
    return {
        "stats": {
            **parsing_stats,
            "condition_group_count": len(state.get("condition_groups", [])),
            "satisfiable_group_count": len(state.get("satisfiable_groups", [])),
            "quality_weight_count": len(state.get("quality_weights", {})),
        },
        "concerns": [],
    }


def _assign_or_skip_concern_workers(state: InfluentialState) -> list[Send] | str:
    """Fan out to workers, or continue when no satisfiable groups exist."""
    sends = assign_concern_workers(state)
    if sends:
        return sends
    return "identify_influential_sets"


def _requirement_key(requirement: dict) -> object:
    """Stable identity for removing requirements from working lists."""
    return requirement.get("id", id(requirement))


def _quality_set(requirement: dict) -> set[str]:
    """Return normalized quality attributes for a parsed ASR."""
    return {
        str(quality).strip()
        for quality in requirement.get("quality_attributes", [])
        if str(quality).strip()
    }


def _requirements_for_concern(concern: dict) -> list[dict]:
    """Flatten condition-group requirements from a concern."""
    requirements: list[dict] = []
    for condition_group in concern.get("satisfiable_group", {}).get("condition_groups", []):
        requirements.extend(condition_group.get("requirements", []))
    return requirements


def _remove_requirement_once(requirements: list[dict], requirement: dict) -> list[dict]:
    """Remove one matching requirement, matching C# List.Remove behavior."""
    removed_key = _requirement_key(requirement)
    for index, candidate in enumerate(requirements):
        if _requirement_key(candidate) == removed_key:
            return [*requirements[:index], *requirements[index + 1:]]
    return requirements


def _weights_for_concern(concern: dict) -> dict[str, int]:
    """Get baseline concern weights, deriving them if the worker omitted them."""
    weights = dict(concern.get("weights", {}))
    if weights:
        return weights

    inferred = infer_weights_from_group(concern.get("satisfiable_group", {}))
    return normalize_weights(inferred)


def _optimize_concern(
    matrix: dict[str, dict[str, int]],
    weights: dict[str, int],
    config: ExperimentConfig,
) -> list[dict]:
    """Run optimization against an existing satisfiable group."""
    return _run_optimizer(matrix, weights, config)


def _changed_decisions(
    original_decisions: list[dict],
    new_decisions: list[dict],
) -> list[dict]:
    """Return decision changes keyed by architecture pattern name."""
    new_by_name = {
        decision.get("arch_pattern_name"): decision
        for decision in new_decisions
    }

    changed: list[dict] = []
    for original in original_decisions:
        new = new_by_name.get(original.get("arch_pattern_name"))
        if not new:
            continue

        if original.get("selected_pattern") != new.get("selected_pattern"):
            changed.append({
                "original": original,
                "new": new,
            })

    return changed


def _perform_qa_sensitivity_analysis(
    matrix: dict[str, dict[str, int]],
    config: ExperimentConfig,
    concern: dict,
    baseline_weights: dict[str, int],
) -> dict[str, float]:
    """Mirror PerformQASensitivityAnalysis for one concern.

    The C# code perturbs each quality by delta=max(weight), re-optimizes the
    same satisfiable group, and records how many selected patterns change.
    """
    if not baseline_weights:
        return {}

    delta = max(baseline_weights.values())
    original_decisions = list(concern.get("decisions", []))
    sensitivity: dict[str, float] = {}

    for quality in baseline_weights:
        perturbed_weights = dict(baseline_weights)
        perturbed_weights[quality] = max(perturbed_weights.get(quality, 0) - delta, 0)

        new_decisions = _optimize_concern(matrix, perturbed_weights, config)
        sensitivity[quality] = float(len(_changed_decisions(original_decisions, new_decisions)))

    return sensitivity


def _most_sensitive_quality(sensitivities: dict[str, float]) -> tuple[str, float]:
    """Return the highest sensitivity item, using C# Aggregate tie behavior."""
    _index, item = max(
        enumerate(sensitivities.items()),
        key=lambda indexed_item: (indexed_item[1][1], indexed_item[0]),
    )
    return item


def identify_influential_sets(state: InfluentialState) -> dict:
    """Identify influential requirement sets from baseline concerns.

    This follows the C# loop:
    - rank QAs by sensitivity
    - for each sensitive QA, remove contributing requirements from the
      satisfiable group by decrementing their QA weights
    - re-run optimization against the same satisfiable group
    - record the accumulated requirement set when any decision changes
    """
    matrix = state["matrix"]
    config = ExperimentConfig.from_dict(state.get("experiment_config", {}))

    influential_sets: list[dict] = []

    for concern_index, concern in enumerate(state.get("concerns", [])):
        baseline_weights = _weights_for_concern(concern)
        original_decisions = list(concern.get("decisions", []))
        sensitivities = _perform_qa_sensitivity_analysis(
            matrix,
            config,
            concern,
            baseline_weights,
        )

        working_weights = dict(baseline_weights)
        satisfiable_requirements = _requirements_for_concern(concern)
        influential_set: list[dict] = []

        while sensitivities:
            sensitive_quality, _score = _most_sensitive_quality(sensitivities)
            sensitivities.pop(sensitive_quality)

            if not sensitivities:
                break

            contributing_requirements = [
                requirement for requirement in satisfiable_requirements
                if sensitive_quality in _quality_set(requirement)
            ]

            for requirement in list(contributing_requirements):
                for quality in _quality_set(requirement):
                    working_weights[quality] = working_weights.get(quality, 0) - 1

                influential_set.append(requirement)

                satisfiable_requirements = _remove_requirement_once(
                    satisfiable_requirements,
                    requirement,
                )

                new_decisions = _optimize_concern(matrix, working_weights, config)
                changed = _changed_decisions(original_decisions, new_decisions)

                if changed:
                    influential_sets.append({
                        "concern_index": concern_index,
                        "changed_decisions": changed,
                        "requirements": list(influential_set),
                    })
                    influential_set = []
                    working_weights = dict(baseline_weights)

    counts_by_requirement_count: dict[int, int] = {}
    for influential_set in influential_sets:
        requirement_count = len(influential_set.get("requirements", []))
        counts_by_requirement_count[requirement_count] = (
            counts_by_requirement_count.get(requirement_count, 0) + 1
        )

    stats = {
        **state.get("stats", {}),
        "influential_set_count": len(influential_sets),
        "influential_sets": influential_sets,
        "influential_set_counts": {
            f"AIS of {requirement_count}": count
            for requirement_count, count in sorted(counts_by_requirement_count.items())
        },
    }

    return {
        "influential_sets": influential_sets,
        "stats": stats,
    }


def build_influential_sets() -> StateGraph:
    """Build the InfluentialSets experiment graph (uncompiled)."""
    builder = StateGraph(
        InfluentialState,
        input_schema=ARLOInput,
        output_schema=ARLOOutput,
        context_schema=ARLOContext,
    )

    builder.add_node("parse_requirements", parse_requirements)
    builder.add_node("generate_embeddings", generate_embeddings)
    builder.add_node("cluster_conditions", cluster_conditions)
    builder.add_node("generate_satisfiable_groups", generate_satisfiable_groups)
    builder.add_node("infer_quality_weights", infer_quality_weights)
    builder.add_node("assign_concern_workers", _prepare_influential_fan_out)
    builder.add_node("concern_worker", concern_worker)
    builder.add_node("identify_influential_sets", identify_influential_sets)

    builder.add_sequence([check_condition_equivalence, build_condition_groups])

    # Baseline ARLO run.
    builder.add_edge(START, "parse_requirements")
    builder.add_edge("parse_requirements", "generate_embeddings")
    builder.add_edge("generate_embeddings", "cluster_conditions")
    builder.add_edge("cluster_conditions", "check_condition_equivalence")
    builder.add_edge("build_condition_groups", "generate_satisfiable_groups")
    builder.add_edge("generate_satisfiable_groups", "infer_quality_weights")
    builder.add_edge("infer_quality_weights", "assign_concern_workers")

    builder.add_conditional_edges(
        "assign_concern_workers",
        _assign_or_skip_concern_workers,
        ["concern_worker", "identify_influential_sets"],
    )
    builder.add_edge("concern_worker", "identify_influential_sets")
    builder.add_edge("identify_influential_sets", END)

    return builder
