# Phase 2: Traceability Axes (Nodes 2 & 3)

## Objective

Implement Axis 1 (Functional Traceability) and Axis 2 (ASR Coverage) scoring, introducing the first deterministic grading math and LLM skill integrations.

---

## Scope

### In Scope (Vertical Slice)

- **Node 2 (Functional Traceability):** Deterministic coverage calculations, orphan penalties, and the LLM call using the `Functional_Depth_Evaluation.md` skill.
- **Node 3 (ASR Coverage):** Deterministic ASR mapping calculations, contradiction penalties, and the LLM call for Technology Specificity.
- Prompt template scaffolding and structured JSON output parsing for the LLMs.

### Mocks / Extensibility

- Node 4 remains a mock passthrough (0 points, no reasoning).
- Node 5's LLM executive summary remains stubbed with a static Markdown string.
- Nodes 2 and 3 now output real, testable scores that Node 5 successfully rolls up into the final JSON report.

### Estimated OpenSpec Task Count: ~10–14 tasks.

---

## Prerequisites from Phase 1

Phase 2 assumes the following are complete and functional:
- State schemas (`schemas.py`, `models.py`) with all TypedDicts
- LangGraph StateGraph wiring (`graphs/core.py`, `runner.py`)
- Node 1 (Data Preparation) producing a valid `traceability_matrix`, `orphaned_reqs`, technology list, and patterns
- Node 5 (Report) deterministic roll-up of axis scores into `ScoringReport`
- Full pipeline running end-to-end with mock nodes

---

## Scoring Rubric: Axis 1 — Functional Traceability (25 Points)

Evaluates whether every functional (non-ASR) requirement is mapped to at least one architecture entity, and whether the mapping reaches adequate depth.

| Sub-rubric | Points | Method |
|------------|--------|--------|
| Mapping coverage | 15 pts | Deterministic: `(mapped functional reqs / total functional reqs) × 15` |
| Depth of resolution | 10 pts | LLM-evaluated: do requirements trace down to appropriate C4 levels? Data-handling requirements should reach the component level; broad business requirements may reasonably stop at the system or container level |
| Orphan penalty | -1 per orphan, max -10 | Deterministic: deduction for each functional requirement mapped to zero entities |

### Depth Evaluation Rationale

SA examines the deepest C4 level (component > container > system) at which each requirement is traced. The LLM receives a distribution summary — e.g., "60% at component level, 30% at container level, 10% at system level" — and judges whether the distribution is appropriate for the nature of the requirements.

---

## Scoring Rubric: Axis 2 — ASR Coverage (25 Points)

Evaluates whether Architecturally Significant Requirements (ASRs) are properly traced into the architecture.

| Sub-rubric | Points | Method |
|------------|--------|--------|
| ASR mapping coverage | 15 pts | Deterministic: `(mapped ASRs / total ASRs) × 15` |
| Technology specificity | 10 pts | LLM-evaluated: rewards specific, compatible technology choices (e.g., "PostgreSQL 15") over generic placeholders (e.g., "Database"). Generic values are penalised only when the relevant quality attribute demands a specific property |
| Contradiction penalty | -5 pts | Deterministic per contradiction found (e.g., synchronous pattern chosen for an ASR demanding asynchronous resilience) |

---

## Node 2: Functional Traceability Score (Replaces Mock)

### Deterministic Step

1. From `traceability_matrix`, count functional requirements (from `non_asr` list) that are mapped to at least one entity.
2. Compute mapping coverage: `(mapped_functional / total_functional) × 15`
3. Count orphaned functional requirements and apply penalty: `-1` per orphan, capped at `-10`.
4. Build depth distribution summary: percentage of functional requirements at each C4 level (system, container, component).

### LLM Step

- **Skill:** `Functional_Depth_Evaluation.md`
- **Prompt template:** `prompts/functional_depth.md`
- **Input to LLM:**
  - The depth distribution summary (percentage at each C4 level)
  - The list of functional requirements with their deepest traced level
  - Context about what each C4 level represents
- **Expected LLM output:** Structured JSON with:
  - `score` (integer, 0–10): Depth adequacy score
  - `reasoning` (string): Explanation of the depth assessment

### Output

Populates `score_functional` in state as an `AxisScore`:
- `awarded`: coverage_score + depth_score + orphan_penalty (clamped to ≥0)
- `possible`: 25
- `sub_scores`: `{"mapping_coverage": X, "depth_of_resolution": Y}`
- `llm_reasoning`: The LLM's reasoning string
- `penalties_applied`: List of orphan penalties

---

## Node 3: ASR Coverage Score (Replaces Mock)

### Deterministic Step

1. From `traceability_matrix`, count ASR requirements (from `asrs` list) that are mapped to at least one entity.
2. Compute ASR mapping coverage: `(mapped_asrs / total_asrs) × 15`
3. Identify technology contradictions: cases where the chosen technology or pattern contradicts an ASR's quality attribute requirement (e.g., synchronous pattern for an async-demanding ASR).
4. Apply contradiction penalty: `-5` per contradiction found.

### LLM Step

- **Skill:** Technology Specificity evaluation (part of ASR coverage methodology)
- **Prompt template:** `prompts/technology_specificity.md` (new file)
- **Input to LLM:**
  - The flattened technology list (entity ID → technology value)
  - The ASR requirements with their associated quality attributes
  - Quality weights from ARLO
- **Expected LLM output:** Structured JSON with:
  - `score` (integer, 0–10): Technology specificity score
  - `reasoning` (string): Explanation of technology assessment

### Output

Populates `score_asr` in state as an `AxisScore`:
- `awarded`: coverage_score + specificity_score + contradiction_penalty (clamped to ≥0)
- `possible`: 25
- `sub_scores`: `{"asr_mapping_coverage": X, "technology_specificity": Y}`
- `llm_reasoning`: The LLM's reasoning string
- `penalties_applied`: List of contradiction penalties

---

## Skills & LLM Integration

### Skill Files Referenced

| Skill | Node | Purpose |
|-------|------|---------|
| `Functional_Depth_Evaluation.md` | Node 2 | Guidelines for judging appropriate requirement-to-C4-level mapping depth |

### Prompt Template Format

Each prompt template:
1. States the evaluation task clearly
2. Provides the input data in a structured format
3. Specifies the exact JSON output schema expected
4. Includes constraints from the skill's normative rules
5. Provides an example input/output pair

### Structured Output Parsing

- LLM responses are parsed as JSON
- Schema validation ensures `score` is within bounds and `reasoning` is non-empty
- Fallback: if parsing fails, score defaults to 0 with error reasoning logged

---

## Files Modified / Created

### Modified

| File | Changes |
|------|---------|
| `nodes/axis_functional.py` | Replace mock with full deterministic + LLM implementation |
| `nodes/axis_asr.py` | Replace mock with full deterministic + LLM implementation |

### New

| File | Purpose |
|------|---------|
| `prompts/functional_depth.md` | Runtime prompt template for Node 2 LLM call |
| `prompts/technology_specificity.md` | Runtime prompt template for Node 3 LLM call |

---

## Verification

After Phase 2:
- Nodes 2 and 3 produce real, non-zero `AxisScore` values based on actual input data
- Node 5 correctly sums the real Axis 1 and Axis 2 scores with the mock Axis 3 score (0)
- The `scoring_report.json` contains valid, mathematically consistent scores
- LLM calls return parseable structured JSON matching the expected schema
- Edge cases handled: zero requirements, all orphans, empty technology lists
