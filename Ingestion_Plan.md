# Data Ingestion & Requirement Filtering Plan

## 0) Goal of this Portion

Define a two-stage pre-processing pipeline that sits **upstream of ARLO**. Stage 1 (Data Ingestion) accepts heterogeneous input formats (PDF, DOCX, TXT, JSON) and converts them into the standard `dict[str, str]` requirement schema that ARLO consumes. Stage 2 (Requirement Filtering Agent) classifies each extracted text block as **Signal** (meaningful high-level requirement) or **Noise** (implementation detail, traceback, terminal output), drops noise entries below a user-defined confidence threshold, and emits a clean requirement set ready for ARLO's `parse_requirements` node.

> **Pipeline position note:** This module is the **first stage** of I-Architect. Its sole output is a validated `dict[str, str]` written to `ARLOInput.requirements`. It produces no architecture, no diagrams, no embeddings. ARLO, RAA, SA, and AGA are all downstream consumers.

---

## 1) Inputs and Assumptions

### Inputs from Parent Pipeline / User
- **`file_path`** (`str`) — absolute path to the uploaded file (PDF, DOCX, TXT, or JSON).
- **`ingestion_config`** (optional) — user-configurable parameters for extraction behaviour: ID prefix, minimum block length, PDF engine preference, header/footer detection threshold.
- **`filter_config`** (optional) — user-configurable parameters for the Requirement Filtering Agent: confidence threshold, batch size, enable/disable toggle, reporting flags.

### Inputs from LLM Provider
- A `ChatOpenAI` (or compatible `BaseChatModel`) instance, shared with ARLO. The RFA uses this for classification calls.

### Assumptions
- The ingestion pipeline runs **before ARLO**. No ARLO state channels exist yet.
- The pipeline is invoked as a standalone LangGraph `StateGraph` by the parent orchestrator — not as a subgraph inside ARLO.
- OCR is explicitly out of scope; scanned PDFs without embedded text are unsupported.
- The pipeline is strictly sequential — no parallel fan-out is used within a single file ingestion.
- The ingestion pipeline uses format-specific Python libraries (`pdfplumber`, `python-docx`, `chardet`) directly instead of LangChain's `BaseLoader` document loader integrations. LangChain's document loaders provide a uniform `Document` abstraction suitable for RAG-style ingestion, but the ingestion pipeline requires fine-grained control over extraction heuristics (header/footer stripping, table-aware parsing, structured TXT detection) that the generic loader interface does not expose. This is an intentional design decision.

### Integration Pattern
The ingestion pipeline is implemented as a standalone LangGraph `StateGraph`. The parent orchestrator invokes the ingestion graph first, then passes its output (`extracted_requirements`, a `dict[str, str]`) directly to ARLO's input channel. This separation mirrors the AGA-to-SA handoff pattern: each stage is independently testable, and state schemas are not coupled across graph boundaries.

---

## 2) Authoritative Source Register

**Purpose:** Anchor the RFA's Signal/Noise classification criteria to authoritative requirement-quality standards, with explicit normative constraints rather than ad-hoc definitions.

### 2A — Source Register Table

| Source | URL | Retrieval Date | Governs |
|--------|-----|----------------|---------|
| IEEE 830 — Recommended Practice for Software Requirements Specifications | https://standards.ieee.org/standard/830-1998.html | (set on retrieval) | Requirement characteristics: clear, complete, consistent, verifiable, traceable |
| Project Noise Taxonomy | This document, renumbered §8B | Internal | Normative classification criteria for Signal vs Noise categories |

### 2B — Normative Prompt Constraints (Derived from Sources)

These paraphrased constraints are embedded into the RFA skill prompt, not raw document text.

**IEEE 830 constraints (Signal characteristics):**
- A well-formed requirement must describe **what** the system must do, not **how** it is implemented.
- A well-formed requirement must be unambiguous, complete, and verifiable.
- A well-formed requirement must state a single behaviour or constraint — compound requirements are a sign of under-specification.

**Signal criteria (project-defined):**
- Functional behaviour descriptions (system actions, responses, workflows).
- Integration point specifications (system interfaces, APIs, data flows).
- Security constraint statements (authentication, encryption, access control).
- Quality attribute requirements (performance, reliability, scalability, usability).
- Business logic rules (workflows, constraints, domain invariants).
- Compliance and regulatory requirements.

**Noise criteria (project-defined):**
- Tracebacks and exception chains (stack traces, error propagation paths).
- Terminal/console output and operational logs (timestamps, log levels, memory metrics).
- Hyper-specific library version dependencies (pinned version conflicts, ABI constraints).
- Isolated runtime state reports (single-node failures, connection pool exhaustion at specific counts).
- Code snippets and configuration fragments (inline code, property files, CLI flags).
- Change log entries and commit messages (version history, patch notes).
- Unit/integration test case descriptions (test names, mock setups, assertions).

### 2C — Retrieval Policy

- The RFA prompt template is stored in `ingestion/prompts/filter_classification.md` and loaded at Node invocation time, following the same convention as `arlo/prompts/`, `raa/prompts/`, `aga/prompts/`, and `sa/prompts/`.
- Each LLM call receives the full RFA prompt with the normative Signal/Noise criteria embedded — classification is the only LLM operation in the ingestion pipeline, so excerpt-scoping per node is not required.
- Direction of authority: **Source Register → Prompt Resource Bundle → skill prompt**.

---

## 3) Standard Requirement Format (Reference)

### 3A — Schema Definition

ARLO expects requirements as a flat JSON object: keys are requirement IDs (strings), values are requirement description text (strings).

```json
{
  "R1": "The system shall allow officers to report their status.",
  "R2": "The dispatch system must deliver sub-second response times.",
  "REQ-1": "The system shall refresh the display every 60 seconds."
}
```

**Structural rules:**
- Top-level value must be a JSON **object** (not an array).
- Every key must be a **non-empty string** (the requirement ID).
- Every value must be a **non-empty string** (the requirement description).
- No nested objects, no arrays, no numeric values.
- Minimum 1 requirement; no enforced maximum (ARLO handles batching internally).

### 3B — ID Convention

IDs follow the pattern `PREFIX-N` where `PREFIX` is an alphabetic string and `N` is a positive integer. Examples: `R1`, `REQ-1`, `FR-42`, `NFR-7`. The ingestion pipeline auto-generates IDs for formats that lack them (PDF, DOCX, TXT) using the prefix `REQ-` by default, configurable via `id_prefix` parameter.

---

## 4) High-Level Pipeline Overview

The ingestion pipeline consists of five sequential steps:

1. **Format Detection & Routing:** Read the file extension, validate the file is non-empty, and dispatch to the appropriate extractor.
2. **Format-Specific Extraction:** Run the PDF, DOCX, TXT, or JSON extraction strategy. Produce raw text blocks.
3. **Normalization:** Assign sequential IDs, deduplicate exact-match descriptions, apply minimum length filtering, and produce a `dict[str, str]`.
4. **Requirement Filtering (RFA):** Classify each requirement as Signal or Noise using batched LLM calls with structured output. Apply the confidence threshold. Produce a clean `dict[str, str]` plus a filtering report.
5. **Output Assembly:** Write the final `dict[str, str]` to the `extracted_requirements` state channel for handoff to ARLO.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Data Ingestion & Filtering                      │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │  File     │───▶│  Format  │───▶│  Extract │───▶│  Normalize   │  │
│  │  Upload   │    │  Router  │    │  (per    │    │  (ID assign, │  │
│  │          │    │          │    │  format) │    │   dedup)     │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────┬───────┘  │
│                                                          │          │
│                       ┌──────────────────────────────────┘          │
│                       │                                             │
│                       ▼                                             │
│              ┌──────────────────┐                                   │
│              │  JSON Compliant? │──── YES ──▶ Passthrough           │
│              │  (skip extract)  │                  │                 │
│              └────────┬─────────┘                  │                │
│                       │ NO (non-JSON or extracted)  │                │
│                       ▼                            ▼                │
│              ┌──────────────────┐    ┌──────────────────┐          │
│              │  Requirement     │───▶│  Clean Output    │          │
│              │  Filtering Agent │    │  dict[str, str]  │          │
│              │  (Signal/Noise)  │    │                  │          │
│              └──────────────────┘    └────────┬─────────┘          │
│                                               │                     │
└───────────────────────────────────────────────┼─────────────────────┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │     ARLO     │
                                        │  (existing)  │
                                        └──────────────┘
```

---

## 5) State Schema

### New State Channels

| Channel | Type | Reducer | Description |
|---------|------|---------|-------------|
| `raw_file_path` | `str` | overwrite | Absolute path to the uploaded file |
| `file_format` | `str` | overwrite | Detected format: `pdf`, `docx`, `txt`, `json` |
| `extracted_blocks` | `list[dict]` | overwrite | Raw text blocks from extraction, before normalization. Each dict: `{"text": str, "source_page": int\|null, "source_section": str\|null}` |
| `ingestion_config` | `dict` | overwrite | Serialized `IngestionConfig` |
| `filter_config` | `dict` | overwrite | Serialized `FilterConfig` |
| `filter_report` | `dict` | overwrite | Filtering summary report (see §8G) |
| `extracted_requirements` | `dict[str, str]` | overwrite | Final clean requirement set after filtering. This is the value passed to `ARLOInput.requirements`. |

### Existing State Reused

| Channel | Target | Used For |
|---------|--------|----------|
| `requirements` | `ARLOInput` | Receives the value of `extracted_requirements` at the ARLO boundary |
| `experiment_config` | `ARLOInput` | Passed through unchanged |
| `matrix` | `ARLOInput` | Passed through unchanged |

### RFA Structured Output Types

**`FilteredRequirement`:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | The requirement ID |
| `classification` | `str` | One of: `"SIGNAL"` or `"NOISE"` |
| `confidence` | `float` | LLM confidence in the classification, range 0.0–1.0 |
| `reason` | `str` | One-sentence justification for the classification |

**`FilterBatch`:**

| Field | Type | Description |
|-------|------|-------------|
| `requirements` | `list[FilteredRequirement]` | All classified requirements in a single batch |

---

## 6) Node Definitions

### Node 1: Format Detection & Routing (Deterministic)
* **Task:** Read the file extension, validate the file is non-empty, and dispatch to the appropriate extractor.
* **Action:**
  1. Validate that `raw_file_path` points to a non-empty file. Raise `EmptyFileError` if the file is 0 bytes.
  2. Extract the file extension (lowercased) and map it to a format: `.pdf` → `pdf`, `.docx` → `docx`, `.txt` → `txt`, `.json` → `json`.
  3. Raise `UnsupportedFormatError(extension)` for unrecognized extensions.
  4. Set `file_format` to the detected format.
* **Output:** `file_format`, `raw_file_path`.

### Node 2: Format-Specific Extraction (Deterministic)
* **Task:** Run the format-specific extraction strategy for the detected format, producing raw text blocks.
* **Action:**
  1. Dispatch to the appropriate extractor based on `file_format`:
     - **PDF:** Extract text page-by-page via `pdfplumber`. Strip headers/footers via frequency analysis. Detect tables and numbered lists. Segment into candidate requirement blocks.
     - **DOCX:** Iterate paragraphs and tables via `python-docx`. Detect list styles and heading-based sections. Filter empty/short paragraphs.
     - **TXT:** Detect encoding via `chardet`. Attempt structured `ID: Description` parsing; fall back to newline-delimited segmentation.
     - **JSON:** Validate schema compliance. If compliant, return the dict as-is (passthrough). If non-compliant, raise `NonStandardJSONError` with the offending keys and a descriptive reason.
  2. Raise `ExtractionError` if no extractable text is found (scanned PDF, image-only DOCX, etc.).
* **Output:** `extracted_blocks` (`list[dict]` of `{text, source_page, source_section}`).

### Node 3: Normalization (Deterministic)
* **Task:** Assign IDs, deduplicate, apply length filtering, and produce a `dict[str, str]` conforming to the standard schema (see §3A).
* **Action:**
  1. If the extractor detected inline IDs (e.g., from structured TXT), validate them for uniqueness and use them. Otherwise, assign sequential IDs using the configured `id_prefix` (default `"REQ-"`).
  2. Normalize whitespace: collapse multiple spaces/tabs to single space, strip leading/trailing whitespace.
  3. Deduplicate: if two blocks have identical text after normalization, keep only the first occurrence and log a warning.
  4. Drop blocks shorter than `min_block_length` characters (default 15).
  5. Truncate blocks longer than `max_block_length` characters (default 2000).
* **Output:** A `dict[str, str]` in the standard schema, written to `extracted_requirements` (tentative — may be reduced by Node 4).

### Node 4: Requirement Filtering — RFA (LLM)
* **Task:** Classify each requirement as Signal or Noise using batched LLM calls with structured output. Apply the confidence threshold to drop Noise entries.
* **Action:**
  1. Partition the requirement dict into batches of up to `filter_batch_size` (default 20).
  2. For each batch, load the RFA prompt template from `ingestion/prompts/filter_classification.md`. The human message contains the serialized batch as a JSON array of `{id, text}` objects.
  3. Invoke the LLM using LangChain's `with_structured_output` method, passing the `FilterBatch` schema (see §5). This ensures the model's response is automatically validated against the schema and returned as a typed object. If the model's response fails schema validation, the call is retried up to 2 times (configurable). LangChain supports multiple structured output methods (`json_schema`, `function_calling`, `json_mode`); the RFA uses the provider's default method unless overridden in the pipeline configuration.
  4. Each classification batch is dispatched as a LangGraph `@task`-decorated function call. The `@task` decorator wraps the LLM invocation in durable execution, ensuring that if the pipeline is interrupted mid-batch, completed batches are not re-executed on resume. This follows the LangGraph durable execution pattern: deterministic and idempotent workflow logic at the node level, with side effects (LLM calls) wrapped in `@task` for checkpoint granularity. Batches that are independent can be dispatched in parallel using the LangGraph Send API if the graph is configured for it.
  5. After all batches return, apply the confidence threshold:
     - NOISE with `confidence >= threshold` → **drop** from the requirement set.
     - NOISE with `confidence < threshold` → **keep** (insufficient confidence to drop).
     - SIGNAL at any confidence → **keep**.
  6. Build the filtering report (see §8G).
* **Output:** Reduced `extracted_requirements` (`dict[str, str]`), `filter_report`.

### Node 5: Output Assembly (Deterministic)
* **Task:** Write the final `dict[str, str]` to the `extracted_requirements` state channel and signal completion.
* **Action:**
  1. Validate that `extracted_requirements` contains at least 1 entry. Raise `EmptyRequirementsError` if empty.
  2. Set the final `extracted_requirements` value. The parent orchestrator reads this channel and passes it to `ARLOInput.requirements`.
* **Output:** Final `extracted_requirements` (`dict[str, str]`).

---

## 7) Part 1 — Data Ingestion Methodology

### 7A — Supported Input Formats

| Format | Extension | Extraction Method | Notes |
|--------|-----------|-------------------|-------|
| **PDF** | `.pdf` | `pdfplumber` (preferred) or `PyMuPDF` fallback | Handles multi-column layouts, tables, headers/footers |
| **DOCX** | `.docx` | `python-docx` | Extracts paragraphs, numbered/bulleted lists, and table cells |
| **TXT** | `.txt` | Raw file read (UTF-8) | Line-delimited; supports `ID: description` and plain-line formats |
| **JSON** | `.json` | `json.load` + schema validation | If compliant → passthrough; if non-compliant → raise exception |

### 7B — PDF Extraction (`pdf_extractor.py`)

1. **Page iteration:** Extract text page-by-page using `pdfplumber.open()`.
2. **Header/footer stripping:** Detect repeating text blocks across pages (page numbers, document titles, confidential notices) via frequency analysis. Text appearing identically on >60% of pages is classified as header/footer and removed.
3. **Table detection:** Use `pdfplumber`'s built-in table extraction. Each table row is concatenated into a single requirement string. Column headers are prepended as context if they contain semantic information (e.g., "Requirement ID", "Description").
4. **Text block segmentation:** After stripping headers/footers, segment remaining text into candidate requirement blocks using:
   - **Numbered list detection:** Regex pattern `^\s*(\d+[\.\)]\s+|[a-zA-Z][\.\)]\s+|•\s+|[-–]\s+)` identifies list items.
   - **Paragraph splitting:** Double newlines (`\n\n`) separate paragraphs when no numbered structure is detected.
   - **Sentence-level fallback:** If paragraphs exceed 500 characters with no list structure, split on sentence boundaries (`. ` followed by uppercase letter).
5. **Encoding cleanup:** Strip non-printable characters, normalize Unicode (NFKD), replace smart quotes with ASCII equivalents.

### 7C — DOCX Extraction (`docx_extractor.py`)

1. **Paragraph iteration:** Iterate `document.paragraphs` and extract `paragraph.text`.
2. **List detection:** Check `paragraph.style.name` for list styles (`List Bullet`, `List Number`, etc.). Each list item becomes one candidate requirement.
3. **Table extraction:** Iterate `document.tables`. For each table, check if the first row contains header keywords (`ID`, `Requirement`, `Description`, `Shall`, `Must`). If yes, extract row-by-row using the header mapping. If no header is detected, concatenate all cells per row.
4. **Heading-based sectioning:** Track heading paragraphs (`Heading 1`, `Heading 2`, etc.) as section context. If a heading contains keywords like "Requirements", "Functional Requirements", "Non-Functional Requirements", mark subsequent paragraphs as high-priority candidates.
5. **Empty paragraph filtering:** Skip paragraphs with only whitespace or fewer than 10 characters.

### 7D — TXT Extraction (`txt_extractor.py`)

1. **Encoding detection:** Use `chardet` to detect file encoding; decode accordingly.
2. **Structured format detection (preferred):** Attempt to parse each line as `ID: Description` using regex `^([A-Za-z]+-?\d+)\s*[:\.]\s*(.+)$`. If >50% of non-empty lines match, treat the file as pre-structured.
   - Example from `KaggleReq.txt`: `REQ-1: The system shall refresh the display every 60 seconds.`
3. **Unstructured fallback:** If structured detection fails:
   - Split on double newlines for paragraph mode.
   - Split on single newlines for line-per-requirement mode (determined by average line length: if avg < 200 chars → line mode; if avg >= 200 chars → paragraph mode).
4. **Bullet/number stripping:** Remove leading bullets, dashes, and numbering artifacts from each extracted block while preserving the semantic content.

### 7E — JSON Validation (`json_validator.py`)

This is the **only format that supports passthrough** — if the JSON is already compliant, no transformation is needed.

1. **Load and parse:** `json.load(file_handle)`.
2. **Schema compliance check:**
   - Is the root value a `dict`? → If no, raise `NonStandardJSONError`.
   - Are all keys non-empty strings? → If no, raise `NonStandardJSONError` with the offending keys.
   - Are all values non-empty strings? → If no, raise `NonStandardJSONError` with the offending keys.
   - Are there nested objects or arrays as values? → If yes, raise `NonStandardJSONError`.
3. **Compliant path:** Return the dict as-is. No extraction, no ID reassignment, no filtering. Skip directly to the Requirement Filtering Agent (Part 2) or, if filtering is disabled, pass straight to ARLO.
4. **Non-compliant path:** Raise `NonStandardJSONError` with a descriptive message. **Do not attempt automatic conversion.** The user must fix the JSON or provide a different format.

**`NonStandardJSONError`** is a subclass of `ValueError`. It carries two fields: `reason` (a human-readable string describing what failed schema validation) and `offending_keys` (an optional list of string keys that violated the schema rules). The exception message is formatted as `"Non-standard JSON format — {reason}: keys {offending_keys}"`.

### 7F — Normalization Step

After format-specific extraction, all text blocks pass through a shared normalizer:

1. **Whitespace normalization:** Collapse multiple spaces/tabs to single space. Strip leading/trailing whitespace.
2. **ID assignment:** For non-JSON formats, assign sequential IDs using the configured prefix: `REQ-1`, `REQ-2`, etc. If the extractor detected inline IDs (e.g., from a structured TXT), use those instead and validate for uniqueness.
3. **Deduplication:** Exact-match deduplication on normalized description text. If two blocks have identical text (after whitespace normalization), keep only the first occurrence and log a warning.
4. **Minimum length filter:** Drop blocks shorter than 15 characters after normalization — these are almost always section headers, page artifacts, or OCR noise, not requirements.
5. **Output:** `dict[str, str]` conforming to the standard schema (§3A).

### 7G — Ingestion Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id_prefix` | `str` | `"REQ-"` | Prefix for auto-generated requirement IDs |
| `min_block_length` | `int` | `15` | Minimum characters for a text block to be considered a valid requirement |
| `max_block_length` | `int` | `2000` | Maximum characters per block; longer blocks are truncated |
| `dedup_enabled` | `bool` | `true` | Enable exact-match deduplication on normalized description text |
| `encoding_fallback` | `str` | `"utf-8"` | Fallback encoding for TXT files when `chardet` detection is inconclusive |
| `pdf_engine` | `str` | `"pdfplumber"` | PDF extraction library: `"pdfplumber"` (preferred) or `"pymupdf"` |
| `header_footer_threshold` | `float` | `0.6` | Fraction of pages on which identical text must appear to be classified as header/footer |

### 7H — Error Handling & Edge Cases

| Scenario | Behaviour |
|----------|-----------|
| Empty file (0 bytes) | Raise `EmptyFileError` |
| PDF with no extractable text (scanned image) | Raise `ExtractionError("No extractable text; OCR not supported")` |
| DOCX with only images/charts | Raise `ExtractionError("No text content found")` |
| JSON with valid structure but 0 requirements | Raise `EmptyRequirementsError` |
| Mixed encoding in TXT | `chardet` auto-detection; log detected encoding |
| File extension doesn't match content | Validate by attempting parse; raise `FormatMismatchError` if parse fails |
| Unsupported file extension | Raise `UnsupportedFormatError(extension)` |

---

## 8) Part 2 — Requirement Filtering Agent

### 8A — Overview and Objective

The Requirement Filtering Agent (RFA) is the **gatekeeper** between raw ingested text and ARLO. Its purpose is to evaluate each requirement and classify it as:

- **Signal** — A meaningful high-level requirement (architectural intent, business logic, integration points, security constraints, quality attributes)
- **Noise** — An overly specific technical detail, implementation artifact, bug report, or operational log entry

Noise entries are **dropped** from the requirement set before it reaches ARLO. The user controls the aggressiveness of filtering via a **confidence threshold**.

### 8B — Classification Criteria

#### Signal (Architectural Requirements)

Characteristics — the text block describes:
- **What** the system must do (functional behaviour)
- **Integration points** (system interfaces, APIs, data flows)
- **Security constraints** (authentication, encryption, access control)
- **Quality attribute requirements** (performance, reliability, scalability, usability)
- **Business logic behaviour** (rules, workflows, constraints)
- **Compliance and regulatory requirements**

#### Noise (Technical & Implementation Details)

The agent is explicitly prompted to flag and drop the following categories:

| Noise Category | Description | Example |
|----------------|-------------|---------|
| **Tracebacks & Exceptions** | Chains of execution errors, stack traces | `Traceback (most recent call last): File "app.py", line 42...` |
| **Terminal Output** | Raw console artifacts, memory metrics, CLI logs | `[INFO] 2024-01-15 Server started on port 8080. Memory: 2.4GB` |
| **Implementation Dependencies** | Hyper-specific library version conflicts | `Requires numpy>=1.24.0,<1.25.0 due to ABI incompatibility with scipy` |
| **Isolated State Reports** | Descriptions of highly specific runtime failures | `The Redis connection pool exhausts after 47 concurrent writes on node 3` |
| **Code Snippets** | Inline code, configuration fragments | `server.port=8443` or `def handle_request(ctx):` |
| **Change Log Entries** | Version history, commit messages | `v2.3.1: Fixed null pointer in auth module` |
| **Test Case Descriptions** | Unit/integration test specifications | `Test: verify that login fails after 3 attempts with wrong password` |

### 8C — LLM Classification Prompt Design

The RFA uses a single LLM call per batch of requirements. The system prompt is loaded from `ingestion/prompts/filter_classification.md` at runtime. It instructs the model to classify each requirement as SIGNAL or NOISE, provides the normative Signal/Noise criteria from the Authoritative Source Register (§2B), and specifies the structured output schema the model must conform to. The human message contains the serialized batch of requirements as a JSON array of `{id, text}` objects.

The RFA invokes the LLM using LangChain's `with_structured_output` method, passing the `FilterBatch` schema (see §5). This ensures the model's response is automatically validated against the schema and returned as a typed object. If the model's response fails schema validation, the call is retried up to 2 times (configurable). LangChain supports multiple structured output methods (`json_schema`, `function_calling`, `json_mode`); the RFA uses the provider's default method unless overridden in the pipeline configuration.

### 8D — Confidence Threshold Mechanism

The user defines a **confidence threshold** (default: `0.7`, range: `0.0`–`1.0`) that controls filtering aggressiveness:

**Decision rules:**

| Classification | Confidence vs Threshold | Action |
|---------------|------------------------|--------|
| NOISE | `confidence >= threshold` | **Drop** — remove from requirement set |
| NOISE | `confidence < threshold` | **Keep** — insufficient confidence to drop; pass to ARLO |
| SIGNAL | any | **Keep** — always pass to ARLO |

**Interpretation:**
- **Low threshold (e.g., 0.3):** Aggressive filtering. Even uncertain noise classifications lead to drops. Risk: may discard borderline requirements.
- **High threshold (e.g., 0.9):** Conservative filtering. Only very obvious noise is dropped. Risk: some noise passes through to ARLO.
- **Threshold = 1.0:** Effectively disables noise filtering (nothing is dropped unless confidence is exactly 1.0).
- **Threshold = 0.0:** Drops everything classified as noise regardless of confidence.

### 8E — Batching Strategy

Requirements are batched for LLM classification to balance cost and context:

- **Batch size:** 20 requirements per LLM call (configurable via `filter_batch_size`).
- **Rationale:** Larger than ARLO's parsing batch (10) because classification is simpler than ASR extraction — less output per item, lower risk of output truncation.
- **Parallel execution:** Batches are independent and can be dispatched in parallel. Each classification batch is wrapped in a LangGraph `@task`-decorated function for durable checkpointing (see §10 for checkpointing details, §6 Node 4 for the `@task` execution pattern).

### 8F — Filtering Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | `bool` | `true` | Master switch for the Requirement Filtering Agent |
| `confidence_threshold` | `float` | `0.7` | Minimum LLM confidence to classify a requirement as NOISE and drop it |
| `filter_batch_size` | `int` | `20` | Number of requirements per LLM classification call |
| `log_dropped` | `bool` | `true` | Log dropped requirements with classification reasons |
| `emit_report` | `bool` | `true` | Produce a filtering summary report (see §8G) |

### 8G — Filtering Report

When `emit_report = True`, the RFA produces a structured summary:

```json
{
  "total_input": 555,
  "total_signal": 530,
  "total_noise_dropped": 20,
  "total_noise_kept": 5,
  "confidence_threshold": 0.7,
  "dropped_requirements": [
    {
      "id": "REQ-42",
      "original_text": "Traceback (most recent call last): ...",
      "confidence": 0.95,
      "reason": "Stack trace / exception chain"
    }
  ],
  "noise_kept_below_threshold": [
    {
      "id": "REQ-117",
      "original_text": "The product must make use of web/application server technology...",
      "confidence": 0.55,
      "reason": "Borderline — mentions specific technologies but also describes an integration constraint"
    }
  ]
}
```

This report is stored in the pipeline state for downstream audit and is included in the final PDF report generated by the reporting agent.

### 8H — Bypass Conditions

The Filtering Agent is **skipped entirely** when:
1. `FilterConfig.enabled = False` (user explicitly disables filtering).
2. The input is a **compliant JSON** that was passed through without extraction (the assumption being that a pre-structured JSON has already been curated by the user).
   - This is configurable: `skip_filter_for_json: bool = True` (default). Set to `False` to force filtering even on compliant JSON inputs.

---

## 9) Skills vs Static Templates

### Use Skills For
- **Signal/Noise classification (RFA LLM call):** requires interpretation of ambiguous requirement text — distinguishing a borderline architectural requirement from a technical implementation detail is a semantic judgment call, not a mechanical rule. The classification criteria from the Authoritative Source Register (§2B) are provided as constraints, but the model must exercise judgment in edge cases.

### Use Static Templates For
- **Format detection and routing:** deterministic extension matching — no interpretation required.
- **All format-specific extraction logic:** PDF layout parsing, DOCX paragraph/table iteration, TXT structured-line regex matching, JSON schema validation — all are deterministic algorithms with no ambiguity.
- **Normalization:** ID assignment, deduplication, length filtering — all mechanical operations applied uniformly.
- **Confidence threshold application:** a fixed arithmetic comparison (`confidence >= threshold`) with no interpretation.
- **Filtering report generation:** deterministic aggregation of counts and lists from classified results.

### Rationale
Following the same principle as RAA, AGA, and SA: LLM reasoning is applied only where interpretation or generation is required. All deterministic operations are kept in code to ensure reproducibility, avoid hallucination in structural operations, and minimize LLM token cost. The ingestion pipeline has exactly one skill (RFA classification); everything else is static.

---

## 10) Checkpointing

### Purpose
The ingestion pipeline is typically short-lived (seconds for extraction, plus one or more LLM calls for filtering). However, for large document sets (~1000+ requirements), the RFA may dispatch many parallel LLM calls. If the process is interrupted mid-filtering, all classified batches are lost and the pipeline must restart from scratch. SQLite checkpointing eliminates this cost by persisting state after each completed batch.

### 10A — Checkpointer Configuration
Use `SqliteSaver` from the `langgraph-checkpoint-sqlite` package (installed separately from `langgraph`). The checkpoint database path is **received from the orchestrator at runtime** — the orchestrator passes a project-scoped path `projects/{project_name}/checkpoints/ingestion.db` when calling `compile_for_production(db_path=...)` (see Orchestrator Plan §6C). The ingestion module's `compile_for_production()` accepts `db_path` as a **required parameter** with no default, ensuring the caller (orchestrator) always provides the project-scoped path.

### 10B — Graph Compilation
Pass the checkpointer at compile time so LangGraph automatically persists state at every super-step boundary. No further instrumentation is required.

### 10C — Thread Identity & Run Configuration
Each pipeline execution is identified by a `thread_id`. Use a stable, deterministic identifier derived from the input file path and a timestamp:

```
thread_id = "ing-" + sha256(file_path + timestamp)[:16]
```

The `ing-` prefix distinguishes ingestion checkpoint threads from RAA (`raa-`), AGA, and SA (`sa-`) threads. The thread ID is passed via `{"configurable": {"thread_id": "<computed_id>"}}`.

### 10D — Resume Semantics
At startup, query the checkpointer for existing state via `graph.get_state(run_config)`. If a snapshot exists and filtering has partially completed, the pipeline resumes from the last committed checkpoint — LangGraph replays from the last completed node, and the `@task`-decorated batch functions skip batches whose results are already persisted. If no snapshot exists, the pipeline starts fresh.

The filtering node (Node 4) is the only expensive step; extraction and normalization are deterministic and cheap to re-run. The `@task` decorator on each batch classification call provides finer granularity than node-level checkpointing: if a crash occurs mid-batch within the filtering node, completed batches are stored as pending writes and are not re-executed on resume.

### 10E — Checkpoint Lifecycle
The checkpoint database follows the same retention policy as the other agents: retained for 7 days after a completed run, then eligible for cleanup. The orchestrator is responsible for archiving or pruning.

---

## 11) Performance & Cost Profile

| Operation | Complexity / Cost |
|-----------|-------------------|
| Format detection & routing | O(1). No LLM cost. |
| PDF extraction | O(pages). No LLM cost. Dominated by `pdfplumber` parse time. |
| DOCX extraction | O(paragraphs + tables). No LLM cost. |
| TXT extraction | O(lines). No LLM cost. |
| JSON validation | O(keys). No LLM cost. |
| Normalization | O(n) where n = extracted blocks. No LLM cost. |
| RFA LLM calls | ⌈n / batch_size⌉ calls (default batch_size = 20). Each call classifies up to 20 requirements. |
| **Total LLM calls** | **⌈n / 20⌉** per ingestion run |
| **Wall-clock estimate (typical run)** | ~5–30 seconds for extraction + 1–10 seconds per LLM batch. A 200-requirement document with default batch size of 20 generates 10 LLM calls; at ~3 seconds per call, total wall-clock is ~30 seconds for filtering. |

Cost is dominated by the RFA LLM calls. Each classification call processes a small prompt context (20 requirement texts, ~2–5 KB), making classification cheap per call. For very large documents (1000+ requirements, 50+ LLM calls), parallel dispatch via `@task` with the Send API can reduce wall-clock time significantly.

---

## 12) Failure Modes & Mitigations

| Risk | Mitigation |
|------|------------|
| PDF with complex multi-column layout misaligns text | `pdfplumber` handles most layouts; log extraction quality metrics; user can pre-convert to TXT |
| LLM classifies a valid requirement as NOISE | Conservative default threshold (0.7); borderline items are kept; filtering report enables post-hoc review |
| LLM returns malformed structured output | Pydantic validation with retry (max 2 retries per batch) via `with_structured_output`; if still failing, keep all items in the batch unfiltered and log warning |
| Very large document (1000+ requirements) | Batching (20 per call) keeps individual LLM calls manageable; parallel dispatch via `@task` with Send API |
| Encoding issues in TXT/PDF | `chardet` detection + NFKD normalization; log detected encoding for debugging |
| Non-standard JSON triggers exception during automated pipeline | Exception is caught by the parent pipeline and surfaced to the user with a clear message and the offending keys |
| Process killed mid-filtering | SQLite checkpoint (§10) persists state after each super-step; `@task` ensures completed batches are not re-executed on resume |
| Checkpoint DB unavailable at startup | Fall back to fresh start; emit a `WARNING` log; do not crash |

---

## 13) Validation & Testing Criteria

### Unit Tests

- **JSON validator** correctly passes both `requirements.json` and `KaggleReq.json` as compliant.
- **JSON validator** raises `NonStandardJSONError` for: arrays, nested objects, empty strings as values, numeric values, empty dict.
- **TXT extractor** correctly parses `KaggleReq.txt` structured format (`ID: description`) and produces matching output to `KaggleReq.json`.
- **Normalizer** assigns sequential IDs with configured prefix.
- **Normalizer** deduplicates exact-match descriptions.
- **Normalizer** drops blocks shorter than `min_block_length`.
- **Filter Agent** classifies a known traceback string as NOISE with confidence > 0.9.
- **Filter Agent** classifies `"The system shall provide end-to-end encryption"` as SIGNAL.
- **Confidence threshold** at 0.7 drops NOISE with confidence 0.8 but keeps NOISE with confidence 0.6.

### Integration Tests

- End-to-end: PDF containing 30 requirements → extracted `dict[str, str]` with 30 entries → filtered set passed to ARLO `parse_requirements` node successfully.
- End-to-end: Compliant JSON → passthrough → ARLO invocation succeeds (no filtering applied when `skip_filter_for_json = True`).
- End-to-end: TXT with mixed noise (tracebacks interleaved with requirements) → filtering drops tracebacks → clean set reaches ARLO.

### Functional Tests

- **Format router** correctly identifies file type from extension and dispatches to the right extractor.
- **Filtering report** contains accurate counts matching the actual kept/dropped split.
- **Bypass logic** correctly skips filtering when `enabled = False` or when input is compliant JSON with `skip_filter_for_json = True`.
- **Checkpoint resume:** simulate a crash mid-filtering; verify that on resume, completed batches are not re-classified, and only the incomplete batch is re-run.

---

## 14) Deliverables for Spec Kit

1. **State schema** — all channels, types, and reducers (§5), including the `FilteredRequirement` and `FilterBatch` structured output types.
2. **Node implementations** — five sequential nodes: format detection & routing, format-specific extraction, normalization, RFA classification, and output assembly (§6).
3. **Format-specific extractors** — PDF, DOCX, TXT extraction logic, and JSON validator (§7B–§7E).
4. **RFA prompt template** — `ingestion/prompts/filter_classification.md` (§8C), loaded at runtime following the `arlo/prompts/` convention.
5. **Configuration dataclasses** — `IngestionConfig` and `FilterConfig`, specified as parameter tables (§7G, §8F).
6. **Custom exceptions** — error taxonomy covering all failure modes: `EmptyFileError`, `ExtractionError`, `EmptyRequirementsError`, `NonStandardJSONError`, `FormatMismatchError`, `UnsupportedFormatError` (§7H).
7. **Checkpointing configuration** — `SqliteSaver` setup with orchestrator-provided `db_path` (project-scoped per Orchestrator Plan §6C), thread ID derivation, resume semantics (§10).
8. **Project structure** — `ingestion/` package layout with `prompts/` subdirectory and `Skills/Ingestion/` resource bundle (§15).

---

## 15) Project Structure & Directory Layout

Following the same convention as `arlo/`, `raa/`, `aga/`, and `sa/`: runtime code and prompt templates live in the agent's code directory; skill definitions and reference documents live in `Skills/`.

### 15A — Code & Prompt Template Directory (`ingestion/`)

```
ingestion/
├── __init__.py
├── config.py                  # IngestionConfig, FilterConfig dataclasses
├── router.py                  # Format detection and routing
├── extractors/
│   ├── __init__.py
│   ├── base.py                # Abstract base extractor
│   ├── pdf_extractor.py       # PDF → text blocks
│   ├── docx_extractor.py      # DOCX → text blocks
│   ├── txt_extractor.py       # TXT → text blocks
│   └── json_validator.py      # JSON schema validation + passthrough
├── normalizer.py              # ID assignment, dedup, length filtering
├── filter_agent.py            # Requirement Filtering Agent (LLM-based)
├── exceptions.py              # Custom exceptions
├── models.py                  # Pydantic models (FilteredRequirement, FilterBatch)
└── prompts/
    └── filter_classification.md  # Runtime prompt for RFA LLM call (§8C)
```

### 15B — Skills Resource Bundle (`Skills/Ingestion/`)

```
Skills/Ingestion/
├── SKILL.MD                    # Ingestion pipeline skill definition
└── references/
    └── Signal_Noise_Taxonomy.md  # Normative classification criteria (§8B)
```

### 15C — Checkpoint Storage

Checkpoint databases are **project-scoped** (per Orchestrator Plan §6C). The orchestrator creates and manages the directory at `projects/{project_name}/checkpoints/` and passes the full path to each agent's `compile_for_production(db_path=...)` call:

```
projects/{project_name}/checkpoints/
├── orchestrator.db           # Orchestrator's own checkpoint
├── ingestion.db              # Ingestion pipeline checkpoints
├── arlo.db                   # ARLO checkpoints
├── raa_graph.db              # RAA checkpoints
├── aga.db                    # AGA checkpoints
├── sa.db                     # SA checkpoints
└── rga.db                    # RGA checkpoints
```

The ingestion module does **not** create or assume a shared `checkpoints/` directory at the project root. Directory creation is the orchestrator's responsibility.

### 15D — Convention

The `ingestion/prompts/` subdirectory follows the same convention as `arlo/prompts/`, `raa/prompts/`, `aga/prompts/`, and `sa/prompts/`. The `Skills/Ingestion/` directory is for skill definitions only — never for runtime code or prompt templates.

---

## 16) Dependencies

| Package | Purpose | Version Constraint |
|---------|---------|-------------------|
| `pdfplumber` | PDF text extraction | `>=0.10.0` |
| `python-docx` | DOCX parsing | `>=1.0.0` |
| `chardet` | TXT encoding detection | `>=5.0.0` |
| `pydantic` | Structured output models (`FilteredRequirement`, `FilterBatch`) | Already in project |
| `langchain-core` | Base types (`HumanMessage`, `SystemMessage`, `AIMessage`), `BaseChatModel` interface, `with_structured_output` method | Already in project |
| `langgraph` | `StateGraph` API, `@task` decorator for durable execution, `Send` API for parallel batch dispatch | Already in project |
| `langgraph-checkpoint-sqlite` | Provides `SqliteSaver` for checkpoint persistence (path provided by orchestrator at runtime per §6C) | Must be installed separately from `langgraph` |

> **Note:** No OCR dependency is included. Scanned PDFs without embedded text are explicitly unsupported in this version. If OCR is needed in the future, `pytesseract` + `pdf2image` can be added as an optional extra.

---

## 17) Open Design Decisions

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Should filtering be mandatory for non-JSON inputs? | (a) Always filter, (b) User opt-in, (c) User opt-out | **(c) Opt-out** — enabled by default, user can disable via `FilterConfig.enabled = False` |
| 2 | Should the filter agent use the same LLM as ARLO? | (a) Same LLM instance, (b) Separate cheaper model | **(a) Same LLM** — simplifies configuration; filtering is low-cost (simple classification) |
| 3 | Should we support batch file uploads (multiple files)? | (a) Single file only, (b) Multiple files merged | **(a) Single file** for v1 — multiple file support can be added later by iterating the ingestion pipeline per file and merging the normalized outputs |
| 4 | Should compliant JSON also go through filtering? | (a) Always skip, (b) Always filter, (c) Configurable | **(c) Configurable** — `skip_filter_for_json` defaults to `True` |
