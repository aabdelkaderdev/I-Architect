# Data Ingestion & Requirement Filtering — Phase 6: JSON Validator & Normaliser

## Summary

This phase defines two sequential operations: the JSON validator (which checks schema compliance and implements the passthrough path) and the normaliser (which assigns IDs, deduplicates, and applies length filtering to every extracted block regardless of source format). They are covered together because normalisation is the direct continuation of extraction for all formats.

**Depends on:** Phase 1 (Foundation & Contracts) — for `NonStandardJSONError`, the standard requirement format (§5), and the JSON passthrough rule. Phase 2 (Configuration) — for `IngestionConfig.id_prefix`, `min_block_length`, `max_block_length`, and `dedup_enabled`. Phase 3 (Format Detection & Routing) — the router dispatches to the JSON validator when `file_format` is `"json"`.

**Required reading before:** Phase 7 (RFA: Signal/Noise Taxonomy & Prompt Spec) — the RFA consumes the normaliser's output.

---

## Part A: JSON Validator

### A1. Purpose

The JSON validator checks whether a `.json` file conforms to the standard requirement format (Phase 1, §5). Compliant files bypass extraction and, by default, filtering. Non-compliant files raise a descriptive error — they are never silently coerced.

### A2. Position in Graph

The JSON validator is the extractor node for `file_format = "json"`. It replaces the PDF/DOCX/TXT extractors in the graph path. The normaliser (Part B of this phase) follows it for non-JSON formats, but for compliant JSON the path is shorter (see A4).

### A3. Input

| Input | Source | Type | Description |
|-------|--------|------|-------------|
| File path | `raw_file_path` state channel | `str` | Absolute path to the JSON file |

### A4. Processing Steps

#### Step 1: Load and Parse

The file is loaded and parsed with `json.load()`. Standard JSON decode errors (malformed syntax, invalid characters) propagate as the library's native exceptions — the orchestrator handles them.

#### Step 2: Schema Compliance Check

The parsed value is checked against every structural rule from Phase 1, §5.2:

| Check | Rule | Failure Response |
|-------|------|-----------------|
| Root type is `dict` | Top-level value must be a JSON object | Raise `NonStandardJSONError` with `reason="Root value is not a dict"` |
| All keys are non-empty strings | Every key must be a string with length ≥ 1 | Raise `NonStandardJSONError` with `offending_keys` listing the invalid keys |
| All values are non-empty strings | Every value must be a string with length ≥ 1 | Raise `NonStandardJSONError` with `offending_keys` listing the invalid keys |
| No nested structures | Values must not be dicts, lists, or numbers | Raise `NonStandardJSONError` with `offending_keys` listing keys with invalid value types |

All checks run — the validator does not stop at the first failure. The error message aggregates all failures found.

#### Step 3: Compliant Path (Passthrough)

If all checks pass, the dict is returned as-is. No extraction, no ID reassignment, no normalisation. The `extracted_requirements` state channel is set directly to the parsed dict.

By default, filtering is also skipped (controlled by `FilterConfig.skip_filter_for_json` — see Phase 2). The assumption is that a pre-structured JSON has already been curated.

#### Step 4: Non-Compliant Path

If any check fails, `NonStandardJSONError` is raised with:
- `reason`: a human-readable string describing what failed.
- `offending_keys`: an optional list of string keys that violated the schema.

The message is formatted as: `"Non-standard JSON format — {reason}: keys {offending_keys}"`.

The pipeline does not attempt to convert non-compliant JSON into compliant form. The user must fix the file or provide a different format.

---

## Part B: Normaliser

### B1. Purpose

The normaliser takes raw extracted blocks from any format (PDF, DOCX, TXT) and converts them into a clean `dict[str, str]` conforming to the standard requirement format. It assigns IDs, normalises whitespace, deduplicates, and filters by length. It is entirely deterministic.

### B2. Position in Graph

```
Extractor (PDF/DOCX/TXT) → Normaliser → RFA → Output
```

The normaliser is Node 3 of 5 in the ingestion graph. The JSON validator bypasses it. See Phase 9 for the full graph definition.

### B3. Input

| Input | Source | Type | Description |
|-------|--------|------|-------------|
| Extracted blocks | `extracted_blocks` state channel | `list[dict]` | Raw text blocks from the extractor (Phase 4 or Phase 5) |
| ID prefix | `ingestion_config.id_prefix` | `str` | Prefix for auto-generated IDs |
| Min block length | `ingestion_config.min_block_length` | `int` | Minimum characters to keep |
| Max block length | `ingestion_config.max_block_length` | `int` | Maximum characters; longer blocks truncated |
| Dedup enabled | `ingestion_config.dedup_enabled` | `bool` | Whether to deduplicate |

### B4. Processing Steps

#### Step 1: ID Assignment

Each block is assigned an ID:

- **Inline IDs present (structured TXT):** If the extractor detected inline IDs, the normaliser validates them for uniqueness. Duplicate inline IDs trigger a warning and sequential suffixes are appended (e.g., `REQ-1` and `REQ-1_2`). After validation, the inline IDs are used as-is.

- **No inline IDs (all other formats):** Sequential IDs are auto-generated using the configured `id_prefix`. The first block gets `{prefix}1`, the second `{prefix}2`, and so on. IDs are 1-based.

#### Step 2: Whitespace Normalisation

For every block's text:
- Multiple consecutive spaces and tabs are collapsed to a single space.
- Leading and trailing whitespace is stripped.
- Internal newlines are replaced with spaces.

The original text is not preserved — only the normalised form moves forward.

#### Step 3: Length Filtering

Two checks are applied after whitespace normalisation:

- **Minimum length:** Blocks shorter than `min_block_length` characters (default 15) are dropped. These are almost always section headers, page number artifacts, or fragments without semantic content.

- **Maximum length:** Blocks longer than `max_block_length` characters (default 2000) are truncated to the limit. This guards against malformed extraction producing oversized entries from, for example, a PDF page that was one continuous text blob.

#### Step 4: Deduplication

If `dedup_enabled` is `true`, the normaliser checks for exact-match descriptions (after whitespace normalisation). If two blocks have identical text, the second occurrence is dropped and a warning is logged. The first occurrence keeps its ID.

Deduplication is case-sensitive and whitespace-sensitive. "The system shall log in users" and "The system shall  log in users" (double space) are not duplicates — whitespace normalisation runs first, so the double space would already be collapsed.

### B5. Output

| Output | Channel | Type | Description |
|--------|---------|------|-------------|
| Normalised requirements | `extracted_requirements` | `dict[str, str]` | A clean dict conforming to the standard requirement format (Phase 1, §5). This is the tentative output — the RFA may reduce it further. |

If the dict is empty after length filtering and deduplication, the normaliser raises `EmptyRequirementsError`.

---

## 6. Combined Flow

```
Non-JSON formats:
  Extractor → extracted_blocks → Normaliser → extracted_requirements (tentative) → RFA

JSON format (compliant):
  JSON Validator → extracted_requirements (final, passthrough) → [bypass RFA]

JSON format (non-compliant):
  JSON Validator → NonStandardJSONError (pipeline halts)
```

---

## Phase Complete When...

- JSON validator: all four schema compliance checks are specified with their failure responses.
- JSON validator: the passthrough path and the non-compliant error path are both defined.
- Normaliser: ID assignment rules (inline preservation vs auto-generation) are specified.
- Normaliser: whitespace normalisation, length filtering (min and max), and deduplication rules are specified with their edge cases.
- The combined flow diagram correctly shows the three paths (non-JSON, compliant JSON, non-compliant JSON).
- Error conditions are paired with their exception types.
- No extraction logic, LLM classification, filtering, or state schema details appear in this file.
