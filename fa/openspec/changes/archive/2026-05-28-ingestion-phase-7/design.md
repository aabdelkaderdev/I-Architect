## Context

The Requirement Filtering Agent (RFA) acts as a critical gatekeeper for the ingestion pipeline, evaluating raw requirement text to separate architectural Signal from implementation Noise. As defined in Phase 7, this requires defining the prompt taxonomy, the system and human messages, and strict structured output formats (`FilteredRequirement`, `FilterBatch`) to ensure the LLM's classification can be predictably consumed by deterministic downstream nodes.

## Goals / Non-Goals

**Goals:**
- Define the prompt specification for the LLM that encapsulates the IEEE 830 constraints and project Noise Taxonomy.
- Establish Pydantic models for structured output parsing of LLM responses.
- Load prompts dynamically at Node invocation time to allow prompt iteration without graph recompilation.

**Non-Goals:**
- Implementing batching logic, thresholds, or report generation (deferred to Phase 8).
- Replacing the LLM with deterministic regex/rules for classification.
- Any other ingestion pipeline logic (e.g., normalization or parsing).

## Decisions

- **Structured Output**: LangChain's `with_structured_output(FilterBatch)` will be used to bind the LLM response directly to Pydantic models. The `classification` field uses `Literal["SIGNAL", "NOISE"]` (not plain `str`) to enforce the constrained vocabulary at the Pydantic schema level — this is what instructs the provider's structured output mechanism to restrict the enum. All fields use `Field(description=...)` to provide schema hints to the model.
- **Retry on Malformed Output**: `with_structured_output` does not automatically retry on validation failures. Retry behavior must be implemented explicitly — either via `llm.with_structured_output(FilterBatch).with_retry(stop_after_attempt=3)` (chains retry AFTER binding so it catches `ValidationError`), or by using `with_structured_output(include_raw=True)` to receive `{"parsed": ..., "parsing_error": ...}` and retrying manually when `parsing_error` is non-null. The implementation SHALL use the `with_retry()` chained approach so retries are transparent to the calling node.
- **Prompt Structure**: The prompt will have a static system message (containing constraints and output schemas) and a dynamic human message (containing JSON-serialized batch data). The system message is constructed at invocation time by reading `ingestion/prompts/filter_classification.md` from disk, then passed as a `SystemMessage` alongside a `HumanMessage` with the batch JSON.
- **Dynamic Prompt Loading**: The prompt file is read at Node invocation time — not at graph compilation time — so prompt iteration does not require graph recompilation. The file is loaded using standard `pathlib.Path` reads relative to the `ingestion/prompts/` directory.

## Risks / Trade-offs

- **[Risk] Non-conformant Output from LLM** → **Mitigation**: `Literal["SIGNAL", "NOISE"]` in the Pydantic schema constrains the provider's output. Explicit retry via `with_retry(stop_after_attempt=3)` handles transient failures. Pydantic `ValidationError` on all retries bubbles up as a hard error.
- **[Risk] Hallucination in Classification** → **Mitigation**: `confidence: float = Field(ge=0.0, le=1.0, description=...)` and `reason: str = Field(description=...)` force the LLM to produce a bounded score and a textual justification, making misclassifications auditable.
