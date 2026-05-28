# Data Ingestion & Requirement Filtering — Phase 1: Foundation & Contracts

## Summary

This phase defines the shared contracts that every other ingestion phase depends on: where the ingestion pipeline sits in the I-Architect system, the two stages it comprises, what inputs it accepts, the standard requirement format it must produce, and every exception the pipeline can raise. It contains no extractor logic, no LLM behaviour, and no configuration — only the boundary definitions that make independent development of later phases possible.

**Depends on:** nothing. This is the first phase and has no internal dependencies.

**Required reading before:** Phase 2 (Configuration), Phase 3 (Format Detection & Routing), Phase 9 (LangGraph Wiring & State Schema).

---

## 1. Purpose

The Data Ingestion & Requirement Filtering pipeline is the **first module** in the I-Architect system. It accepts heterogeneous input formats (PDF, DOCX, TXT, JSON) and produces a single validated `dict[str, str]` of requirements, written to a state channel for handoff to ARLO. It produces no architecture, no diagrams, and no embeddings — it is purely a pre-processing stage.

The pipeline is invoked as a standalone LangGraph `StateGraph` by the parent orchestrator, not as a subgraph inside ARLO. It is independently testable, and its state schema is not coupled across graph boundaries.

---

## 2. Pipeline Position

```
Ingestion Pipeline → ARLO → RAA → AGA → SA
                     ↑
               (downstream consumers)
```

The ingestion pipeline runs **before ARLO**. No ARLO state channels exist when it runs. Its sole output is a clean, validated requirement set that the orchestrator hands off to `ARLOInput.requirements`.

The orchestrator is not part of this module. It triggers the ingestion graph, passes the LLM instance to it via LangGraph's runtime context (never through state channels), and handles the output handoff to ARLO. The orchestrator module is not yet developed.

---

## 3. Two-Stage Design Summary

The pipeline has two distinct stages:

### Stage 1 — Data Ingestion

Accepts a file path, detects the format, extracts raw text blocks using format-specific Python libraries, and normalises them into a `dict[str, str]` with auto-assigned IDs. This stage is entirely deterministic — no LLM calls.

### Stage 2 — Requirement Filtering Agent (RFA)

An LLM-based classifier that evaluates each requirement entry and labels it as **Signal** (a meaningful high-level requirement) or **Noise** (a traceback, log output, code snippet, or other implementation artifact). Noise entries above a configurable confidence threshold are dropped. The RFA emits a clean `dict[str, str]` plus a filtering report.

The RFA can be disabled entirely via configuration. When disabled, the normalised output from Stage 1 passes through unchanged.

---

## 4. Inputs

### 4.1 From the Orchestrator

| Input | Type | Description |
|-------|------|-------------|
| `file_path` | `str` | Absolute path to the uploaded file (PDF, DOCX, TXT, or JSON) |
| `ingestion_config` | `dict` (optional) | Serialised `IngestionConfig` — see Phase 2 |
| `filter_config` | `dict` (optional) | Serialised `FilterConfig` — see Phase 2 |

### 4.2 From the LLM Provider

A `ChatOpenAI` (or compatible `BaseChatModel`) instance, shared with ARLO. The orchestrator passes this via LangGraph's runtime `context`, never through state channels. State must remain serialisable — the LLM instance must not appear in any state channel.

The RFA uses this LLM for classification calls. Data Ingestion (Stage 1) does not use the LLM at all.

### 4.3 Assumptions

- The ingestion pipeline runs before ARLO. No ARLO state channels exist yet.
- The pipeline is invoked as a standalone LangGraph `StateGraph` by the parent orchestrator.
- OCR is explicitly out of scope. Scanned PDFs without embedded text are unsupported.
- The pipeline is strictly sequential — no parallel fan-out within a single file ingestion.
- Multiple file support is out of scope for v1. The pipeline processes one file per invocation.

---

## 5. Standard Requirement Format

ARLO expects requirements as a flat JSON object. Every extractor and the normaliser must produce output conforming to this schema.

### 5.1 Schema

```json
{
  "R1": "The system shall allow officers to report their status.",
  "R2": "The dispatch system must deliver sub-second response times.",
  "REQ-1": "The system shall refresh the display every 60 seconds."
}
```

### 5.2 Structural Rules

| Rule | Description |
|------|-------------|
| Root type | Must be a JSON **object** (not an array) |
| Key type | Every key must be a **non-empty string** (the requirement ID) |
| Value type | Every value must be a **non-empty string** (the requirement description) |
| No nesting | No nested objects, no arrays, no numeric values as values |
| Minimum size | At least 1 requirement entry |
| Maximum size | No enforced maximum — ARLO handles batching internally |

### 5.3 ID Convention

IDs follow the pattern `PREFIX-N` where `PREFIX` is an alphabetic string and `N` is a positive integer.

Valid examples: `R1`, `REQ-1`, `FR-42`, `NFR-7`.

For formats that lack inline IDs (PDF, DOCX, unstructured TXT), the ingestion pipeline auto-generates IDs using the configured prefix (default `"REQ-"`). For formats that provide their own IDs (structured TXT, JSON), the pipeline preserves them after validating uniqueness.

---

## 6. Intentional Design Decision: No LangChain Document Loaders

The ingestion pipeline does **not** use LangChain's `BaseLoader` document loader integrations. Format-specific Python libraries are used directly:

| Format | Library |
|--------|---------|
| PDF | `pdfplumber` |
| DOCX | `python-docx` |
| TXT | `chardet` + raw file read |
| JSON | `json.load` + manual validation |

This is an explicit design decision, not an oversight. LangChain's document loaders provide a uniform `Document` abstraction suitable for RAG-style ingestion, but the ingestion pipeline requires fine-grained control over extraction heuristics — header/footer stripping, table-aware parsing, structured TXT detection — that the generic loader interface does not expose. Direct library use gives each extractor full control over its extraction strategy.

---

## 7. JSON Passthrough Rule

Compliant JSON files that already match the standard requirement format (§5) **bypass extraction entirely**. The file is validated against the schema, and if compliant, the dict is returned as-is. No ID reassignment, no normalisation, no text extraction.

By default, filtering is also skipped for compliant JSON (configurable — see Phase 2, `FilterConfig.skip_filter_for_json`). The assumption is that a pre-structured JSON has already been curated by the user.

Non-compliant JSON (arrays, nested objects, numeric values, empty strings) raises a validation error — it is never silently coerced into the standard format.

---

## 8. Exception Taxonomy

All exceptions the ingestion pipeline can raise. Later phases reference these by name.

| Exception | Parent | Description |
|-----------|--------|-------------|
| `EmptyFileError` | `ValueError` | Raised when the input file is 0 bytes. Cannot proceed with an empty file. |
| `UnsupportedFormatError` | `ValueError` | Raised when the file extension does not match any supported format. Carries the unrecognised extension. |
| `ExtractionError` | `RuntimeError` | Raised when a format-specific extractor finds no extractable text (scanned PDF with no embedded text, image-only DOCX, etc.). Carries a human-readable reason. |
| `EmptyRequirementsError` | `ValueError` | Raised when the final requirement set contains zero entries. The pipeline must produce at least one requirement. |
| `NonStandardJSONError` | `ValueError` | Raised when a JSON file fails schema validation. Carries `reason` (human-readable description of the failure) and `offending_keys` (optional list of keys that violated the schema). Message format: `"Non-standard JSON format — {reason}: keys {offending_keys}"`. |
| `FormatMismatchError` | `ValueError` | Raised when a file's extension does not match its content (e.g., a PDF saved with a `.txt` extension). Detected by attempting to parse and failing. |

---

## 9. Output Contract

The ingestion pipeline produces exactly one output written to the `extracted_requirements` state channel:

| Channel | Type | Description |
|---------|------|-------------|
| `extracted_requirements` | `dict[str, str]` | The final clean requirement set after extraction, normalisation, and filtering. This is the value the orchestrator passes to `ARLOInput.requirements`. |

All entries conform to the standard requirement format (§5). The dict contains at least one entry; an empty dict triggers `EmptyRequirementsError`.

---

## Phase Complete When...

- The pipeline position and two-stage design are documented and unambiguous.
- Every input is named, typed, and its source identified.
- The standard requirement format (`dict[str, str]`) is specified with all structural rules.
- The "no LangChain document loaders" design decision is stated with its rationale.
- The JSON passthrough rule is defined.
- All six exceptions are named, categorised, and described with their trigger conditions.
- The output contract (channel name, type, content) is specified.
- No extractor logic, LLM behaviour, configuration fields, or state schema details appear in this file.
