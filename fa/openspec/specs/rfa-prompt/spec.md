## ADDED Requirements

### Requirement: Structured Classification Output
The system SHALL use `llm.with_structured_output(FilterBatch).with_retry(stop_after_attempt=3)` to parse the LLM's classification response into a `FilterBatch` containing `FilteredRequirement` objects. The `classification` field SHALL be typed as `Literal["SIGNAL", "NOISE"]` to enforce the constrained vocabulary at the Pydantic schema level. All fields SHALL use `Field(description=...)` to provide schema hints to the model.

#### Scenario: Valid classification format
- **WHEN** the LLM returns a well-formed response matching the `FilterBatch` schema
- **THEN** the system returns a validated `FilterBatch` object with each `classification` restricted to `"SIGNAL"` or `"NOISE"` by Pydantic's `Literal` type

#### Scenario: Invalid classification retry
- **WHEN** the LLM returns malformed output or the Pydantic schema validation fails
- **THEN** the `with_retry(stop_after_attempt=3)` chain automatically retries up to 2 additional times before raising a `ValidationError`

### Requirement: Dynamic Prompt Loading
The system SHALL load the RFA prompt from `ingestion/prompts/filter_classification.md` at Node invocation time rather than graph compilation time.

#### Scenario: Prompt iteration
- **WHEN** the prompt file is modified on disk
- **THEN** the next pipeline run will use the updated prompt without requiring graph recompilation

### Requirement: Signal and Noise Constraints
The RFA prompt SHALL define constraints based on IEEE 830 and project taxonomy, explicitly listing categories for Functional behavior, Integration points, and others as Signal, and tracebacks, logs, etc., as Noise.

#### Scenario: Classification mapping
- **WHEN** building the system message for the LLM
- **THEN** the system provides the exhaustive list of Noise categories and Signal characteristics to guide the model's response
