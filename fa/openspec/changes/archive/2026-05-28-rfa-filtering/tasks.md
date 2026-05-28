## 1. Types and Schemas

- [x] 1.1 Define `DroppedRequirement` as a `TypedDict` with fields: `id`, `original_text`, `confidence`, `reason`
- [x] 1.2 Define `KeptNoiseRequirement` as a `TypedDict` with fields: `id`, `original_text`, `confidence`, `reason`
- [x] 1.3 Define `FilterReport` as a `TypedDict` with fields: `total_input`, `total_signal`, `total_noise_dropped`, `total_noise_kept`, `confidence_threshold`, `dropped_requirements`, `noise_kept_below_threshold`
- [x] 1.4 Add `filter_report: NotRequired[dict | None]` to `IngestionState` in `schema.py`

## 2. Core Filtering Mechanics

- [x] 2.1 Implement requirement batching function to partition the input dict sequentially into JSON arrays of `{id, text}` objects
- [x] 2.2 Implement LLM classification using `llm.with_structured_output(FilterBatch)` (existing Pydantic schema in `schema.py`)
- [x] 2.3 Implement confidence threshold logic (Signal always kept; Noise dropped only if confidence >= threshold)
- [x] 2.4 Implement filter report generation as a `FilterReport` TypedDict, tracking totals and compiling lists of dropped/kept items
- [x] 2.5 Implement dropped requirement WARNING-level logging when `FilterConfig.log_dropped` is true

## 3. RFA Node Integration

- [x] 3.1 Implement bypass logic for `FilterConfig.enabled = false` (no-op, return unchanged requirements, `filter_report = null`)
- [x] 3.2 Implement bypass logic for compliant JSON passthrough skip (check file extension via state)
- [x] 3.3 Update `rfa_node` to use `runtime: Runtime[IngestionContext]` signature and access LLM as `runtime.context.llm`
- [x] 3.4 Update `rfa_node` to return both `extracted_requirements` and `filter_report` in its output dict

## 4. Testing

- [x] 4.1 Write unit tests for requirement batching functionality
- [x] 4.2 Write unit tests for bypass conditions (filtering disabled, JSON skip)
- [x] 4.3 Write unit tests for confidence threshold decision matrix (signal kept, confident noise dropped, uncertain noise kept)
- [x] 4.4 Write unit tests for filter report generation and dropped requirement logging
