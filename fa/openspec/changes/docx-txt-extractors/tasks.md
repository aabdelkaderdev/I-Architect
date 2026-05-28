## 1. Setup

- [x] 1.1 Verify `python-docx` and `chardet` are in project dependencies (both are already imported in `extractors.py`)
- [x] 1.2 Verify Phase 1 error classes (`ExtractionError`, `FormatMismatchError`) are importable from `ingestion.exceptions`

## 2. DOCX Extractor — Rewrite `extract_from_docx` in `ingestion/extractors.py`

- [x] 2.1 Change return type from `list[str]` to `list[dict]` (each dict: `text`, `source_page`, `source_section`)
- [x] 2.2 Implement paragraph iteration with filtering (skip whitespace-only or < 10 chars)
- [x] 2.3 Implement list detection via `paragraph.style.name` (`List Bullet`, `List Number`, `List Paragraph`) with marker stripping and nested-list flattening
- [x] 2.4 Implement heading-based section tracking (`Heading 1`–`Heading 3`) to populate `source_section` for blocks under requirement-related headings
- [x] 2.5 Implement table extraction with header-row detection (≥ 2 keyword matches) and cell concatenation
- [x] 2.6 Raise `FormatMismatchError` if file cannot be opened as DOCX; raise `ExtractionError("No text content found")` if no text blocks extracted

## 3. TXT Extractor — Rewrite `extract_from_txt` in `ingestion/extractors.py`

- [x] 3.1 Change return type from `list[str]` to `list[dict]` (each dict: `text`, `source_page` = None, `source_section` = None)
- [x] 3.2 Implement encoding detection via `chardet` with < 0.7 confidence fallback to `encoding_fallback` parameter
- [x] 3.3 Implement structured format detection: regex `^([A-Za-z]+-?\d+)\s*[:\.]\s*(.+)$`, use if > 50% of non-empty lines match, capturing inline IDs
- [x] 3.4 Implement unstructured fallback with mode detection (average line length < 200 → line mode, ≥ 200 → paragraph mode on `\n\n`)
- [x] 3.5 Implement bullet/number prefix stripping via regex `^\s*(\d+[\.\\)]\s+|[a-zA-Z][\.\\)]\s+|•\s+|[-–]\s+)`
- [x] 3.6 Raise `ExtractionError("No text content found")` if no non-whitespace text; raise `ExtractionError` with encoding details on decode failure

## 4. Graph Node Updates in `ingestion/graph.py`

- [x] 4.1 Update `docx_extractor_node` to write to `extracted_blocks` instead of calling `generate_ids_for_blocks` inline (matching `pdf_extractor_node` pattern)
- [x] 4.2 Update `txt_extractor_node` to write to `extracted_blocks` instead of calling `generate_ids_for_blocks` inline (matching `pdf_extractor_node` pattern)
- [x] 4.3 Verify `normaliser_node` bridge already handles `extracted_blocks` → `extracted_requirements` for both new extractors

## 5. Testing

- [x] 5.1 Write unit tests for `extract_from_docx` (paragraphs, lists, tables with/without headers, heading sections, empty documents, corrupt files)
- [x] 5.2 Write unit tests for `extract_from_txt` (encoding detection, structured vs unstructured, bullet stripping, empty files, decode failures)
- [x] 5.3 Verify graph integration: both extractors write `extracted_blocks`, normaliser bridge converts to `extracted_requirements`
