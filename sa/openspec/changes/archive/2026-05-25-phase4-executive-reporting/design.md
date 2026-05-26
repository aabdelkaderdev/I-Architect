## Context

The Scoring Agent is currently in Phase 3 where it can score Axis 1, 2, and 3 deterministically and with LLM-assisted evaluation. However, the final Phase 4 step (Node 5) still relies on a static Markdown stub for the executive summary, and output files are not properly persisted with directory validation. This change will replace the stub with a real LLM integration using the `Executive_Summary_Writer.md` skill, output the generated summary to `scoring_report.md`, and write the full JSON to `scoring_report.json` with robust error handling for file I/O and LLM failures.

The existing codebase already uses LangChain's `init_chat_model` (from `langchain.chat_models`) with `model.with_structured_output()` for standalone model calls in `sa/utils/llm.py`. This Phase 4 change follows the exact same pattern — no agent framework (`create_agent`) is needed here since we are making a single standalone LLM call within the pipeline node.

## Goals / Non-Goals

**Goals:**
- Implement LLM-driven executive summary generation in Node 5 using `model.with_structured_output()` with a Pydantic schema.
- Add a new `ExecutiveSummaryResult` Pydantic model to enforce LLM output structure (markdown narrative, key findings list, overall grade).
- Create `prompts/executive_summary.md` as the prompt template, following the existing pattern (string `.format()` interpolation) used by `saam_validation.md` and other prompt files.
- Add a new helper function `generate_executive_summary_with_llm()` in `sa/utils/llm.py` following the established pattern.
- Validate output directories and save `scoring_report.md` and `scoring_report.json` successfully.
- Implement graceful fallback to the existing deterministic stub if the LLM fails.

**Non-Goals:**
- Making changes to the scoring logic or rubrics in Nodes 1-4.
- Creating the actual output directory (this is the orchestrator's responsibility).
- Migrating to the `create_agent` + `response_format` agent-based API — the codebase uses standalone model calls and this is appropriate for the pipeline's non-agentic LLM calls.

## Decisions

### LLM Output Parsing via `with_structured_output`

Following the existing pattern in `sa/utils/llm.py`, we will:
1. Initialize the model via `init_chat_model(model, model_provider=provider, temperature=0.0)` from `langchain.chat_models`.
2. Bind structured output via `model.with_structured_output(ExecutiveSummaryResult)` using a Pydantic `BaseModel`.
3. Invoke with `structured_model.invoke([HumanMessage(content=prompt_text)])` using `HumanMessage` from `langchain.messages`.

The `ExecutiveSummaryResult` Pydantic model will use `Field` constraints (e.g., `min_length`, `max_length` on the `key_findings` list) to enforce the skill's constraints at parse time.

This is consistent with the current LangChain docs which confirm that `with_structured_output` on standalone models supports Pydantic models with field validation and descriptions.

### Prompt Template

The prompt template at `sa/prompts/executive_summary.md` will use Python `str.format()` placeholders (e.g., `{axis1_score}`, `{orphaned_requirements}`) matching the existing pattern used by `saam_validation.md`. No LangChain `PromptTemplate` class is needed — the codebase reads the template file and calls `.format()` directly.

### Error Handling

- If the LLM call fails (network error, parsing error, etc.), the function returns a fallback `ExecutiveSummaryResult` with the static stub markdown — identical to how existing LLM helpers return default objects on exception.
- If file writing fails, the error is raised to the orchestrator, but the `ScoringReport` object is still returned in state.

### Directory Validation

Node 5 will check if the `output_path` exists and is writable. Per Phase 4 requirements, if the directory is missing it raises a clear error (the orchestrator is responsible for creating it), rather than using `os.makedirs` as the current code does.

## Risks / Trade-offs

- [Risk] LLM hallucinating score values in the summary → Mitigation: The prompt template will strictly instruct the LLM to reference actual provided scores and percentages, and the `key_findings` field is constrained to 3-5 items via Pydantic validation.
- [Risk] File system write permissions failures → Mitigation: Check directory writability before attempting to write files and provide explicit error logging.
- [Risk] `with_structured_output` parsing failure for edge-case LLM outputs → Mitigation: The entire call is wrapped in try/except, falling back to the static stub, consistent with the existing pattern.
