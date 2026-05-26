## 1. Models and Utilities Setup

- [x] 1.1 Define `SAAMEvaluationResult` Pydantic `BaseModel` in `sa/state/models.py` with fields: `score` (int, ge=0, le=30), `reasoning` (str), and `attribute_assessments` (list)
- [x] 1.2 Create `utils/plantuml_parser.py` with regex-based PlantUML C4 macro parser to extract aliases and types
- [x] 1.3 Handle edge cases in parser: ignoring single-line comments (`'`) and gracefully handling missing matches

## 2. LLM Integration Setup

- [x] 2.1 Create `prompts/saam_validation.md` defining strict LLM instructions for evaluating pattern-to-attribute mappings mechanistically
- [x] 2.2 Add `evaluate_saam_with_llm` helper in `utils/llm.py` that uses `init_chat_model` and `model.with_structured_output(SAAMEvaluationResult)` without explicit `method`/`strict` params (auto-strategy selection per current LangChain docs)
- [x] 2.3 Ensure message construction uses `from langchain.messages import HumanMessage` (not deprecated `langchain_core.messages`)

## 3. Node 4 Implementation — Deterministic Scoring

- [x] 3.1 Implement render completeness verification (check that context, container, and component diagram strings are non-empty)
- [x] 3.2 Implement entity inclusion verification using the `plantuml_parser` to check expected versus actual entities
- [x] 3.3 Implement hierarchy validity verification (check that C4 elements only appear at their correct diagram level)
- [x] 3.4 Calculate proportional score deductions for diagram correctness and record specific `DiagramIssue` types

## 4. Node 4 Implementation — SAAM Scoring

- [x] 4.1 Integrate LLM evaluation call in `nodes/axis_saam.py` utilizing the new `evaluate_saam_with_llm` helper and prompt template
- [x] 4.2 Parse `SAAMEvaluationResult` structured output to extract SAAM `score`, `reasoning`, and `attribute_assessments`

## 5. Output Structure and Reporting

- [x] 5.1 Populate and return the complete `score_saam` AxisScore (combining deterministic and LLM scores out of 50 total points)
- [x] 5.2 Update final report generation to include the Node 4 `score_saam` metrics and inject `diagram_issues` into the `GapAnalysis`
- [x] 5.3 Run an end-to-end pipeline test to verify mathematically consistent 100-point reporting in `scoring_report.json`

## 6. Import Path Cleanup

- [x] 6.1 Update existing `utils/llm.py` import from `from langchain_core.messages import HumanMessage` to `from langchain.messages import HumanMessage`
