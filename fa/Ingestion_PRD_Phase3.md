# Data Ingestion & Requirement Filtering — Phase 3: Format Detection & Routing

## Summary

This phase defines the format router — the first node in the ingestion graph. It validates the input file, detects the format from the file extension, and dispatches to the correct extractor. It contains no extraction logic and no LLM behaviour.

**Depends on:** Phase 1 (Foundation & Contracts) — for `EmptyFileError`, `UnsupportedFormatError`, and the supported format list. Phase 2 (Configuration) — for `IngestionConfig`, though the router itself uses only `id_prefix`.

**Required reading before:** Phase 4 (PDF Extractor), Phase 5 (DOCX & TXT Extractors), Phase 6 (JSON Validator & Normaliser). Each extractor is a dispatch target of this node.

---

## 1. Purpose

The format router is the first node in the ingestion graph. It answers one question: "given this file, which extractor should run?" It validates that the file is processable before any extraction work begins, failing fast on empty files and unsupported formats.

---

## 2. Position in Graph

```
File Upload → Format Router → Extractor (per format) → Normaliser → RFA → Output
```

This is Node 1 of 5 in the sequential ingestion graph. If this node fails, no subsequent node runs. See Phase 9 for the full graph definition.

---

## 3. Input

| Input | Source | Type | Description |
|-------|--------|------|-------------|
| File path | `raw_file_path` state channel | `str` | Absolute path to the uploaded file, set by the orchestrator before graph invocation |

---

## 4. Processing Steps

### Step 1: File Validation

The router verifies that the file at `raw_file_path` exists and is non-empty (size > 0 bytes).

- If the file does not exist, the behaviour is a standard filesystem error — the orchestrator should validate existence before invoking the graph.
- If the file is 0 bytes, the router raises `EmptyFileError`.

### Step 2: Extension Detection

The router extracts the file extension (lowercased) and maps it to a canonical format name using a static mapping:

| Extension | Canonical Format | Dispatches To |
|-----------|-----------------|---------------|
| `.pdf` | `pdf` | PDF Extractor (Phase 4) |
| `.docx` | `docx` | DOCX Extractor (Phase 5) |
| `.txt` | `txt` | TXT Extractor (Phase 5) |
| `.json` | `json` | JSON Validator (Phase 6) |

If the extension is not in this table, the router raises `UnsupportedFormatError` carrying the unrecognised extension.

### Step 3: Format Write

The router writes the canonical format string (`"pdf"`, `"docx"`, `"txt"`, or `"json"`) to the `file_format` state channel. The graph's conditional edge reads this channel to route to the correct extractor node.

---

## 5. Format Mismatch Handling

The router does **not** inspect file content to verify that the extension matches the actual format. Format mismatch (a PDF saved as `.txt`, a DOCX saved as `.pdf`) is detected by the extractor when it attempts to parse the file and fails. The extractor raises `FormatMismatchError` at that point.

This is intentional: content sniffing would require each extractor's parsing logic to be duplicated in the router. Failing at extraction time keeps the router simple and the error message specific (the extractor knows _why_ the parse failed).

---

## 6. Output

| Output | Channel | Type | Description |
|--------|---------|------|-------------|
| Detected format | `file_format` | `str` | One of `"pdf"`, `"docx"`, `"txt"`, or `"json"` |
| File path | `raw_file_path` | `str` | Passed through unchanged |

The graph uses `file_format` to route to the correct extractor via a conditional edge. No other node reads `file_format` for routing — it is set once and consumed by the edge condition.

---

## 7. Error Handling

| Condition | Response |
|-----------|----------|
| File is 0 bytes | Raise `EmptyFileError`. Do not proceed. |
| Extension not in supported list | Raise `UnsupportedFormatError(extension)`. Do not proceed. |
| File does not exist | Filesystem error. Orchestrator responsibility — the router does not catch this. |

---

## Phase Complete When...

- The three processing steps (validate, detect, write) are specified with their inputs and outputs.
- The extension-to-format mapping table covers all four supported formats.
- The format mismatch policy is documented (detected at extraction time, not by the router).
- Error conditions are paired with their exception types from Phase 1.
- No extraction logic, extractor internals, or normalisation behaviour appears in this file.
