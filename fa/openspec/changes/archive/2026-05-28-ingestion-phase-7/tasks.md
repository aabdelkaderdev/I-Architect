## 1. Pydantic Models

- [x] 1.1 Define `FilteredRequirement` Pydantic model with fields: `id: str`, `classification: Literal["SIGNAL", "NOISE"]`, `confidence: float = Field(ge=0.0, le=1.0, description=...)`, `reason: str = Field(description=...)`.
- [x] 1.2 Define `FilterBatch` Pydantic model with a single field: `requirements: list[FilteredRequirement]`.

## 2. Prompt Template

- [x] 2.1 Create `ingestion/prompts/filter_classification.md` file.
- [x] 2.2 Write the static system message incorporating IEEE 830 constraints, Signal/Noise taxonomy, and output schemas.
- [x] 2.3 Write the dynamic human message template that accepts a JSON-serialized batch of `{id, text}` objects.

## 3. RFA Node Update

- [x] 3.1 Implement prompt loading logic using `pathlib.Path` to read `filter_classification.md` from disk at Node invocation time.
- [x] 3.2 Build the structured LLM chain using `llm.with_structured_output(FilterBatch).with_retry(stop_after_attempt=3)` — chaining `with_retry` AFTER `with_structured_output` ensures retries happen on `ValidationError` during Pydantic parsing.
- [x] 3.3 Invoke the chain with `[SystemMessage(content=system_prompt), HumanMessage(content=batch_json)]`; catch any remaining `ValidationError` after exhausted retries and propagate as a hard pipeline error.
