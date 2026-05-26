## Why

This change completes the pipeline by implementing the LLM-driven executive summary (Node 5), finalizing all output artifacts, and validating end-to-end execution. After this phase, no mocks remain and the Scoring Agent will be fully functional and ready to be invoked by the Orchestrator.

The LLM integration follows the existing codebase pattern: standalone model calls via `init_chat_model` (from `langchain.chat_models`) + `model.with_structured_output()` with Pydantic schemas + `HumanMessage` from `langchain.messages`. No agent framework (`create_agent`) is needed.

## What Changes

- Add an `ExecutiveSummaryResult` Pydantic model and a `generate_executive_summary_with_llm()` helper in `sa/utils/llm.py`, following the same pattern as the existing `evaluate_with_llm` and `evaluate_saam_with_llm` functions.
- Create `sa/prompts/executive_summary.md` prompt template with `str.format()` placeholders (same pattern as `saam_validation.md`).
- Update `sa/nodes/report.py` to call the new LLM helper, populate real executive summary data, compose `scoring_report.md`, and validate the output directory.
- Add graceful fallback to a static stub if the LLM call fails.

## Capabilities

### New Capabilities
- `executive-reporting`: Implements the LLM step for Node 5, leveraging the `Executive_Summary_Writer.md` skill via `with_structured_output(ExecutiveSummaryResult)` to generate `scoring_report.md` with key findings and an overall assessment.

### Modified Capabilities
- `deterministic-reporting`: Modifies the existing deterministic Node 5 implementation to replace `os.makedirs` with directory validation, integrate the new LLM-driven executive summary, and write both output files.

## Impact

- **Modified:** `sa/nodes/report.py` — replace LLM stub and `os.makedirs` with real integration and directory validation.
- **Modified:** `sa/state/models.py` — add `ExecutiveSummaryResult` Pydantic model.
- **Modified:** `sa/utils/llm.py` — add `generate_executive_summary_with_llm()` helper.
- **Created:** `sa/prompts/executive_summary.md` — runtime prompt template.
- Removes the last mocks from the pipeline, making the agent fully operational.
