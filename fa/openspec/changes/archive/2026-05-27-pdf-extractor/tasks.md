# Tasks: PDF Extractor (Phase 4)

## 1. State Schema

- [x] Add `extracted_blocks: NotRequired[list[dict]]` to `IngestionState` in [schema.py](file:///e:/file1/fa/ingestion/schema.py). This channel holds the extractor → normaliser handoff. Each dict has keys `text` (str), `source_page` (int | None), `source_section` (str | None).

## 2. Extraction Pipeline

- [x] Rewrite `extract_from_pdf` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) to return `list[dict]` instead of `list[str]`. The function signature becomes:
  ```python
  def extract_from_pdf(file_path: str, pdf_engine: str = "pdfplumber", header_footer_threshold: float = 0.6) -> list[dict]:
  ```

- [x] Implement **page iteration** (Step 1): open the PDF with the configured engine, iterate pages, collect `(page_number, page_text)` tuples. Raise `ExtractionError("No extractable text; OCR not supported")` if all pages yield no text. Raise `FormatMismatchError` if the file is not a valid PDF.

- [x] Implement **header/footer stripping** (Step 2): after all pages are extracted, compute line frequencies across pages (after whitespace normalisation). Remove lines appearing on more than `header_footer_threshold` fraction of pages.

- [x] Implement **table detection** (Step 3): use `pdfplumber.Page.extract_tables()` (or PyMuPDF equivalent). Classify first-row headers as semantic if they contain any of: `ID`, `Requirement`, `Description`, `Shall`, `Must`, `Functional`, `Non-Functional`, `Constraint`. Prepend semantic headers as `"Header: Value | ..."`. Exclude table regions from subsequent text segmentation.

- [x] Implement **text block segmentation** (Step 4): apply the three-tier fallback — numbered list regex `^\s*(\d+[\.\)]\s+|[a-zA-Z][\.\)]\s+|•\s+|[-–]\s+)`, then paragraph splitting on `\n\n`, then sentence splitting on `\.\s+[A-Z]` for paragraphs exceeding 500 characters.

- [x] Implement **encoding cleanup** (Step 5): strip non-printable characters, apply `unicodedata.normalize("NFKD", ...)`, replace smart quotes with ASCII equivalents. Emit blocks that have at least one non-whitespace character.

## 3. Node Update

- [x] Update `pdf_extractor_node` in [graph.py](file:///e:/file1/fa/ingestion/graph.py) to write `{"extracted_blocks": blocks}` instead of calling `generate_ids_for_blocks` and writing to `extracted_requirements`.

- [x] Add a temporary bridge in `normaliser_node` in [graph.py](file:///e:/file1/fa/ingestion/graph.py) to convert `extracted_blocks` → `extracted_requirements` for downstream RFA compatibility (until Phase 6 refactors the normaliser).

## 4. Unit Tests

- [x] Create `tests/test_pdf_extractor.py` with tests for:
  - **Header/footer stripping** — text appearing on > 60% of pages is removed; text on ≤ 60% is preserved.
  - **Table detection** — rows with semantic headers (`ID`, `Description`) are formatted as `"ID: REQ-1 | Description: The system shall..."`. Rows with non-semantic headers are space-joined without prepending.
  - **Numbered list segmentation** — input with `1. ...`, `a) ...`, `• ...` is split at list-item boundaries.
  - **Paragraph segmentation** — input with `\n\n` separators produces one block per paragraph.
  - **Sentence fallback** — a 600-character paragraph with no list structure is split on `. [A-Z]` boundaries.
  - **Encoding cleanup** — smart quotes are replaced, non-printable chars are stripped, Unicode is NFKD-normalised.
  - **No extractable text** → `ExtractionError` raised.
  - **Corrupt PDF** → `ExtractionError` raised with library error.
  - **Output format** — each returned dict has `text` (str), `source_page` (int | None), `source_section` (str | None).
