## Context

The Scoring Agent evaluates architectures across three axes using a LangGraph `StateGraph` pipeline. Node 4 covers Axis 3: SAAM Evaluation & Diagram Verification, which is the most complex node and holds 50 points of the 100-point total. The current implementation of Node 4 uses mocks. We need to replace it with a functional deterministic parser for PlantUML strings and an LLM call for SAAM-based quality attribute analysis using the `SAAM_Validation.md` skill.

The project currently uses:
- `langchain.chat_models.init_chat_model` for model initialization
- `model.with_structured_output(PydanticSchema)` for structured LLM responses (auto-selects best strategy per model capabilities)
- `langchain.messages.HumanMessage` for message construction
- `langgraph.graph.StateGraph` with `langgraph.constants.START`/`END` for the pipeline graph

## Goals / Non-Goals

**Goals:**
- Create a lightweight regex-based parser to extract C4 macros (aliases and element types) from PlantUML strings.
- Implement deterministic checks for render completeness (non-empty diagrams), entity inclusion (all expected entities present), and hierarchy validity (C4 elements in the correct diagram levels).
- Define a new `SAAMEvaluationResult` Pydantic model (with `score: int` constrained 0–30, `reasoning: str`, and `attribute_assessments: list`) for the SAAM LLM structured output.
- Integrate an LLM step utilizing `SAAM_Validation.md` via `init_chat_model` and `with_structured_output(SAAMEvaluationResult)` — letting LangChain auto-select the best structured output strategy (ProviderStrategy for OpenAI/Anthropic/Gemini, ToolStrategy otherwise).

**Non-Goals:**
- Implementing a full abstract syntax tree (AST) parser for PlantUML.
- Writing new skill files for Phase 3 (we assume `SAAM_Validation.md` is provided or will be implemented separately per the input specification).
- Migrating existing nodes to use `create_agent` — we continue using standalone model calls with `with_structured_output` consistent with the existing `utils/llm.py` pattern.

## Decisions

- **PlantUML Parsing Strategy**:
  - *Decision*: Use regex matching against standardized C4 macros (e.g., `System()`, `Container()`) to extract the alias (first argument) and the C4 type (macro name).
  - *Rationale*: A full PlantUML parser is overly complex for our needs. Since AGA generates standardized C4 macros using canonical IDs as aliases, regex is robust and lightweight enough to verify structural correctness.
  - *Alternative considered*: Using a PlantUML library — rejected due to unnecessary complexity and dependency overhead.

- **Scoring Approach**:
  - *Decision*: Score diagram correctness deterministically using proportional deductions for missing or misplaced entities. The SAAM score will be LLM-generated based on the strict evaluation criteria defined in the skill file.
  - *Rationale*: This provides a clear, math-based separation of concerns — deterministic aspects handle structural verification, while the LLM handles semantic architectural evaluation.

- **LLM Structured Output**:
  - *Decision*: Define `SAAMEvaluationResult` as a Pydantic `BaseModel` and pass it directly to `model.with_structured_output(SAAMEvaluationResult)` without specifying `method` or `strict`.
  - *Rationale*: Per current LangChain docs, when a Pydantic schema is passed directly, LangChain auto-selects ProviderStrategy if the model supports native structured output, falling back to ToolStrategy. This is the idiomatic approach and keeps the code provider-agnostic.
  - *Alternative considered*: Explicitly specifying `method="json_schema", strict=True` — rejected because it couples to specific provider features and the auto-selection is more portable.

- **Import Paths**:
  - *Decision*: Use `from langchain.messages import HumanMessage` (not `langchain_core.messages`).
  - *Rationale*: Current LangChain docs import messages from `langchain.messages`. The `langchain_core` path is deprecated.

## Risks / Trade-offs

- **Risk: Fragile Regex Parsing**
  - *Context*: Comments, multi-line definitions, or non-standard syntax in PlantUML might break regex extractors.
  - *Mitigation*: The parser will specifically ignore comment lines (starting with `'`) and handle standard single-line definitions. If multi-line definitions are common, the regex will need to account for them.

- **Risk: LLM SAAM Evaluation Hallucination**
  - *Context*: The LLM might award points just because a pattern name matches a quality attribute name without checking mechanistic justification.
  - *Mitigation*: The `SAAM_Validation.md` prompt must strictly instruct the LLM to award zero points for generic matching and demand stimulus-response scenario analysis.

- **Risk: Structured Output Compatibility**
  - *Context*: Some model providers may not support the `SAAMEvaluationResult` schema natively.
  - *Mitigation*: LangChain's auto-strategy selection handles this — falling back to ToolStrategy (tool calling) when ProviderStrategy is unavailable. The existing `evaluate_with_llm` error handling pattern will catch and gracefully degrade any failures.
