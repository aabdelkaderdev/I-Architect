# SAAM — Adapted for RAA Judge

## 1. Purpose

Adapted 5-step SAAM process for evaluating and merging three competing ArchFragments in the RAA judge node. Quality attributes and weights come from ARLO — the judge does not choose them.

> **Source:** [SEI Technical Report](https://sei.cmu.edu/documents/150/2007_019_001_29297.pdf)
>
> **Adaptation notice:** This is a structured adaptation of SAAM for the RAA judge context, not a verbatim implementation. The core SAAM mechanics — scenario classification, individual evaluation, and scenario interaction analysis — are preserved. Scenario derivation is requirement-driven rather than stakeholder-workshop-driven, reflecting the automated pipeline context. Any stakeholder audit should treat this as a SAAM-derived method, not strict SAAM.

## 2. Input

The judge node receives these state channels:

- **`batch_outputs`** (`dict[int, list[ArchFragment]]`): All three RAA subgraph outputs for the current batch, keyed by batch index.
- **`quality_weights`** (`dict[str, int]`): Aggregate ARLO quality-attribute frequency counts.
- **`running_arch_model`** (`ArchModel`): Accumulated architecture from prior batches. Used for contradiction detection.
- **`incoherent_batches`** (`list[IncoherentBatchRecord]`): Flags indicating whether the current batch requires the 0.5× SAAM weight multiplier.

The judge LLM (`llm_judge`) is received from LangGraph runtime context, not from state channels.

## 3. Normative rules

### Adapted 5-Step Process

| Step | Original SAAM | RAA Judge Adaptation |
|------|--------------|---------------------|
| 1. Describe Architectures | Develop/describe candidate architecture(s) | Each ArchFragment is a candidate: a partitioned C4 entity set with directed relationships |
| 2. Develop Scenarios | Construct usage and change scenarios to probe the architecture | Derive one scenario per batch requirement; scenario intent (usage vs. change) inferred from requirement type |
| 3. Classify Scenarios | Classify each scenario as **direct** (satisfied as-is) or **indirect** (requires structural change) | For each fragment: classify each scenario as direct, indirect, or not-covered per the classification rules below |
| 4. Individual Evaluation | Score each architecture against each scenario | Weighted coverage scoring per fragment across all classified scenarios |
| 5. Scenario Interaction | Identify components modified by multiple indirect scenarios (hotspots) | Cross-fragment hotspot analysis over indirect scenarios; results recorded in `open_questions` |

### Step 3 — Scenario Classification Rules

Each scenario is classified **per fragment independently.** The same scenario may be direct in one fragment and indirect in another.

| Classification | Definition | Scoring |
|---|---|---|
| **Direct** | The fragment contains an entity or relationship that satisfies the scenario without any structural addition or modification | `1.0` |
| **Indirect** | The fragment partially addresses the scenario but requires a structural change (new entity, new relationship, or modification of an existing one) to fully satisfy it | `0.5` |
| **Not Covered** | The fragment has no entity or relationship that addresses the scenario | `0.0` |

**Classification rules (apply in order, stop at first match):**

1. **Direct** — the fragment contains at least one entity or relationship whose `requirement_id` matches the scenario, AND the fragment's `rationale.gaps` does not list that requirement. The scenario is fully satisfied as-is.
2. **Indirect** — the fragment's `rationale.gaps` lists the requirement ID, OR a matching entity/relationship exists but is missing required technology annotation or a relationship direction. The scenario is partially addressed but needs a structural change.
3. **Not Covered** — the requirement ID is absent from the fragment's entities, relationships, and rationale entirely.

> **Fallback:** If a fragment omits `rationale.gaps`, treat every partially-matched scenario conservatively as **Indirect**. Classification accuracy is degraded; log a warning.

## 4. Decision guidelines

### Step 4 — Scoring

#### Per-Scenario Score

| Classification | Score |
|---|---|
| Direct | `1.0` |
| Indirect | `0.5` |
| Not Covered | `0.0` |

#### Fragment Score Formula

```
fragment_score = Σ(scenario_score × qa_weight) / Σ(qa_weight)
```

- `qa_weight` comes from ARLO `quality_weights` for the scenario's quality attribute.
- Requirements with no QA classification use default weight `0.05`.
- For `reduced_confidence` batches: apply a **0.5× multiplier** to the final `fragment_score` before comparison. Record the multiplier in model metadata.

### Step 5 — Scenario Interaction (Hotspot Detection)

A **hotspot** is a C4 entity that multiple *indirect* scenarios across the candidate fragments require structural changes to. This is the core scenario interaction signal from SAAM — shared modification targets indicate architectural coupling risk.

#### Hotspot Classification

| Hotspot Type | Condition | Risk Label |
|---|---|---|
| **Change-risk hotspot** | Entity is the target of ≥ 3 *indirect* scenarios across all fragments | `change_risk` |
| **Coupling hotspot** | Entity is the target of ≥ 5 scenarios total (direct + indirect) across all fragments | `high_coupling` |
| **Cross-fragment contention** | Entity is classified as *indirect* in ≥ 2 different fragments for different scenarios | `contention` |

All hotspots are recorded in `open_questions` with the entity ID, hotspot type, and the list of contributing scenario IDs. They are **not** automatically resolved by the judge; they are flagged for downstream review or the final reconciliation pass.

**Hotspot detection rules (evaluate every entity that appears in any fragment):**

1. Collect all scenarios classified as **Indirect** for each entity, across all three fragments.
2. Collect all scenarios (Direct + Indirect) for each entity, across all three fragments.
3. Track which fragments classify a given entity as Indirect, and for which scenarios.
4. Apply the thresholds from the table above to assign hotspot types. An entity may carry more than one hotspot label simultaneously.
5. Record each hotspot in `open_questions`: include the entity ID, hotspot type, and the full list of contributing scenario IDs.

### Merge Algorithm (Deterministic — No LLM)

Applied after the winning fragment is selected by score. Runs in order; steps are not skippable.

1. **Entity deduplication** — canonical IDs: lowercase, snake_case, trimmed. Entities present in multiple fragments are merged: longest description wins; any technology annotation from any fragment is retained. Direct-classified entities take precedence over indirect-classified ones when descriptions conflict.

2. **Relationship deduplication** — canonical key = `(source_id, target_id, interaction_type)`. Conflicts: prefer the relationship from the higher-scoring fragment. Irreconcilable conflicts (contradictory directions) → `open_questions`.

3. **Coverage union** — entities/relationships from non-selected fragments that have at least one *direct* or *indirect* classification (score > 0) and are absent from the selected fragment are added to the merged output. Entities contributed only by `not_covered` classifications are discarded.

4. **Residual scan** — before finalising, check each discarded fragment for entities or relationships that cover scenarios not covered by the merged output. Carry forward any such elements via the coverage union rule above.

### Tie-Breaking

A tie occurs when two or more fragments share the highest `fragment_score` within rounding tolerance (`|Δscore| < 0.01`).

**Resolution order (apply in sequence until tie is broken):**

| Priority | Rule | Rationale |
|---|---|---|
| 1 | Prefer the fragment with the **higher count of direct-classified scenarios** | More direct coverage means fewer structural changes required — the primary SAAM signal |
| 2 | Prefer the fragment with the **lower count of change-risk hotspots** | Fewer indirect-scenario collisions indicates lower coupling risk |
| 3 | Prefer the fragment with **higher summed `qa_weight` across direct scenarios** | Directly satisfying higher-priority quality attributes is more valuable than satisfying low-weight ones |
| 4 | If still tied: record tie in `open_questions` and trigger a **targeted LLM reconciliation pass** scoped strictly to the tied fragments; do not select arbitrarily | Arbitrary selection on entity count is not architecturally grounded and is removed |

## 5. Output schema

The judge produces updates to these state channels:

- **`best_batch_output`** (`dict[int, ArchFragment]`): Judge-selected and merged fragment for this batch, keyed by batch index.
- **`running_arch_model`** (`ArchModel`): Accumulated hierarchical architecture model, updated with this batch's merged entities.
- **`open_questions`** (`list[OpenQuestion]`): Hotspots, ties, hierarchy conflicts, coverage gaps, and scope conflicts.
- **`batch_cursor`** (`int`): Advanced by 1 after judge completes.

**Confidence metadata:** For entities originating from incoherent batches, write a `ConfidenceRecord` with `reduced_confidence=True`, the `source_batch` index, and the fragment's `saam_score`.

See `raa/state/types.py` for the complete dataclass field definitions of `ArchFragment`, `ArchModel`, `OpenQuestion`, and `ConfidenceRecord`.

## 6. Error cases

| Situation | Action |
|-----------|--------|
| All fragments score 0 | Flag batch in `open_questions`; skip `running_arch_model` update; advance `batch_cursor` |
| Score tie after all tie-breaking rules exhausted | Add to `open_questions`; trigger scoped LLM reconciliation pass; do not select arbitrarily |
| Fragment contradicts `running_arch_model` | Discard contradicting entities from that fragment before scoring; log conflict in `open_questions` |
| Empty fragment (subgraph failed) | Exclude from scoring and merge entirely; if all three subgraphs fail, flag batch and skip |
| No scenarios can be derived from batch requirements | Skip SAAM scoring; flag batch in `open_questions` with reason `no_scoreable_scenarios` |
| Incoherent batch detected | Apply 0.5× SAAM weight multiplier; record `reduced_confidence=True` in per-entity `ConfidenceRecord` |

## 7. Examples

**Worked example from requirements dataset:**

Batch index 2, three fragments from RAA-A, RAA-B, RAA-C. Batch requirements: R10 (Security, weight 4), R11 (Performance, weight 3).

Fragment A (SAAM-first strategy):
- Covers R10 directly, R11 indirectly. Gaps: none for R10, R11 listed in gaps.
- fragment_score = (1.0×4 + 0.5×3) / (4+3) = (4 + 1.5) / 7 = 0.786

Fragment B (pattern-driven strategy):
- Covers R10 indirectly, R11 directly.
- fragment_score = (0.5×4 + 1.0×3) / 7 = (2 + 3) / 7 = 0.714

Fragment C (entity-driven strategy):
- Covers R10 directly, R11 not_covered.
- fragment_score = (1.0×4 + 0.0×3) / 7 = 4 / 7 = 0.571

**Result:** Fragment A selected (score 0.786). Fragment B entities with coverage > 0 merged via coverage union. Fragment C discarded. Hotspots: none (no entity receives ≥3 indirect scenarios across fragments). Batch cursor advanced to 3.
