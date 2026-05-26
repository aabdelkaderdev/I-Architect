# axis-saam Specification

## Purpose
TBD - created by archiving change phase3-saam-diagram-verification. Update Purpose after archive.
## Requirements
### Requirement: SAAM LLM Validation
The system SHALL evaluate architectural patterns and technology choices against the top quality attributes using an LLM via `init_chat_model` and `with_structured_output(SAAMEvaluationResult)`.

#### Scenario: Pattern effectively addresses quality attribute
- **WHEN** a pattern is declared that addresses a top quality attribute and its stimulus-response scenario is mechanistically justified
- **THEN** the LLM awards appropriate points and provides a detailed reasoning

#### Scenario: Generic pattern reasoning
- **WHEN** a pattern name matches a quality attribute but lacks mechanistic justification for the stimulus-response scenario
- **THEN** the LLM awards zero points for that mapping

### Requirement: SAAMEvaluationResult Pydantic Model
The system SHALL define a `SAAMEvaluationResult` Pydantic `BaseModel` with fields: `score` (int, 0–30), `reasoning` (str), and `attribute_assessments` (list of per-attribute dicts). This model SHALL be passed to `model.with_structured_output(SAAMEvaluationResult)` without explicit `method` or `strict` parameters, allowing LangChain to auto-select the optimal strategy.

#### Scenario: Structured output auto-strategy
- **WHEN** `evaluate_saam_with_llm` is called and the model supports native structured output (ProviderStrategy)
- **THEN** LangChain uses ProviderStrategy for maximum reliability

#### Scenario: Structured output fallback
- **WHEN** the model does not support native structured output
- **THEN** LangChain falls back to ToolStrategy (tool calling) transparently

### Requirement: Node 4 Output Structuring
The system SHALL populate the `score_saam` AxisScore with the combined LLM SAAM score and deterministic diagram score, out of 50 total points.

#### Scenario: Output Generation
- **WHEN** Node 4 completes both deterministic verification and LLM evaluation
- **THEN** `score_saam` is populated with `awarded` points, `possible` set to 50, `sub_scores`, `llm_reasoning`, and `penalties_applied`

