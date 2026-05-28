## Context

The RFA (Requirement Filtering Agent) identifies noise in requirement sets. This design covers the operational mechanics of the RFA node in the ingestion graph (Node 4 of 5), defining how requirements are batched for classification, how the confidence threshold is applied to determine whether to drop or keep requirements, and how the results are reported.

The RFA node follows the LangGraph node function signature `def rfa_node(state: IngestionState, runtime: Runtime[IngestionContext])`, where `Runtime` is imported from `langgraph.runtime`. The LLM instance is accessed via `runtime.context.llm` — the `IngestionContext` dataclass is passed to the graph at invocation time via the `context` parameter and declared on the graph builder via `context_schema=IngestionContext`.

LLM classification uses `llm.with_structured_output(FilterBatch)` to obtain validated Pydantic model output directly from the LLM, following the LangChain structured output pattern for Pydantic schemas.

## Goals / Non-Goals

**Goals:**
- Implement batching for requirements sent to the LLM (default size 20).
- Apply a confidence threshold to decide what to drop (Signal always kept; Noise dropped if confidence >= threshold).
- Provide bypass/disable paths for the RFA node.
- Generate a comprehensive Filtering Report tracking total inputs, dropped noise, and kept noise.
- Add `filter_report` as a `NotRequired` channel to `IngestionState`.

**Non-Goals:**
- Defining the classification taxonomy or prompt (covered in Phase 7).
- Defining the full LangGraph wiring and state schema (covered in Phase 9).
- Modifying the normaliser output or earlier graph stages.

## Decisions

- **Runtime Context for LLM:** The LLM is injected via `Runtime[IngestionContext]` and accessed as `runtime.context.llm`. This follows the LangGraph dependency injection pattern — the LLM is static context for the run, not mutable graph state.
- **Structured Output:** Classification uses `llm.with_structured_output(FilterBatch)` where `FilterBatch` is a Pydantic `BaseModel`. Pydantic provides the richest validation (field constraints, descriptions, nested structures) and is the recommended schema type for structured output per LangChain docs.
- **Report Types:** `DroppedRequirement`, `KeptNoiseRequirement`, and `FilterReport` are defined as `TypedDict` (not Pydantic) since they are internal report data structures, not LLM output schemas. This keeps them lightweight and consistent with the `IngestionState` TypedDict convention.
- **Batch Size:** A batch size of 20 was chosen because classification is a simpler task than extraction, meaning less output per item and a lower risk of output truncation. This reduces the number of LLM calls and total latency.
- **Batch Construction:** Requirements will be grouped sequentially based on the natural order of the input dict. No sorting, shuffling, or grouping will be applied to preserve simplicity.
- **Parallel Execution:** Batches will be evaluated independently. The exact mechanism of parallelism will be delegated to the graph implementation (Phase 9).
- **Threshold Application:** The system conservatively drops entries. Signal is always kept, and Noise is kept unless the confidence is greater than or equal to the configurable threshold.

## Risks / Trade-offs

- **Empty Output Dict:** If the threshold is low or there is overwhelming noise, the RFA might drop all requirements.
  - *Mitigation*: The RFA gracefully produces an empty output dict and report. The Output Assembly node will explicitly handle `EmptyRequirementsError`.
- **High Threshold Tuning:** Tuning the confidence threshold requires balance. Too low (e.g., 0.3) risks discarding borderline requirements, while too high (e.g., 0.9) risks allowing too much noise through.
  - *Mitigation*: Expose threshold configuration and log all dropped items to provide an audit trail.
