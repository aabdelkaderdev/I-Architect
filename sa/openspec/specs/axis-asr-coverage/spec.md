## ADDED Requirements

### Requirement: Deterministic ASR Mapping Coverage
The system SHALL compute the ASR mapping coverage deterministically as `(mapped asrs / total asrs) × 15`. It SHALL handle the edge case of zero ASRs without raising zero-division errors.

#### Scenario: Partial ASR coverage
- **WHEN** half of the ASRs are mapped
- **THEN** the mapping coverage score component is appropriately computed (e.g. 7.5)

#### Scenario: Zero ASRs
- **WHEN** the input contains no ASR requirements
- **THEN** the mapping coverage computation avoids zero-division errors and returns 0

### Requirement: Deterministic Contradiction Penalty
The system SHALL identify technology contradictions based on ASR quality attributes and deduct 5 points per contradiction.

#### Scenario: Single contradiction found
- **WHEN** exactly 1 contradiction is identified
- **THEN** the contradiction penalty is -5

### Requirement: LLM Technology Specificity Evaluation via with_structured_output
The system SHALL initialize a chat model using `init_chat_model` from `langchain.chat_models` and bind it to a Pydantic `BaseModel` schema via `model.with_structured_output(LLMEvaluationResult)`. The same `LLMEvaluationResult` schema (with `score: int` 0–10 and `reasoning: str`) SHALL be reused from Node 2. The system SHALL invoke the structured model with the technology list, ASR requirements, and quality weights as prompt content loaded from `prompts/technology_specificity.md`.

#### Scenario: LLM structured output returns valid specificity evaluation
- **WHEN** the structured model returns a validated `LLMEvaluationResult` with `score=9` and `reasoning="..."`
- **THEN** the system applies the specificity score of 9 and records the reasoning

#### Scenario: LLM invocation or validation fails
- **WHEN** the `with_structured_output` invocation raises an exception
- **THEN** the specificity score defaults to 0 and the error message is recorded in reasoning

### Requirement: ASR Coverage Score Output
The system SHALL output an `AxisScore` object containing `awarded` (sum of coverage, specificity, and penalty, clamped to >=0), `possible` (25), `sub_scores`, `llm_reasoning`, and `penalties_applied`.

#### Scenario: Final score calculation with penalties clamping to zero
- **WHEN** coverage is 0, specificity is 0, and penalty is -5
- **THEN** the awarded score is clamped to 0
