## ADDED Requirements

### Requirement: Filtering bypass
The RFA node SHALL bypass filtering entirely if filtering is disabled or if the input was compliant JSON and the skip flag is enabled. The bypass check occurs before any batching or LLM calls.

#### Scenario: Filtering disabled
- **WHEN** `FilterConfig.enabled` is false
- **THEN** the normalised requirement set passes through unchanged, no LLM calls are made, and the filter report is `null`

#### Scenario: Compliant JSON skip enabled
- **WHEN** `FilterConfig.skip_filter_for_json` is true AND the input file extension is `.json`
- **THEN** the normalised requirement set passes through unchanged, no LLM calls are made, and the filter report is `null`

### Requirement: Requirement batching
The RFA SHALL partition the requirement dict into batches of size up to `FilterConfig.filter_batch_size` (default 20) for LLM classification, preserving natural dictionary order. Each batch is serialised as a JSON array of `{id, text}` objects.

#### Scenario: Requirements exceed batch size
- **WHEN** filtering is active and the requirement set is larger than `filter_batch_size`
- **THEN** the RFA chunks the requirements sequentially into multiple JSON array batches without sorting or shuffling

#### Scenario: Requirements within batch size
- **WHEN** filtering is active and the requirement set is smaller than or equal to `filter_batch_size`
- **THEN** all requirements are sent in a single batch

### Requirement: Structured LLM classification
The RFA SHALL use `llm.with_structured_output(FilterBatch)` to obtain validated Pydantic model output from the LLM, where `FilterBatch` contains a list of `FilteredRequirement` entries with `id`, `classification` (SIGNAL/NOISE), `confidence` (0.0–1.0), and `reason` fields.

#### Scenario: LLM returns structured classification
- **WHEN** a batch of requirements is sent to the LLM via `with_structured_output(FilterBatch)`
- **THEN** the response is a validated `FilterBatch` Pydantic model containing one `FilteredRequirement` per input requirement

### Requirement: LLM access via runtime context
The RFA node SHALL access the LLM instance via `runtime.context.llm` where `runtime` is a `Runtime[IngestionContext]` parameter injected by LangGraph. The `IngestionContext` dataclass is declared on the `StateGraph` via `context_schema=IngestionContext`.

#### Scenario: RFA node receives runtime
- **WHEN** the RFA node executes
- **THEN** it receives `runtime: Runtime[IngestionContext]` as its second parameter and accesses the LLM as `runtime.context.llm`

### Requirement: Confidence threshold dropping
The RFA SHALL evaluate each classified requirement against the confidence threshold. Signal entries are always kept. Noise entries are kept only if their confidence score is strictly below the threshold.

#### Scenario: Signal entry
- **WHEN** the LLM classifies a requirement as SIGNAL
- **THEN** the requirement is kept in the output set, regardless of confidence score

#### Scenario: Confident noise entry
- **WHEN** the LLM classifies a requirement as NOISE with confidence >= threshold
- **THEN** the requirement is dropped from the output set

#### Scenario: Uncertain noise entry
- **WHEN** the LLM classifies a requirement as NOISE with confidence < threshold
- **THEN** the requirement is kept in the output set

### Requirement: Filtering report generation
When `FilterConfig.emit_report` is true, the RFA SHALL produce a structured filtering report (as a `TypedDict`) detailing total input, total signal, total noise dropped, total noise kept, confidence threshold, and details for every dropped and below-threshold kept requirement. The report is written to the `filter_report` state channel.

#### Scenario: Report enabled
- **WHEN** filtering completes and `FilterConfig.emit_report` is true
- **THEN** a complete structured report is produced in the `filter_report` channel alongside the reduced `extracted_requirements` dict

#### Scenario: Report disabled
- **WHEN** filtering completes and `FilterConfig.emit_report` is false
- **THEN** the `filter_report` channel is set to `null`

### Requirement: Dropped requirement logging
When `FilterConfig.log_dropped` is true, the RFA SHALL log every dropped requirement at WARNING level.

#### Scenario: Dropped item logging
- **WHEN** an entry is dropped and `FilterConfig.log_dropped` is true
- **THEN** a WARNING level log is generated with the requirement's ID, confidence score, and reason

### Requirement: Filter report state channel
The `IngestionState` TypedDict SHALL include a `filter_report` key as `NotRequired[dict | None]` to carry the filtering report output from the RFA node.

#### Scenario: State schema includes filter_report
- **WHEN** the ingestion graph state is defined
- **THEN** `IngestionState` includes `filter_report: NotRequired[dict | None]`
