# Pattern Selection — Skill Reference

## 1. Purpose

Guidelines for selecting architectural patterns from the quality-architecture pattern matrix (`data/matrix.json`). Used primarily by the RAA-B (pattern-driven) subgraph. References Quality_Attributes.md for attribute definitions.

## 2. Input

- **Batch requirements** (normalized): `list[dict]` with quality attribute classifications from ARLO.
- **Quality-architecture matrix**: `dict[str, dict[str, int]]` — pre-loaded mapping of quality attributes to pattern support scores.
- **ARLO quality weights**: `dict[str, int]` — aggregate frequency counts per quality attribute.
- **Experiment configuration**: `dict` including optimizer selection (ILP or Greedy).

## 3. Normative rules

1. **Optimizer precedence:** Use the ILP (Integer Linear Programming) optimizer when the `experiment_config.optimizer` is `"ILP"` and the matrix dimensions permit. Fall back to Greedy when ILP would exceed solving time limits.
2. **Quality-attribute mapping:** Every selected pattern must explicitly reference the quality attributes it addresses. The mapping must be traceable to the quality-architecture matrix.
3. **Pattern compatibility:** Some patterns are mutually incompatible (e.g., monolithic and microservices). Check the matrix compatibility rules before selecting multiple patterns.
4. **Coverage requirement:** Selected patterns must collectively cover at least 80% of the batch's active quality attributes.
5. **Rationale requirement:** Every selected pattern must include a rationale string explaining why it was chosen for this requirement set.

## 4. Decision guidelines

- **ILP solver:** Formulates pattern selection as a maximization problem over weighted quality-attribute coverage subject to compatibility constraints.
- **Greedy fallback:** When ILP is not applicable, select patterns in descending order of weighted quality-attribute coverage until all batch quality attributes are addressed or the coverage threshold is met.
- **Multi-pattern combinations:** Prefer pattern combinations that have been validated together in the matrix. Avoid combinations flagged as incompatible.
- **Weight tie-breaking:** When two patterns address the same quality attributes with equal coverage, prefer the pattern that has been selected in prior batches (promotes consistency).
- **Empty quality attributes:** When no quality attributes are active in the batch, select no patterns. Return an empty `patterns` list.

## 5. Output schema

The subgraph outputs `list[ArchPattern]` in `ArchFragment.patterns`:
- `name: str` — Pattern name from the quality-architecture matrix.
- `rationale: str` — Explanation of why this pattern was selected.
- `quality_attributes: list[str]` — Quality attributes this pattern addresses.

Patterns are written to the fragment's `patterns` list and merged into `ArchModel.patterns` by the judge.

## 6. Error cases

| Situation | Handling |
|-----------|----------|
| ILP solver timeout | Fall back to Greedy; record `solver_fallback` in `rationale.confidence_notes` |
| Matrix missing for a requested quality attribute | Skip that attribute; record in `rationale.gaps` |
| No compatible pattern combination found | Select the single highest-coverage pattern; record in `rationale.gaps` |
| All patterns rejected by compatibility rules | Return empty `patterns` list; record in `rationale.confidence_notes` |
| Matrix file not found at expected path | Raise a clear error with the expected path; do not silently skip |

## 7. Examples

**Worked example from requirements dataset:**

Batch quality attributes (with weights): Security (5), Maintainability (3), Performance (2).

Matrix lookup produces:
- Pattern `layered` covers Maintainability (score 4) and Performance (score 3). Total weighted coverage: 3×4 + 2×3 = 18.
- Pattern `event-driven` covers Performance (score 5) and Security (score 3). Total weighted coverage: 2×5 + 5×3 = 25.
- Pattern `cqrs` covers Performance (score 5). Total weighted coverage: 2×5 = 10.

Greedy selection: event-driven (25), then layered (18) — both are compatible. Selected patterns: `event-driven` and `layered`, collectively covering Security, Maintainability, and Performance.
