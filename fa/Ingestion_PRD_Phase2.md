# Data Ingestion & Requirement Filtering — Phase 2: Configuration

## Summary

This phase defines the two configuration dataclasses — `IngestionConfig` and `FilterConfig` — that control every tunable behaviour in the ingestion pipeline. Every extractor, the normaliser, and the RFA reference these values. Settling them now prevents configuration drift across phases.

**Depends on:** Phase 1 (Foundation & Contracts) — the exception taxonomy and the standard requirement format are referenced by configuration defaults and descriptions.

**Required reading before:** Phase 3 (Format Detection & Routing), Phase 4 (PDF Extractor), Phase 5 (DOCX & TXT Extractors), Phase 6 (JSON Validator & Normaliser), Phase 7 (RFA: Signal/Noise Taxonomy & Prompt Spec), Phase 8 (RFA: Batching, Threshold & Filtering Report).

---

## 1. Purpose

Every tunable parameter in the ingestion pipeline lives in one of two configuration objects. Extractors, the normaliser, and the RFA read these values at runtime — they never hardcode defaults. This keeps behaviour auditable, testable, and user-configurable without code changes.

---

## 2. Design Principle

Configuration flows in one direction: the orchestrator deserialises user-provided config (or applies defaults), passes it into the ingestion graph via state channels, and every node reads from state. No node creates or modifies configuration. No node reaches around state to read a global.

---

## 3. IngestionConfig

Controls Stage 1 behaviour: extraction and normalisation.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id_prefix` | `str` | `"REQ-"` | Prefix prepended to auto-generated requirement IDs. The ID format is `{prefix}{N}` where `N` is a 1-based sequential integer. Ignored when inline IDs are detected and preserved (structured TXT, JSON passthrough). |
| `min_block_length` | `int` | `15` | Minimum character count for a text block to be kept as a requirement. Blocks shorter than this after whitespace normalisation are dropped — they are almost always section headers, page artifacts, or OCR noise. |
| `max_block_length` | `int` | `2000` | Maximum character count per requirement. Blocks exceeding this are truncated. Guards against extractors producing oversized entries from malformed layouts. |
| `dedup_enabled` | `bool` | `true` | When enabled, exact-match deduplication runs during normalisation. Two blocks with identical text after whitespace normalisation result in the second occurrence being dropped with a warning. |
| `encoding_fallback` | `str` | `"utf-8"` | Fallback encoding for TXT files when `chardet` detection is inconclusive. Used only after `chardet` reports low confidence. |
| `pdf_engine` | `str` | `"pdfplumber"` | PDF extraction library. `"pdfplumber"` is the preferred default. `"pymupdf"` is available as a fallback for documents where `pdfplumber`'s layout engine misparses complex multi-column layouts. |
| `header_footer_threshold` | `float` | `0.6` | Fraction of pages on which identical text must appear to be classified and stripped as a header or footer. At 0.6, text appearing verbatim on more than 60% of pages is removed. Range: `0.0`–`1.0`. |

---

## 4. FilterConfig

Controls Stage 2 behaviour: the Requirement Filtering Agent.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | `bool` | `true` | Master switch for the RFA. When `false`, the entire filtering stage is skipped and the normalised requirement set passes through unchanged. When `true`, the RFA classifies and filters according to the rules below. |
| `confidence_threshold` | `float` | `0.7` | Minimum LLM confidence for a NOISE classification to trigger a drop. Higher values are more conservative (fewer drops). Lower values are more aggressive (more drops). Range: `0.0`–`1.0`. See Phase 8 for the full decision matrix. |
| `filter_batch_size` | `int` | `20` | Number of requirements per LLM classification call. Larger batches reduce the number of LLM calls but increase per-call token usage. See Phase 8 for batching rationale. |
| `log_dropped` | `bool` | `true` | When enabled, every dropped requirement is logged with its classification, confidence, and reason. |
| `emit_report` | `bool` | `true` | When enabled, the RFA produces a structured filtering report summarising input count, signal count, noise dropped, and noise kept below threshold. See Phase 8 for the report schema. |
| `skip_filter_for_json` | `bool` | `true` | When enabled, compliant JSON inputs that passed through extraction unchanged also skip filtering. The assumption is that pre-structured JSON has already been curated. Set to `false` to force filtering even on compliant JSON. |

---

## 5. Configuration Flow

```
User (or defaults)
       │
       ▼
  Orchestrator (deserialises, validates)
       │
       ▼
  Ingestion State (ingestion_config, filter_config channels)
       │
       ├──▶ Format Router (reads id_prefix)
       ├──▶ Extractors (read pdf_engine, encoding_fallback)
       ├──▶ Normaliser (reads id_prefix, min_block_length, max_block_length, dedup_enabled)
       └──▶ RFA (reads all FilterConfig fields)
```

No node modifies configuration state channels. They are write-once by the orchestrator, read-many by nodes.

---

## 6. Validation Rules

The orchestrator is responsible for validating configuration before graph invocation. These rules are documented here so the orchestrator and the ingestion module agree on what constitutes valid input:

| Field | Rule |
|-------|------|
| `id_prefix` | Non-empty string; only alphabetic characters and hyphens. Must end with a hyphen. |
| `min_block_length` | Integer ≥ 1. Must be less than `max_block_length`. |
| `max_block_length` | Integer ≥ `min_block_length`. |
| `header_footer_threshold` | Float in range `0.0`–`1.0`. |
| `confidence_threshold` | Float in range `0.0`–`1.0`. |
| `filter_batch_size` | Integer ≥ 1. |
| `pdf_engine` | One of `"pdfplumber"` or `"pymupdf"`. |

Invalid configuration should be caught by the orchestrator before the ingestion graph is invoked. If invalid config reaches the ingestion pipeline, behaviour is undefined — the pipeline does not re-validate.

---

## Phase Complete When...

- Every `IngestionConfig` field is named, typed, given a default, and described with its governance scope.
- Every `FilterConfig` field is named, typed, given a default, and described with its governance scope.
- The configuration flow diagram shows which nodes read which config objects.
- Validation rules are explicit enough that the orchestrator can implement them without ambiguity.
- No extraction logic, LLM prompt content, or state schema details appear in this file.
