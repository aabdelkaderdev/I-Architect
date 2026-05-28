## Why

The RFA (Requirement Filtering Agent) needs a mechanism to batch classified requirements, evaluate confidence thresholds to decide what to drop, handle bypass paths, and generate a filtering report. This phase (Phase 8) establishes these mechanics separately from the taxonomy definition (Phase 7), enabling independent iteration of the filtering logic.

## What Changes

- Implements bypass and disable paths (if filtering is disabled or if JSON passthrough skip is enabled).
- Introduces batching of requirements (default size 20) preserving dict natural order.
- Uses `llm.with_structured_output(FilterBatch)` for validated Pydantic model output from the LLM.
- Applies a confidence threshold decision matrix (Signal is always kept; Noise is dropped only if confidence >= threshold).
- Defines a structured Filtering Report (as `TypedDict`) tracking total inputs, signals, dropped noise, and kept noise.
- Adds `filter_report` as a `NotRequired` channel to `IngestionState`.
- Implements logging policy for dropped requirements.

## Capabilities

### New Capabilities
- `rfa-filtering`: Handles batching of classifications, applying confidence threshold rules to drop noise, and generating the filtering report. Accesses the LLM via `Runtime[IngestionContext]` dependency injection.

### Modified Capabilities

## Impact

This will be integrated into the ingestion graph as Node 4 of 5. The RFA node uses the `Runtime[IngestionContext]` pattern (from `langgraph.runtime`) to access the LLM, consistent with the existing `rfa_node` signature. It consumes the `extracted_requirements` channel and `FilterConfig`, producing the reduced `extracted_requirements` and a `filter_report`.
