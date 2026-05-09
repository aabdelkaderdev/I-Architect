"""
Condition equivalence checking, condition group building,
and structured satisfiable group generation.

Contains the private-state pattern: check_condition_equivalence produces
EquivalenceOutput, and build_condition_groups consumes GroupBuilderInput.
These types are wired via add_sequence in Phase 3.
"""
from __future__ import annotations

from langchain_core.messages import HumanMessage
from langgraph.runtime import Runtime
from pydantic import BaseModel

from arlo.llm import render_template
from arlo.nodes.runtime import get_llm
from arlo.state.models import SatGroup
from arlo.state.schemas import (
    ARLOContext,
    ARLOState,
    EquivalenceOutput,
    GroupBuilderInput,
)


class EquivalenceResult(BaseModel):
    """Structured boolean result for condition equivalence."""
    is_equivalent: bool


# ---------------------------------------------------------------------------
# Condition Equivalence (private state producer)
# ---------------------------------------------------------------------------
def check_condition_equivalence(
    state: ARLOState,
    runtime: Runtime[ARLOContext] | None = None,
) -> EquivalenceOutput:
    """Node: Check pairwise condition equivalence via LLM.
    Reads: asrs, llm, cluster_assignments
    Writes (private): similarity_matrix → consumed by build_condition_groups
    """
    asrs: list[dict] = state["asrs"]
    llm = get_llm(state, runtime)
    cluster_assignments: list[int] = state["cluster_assignments"]
    similarity_matrix: list[tuple[int, int, bool]] = []

    _any = "under any circumstances"

    def is_equivalent(condition_a: str, condition_b: str) -> bool:
        prompt = render_template("condition_equivalence", {
            "condition_a": condition_a,
            "condition_b": condition_b,
        })
        result = llm.with_structured_output(EquivalenceResult).invoke([
            HumanMessage(content=prompt)
        ])
        return result.is_equivalent

    def group_by_cluster() -> dict[int, list[int]]:
        cluster_map: dict[int, list[int]] = {}
        for idx in active_indices:
            cluster_map.setdefault(cluster_assignments[idx], []).append(idx)
        return cluster_map

    if not asrs:
        return {"similarity_matrix": similarity_matrix}

    # Conditionless ASRs need no LLM comparison — handled entirely by build_condition_groups
    active_indices = [
        i for i, asr in enumerate(asrs)
        if (asr.get("condition_text") or "").strip().lower() != _any
    ]

    if not active_indices:
        return {"similarity_matrix": similarity_matrix}

    # Within each cluster, compare each condition against existing group nominals
    for cluster_indices in group_by_cluster().values():
        nominal_indices: list[int] = []

        for idx in cluster_indices:
            if not nominal_indices:
                nominal_indices.append(idx)
                continue

            equivalent_group_found = False
            for nominal_idx in nominal_indices:
                is_eq = is_equivalent(asrs[idx]["condition_text"], asrs[nominal_idx]["condition_text"])
                similarity_matrix.append((*sorted((idx, nominal_idx)), is_eq))

                if is_eq:
                    equivalent_group_found = True
                    break

            if not equivalent_group_found:
                nominal_indices.append(idx)

    return {"similarity_matrix": similarity_matrix}


# ---------------------------------------------------------------------------
# Condition Group Building (private state consumer)
# ---------------------------------------------------------------------------
def build_condition_groups(state: GroupBuilderInput) -> dict:
    """Node: Build condition groups from the similarity matrix and clusters.
    Reads (private): similarity_matrix, cluster_assignments, asrs
    Writes: condition_groups
    """
    similarity_matrix: list[tuple[int, int, bool]] = state["similarity_matrix"]
    cluster_assignments: list[int] = state["cluster_assignments"]
    asrs: list[dict] = state["asrs"]
    condition_groups: list[dict] = []

    _any = "under any circumstances"

    # O(1) lookup table — canonical key order (i < j) matches how matrix was written
    equiv_lookup: dict[tuple[int, int], bool] = {
        (i, j): is_eq for i, j, is_eq in similarity_matrix
    }

    def are_equivalent(i: int, j: int) -> bool:
        a, b = sorted((i, j))
        return equiv_lookup.get((a, b), False)

    def group_by_cluster() -> dict[int, list[int]]:
        cluster_map: dict[int, list[int]] = {}
        for idx in active_indices:
            cluster_map.setdefault(cluster_assignments[idx], []).append(idx)
        return cluster_map

    # 1. Conditionless ASRs → single shared group (mirrors C# conditionLessReqs block)
    conditionless_indices = [
        i for i, asr in enumerate(asrs)
        if (asr.get("condition_text") or "").strip().lower() == _any
    ]
    if conditionless_indices:
        condition_groups.append({
            "nominal_condition": asrs[conditionless_indices[0]]["condition_text"],
            "conditions": conditionless_indices,
            "requirements": [asrs[i] for i in conditionless_indices],
            "cluster": -1,
        })

    active_indices = [i for i in range(len(asrs)) if i not in set(conditionless_indices)]

    if not active_indices:
        return {"condition_groups": condition_groups}

    # 2. Replay the same sequential grouping algorithm used during equivalence
    #    checking, now driven by the lookup table instead of live LLM calls
    #    (mirrors C# clusterGroups loop inside foreach (var clusteredReqs in clusterMap))
    for cluster_id, cluster_indices in group_by_cluster().items():
        cluster_groups: list[dict] = []   # groups formed within this cluster

        for idx in cluster_indices:
            if not cluster_groups:
                cluster_groups.append({
                    "nominal_condition": asrs[idx]["condition_text"],
                    "nominal_idx": idx,
                    "conditions": [idx],
                    "requirements": [asrs[idx]],
                    "cluster": cluster_id,
                })
                continue

            equivalent_group_found = False
            for group in cluster_groups:
                if are_equivalent(idx, group["nominal_idx"]):
                    group["conditions"].append(idx)
                    group["requirements"].append(asrs[idx])
                    equivalent_group_found = True
                    break

            if not equivalent_group_found:
                cluster_groups.append({
                    "nominal_condition": asrs[idx]["condition_text"],
                    "nominal_idx": idx,
                    "conditions": [idx],
                    "requirements": [asrs[idx]],
                    "cluster": cluster_id,
                })

        condition_groups.extend(cluster_groups)

    # Strip internal bookkeeping key before writing to state
    for group in condition_groups:
        group.pop("nominal_idx", None)

    return {"condition_groups": condition_groups}

# ---------------------------------------------------------------------------
# Satisfiable Group Generation (LLM call)
# ---------------------------------------------------------------------------
def generate_satisfiable_groups(
    state: ARLOState,
    runtime: Runtime[ARLOContext] | None = None,
) -> dict:
    """Node: Organize conditions into co-satisfiable groups via structured LLM output.
    Reads: condition_groups, llm
    Writes: satisfiable_groups, sat_parse_success, sat_parse_attempts
    """
    llm = get_llm(state, runtime)
    condition_groups = state["condition_groups"]

    # Template already contains all instructions.
    # Only inject the numbered condition list, matching C# L372-375:
    # conditionGroups.Select(cg => conditionGroups.IndexOf(cg) + 1 + ":" + cg.NominalCondition)
    prompt_context: dict = {
        "conditions": "\n".join(
            f"{i + 1}:{cg['nominal_condition']}"
            for i, cg in enumerate(condition_groups)
        )
    }

    prompt_text = render_template("satisfiable_grouping", prompt_context)
    result = llm.with_structured_output(SatGroup).invoke([
        HumanMessage(content=prompt_text)
    ])

    satisfiable_groups: list[dict] = []
    for group_ids in result.group_ids:
        group_conditions = []
        for condition_id in group_ids:
            if condition_id < 1 or condition_id > len(condition_groups):
                raise ValueError(f"Condition group ID out of range: {condition_id}")
            group_conditions.append(condition_groups[condition_id - 1])
        satisfiable_groups.append({"condition_groups": group_conditions})

    return {
        "satisfiable_groups": satisfiable_groups,
        "sat_parse_success": True,
        "sat_parse_attempts": 0,
    }


# ---------------------------------------------------------------------------
# Satisfiable Group Parsing
# ---------------------------------------------------------------------------
def parse_sat_groups(state: ARLOState) -> dict:
    """Compatibility node for older Phase 3 graph shapes.

    `generate_satisfiable_groups` now writes parsed `satisfiable_groups`
    directly. Keep this as a no-op if Phase 3 still wires a generate → parse
    sequence; otherwise omit it from the graph.
    """
    return {
        "satisfiable_groups": state.get("satisfiable_groups", []),
        "sat_parse_success": state.get("sat_parse_success", True),
        "sat_parse_attempts": state.get("sat_parse_attempts", 0),
    }
