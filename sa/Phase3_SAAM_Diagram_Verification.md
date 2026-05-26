# Phase 3: SAAM Evaluation & Diagram Verification (Node 4)

## Objective

Implement Axis 3, the most complex node requiring custom PlantUML parsing and the heavily-weighted SAAM quality attribute evaluation. After this phase, the entire 100-point scoring rubric is fully functional.

---

## Scope

### In Scope (Vertical Slice)

- **PlantUML Parser (`utils/plantuml_parser.py`):** String parsing to extract canonical IDs/aliases, verify completeness, and check cross-level leakage.
- **Node 4 (SAAM — Deterministic, 20 pts):** Diagram correctness grading.
- **Node 4 (SAAM — LLM, 30 pts):** The SAAM evaluation integration using the `SAAM_Validation.md` skill, processing patterns and flattened technology stacks.

### Mocks / Extensibility

- Node 5's LLM executive summary is the only remaining stub.
- The entire 100-point scoring rubric is now fully functional and mathematically sound.

### Estimated OpenSpec Task Count: ~12–15 tasks.

---

## Prerequisites from Phase 2

Phase 3 assumes the following are complete and functional:
- Node 2 (Functional Traceability) producing real `score_functional` with deterministic + LLM scores
- Node 3 (ASR Coverage) producing real `score_asr` with deterministic + LLM scores
- Prompt template scaffolding and structured JSON output parsing established
- Node 5 correctly rolling up all axis scores into the final report

---

## Scoring Rubric: Axis 3 — SAAM Evaluation & Diagram Accuracy (50 Points)

This is the primary axis. It combines SAAM-based quality attribute evaluation with diagram correctness checks. The SAAM (Software Architecture Analysis Method) methodology evaluates whether the architecture's patterns and technology choices genuinely address the system's most important quality attributes.

### 3A. SAAM Quality Attribute Evaluation (30 Points) — LLM

The LLM receives:
- The top-weighted quality attributes from ARLO
- The patterns declared in the architecture model
- The flattened technology stack (technology values per entity)
- The three PlantUML diagram strings

The LLM evaluates whether:
- Declared patterns directly address the quality attribute's stimulus-response scenarios (per SAAM methodology)
- Technology choices are compatible with the quality attribute requirements
- Pattern-to-attribute mappings have mechanistic justification, not just name association

Generic "pattern name matches quality attribute name" reasoning scores zero. A pattern satisfies a quality attribute only if its documented properties address the specific stimulus-response scenario.

### 3B. Diagram Correctness (20 Points) — Deterministic

SA parses each PlantUML string and checks structural correctness against the architecture model:

| Sub-rubric | Points | Method |
|------------|--------|--------|
| Render completeness | 10 pts | All three expected diagram strings are non-empty. Deduct proportionally per missing/empty diagram |
| Entity inclusion | 5 pts | Each diagram's PlantUML source contains the expected entities: context diagram must include all persons and external systems; container diagram must include all containers of the primary system; component diagram must include all components of the selected container |
| Hierarchy validity | 5 pts | C4 element types are used correctly — no containers appearing in context diagrams as top-level, no components appearing in container diagrams. Deductions per misplaced entity |

Alias matching uses the entity's canonical `id` field — AGA is required to use the entity ID as the PlantUML alias, making verification straightforward string matching.

---

## PlantUML Parser (`utils/plantuml_parser.py`)

### Purpose

Parse raw PlantUML source strings to extract structural information for diagram verification.

### Capabilities

1. **Alias Extraction:** Extract all entity aliases (canonical IDs) from a PlantUML string
2. **Entity Type Detection:** Determine the C4 element type declared for each alias (System, Container, Component, Person, System_Ext, etc.)
3. **Completeness Check:** Given a list of expected entity IDs, report which are present and which are missing
4. **Cross-Level Leakage Detection:** Identify entities that appear at incorrect C4 levels (e.g., a Container alias appearing in a Context diagram as a top-level element)

### Parsing Strategy

PlantUML C4 diagrams use standardised macros:
```
System(alias, "Label", "Description")
Container(alias, "Label", "Technology", "Description")
Component(alias, "Label", "Technology", "Description")
Person(alias, "Label", "Description")
System_Ext(alias, "Label", "Description")
```

The parser:
1. Matches lines against C4 macro patterns using regex
2. Extracts the alias (first argument) and the macro name (C4 type)
3. Builds a mapping: `alias → c4_type`
4. Does **not** attempt full PlantUML parsing — only C4 macro extraction

### Edge Cases

- Aliases with underscores, hyphens, or mixed case
- Multi-line macro definitions (rare but possible)
- Comments in PlantUML source (lines starting with `'`)
- `Boundary()` and `System_Boundary()` wrappers (extract children, ignore boundary itself for alias purposes)

---

## Node 4: SAAM & Diagram Score (Replaces Mock)

### Deterministic Step — Diagram Correctness (20 pts)

1. **Render Completeness (10 pts):**
   - Check each of the three PlantUML strings is non-empty
   - Score: `(non_empty_count / 3) × 10`
   - Record a `DiagramIssue` with `issue_type = "empty_diagram"` for each empty string

2. **Entity Inclusion (5 pts):**
   - Parse each PlantUML string using `plantuml_parser` to extract aliases
   - For context diagram: verify all persons and external systems from the architecture model appear
   - For container diagram: verify all containers of the primary system appear
   - For component diagram: verify all components of the selected container appear
   - Score: proportional deduction per missing entity across all three diagrams
   - Record a `DiagramIssue` with `issue_type = "missing_entity"` for each missing entity

3. **Hierarchy Validity (5 pts):**
   - Check that entity aliases in each diagram match the expected C4 level
   - Context diagram should only have Systems, Persons, and External Systems at the top level
   - Container diagram should only have Containers (plus external references)
   - Component diagram should only have Components (plus external references)
   - Record a `DiagramIssue` with `issue_type = "wrong_level"` for each misplaced entity
   - Score: proportional deduction per misplaced entity

### LLM Step — SAAM Evaluation (30 pts)

- **Skill:** `SAAM_Validation.md`
- **Prompt template:** `prompts/saam_validation.md`
- **Input to LLM:**
  - Top-weighted quality attributes (sorted by ARLO weight)
  - Declared patterns from entity metadata
  - Flattened technology stack (entity ID → technology)
  - The three PlantUML diagram strings
- **Expected LLM output:** Structured JSON with:
  - `score` (integer, 0–30): SAAM evaluation score
  - `reasoning` (string): Detailed SAAM analysis
  - `attribute_assessments` (list): Per-attribute evaluation with pattern effectiveness ratings

### Output

Populates `score_saam` in state as an `AxisScore`:
- `awarded`: saam_score + diagram_score (clamped appropriately)
- `possible`: 50
- `sub_scores`: `{"saam_evaluation": X, "render_completeness": Y, "entity_inclusion": Z, "hierarchy_validity": W}`
- `llm_reasoning`: The SAAM LLM's reasoning string
- `penalties_applied`: List of diagram issues converted to penalties

Also populates `diagram_issues` in the `GapAnalysis` for the final report.

---

## Skills & LLM Integration

### Skill Files Referenced

| Skill | Node | Purpose |
|-------|------|---------|
| `SAAM_Validation.md` | Node 4 | SAAM methodology: evaluating whether patterns and technologies satisfy quality attribute stimulus-response scenarios |

### SAAM Skill Key Requirements

The SAAM validation skill enforces:
1. **Mechanistic Justification:** Pattern-to-attribute mappings must be justified by documented properties, not just name matching
2. **Stimulus-Response Analysis:** Each quality attribute is evaluated through its specific stimulus-response scenarios
3. **Technology Compatibility:** Technology choices must be compatible with the quality attributes they claim to support
4. **Zero-Score for Generic Reasoning:** "Circuit breaker pattern supports reliability" without explaining the mechanism scores zero

---

## Files Modified / Created

### Modified

| File | Changes |
|------|---------|
| `nodes/axis_saam.py` | Replace mock with full SAAM + diagram verification implementation |

### New

| File | Purpose |
|------|---------|
| `utils/plantuml_parser.py` | PlantUML source parsing, C4 macro extraction, alias extraction |
| `prompts/saam_validation.md` | Runtime prompt template for Node 4 SAAM LLM call |

---

## Verification

After Phase 3:
- PlantUML parser correctly extracts aliases from all three diagram types
- Diagram correctness scoring produces accurate proportional deductions
- SAAM evaluation LLM call returns parseable structured JSON
- The full 100-point rubric is functional: Axis 1 (25) + Axis 2 (25) + Axis 3 (50) = 100
- Node 5 correctly sums all three real axis scores
- `scoring_report.json` contains a complete, mathematically consistent 100-point breakdown
- Edge cases handled: empty PlantUML strings, missing entities, all-generic technologies
