## Context

Currently, the SA pipeline has Node 1 (Data Preparation) producing structured outputs (`traceability_matrix`, `orphaned_reqs`, technology lists) and Node 5 (Report) capable of deterministically rolling up scores. However, Nodes 2 and 3 are mock passthroughs that yield 0 points. Phase 2 introduces real grading logic, including both deterministic calculations (coverage, penalties) and LLM-based evaluations (depth resolution, technology specificity).

The pipeline is built on **LangGraph** (`StateGraph` with `TypedDict` state), and LLM integrations will use **LangChain's** `init_chat_model` + `with_structured_output` for provider-agnostic model access and type-safe responses.

## Goals / Non-Goals

**Goals:**
- Implement deterministic score computation (coverage, penalties) for Axis 1 (Functional Traceability) and Axis 2 (ASR Coverage).
- Implement structured LLM evaluations using `Functional_Depth_Evaluation.md` and a new Technology Specificity skill, guided by prompt templates.
- Use LangChain's `with_structured_output` with a Pydantic `BaseModel` to get validated, typed LLM responses — eliminating manual JSON parsing.
- Return `AxisScore` state updates from each LangGraph node.

**Non-Goals:**
- Node 4 (Architecture Quality) remains a mock.
- Node 5's LLM executive summary remains a static Markdown stub.
- No agent architecture (`create_agent`) is needed; these are deterministic LangGraph nodes that make a single LLM call each.

## Decisions

- **Model Initialization**: Use `init_chat_model` from `langchain.chat_models` to initialize the LLM. This provides a provider-agnostic interface (e.g. `"openai:gpt-4o"`, `"google_genai:gemini-2.0-flash"`) and supports swapping models without code changes. The model identifier will be read from configuration or environment.
- **Structured LLM Output via `with_structured_output`**: Rather than manually parsing raw JSON from LLM text responses, we will define a Pydantic `BaseModel` (e.g., `LLMEvaluationResult` with `score: int` and `reasoning: str` fields) and call `model.with_structured_output(LLMEvaluationResult)`. This leverages the provider's native structured output or function-calling capabilities for validated responses. Per the LangChain docs, Pydantic models provide the richest feature set with field validation, descriptions, and nested structures.
- **Fallback on LLM Error**: If `with_structured_output` raises a validation error or the LLM invocation fails, the node will catch the exception, log the error, and fallback to a 0 score for the LLM component. The deterministic portions of the score are always preserved.
- **Prompt Templates**: Extracted to separate files (`prompts/functional_depth.md`, `prompts/technology_specificity.md`) rather than inline strings. These are loaded at runtime and passed as the `HumanMessage` content to the structured-output model.
- **State Structure**: Nodes 2 and 3 will populate `score_functional` and `score_asr` respectively, adhering to the `AxisScore` `TypedDict` schema containing `awarded`, `possible`, `sub_scores`, `llm_reasoning`, and `penalties_applied`. This follows the existing LangGraph convention where node functions accept `state: SAState` and return a partial `Dict[str, Any]` update.

## Risks / Trade-offs

- **[Risk] LLM provider doesn't support structured output method** → Mitigation: `with_structured_output` supports multiple methods (`'json_schema'`, `'function_calling'`, `'json_mode'`). If the default method fails, a fallback method can be specified. In the worst case, the fallback-to-0 handler ensures pipeline continuity.
- **[Risk] Missing data from Node 1** → Mitigation: Use safe defaults (e.g. empty lists or dicts) and avoid zero-division errors in deterministic score math (e.g. `(mapped / total)` when `total == 0`).
- **[Risk] Pydantic validation rejects legitimate LLM output** → Mitigation: Keep the `LLMEvaluationResult` schema minimal (`score: int`, `reasoning: str`) to minimize validation friction. Use `Field(ge=0, le=10)` constraints on `score` to catch out-of-range values early.
