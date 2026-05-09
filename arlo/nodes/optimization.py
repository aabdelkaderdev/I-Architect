"""
ILP / Greedy optimization and concern_worker fan-out.

The concern_worker is the target of the Send API fan-out — it receives
a ConcernWorkerState slice and processes a single satisfiable group.
"""
from __future__ import annotations

from langgraph.types import Send

from arlo.state.config import ExperimentConfig
from arlo.state.schemas import ARLOState, ConcernWorkerState
from arlo.nodes.weights import infer_weights_from_group, normalize_weights


# ---------------------------------------------------------------------------
# Fan-out Router (used as a conditional edge in Phase 3)
# ---------------------------------------------------------------------------
def assign_concern_workers(state: ARLOState) -> list[Send]:
    """Fan-out: one Send per satisfiable group.

    Called as a conditional edge function. Returns a list of Send objects
    that dispatch each satisfiable group to its own concern_worker instance.
    """
    return [
        Send("concern_worker", {
            "satisfiable_group": sg,
            "matrix": state["matrix"],
            "experiment_config": state["experiment_config"],
        })
        for sg in state.get("satisfiable_groups", [])
    ]


# ---------------------------------------------------------------------------
# Concern Worker (Send API target)
# ---------------------------------------------------------------------------
def concern_worker(state: ConcernWorkerState) -> dict:
    """Worker node: infer weights → normalize → optimize → assemble concern.

    Each worker receives a ConcernWorkerState slice with a single
    satisfiable group. Results are collected via the `add` reducer
    on `concerns` in the parent ARLOState.
    """
    sg = state["satisfiable_group"]
    matrix = state["matrix"]
    config = ExperimentConfig.from_dict(state["experiment_config"])

    # Step 1: Infer weights for this specific group
    weights = infer_weights_from_group(sg)

    # Step 2: Normalize weights
    normalized = normalize_weights(weights)

    # Step 3: Run optimizer
    decisions = _run_optimizer(matrix, normalized, config)

    # Step 4: Assemble concern
    concern = {
        "satisfiable_group": sg,
        "weights": normalized,
        "decisions": decisions,
    }
    return {"concerns": [concern]}


# ---------------------------------------------------------------------------
# Internal optimizer helpers
# ---------------------------------------------------------------------------
def _run_optimizer(
    matrix: dict[str, dict[str, int]],
    weights: dict[str, int],
    config: ExperimentConfig,
) -> list[dict]:
    """Run ILP or Greedy optimization based on experiment config."""
    if config.optimizer == "ILP":
        return _run_ilp(matrix, weights)
    else:
        return _run_greedy(matrix, weights)



def _run_ilp(
    matrix: dict[str, dict[str, int]],
    weights: dict[str, int],
    groups: dict[str, str] | None = None,  # row_name -> group_name (mirrors matrix.RowGroups)
    desired_qualities: list[str] | None = None,  # if None, all columns in `weights` are used
) -> list[dict]:
    """
    Integer Linear Programming optimization using python-mip.

    Args:
        matrix:             { row_name: { column_name: int_value } }
                            Each row is a candidate pattern; columns are quality attributes.
        weights:            { column_name: int_weight }
                            Importance weight for each quality column.
        groups:             { row_name: group_name }  (optional)
                            When supplied, enforces that exactly ONE row is selected
                            per group — mirroring the C# OnlyOneRowInGroup constraint.
        desired_qualities:  Subset of column names to consider in scoring.
                            Defaults to all keys present in `weights`.

    Returns:
        List of decision dicts, one per selected row:
            {
                "arch_pattern_name": str,    # group name (or row name when no groups)
                "selected_pattern":  str,    # row name
                "score":             int,
                "satisfied_qualities":   [(col, val), ...],  # val > 0
                "unsatisfied_qualities": [(col, val), ...],  # val < 0
            }
    """
    import mip
    from mip import Model, xsum, BINARY, MAXIMIZE, OptimizationStatus

    if not matrix:
        return []

    # ── Resolve desired qualities ────────────────────────────────────────────
    desired = set(desired_qualities) if desired_qualities else set(weights.keys())

    # ── Build model ──────────────────────────────────────────────────────────
    model = Model(sense=MAXIMIZE)
    model.verbose = 0  # suppress solver output

    # Binary variable x[row] ∈ {0, 1}: 1 = pattern is selected
    x: dict[str, mip.Var] = {
        row: model.add_var(name=row, var_type=BINARY)
        for row in matrix
    }

    # ── Constraints: exactly one row per group ───────────────────────────────
    # Mirrors: constraint.SetCoefficient(variables[row.Key], 1)  with lb=ub=1
    if groups:
        unique_groups = set(groups.values())
        for group in unique_groups:
            group_rows = [row for row, g in groups.items() if g == group and row in x]
            if group_rows:
                model += xsum(x[row] for row in group_rows) == 1, f"OnlyOneRowInGroup_{group}"
    # Without group info the ILP still runs; every row is a free binary choice.

    # ── Objective: maximise weighted quality coverage ────────────────────────
    # rowScore = Σ  cell_value * column_weight   for all (col ∈ desired) in that row
    def row_score(row: str) -> int:
        return sum(
            val * weights.get(col, 0)
            for col, val in matrix[row].items()
            if col in desired
        )

    model.objective = xsum(row_score(row) * x[row] for row in matrix)

    # ── Solve ────────────────────────────────────────────────────────────────
    status = model.optimize()

    if status not in (OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE):
        return []

    # ── Extract decisions ────────────────────────────────────────────────────
    # Mirrors the C# post-solve loop: only emit rows whose variable == 1
    decisions: list[dict] = []

    # Determine arch_pattern_name: group label when groups are provided,
    # otherwise fall back to the row name itself.
    def arch_name(row: str) -> str:
        return groups[row] if (groups and row in groups) else row

    # When groups are active, emit only ONE decision per group (the selected row),
    # matching the C# `break` after finding the first selected row in each group.
    emitted_groups: set[str] = set()

    for row, cols in matrix.items():
        var = x[row]
        if var.x is None or var.x < 0.5:   # not selected
            continue

        group_label = arch_name(row)

        # Skip duplicates if the ILP somehow selected two rows in the same group
        if groups and group_label in emitted_groups:
            continue
        emitted_groups.add(group_label)

        # Compute per-row details (mirrors the C# inner loop)
        score = 0
        satisfied: list[tuple[str, int]] = []
        unsatisfied: list[tuple[str, int]] = []

        for col, val in cols.items():
            if col not in desired:
                continue
            score += val * weights.get(col, 0)
            if val > 0:
                satisfied.append((col, val))
            elif val < 0:
                unsatisfied.append((col, val))

        decisions.append({
            "arch_pattern_name":    group_label,
            "selected_pattern":     row,
            "score":                score,
            "satisfied_qualities":  satisfied,
            "unsatisfied_qualities": unsatisfied,
        })

    return decisions


def _run_greedy(
    matrix: dict[str, dict[str, int]],
    weights: dict[str, int],
    groups: dict[str, str] | None = None,  # row_name -> group_name (mirrors matrix.RowGroups)
    desired_qualities: list[str] | None = None,  # if None, all columns in `weights` are used
) -> list[dict]:
    """Greedy optimizer.

    Mirrors the C# implementation: for each architecture pattern group,
    score every row in that group and keep the row with the highest weighted
    score. Ties keep the first row encountered because the update condition is
    strict `>`, matching the C# `if (rowValue > decision.Score)`.
    """
    if not matrix:
        return []

    desired = set(desired_qualities) if desired_qualities else set(weights.keys())

    # Build row groups in insertion order, mirroring RowGroups.GroupBy(...).
    rows_by_group: dict[str, list[str]] = {}
    for row in matrix:
        group = groups.get(row, row) if groups else row
        rows_by_group.setdefault(group, []).append(row)

    decisions: list[dict] = []

    for group, rows in rows_by_group.items():
        best_decision: dict | None = None
        best_score = -2**31  # mirrors int.MinValue closely enough for scoring

        for row in rows:
            satisfied_qualities: list[tuple[str, int]] = []
            unsatisfied_qualities: list[tuple[str, int]] = []
            row_value = 0

            for column, value in matrix[row].items():
                if column not in desired:
                    continue

                row_value += value * weights.get(column, 0)

                if value > 0:
                    satisfied_qualities.append((column, value))
                elif value < 0:
                    unsatisfied_qualities.append((column, value))

            if row_value > best_score:
                best_score = row_value
                best_decision = {
                    "arch_pattern_name": group,
                    "selected_pattern": row,
                    "score": row_value,
                    "satisfied_qualities": satisfied_qualities,
                    "unsatisfied_qualities": unsatisfied_qualities,
                }

        if best_decision is not None:
            decisions.append(best_decision)

    return decisions
