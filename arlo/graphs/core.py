"""
Core ARLO pipeline graph construction.

build_arlo_subgraph() returns a compiled StateGraph that can be
embedded as a subgraph in the parent pipeline or run standalone.
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

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
from arlo.state.schemas import ARLOContext, ARLOInput, ARLOOutput, ARLOState


def build_arlo_subgraph() -> StateGraph:
    """Build and return the uncompiled ARLO StateGraph builder.

    The caller is responsible for compiling with a checkpointer:
        graph = build_arlo_subgraph().compile(checkpointer=checkpointer)

    Returns an uncompiled StateGraph so that the parent pipeline can
    control checkpointer and other compile-time settings.
    """
    builder = StateGraph(
        ARLOState,
        input_schema=ARLOInput,
        output_schema=ARLOOutput,
        context_schema=ARLOContext,
    )

    # ----- Register all nodes -----
    builder.add_node("parse_requirements", parse_requirements)
    builder.add_node("generate_embeddings", generate_embeddings)
    builder.add_node("cluster_conditions", cluster_conditions)
    builder.add_node("generate_satisfiable_groups", generate_satisfiable_groups)
    builder.add_node("infer_quality_weights", infer_quality_weights)
    builder.add_node("assign_concern_workers", _forward_to_fan_out)
    builder.add_node("concern_worker", concern_worker)

    # Private-state channel: equivalence → group builder
    builder.add_sequence([check_condition_equivalence, build_condition_groups])

    # ----- Sequential edges: START → parse → embed → cluster -----
    builder.add_edge(START, "parse_requirements")
    builder.add_edge("parse_requirements", "generate_embeddings")
    builder.add_edge("generate_embeddings", "cluster_conditions")

    # ----- Private-state sequence: cluster → equivalence → group builder -----
    builder.add_edge("cluster_conditions", "check_condition_equivalence")

    # ----- Sequential edge: group builder → satisfiable groups -----
    builder.add_edge("build_condition_groups", "generate_satisfiable_groups")

    # ----- Aggregate quality weights for ARLOOutput -----
    builder.add_edge("generate_satisfiable_groups", "infer_quality_weights")
    builder.add_edge("infer_quality_weights", "assign_concern_workers")

    # ----- Fan-out: Send API for parallel concern workers -----
    builder.add_conditional_edges(
        "assign_concern_workers",
        assign_concern_workers,
        ["concern_worker"],
    )

    # ----- Fan-in: all concern_workers → END -----
    builder.add_edge("concern_worker", END)

    return builder


def _forward_to_fan_out(state: ARLOState) -> dict:
    """Thin forwarding node that collects stats before fan-out.

    This node runs after aggregate quality-weight inference and before the
    Send API fan-out. It finalizes the stats dict with grouping metadata.
    """
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
