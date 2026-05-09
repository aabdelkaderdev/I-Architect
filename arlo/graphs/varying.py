"""
VaryingRequirements experiment graph.

Implements the C# VaryingRequirementsExperiment shape:
parse ASRs once, run one full decision round, then repeatedly remove a
batch of ASRs and re-run architectural decision selection.
"""
from __future__ import annotations

import random
from operator import add
from typing import Annotated

from langgraph.graph import END, START, StateGraph
from langgraph.types import Overwrite
from typing_extensions import TypedDict

from arlo.nodes.clustering import cluster_conditions
from arlo.nodes.embedding import generate_embeddings
from arlo.nodes.grouping import (
    build_condition_groups,
    check_condition_equivalence,
    generate_satisfiable_groups,
)
from arlo.nodes.optimization import assign_concern_workers, concern_worker
from arlo.nodes.parsing import parse_requirements
from arlo.nodes.weights import infer_quality_weights
from arlo.state.schemas import ARLOInput, ARLOOutput, ARLOState


class VaryingState(ARLOState, total=False):
    """Internal state for the VaryingRequirements experiment."""
    original_asrs: list[dict]
    removal_step: float
    removal_count: int
    varying_round: int
    varying_results: Annotated[list[dict], add]


def _removal_strategy_config(state: VaryingState) -> dict:
    """Read removal strategy config, accepting C# and Python naming styles."""
    experiment_config = state.get("experiment_config", {})
    return (
        experiment_config.get("removal_strategy")
        or experiment_config.get("removalStratgy")
        or {}
    )


def _quality_set(requirement: dict) -> set[str]:
    """Return normalized quality attributes for a parsed ASR."""
    return {
        str(quality).strip()
        for quality in requirement.get("quality_attributes", [])
        if str(quality).strip()
    }


def _candidate_asrs_for_removal(state: VaryingState) -> list[dict]:
    """Mirror RemoveAsrs candidate selection from the C# experiment."""
    asrs = list(state.get("asrs", []))
    strategy = _removal_strategy_config(state)
    kind = str(strategy.get("kind", "random")).lower()

    if kind == "targeted":
        desired_qas = {
            str(quality).strip()
            for quality in (
                strategy.get("desired_qas")
                or strategy.get("desiredQAs")
                or []
            )
            if str(quality).strip()
        }
        undesired_qas = {
            str(quality).strip()
            for quality in (
                strategy.get("undesired_qas")
                or strategy.get("undesiredQAs")
                or []
            )
            if str(quality).strip()
        }

        return [
            asr for asr in asrs
            if not (_quality_set(asr) & desired_qas)
            and bool(_quality_set(asr) & undesired_qas)
        ]

    seed = int(state.get("experiment_config", {}).get("removal_seed", 0))
    round_index = int(state.get("varying_round", 0))
    rng = random.Random(seed + round_index)
    rng.shuffle(asrs)
    return asrs


def initialize_varying(state: VaryingState) -> dict:
    """Initialize removal settings after ASR parsing.

    C# keeps an `asrsCopy` and computes:
        removeCount = (int)(asrsCopy.Count * 0.2)
    """
    asrs = list(state.get("asrs", []))
    experiment_config = state.get("experiment_config", {})
    removal_step = float(experiment_config.get("removal_step", 0.2))
    if removal_step <= 0:
        removal_step = 0.2

    return {
        "original_asrs": asrs,
        "removal_step": removal_step,
        "removal_count": int(len(asrs) * removal_step),
        "varying_round": 0,
        "varying_results": [],
        "concerns": Overwrite([]),
    }


def _prepare_varying_fan_out(state: VaryingState) -> dict:
    """Finalize per-round stats before Send API fan-out."""
    parsing_stats = state.get("parsing_stats", {})
    return {
        "stats": {
            **parsing_stats,
            "varying_round": state.get("varying_round", 0),
            "active_asr_count": len(state.get("asrs", [])),
            "condition_group_count": len(state.get("condition_groups", [])),
            "satisfiable_group_count": len(state.get("satisfiable_groups", [])),
            "quality_weight_count": len(state.get("quality_weights", {})),
        },
        "concerns": [],
    }


def record_round(state: VaryingState) -> dict:
    """Record the current decision round before trying to remove ASRs."""
    original_count = len(state.get("original_asrs", []))
    active_count = len(state.get("asrs", []))
    removed_count = max(original_count - active_count, 0)
    removed_ratio = removed_count / original_count if original_count else 0.0

    round_result = {
        "round": state.get("varying_round", 0),
        "active_asr_count": active_count,
        "removed_asr_count": removed_count,
        "removed_ratio": removed_ratio,
        "quality_weights": dict(state.get("quality_weights", {})),
        "concerns": list(state.get("concerns", [])),
    }
    all_results = [*state.get("varying_results", []), round_result]

    return {
        "varying_results": [round_result],
        "stats": {
            **state.get("stats", {}),
            "varying_rounds_completed": len(all_results),
            "varying_results": all_results,
        },
    }


def can_remove_more_asrs(state: VaryingState) -> str:
    """Route after recording a decision round."""
    remove_count = int(state.get("removal_count", 0))
    if remove_count <= 0:
        return "end"

    candidates = _candidate_asrs_for_removal(state)
    if not candidates:
        return "end"

    return "remove_asrs"


def remove_asrs(state: VaryingState) -> dict:
    """Remove one ASR batch, then reset per-round derived state.

    Mirrors the C# behavior:
    - random removal by default
    - targeted removal when the configured strategy requests it
    - remove at most `remove_count`
    - stop naturally when no candidates remain
    """
    asrs = list(state.get("asrs", []))
    candidates = _candidate_asrs_for_removal(state)
    remove_count = min(int(state.get("removal_count", 0)), len(candidates))

    if remove_count <= 0:
        return {}

    removed_ids = {
        asr.get("id")
        for asr in candidates[:remove_count]
    }
    remaining_asrs = [
        asr for asr in asrs
        if asr.get("id") not in removed_ids
    ]

    return {
        "asrs": remaining_asrs,
        "varying_round": int(state.get("varying_round", 0)) + 1,
        "embeddings": [],
        "cluster_assignments": [],
        "condition_groups": [],
        "satisfiable_groups": [],
        "sat_parse_attempts": 0,
        "sat_parse_success": False,
        "quality_weights": {},
        "stats": {},
        "concerns": Overwrite([]),
    }


def build_varying_reqs() -> StateGraph:
    """Build the VaryingRequirements experiment graph (uncompiled)."""
    builder = StateGraph(
        VaryingState,
        input_schema=ARLOInput,
        output_schema=ARLOOutput,
    )

    builder.add_node("parse_requirements", parse_requirements)
    builder.add_node("initialize_varying", initialize_varying)
    builder.add_node("generate_embeddings", generate_embeddings)
    builder.add_node("cluster_conditions", cluster_conditions)
    builder.add_node("generate_satisfiable_groups", generate_satisfiable_groups)
    builder.add_node("infer_quality_weights", infer_quality_weights)
    builder.add_node("assign_concern_workers", _prepare_varying_fan_out)
    builder.add_node("concern_worker", concern_worker)
    builder.add_node("record_round", record_round)
    builder.add_node("remove_asrs", remove_asrs)

    builder.add_sequence([check_condition_equivalence, build_condition_groups])

    # Parse once, then repeatedly run the decision pipeline over current ASRs.
    builder.add_edge(START, "parse_requirements")
    builder.add_edge("parse_requirements", "initialize_varying")
    builder.add_edge("initialize_varying", "generate_embeddings")
    builder.add_edge("generate_embeddings", "cluster_conditions")
    builder.add_edge("cluster_conditions", "check_condition_equivalence")
    builder.add_edge("build_condition_groups", "generate_satisfiable_groups")
    builder.add_edge("generate_satisfiable_groups", "infer_quality_weights")
    builder.add_edge("infer_quality_weights", "assign_concern_workers")

    builder.add_conditional_edges(
        "assign_concern_workers",
        assign_concern_workers,
        ["concern_worker"],
    )
    builder.add_edge("concern_worker", "record_round")

    builder.add_conditional_edges(
        "record_round",
        can_remove_more_asrs,
        {
            "remove_asrs": "remove_asrs",
            "end": END,
        },
    )
    builder.add_edge("remove_asrs", "generate_embeddings")

    return builder
