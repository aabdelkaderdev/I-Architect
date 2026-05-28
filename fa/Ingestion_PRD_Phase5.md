# Data Ingestion & Requirement Filtering — Phase 5: DOCX & TXT Extractors

## Summary

This phase defines the extraction strategies for DOCX and TXT files. These two extractors are covered together because they are comparably sized and share the same output contract. Each converts its format into raw text blocks suitable for normalisation, with no LLM involvement.

**Depends on:** Phase 1 (Foundation & Contracts) — for `ExtractionError`, `FormatMismatchError`, and the no-LangChain-design decision. Phase 2 (Configuration) — for `IngestionConfig.encoding_fallback`. Phase 3 (Format Detection & Routing) — the router dispatches to these extractors when `file_format` is `"docx"` or `"txt"`.

**Required reading before:** Phase 6 (JSON Validator & Normaliser) — the normaliser consumes these extractors' output.

---

## Part A: DOCX Extractor

### A1. Purpose

The DOCX extractor reads a `.docx` file, iterates paragraphs and tables, detects list styles and heading-based sections, and emits candidate requirement blocks. It uses `python-docx`.

### A2. Input

| Input | Source | Type | Description |
|-------|--------|------|-------------|
| File path | `raw_file_path` state channel | `str` | Absolute path to the DOCX file |

### A3. Extraction Strategy

#### A3.1 Paragraph Iteration

The extractor iterates every paragraph in the document and reads `paragraph.text`. Each paragraph is evaluated for its style and content before being accepted as a candidate block.

#### A3.2 List Detection

The extractor checks `paragraph.style.name` for list-related styles: `List Bullet`, `List Number`, `List Paragraph`, and similar variants. Each list item becomes one candidate requirement block, with the list marker (bullet character or number) stripped from the text.

Nested lists are flattened — each item at any nesting level becomes its own candidate block. The nesting structure is not preserved.

#### A3.3 Table Extraction

The extractor iterates all tables in the document. For each table:

1. **Header detection:** The first row is inspected for header keywords (`ID`, `Requirement`, `Description`, `Shall`, `Must`, `Functional`, `Non-Functional`). If two or more cells match, the row is treated as a header row and used to label subsequent row data.

2. **Row extraction:** Each subsequent row is concatenated into a single requirement string. If a header row was detected, each cell is prefixed with its column header (e.g., `"ID: REQ-1 | Description: The system shall..."`). If no header was detected, cells are concatenated with a separator.

3. **Empty tables:** Tables where all cells are empty or whitespace-only are skipped.

#### A3.4 Heading-Based Sectioning

The extractor tracks heading paragraphs (`Heading 1`, `Heading 2`, `Heading 3`, etc.) as section context. If a heading contains keywords like `Requirements`, `Functional Requirements`, `Non-Functional Requirements`, `Business Requirements`, or `System Requirements`, subsequent paragraphs (until the next heading of equal or higher level) are marked as high-priority candidates.

Heading text itself is not emitted as a requirement block — it is recorded in the `source_section` field of the blocks that follow it.

#### A3.5 Empty and Short Paragraph Filtering

Paragraphs with only whitespace or fewer than 10 characters are skipped at this stage. This is a lightweight pre-filter; the normaliser (Phase 6) applies the definitive `min_block_length` check.

### A4. DOCX Output

| Output | Channel | Type | Description |
|--------|---------|------|-------------|
| Extracted blocks | `extracted_blocks` | `list[dict]` | Each dict has: `text` (str), `source_page` (null for DOCX — page numbers are not reliably available), `source_section` (str or null, the nearest heading text if applicable) |

### A5. DOCX Error Handling

| Condition | Response |
|-----------|----------|
| Document contains no text (only images, charts, or empty paragraphs) | Raise `ExtractionError("No text content found")` |
| File cannot be opened as DOCX | Raise `FormatMismatchError` |

---

## Part B: TXT Extractor

### B1. Purpose

The TXT extractor reads a plain-text file, detects its encoding, attempts to parse structured `ID: Description` lines, and falls back to paragraph or line-based segmentation when no structure is found.

### B2. Input

| Input | Source | Type | Description |
|-------|--------|------|-------------|
| File path | `raw_file_path` state channel | `str` | Absolute path to the TXT file |
| Encoding fallback | `ingestion_config.encoding_fallback` | `str` | Fallback encoding when `chardet` is inconclusive |

### B3. Extraction Strategy

#### B3.1 Encoding Detection

The extractor reads the raw bytes and passes them through `chardet` to detect the file encoding. If `chardet` reports a confidence below 0.7, the extractor falls back to `encoding_fallback` (default `"utf-8"`) and logs the detected-but-uncertain encoding.

The file is then decoded using the determined encoding. Decoding failures with the detected encoding trigger a retry with the fallback encoding.

#### B3.2 Structured Format Detection (Preferred Path)

The extractor attempts to parse each non-empty line against the pattern:

```
^([A-Za-z]+-?\d+)\s*[:\.]\s*(.+)$
```

This matches lines like `REQ-1: The system shall refresh the display every 60 seconds.`

If more than 50% of non-empty lines match this pattern, the file is treated as pre-structured:
- The matched ID (e.g., `REQ-1`) is recorded as the inline ID.
- The matched description is recorded as the requirement text.
- Unmatched lines are skipped.

Inline IDs are preserved through normalisation (see Phase 6). The normaliser validates them for uniqueness.

#### B3.3 Unstructured Fallback

If structured format detection fails (fewer than 50% of lines match), the extractor falls back to segmentation:

1. **Mode detection:** The extractor computes the average line length of non-empty lines. If the average is under 200 characters, it uses **line mode** — each non-empty line is one candidate requirement. If the average is 200 characters or more, it uses **paragraph mode** — text is split on double newlines (`\n\n`), and each paragraph is one candidate block.

2. **Line mode:** Each non-empty line becomes one block. Blank lines are skipped.

3. **Paragraph mode:** Text is split on `\n\n`. Each resulting paragraph has its internal newlines collapsed to spaces.

#### B3.4 Bullet and Number Stripping

In both structured and unstructured paths, leading bullets, dashes, and numbering artifacts are stripped from the description text. The regex `^\s*(\d+[\.\)]\s+|[a-zA-Z][\.\)]\s+|•\s+|[-–]\s+)` removes the marker while preserving the semantic content that follows.

### B4. TXT Output

| Output | Channel | Type | Description |
|--------|---------|------|-------------|
| Extracted blocks | `extracted_blocks` | `list[dict]` | Each dict has: `text` (str), `source_page` (null for TXT), `source_section` (null for TXT) |

For structured TXT, the extracted blocks carry the inline ID in a field recognised by the normaliser. The exact mechanism (a separate field on the block dict, or a marker in the text) is an implementation detail of the normaliser integration — see Phase 6.

### B5. TXT Error Handling

| Condition | Response |
|-----------|----------|
| File contains no non-whitespace characters | Raise `ExtractionError("No text content found")` |
| File cannot be decoded with detected or fallback encoding | Raise `ExtractionError` with the encoding details |

---

## Phase Complete When...

- DOCX: paragraph iteration, list detection via style names, table extraction with header detection, heading-based sectioning, and the 10-character pre-filter are all specified.
- TXT: encoding detection via `chardet` with fallback, structured format detection (50% threshold rule), unstructured fallback with mode detection (200-char average threshold), and bullet/number stripping are all specified.
- Both extractors' output schemas match the `extracted_blocks` contract defined in Phase 4.
- Error conditions are paired with their exception types.
- No normalisation, ID assignment, or filtering logic appears in this file.
