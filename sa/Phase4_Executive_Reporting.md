# Phase 4: Executive Reporting & Finalization (Node 5)

## Objective

Complete the pipeline by implementing the LLM-driven executive summary, finalize all output artifacts, and validate end-to-end execution. After this phase, no mocks remain — the agent is fully functional and ready to be invoked by the Orchestrator.

---

## Scope

### In Scope (Vertical Slice)

- **Node 5 (Report — LLM):** Integration of the `Executive_Summary_Writer.md` skill to generate the narrative summary and key findings.
- Writing the generated narrative to `scoring_report.md`.
- Directory validation and error handling for output paths.
- End-to-end integration testing of the finished pipeline.

### Mocks / Extensibility

- **No mocks remain.** The agent is fully functional and ready to be invoked by the Orchestrator.

### Estimated OpenSpec Task Count: ~6–9 tasks.

---

## Prerequisites from Phase 3

Phase 4 assumes the following are complete and functional:
- All three axis scoring nodes (2, 3, 4) producing real `AxisScore` values
- Full 100-point rubric functional: Axis 1 (25) + Axis 2 (25) + Axis 3 (50)
- Node 5 deterministic roll-up (grading, `ScoringReport` JSON construction) working correctly
- PlantUML parser producing accurate diagram issue reports
- `GapAnalysis` populated with orphaned requirements and diagram issues

---

## Node 5: Report Compilation (Complete Implementation)

### Deterministic Step (Already Implemented in Phase 1)

- Sums the three axis scores
- Computes letter grade: A (≥90), B (≥80), C (≥70), D (≥60), F (<60)
- Builds the structured `ScoringReport` JSON object
- Populates `ReportSummary`, `AxisBreakdown`, and `GapAnalysis`

### LLM Step (New in Phase 4)

- **Skill:** `Executive_Summary_Writer.md`
- **Prompt template:** `prompts/executive_summary.md`
- **Input to LLM:**
  - All three `AxisScore` objects with their sub-scores and reasoning
  - Orphaned requirements list
  - Diagram issues list
  - Total score and letter grade
  - Quality weights context from ARLO
- **Expected LLM output:** Structured JSON with:
  - `markdown` (string): Full executive summary in Markdown format
  - `key_findings` (list[str]): 3–5 concise findings, each ≤25 words
  - `overall_grade` (string): Letter grade

### Skill Constraints (from `Executive_Summary_Writer.md`)

The executive summary skill enforces:
1. **Structure:** Opening paragraph with overall assessment, per-axis breakdown, and closing recommendations
2. **Findings Format:** Each finding must be ≤25 words and actionable
3. **Count Constraint:** Exactly 3–5 key findings
4. **Tone:** Professional, objective, assessment-oriented (not promotional)
5. **Score Reference:** Must reference actual scores and percentages, not vague qualifiers
6. **No Fabrication:** Must not mention issues not found in the data

---

## Filesystem Output

### `scoring_report.json`

Written to `{output_path}/scoring_report.json`. Contains the full `ScoringReport` JSON object with all scores, reasoning, gap analysis, and executive summary.

### `scoring_report.md`

Written to `{output_path}/scoring_report.md`. The LLM-generated narrative report suitable for human review. Contains:
- Executive summary (from the LLM)
- Score breakdown table
- Key findings list
- Gap analysis highlights
- Overall grade

### Directory Validation

Before writing output files:
1. Validate that `output_path` exists and is a directory
2. If the path does not exist, raise a clear error (the orchestrator is responsible for creating it)
3. If the path is not writeable, raise an error with the specific permission issue
4. Log the output file paths after successful writes

---

## Error Handling

### LLM Executive Summary Failures

If the LLM call fails or returns unparseable output:
1. Log the error with full context
2. Fall back to the static Markdown stub (from Phase 1)
3. Set `executive_summary.markdown` to the stub content
4. Set `executive_summary.key_findings` to `["Executive summary generation failed — see scoring_report.json for full data"]`
5. The rest of the report (`scoring_report.json`) is still valid and complete

### Output Write Failures

If writing to the filesystem fails:
1. Log the error
2. Return the `ScoringReport` object in state regardless (the orchestrator can access it)
3. Raise the error to the orchestrator for handling

---

## Skills & LLM Integration

### Skill Files Referenced

| Skill | Node | Purpose |
|-------|------|---------|
| `Executive_Summary_Writer.md` | Node 5 | Formatting constraints for translating score data into a readable executive summary |

### Complete LLM Call Summary (All Phases)

| Skill | Node | Phase Introduced | Purpose |
|-------|------|-----------------|---------|
| `Functional_Depth_Evaluation.md` | Node 2 | Phase 2 | Depth adequacy judgment |
| Technology Specificity | Node 3 | Phase 2 | Technology choice evaluation |
| `SAAM_Validation.md` | Node 4 | Phase 3 | SAAM pattern effectiveness |
| `Executive_Summary_Writer.md` | Node 5 | Phase 4 | Executive summary generation |

---

## Files Modified / Created

### Modified

| File | Changes |
|------|---------|
| `nodes/report.py` | Replace LLM stub with real `Executive_Summary_Writer.md` skill integration; add `scoring_report.md` writing; add directory validation |

### New

| File | Purpose |
|------|---------|
| `prompts/executive_summary.md` | Runtime prompt template for Node 5 LLM call |

---

## End-to-End Integration Testing

### Test Scenarios

1. **Happy Path:** Full pipeline with valid `arch_model_test_result.json`, three valid PlantUML strings, and complete requirements data → produces valid `scoring_report.json` and `scoring_report.md`
2. **Partial Input:** Missing one or more PlantUML strings → pipeline still completes with proportional deductions
3. **Empty Requirements:** No functional requirements or no ASRs → scores are 0 for the respective axis without errors
4. **LLM Failure Graceful Degradation:** Simulated LLM failures → pipeline produces valid JSON report with stub executive summary
5. **Score Consistency:** Verify `total_score == axis1.awarded + axis2.awarded + axis3.awarded` across multiple runs
6. **Grade Boundaries:** Test exact boundary values (59.9 → F, 60.0 → D, 69.9 → D, 70.0 → C, etc.)

### Validation Checklist

- [ ] `scoring_report.json` is valid JSON and matches the `ScoringReport` schema
- [ ] `scoring_report.md` is well-formed Markdown
- [ ] All three axis scores sum to `total_score`
- [ ] Grade letter matches the score thresholds
- [ ] `gap_analysis.orphaned_requirements` matches the actual orphan count
- [ ] `gap_analysis.diagram_issues` matches the actual diagram issues found
- [ ] `executive_summary.key_findings` contains 3–5 items, each ≤25 words
- [ ] Output files are written to the correct `output_path`
- [ ] Error handling works for invalid output paths

---

## Final State

After Phase 4 completion:
- **No mocks remain** in any node
- **3 LLM calls** are fully integrated with structured output parsing
- **100-point rubric** is fully operational
- **Both output files** (`scoring_report.json`, `scoring_report.md`) are produced
- The SA agent is **ready for orchestrator integration**

### Complete Pipeline

```
Node 1 (Prep)       → Deterministic: hierarchy, traceability matrix, tech stack
Node 2 (Functional) → Deterministic + LLM: mapping coverage, depth evaluation
Node 3 (ASR)        → Deterministic + LLM: ASR coverage, technology specificity
Node 4 (SAAM)       → Deterministic + LLM: diagram correctness, SAAM evaluation
Node 5 (Report)     → Deterministic + LLM: score roll-up, executive summary, file output
```
