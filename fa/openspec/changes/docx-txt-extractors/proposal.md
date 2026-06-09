## Why

The ingestion pipeline needs to extract raw text blocks from DOCX and TXT files. This satisfies Phase 5 of the ingestion PRD. Both extractors convert their format into raw candidate requirement blocks suitable for normalisation, with no LLM involvement. The current implementations in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) are stubs that return `list[str]` — they need to be rewritten to return `list[dict]` blocks conforming to the `extracted_blocks` contract established in Phase 4.

## What Changes

- Rewrite `extract_from_docx` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) to parse paragraphs, identify lists via style names, extract tables with header detection, and track heading-based sections. Returns `list[dict]` with `text`, `source_page`, `source_section`.
- Rewrite `extract_from_txt` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) to detect file encoding via `chardet`, attempt structured `ID: Description` parsing, and fall back to line/paragraph segmentation. Returns `list[dict]`.
- Update `docx_extractor_node` and `txt_extractor_node` in [graph.py](file:///e:/file1/fa/ingestion/graph.py) to write to the `extracted_blocks` state channel (matching the `pdf_extractor_node` pattern), instead of calling `generate_ids_for_blocks` inline.

## Capabilities

### New Capabilities
- `docx-extractor`: Extracts raw requirement blocks from DOCX files by parsing styles, tables, and headings.
- `txt-extractor`: Extracts raw requirement blocks from TXT files via structured regex matching or unstructured text chunking.

### Modified Capabilities

## Impact

- **Code:** Rewrites `extract_from_docx` and `extract_from_txt` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py). Updates two graph nodes in [graph.py](file:///e:/file1/fa/ingestion/graph.py) to use the `extracted_blocks` channel.
- **Dependencies:** `python-docx` and `chardet` are already imported in the existing codebase. No new dependencies.
- **Downstream:** The existing `normaliser_node` bridge in [graph.py](file:///e:/file1/fa/ingestion/graph.py) already handles `extracted_blocks` → `extracted_requirements`, so downstream compatibility is preserved.
