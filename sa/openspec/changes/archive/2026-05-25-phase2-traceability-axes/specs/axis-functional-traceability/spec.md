## ADDED Requirements

### Requirement: Deterministic Functional Mapping Coverage
The system SHALL compute the functional requirement mapping coverage deterministically as `(mapped functional reqs / total functional reqs) × 15`. It SHALL handle edge cases such as zero functional requirements without raising zero-division errors.

#### Scenario: All functional requirements mapped
- **WHEN** all functional requirements are mapped to at least one entity
- **THEN** the mapping coverage score component is 15

#### Scenario: Zero functional requirements
- **WHEN** the input contains no functional requirements
- **THEN** the mapping coverage computation avoids zero-division errors and returns 0

### Requirement: Deterministic Orphan Penalty
The system SHALL deduct 1 point for every functional requirement that is mapped to zero entities, up to a maximum deduction of 10 points.

#### Scenario: Single orphan functional requirement
- **WHEN** there is exactly 1 functional requirement mapped to 0 entities
- **THEN** the orphan penalty is -1

#### Scenario: High number of orphans
- **WHEN** there are 15 orphaned functional requirements
- **THEN** the orphan penalty is capped at -10

### Requirement: LLM Functional Depth Evaluation via with_structured_output
The system SHALL initialize a chat model using `init_chat_model` from `langchain.chat_models` and bind it to a Pydantic `BaseModel` schema via `model.with_structured_output(LLMEvaluationResult)`. The `LLMEvaluationResult` model SHALL define `score: int` (0–10) and `reasoning: str` fields. The system SHALL invoke the structured model with the depth distribution summary and functional requirements as prompt content.

#### Scenario: LLM structured output returns valid result
- **WHEN** the structured model returns a validated `LLMEvaluationResult` with `score=8` and `reasoning="..."`
- **THEN** the system applies the depth score of 8 and records the reasoning

#### Scenario: LLM invocation or validation fails
- **WHEN** the `with_structured_output` invocation raises an exception (validation error, API error, etc.)
- **THEN** the depth score defaults to 0 and the error message is recorded in reasoning

### Requirement: Functional Traceability Score Output
The system SHALL output an `AxisScore` object containing `awarded` (sum of coverage, depth, and penalty, clamped to >=0), `possible` (25), `sub_scores`, `llm_reasoning`, and `penalties_applied`.

#### Scenario: Final score calculation
- **WHEN** coverage is 15, depth is 8, and penalty is -2
- **THEN** the awarded score is 21 out of 25
