# Data Ingestion & Requirement Filtering — Phase 8: RFA Batching, Threshold & Filtering Report

## Summary

This phase defines how the RFA uses the classification results from Phase 7: how the normalised requirement set is split into batches for the LLM, how the confidence threshold is applied to each classification to decide what to drop, the bypass and disable paths that skip filtering entirely, and the structure of the filtering report produced alongside the clean requirement set.

**Depends on:** Phase 7 (RFA: Signal/Noise Taxonomy & Prompt Spec) — for the classification criteria, prompt template, and structured output schema this phase consumes. Phase 2 (Configuration) — for `FilterConfig` (all fields). Phase 6 (JSON Validator & Normaliser) — this phase receives the normalised `dict[str, str]` as input.

**Required reading before:** Phase 9 (LangGraph Wiring & State Schema) — the RFA node definition references the batching and threshold rules defined here.

---

## 1. Purpose

The RFA does three things after receiving classifications from the LLM: it decides what to drop based on a confidence threshold, it tracks what was dropped and why, and it produces a structured report. This phase defines the mechanics — the "how" — separate from the taxonomy (Phase 7) so each can be iterated independently.

---

## 2. Position in Graph

```
Normaliser → RFA → Output Assembly
```

The RFA is Node 4 of 5 in the ingestion graph. It reads the tentative `extracted_requirements` from the normaliser and writes the reduced `extracted_requirements` plus a `filter_report`. See Phase 9 for the full graph definition.

---

## 3. Input

| Input | Source | Type | Description |
|-------|--------|------|-------------|
| Requirements | `extracted_requirements` state channel | `dict[str, str]` | The normalised requirement set from Phase 6 |
| All FilterConfig fields | `filter_config` state channel | `dict` | Serialised `FilterConfig` — see Phase 2 |

---

## 4. Bypass and Disable Paths

The RFA is skipped entirely when either condition is true:

| Condition | Config Field | Behaviour |
|-----------|-------------|-----------|
| User disables filtering | `FilterConfig.enabled = false` | The normalised requirement set passes through unchanged. No LLM calls are made. No report is generated. |
| Compliant JSON passthrough with skip enabled | `FilterConfig.skip_filter_for_json = true` AND the input was a compliant JSON | The requirement set passes through unchanged. No LLM calls are made. No report is generated. |

Both conditions are checked before any batching begins. If either is true, the RFA node is effectively a no-op — it writes the input `extracted_requirements` to its output unchanged and sets `filter_report` to `null`.

---

## 5. Batching Strategy

When filtering is active, the requirement dict is partitioned into batches for LLM classification.

### 5.1 Batch Size

Each batch contains up to `filter_batch_size` requirements (default 20). The last batch may be smaller.

### 5.2 Rationale

A batch size of 20 is larger than ARLO's parsing batch size (10) because classification is a simpler task than ASR extraction — less output per item, lower risk of output truncation. Fewer, larger batches mean fewer LLM calls and lower total latency.

### 5.3 Batch Construction

Requirements are serialised as a JSON array of `{id, text}` objects. The order within a batch is the iteration order of the input dict. No sorting, shuffling, or grouping is applied — the dict's natural order is preserved.

### 5.4 Parallel Execution

Batches are independent of each other. Each batch classification is dispatched as a separate call, and batches can run in parallel if the graph is configured for it. The specific parallelism mechanism is an implementation detail of the graph wiring (see Phase 9).

---

## 6. Confidence Threshold Mechanism

After all batches return, each classified requirement is evaluated against the confidence threshold.

### 6.1 Decision Matrix

| Classification | Confidence vs Threshold | Action |
|---------------|------------------------|--------|
| SIGNAL | Any value | **Keep** — always pass to ARLO |
| NOISE | `confidence >= threshold` | **Drop** — remove from requirement set |
| NOISE | `confidence < threshold` | **Keep** — insufficient confidence to drop; pass to ARLO |

Signal entries are never dropped, regardless of confidence. Noise entries are only dropped when the LLM is sufficiently confident that the entry is noise.

### 6.2 Threshold Interpretation

| Threshold Range | Behaviour |
|-----------------|-----------|
| Low (e.g., 0.3) | Aggressive filtering. Even uncertain noise classifications lead to drops. Risk: may discard borderline requirements. |
| Default (0.7) | Balanced. Only reasonably confident noise classifications are dropped. |
| High (e.g., 0.9) | Conservative filtering. Only very obvious noise is dropped. Risk: some noise passes through to ARLO. |
| 1.0 | Effectively disables noise filtering — nothing is dropped unless confidence is exactly 1.0. |
| 0.0 | Drops everything classified as NOISE regardless of confidence. |

### 6.3 Edge Cases

- **All entries are Signal:** Nothing is dropped. The output dict is identical to the input.
- **All entries are Noise above threshold:** The entire dict is dropped. If the result is empty, `EmptyRequirementsError` is raised at the Output Assembly node (see Phase 9), not here — the RFA reduces the set; output assembly validates the result.
- **Empty input dict:** The RFA node handles this gracefully — it produces an empty output dict and a report showing zero items. Output assembly will raise `EmptyRequirementsError`.

---

## 7. Filtering Report

When `FilterConfig.emit_report` is `true`, the RFA produces a structured summary of its decisions.

### 7.1 Report Schema

| Field | Type | Description |
|-------|------|-------------|
| `total_input` | `int` | Number of requirements before filtering |
| `total_signal` | `int` | Number classified as SIGNAL (all kept) |
| `total_noise_dropped` | `int` | Number classified as NOISE with confidence ≥ threshold (dropped) |
| `total_noise_kept` | `int` | Number classified as NOISE with confidence < threshold (kept) |
| `confidence_threshold` | `float` | The threshold used for this run |
| `dropped_requirements` | `list[DroppedRequirement]` | Details for every dropped entry |
| `noise_kept_below_threshold` | `list[KeptNoiseRequirement]` | Details for noise entries kept below threshold |

### 7.2 DroppedRequirement

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | The requirement ID |
| `original_text` | `str` | The full requirement text that was dropped |
| `confidence` | `float` | The LLM's confidence score |
| `reason` | `str` | The LLM's one-sentence justification |

### 7.3 KeptNoiseRequirement

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | The requirement ID |
| `original_text` | `str` | The full requirement text |
| `confidence` | `float` | The LLM's confidence score (below threshold) |
| `reason` | `str` | The LLM's justification for the noise classification |

### 7.4 Logging

When `FilterConfig.log_dropped` is `true`, every dropped requirement is logged at `WARNING` level with its ID, confidence, and reason. This provides an audit trail even if the full report is not emitted.

---

## 8. Output

| Output | Channel | Type | Description |
|--------|---------|------|-------------|
| Filtered requirements | `extracted_requirements` | `dict[str, str]` | The reduced requirement set. Signal entries plus noise entries kept below threshold. |
| Filter report | `filter_report` | `dict` or `null` | The filtering report as defined in §7.1, or `null` if filtering was bypassed. |

---

## Phase Complete When...

- Bypass conditions are specified: `enabled = false` and compliant JSON skip.
- Batching strategy is defined: size, rationale, construction rules, and parallelism note.
- The confidence threshold decision matrix is specified with all three cases.
- Threshold interpretation ranges (low, default, high, 1.0, 0.0) are documented.
- The filtering report schema is fully typed with all three nested types.
- Edge cases (all signal, all noise, empty input) are handled.
- The logging policy for dropped requirements is specified.
- No prompt content, taxonomy criteria, or state schema details appear in this file.
