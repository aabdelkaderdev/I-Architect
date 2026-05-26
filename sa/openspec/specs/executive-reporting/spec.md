# executive-reporting Specification

## Purpose
TBD - created by archiving change phase4-executive-reporting. Update Purpose after archive.
## Requirements
### Requirement: LLM Executive Summary Generation
The system SHALL invoke the `Executive_Summary_Writer.md` skill using an LLM via `init_chat_model` (from `langchain.chat_models`) and `model.with_structured_output(ExecutiveSummaryResult)` to generate an executive summary based on the evaluated axis scores, gap analysis, and overall grade.

#### Scenario: Successful Summary Generation
- **WHEN** the agent reaches Node 5 and the LLM call via `with_structured_output` succeeds
- **THEN** the system generates a validated `ExecutiveSummaryResult` Pydantic object containing `markdown`, exactly 3-5 `key_findings` (each ≤25 words), and an `overall_grade` matching the calculated grade

### Requirement: Executive Summary Pydantic Model
The system SHALL define an `ExecutiveSummaryResult` Pydantic `BaseModel` in `sa/state/models.py` with fields `markdown` (str), `key_findings` (list[str]), and `overall_grade` (str), using `Field` descriptions to guide the LLM's structured output.

#### Scenario: Schema Validation
- **WHEN** the LLM returns structured output via `with_structured_output`
- **THEN** the result is automatically validated by Pydantic against the `ExecutiveSummaryResult` schema before being used in the report

### Requirement: Executive Summary LLM Helper
The system SHALL add a `generate_executive_summary_with_llm(prompt_text)` function in `sa/utils/llm.py` following the established pattern: initialize model via `init_chat_model`, bind with `with_structured_output(ExecutiveSummaryResult)`, invoke with `[HumanMessage(content=prompt_text)]` from `langchain.messages`.

#### Scenario: Helper Function Invocation
- **WHEN** `node_report` calls `generate_executive_summary_with_llm` with a formatted prompt string
- **THEN** it returns an `ExecutiveSummaryResult` instance (real or fallback)

### Requirement: Prompt Template
The system SHALL create `sa/prompts/executive_summary.md` as a prompt template using Python `str.format()` placeholders (e.g., `{total_score}`, `{grade}`, `{axis1_summary}`), consistent with existing prompt templates like `saam_validation.md`.

#### Scenario: Prompt Rendering
- **WHEN** `node_report` reads and formats the prompt template with actual score data
- **THEN** the resulting prompt string contains all axis scores, orphaned requirements, diagram issues, total score, and grade

### Requirement: Markdown Report Output
The system SHALL export the narrative `scoring_report.md` to the output directory, combining the LLM-generated executive summary with the score breakdown, key findings, gap analysis highlights, and overall grade.

#### Scenario: Markdown Export
- **WHEN** Node 5 successfully completes summary generation
- **THEN** it writes `scoring_report.md` alongside `scoring_report.json`

### Requirement: LLM Failure Fallback
The system SHALL gracefully fall back to a static Markdown stub for the executive summary if the LLM call fails, without failing the overall pipeline or missing the JSON output. The fallback follows the same try/except pattern used by `evaluate_with_llm` and `evaluate_saam_with_llm` in `sa/utils/llm.py`.

#### Scenario: Fallback on LLM Failure
- **WHEN** the LLM request in Node 5 fails or `with_structured_output` raises a validation error
- **THEN** the `executive_summary.markdown` is set to the static stub, `key_findings` contains `["Executive summary generation failed — see scoring_report.json for full data"]`, and `scoring_report.json` is still successfully written

