# Data Ingestion & Requirement Filtering — Phase 4: PDF Extractor

## Summary

This phase defines the PDF extraction strategy — how a PDF file is converted into raw text blocks suitable for normalisation. It covers page-by-page traversal, header/footer detection, table-aware parsing, and text block segmentation. It contains no normalisation logic and no LLM behaviour.

**Depends on:** Phase 1 (Foundation & Contracts) — for `ExtractionError`, `FormatMismatchError`, and the intentional no-LangChain-design decision. Phase 2 (Configuration) — for `IngestionConfig.pdf_engine` and `IngestionConfig.header_footer_threshold`. Phase 3 (Format Detection & Routing) — the router dispatches to this extractor when `file_format` is `"pdf"`.

**Required reading before:** Phase 6 (JSON Validator & Normaliser) — the normaliser consumes this extractor's output.

---

## 1. Purpose

The PDF extractor reads a PDF file page by page, strips repetitive headers and footers, detects and preserves table structure, segments the remaining text into candidate requirement blocks, and emits a list of raw text blocks. It uses `pdfplumber` as the preferred engine with `PyMuPDF` as a configurable fallback.

---

## 2. Position in Graph

```
Format Router → PDF Extractor → Normaliser → RFA → Output
```

This is one of four possible Node 2 paths. The router's conditional edge selects it when `file_format` is `"pdf"`.

---

## 3. Input

| Input | Source | Type | Description |
|-------|--------|------|-------------|
| File path | `raw_file_path` state channel | `str` | Absolute path to the PDF file |
| PDF engine | `ingestion_config.pdf_engine` | `str` | `"pdfplumber"` or `"pymupdf"` |
| Header/footer threshold | `ingestion_config.header_footer_threshold` | `float` | Fraction of pages for header/footer detection |

---

## 4. Extraction Strategy

### 4.1 Page Iteration

The extractor opens the PDF and iterates page by page, extracting text from each page. If no text is extractable from any page — the PDF is a scanned image without embedded text — the extractor raises `ExtractionError("No extractable text; OCR not supported")`. OCR is out of scope.

### 4.2 Header/Footer Stripping

After all pages are extracted, the extractor identifies repetitive text blocks — page numbers, document titles, confidential notices — via frequency analysis.

**Rule:** Text that appears identically on more than `header_footer_threshold` (default 60%) of pages is classified as a header or footer and removed from every page it appears on.

The threshold comparison is strict: a text block must match verbatim (after whitespace normalisation) to count toward the frequency. Near-duplicates (page numbers that increment) are not caught by frequency analysis and pass through — they are handled later by the normaliser's minimum length filter (see Phase 6).

### 4.3 Table Detection

The extractor uses the PDF library's built-in table extraction. Each table row is concatenated into a single requirement string.

Column headers are prepended as context if they contain semantic information. A header is considered semantic if it contains keywords like `ID`, `Requirement`, `Description`, `Shall`, `Must`, `Functional`, `Non-Functional`, or `Constraint`. A header like `No.` or `#` alone is not semantic and is not prepended.

Example: a row `[ "REQ-1", "The system shall refresh every 60 seconds" ]` with headers `[ "ID", "Description" ]` produces the string `"ID: REQ-1 | Description: The system shall refresh every 60 seconds"`.

### 4.4 Text Block Segmentation

After header/footer stripping, the remaining text on each page is segmented into candidate requirement blocks using a three-tier strategy:

1. **Numbered list detection (preferred).** A regex pattern identifies list items: `^\s*(\d+[\.\)]\s+|[a-zA-Z][\.\)]\s+|•\s+|[-–]\s+)`. Each list item becomes one candidate block.

2. **Paragraph splitting (fallback).** If no numbered structure is detected, double newlines (`\n\n`) separate paragraphs. Each paragraph becomes one candidate block.

3. **Sentence-level fallback.** If a paragraph exceeds 500 characters with no list structure, it is split on sentence boundaries (a period followed by a space and an uppercase letter). This prevents multi-hundred-character blobs from becoming single blocks.

### 4.5 Encoding Cleanup

Every extracted block passes through a cleanup step:
- Non-printable characters are stripped.
- Unicode is normalised to NFKD form.
- Smart quotes and other typographic characters are replaced with ASCII equivalents.

---

## 5. What Constitutes a Valid Extracted Block

A block extracted by the PDF extractor is a candidate — it has not yet been validated as a requirement. The normaliser (Phase 6) makes the final decision on what to keep and what to drop.

At this stage, a block is considered extractable if:
- It contains at least one non-whitespace character.
- It is not an empty string.
- It was not stripped as a header or footer.

There is no minimum length enforcement at this stage — that belongs to the normaliser.

---

## 6. Output

| Output | Channel | Type | Description |
|--------|---------|------|-------------|
| Extracted blocks | `extracted_blocks` | `list[dict]` | Each dict has: `text` (str, the candidate requirement text), `source_page` (int or null, the page number), `source_section` (str or null, section context if detected) |

The normaliser (Phase 6) reads `extracted_blocks` as its input.

---

## 7. Error Handling

| Condition | Response |
|-----------|----------|
| No extractable text on any page (scanned image PDF) | Raise `ExtractionError("No extractable text; OCR not supported")` |
| PDF file is corrupt or cannot be opened | Raise `ExtractionError` with the library's error message |
| PDF opens but content is not valid for the declared format | Raise `FormatMismatchError` |

---

## Phase Complete When...

- Page-by-page traversal logic is specified.
- Header/footer detection via frequency analysis is defined with its threshold rule.
- Table detection behaviour is specified, including the semantic header keywords list.
- The three-tier text block segmentation strategy is defined with its fallback chain.
- Encoding cleanup rules are listed.
- Output schema (`extracted_blocks` dict fields) is specified.
- Error conditions are paired with their exception types.
- No normalisation, ID assignment, or filtering logic appears in this file.
