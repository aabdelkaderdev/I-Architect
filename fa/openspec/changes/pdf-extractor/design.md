# Design: PDF Extractor (Phase 4)

## Architecture

The PDF extractor is a pure-Python node in the LangGraph `StateGraph`. It receives the file path and configuration from state, performs all extraction logic without LLM calls, and writes its output to an `extracted_blocks` state channel. It does not need `runtime` or `config` — it reads only from `state`.

```
START → format_router → [conditional edge on file_format] → pdf_extractor → normaliser → rfa → END
```

The `pdf_extractor_node` in [graph.py](file:///e:/file1/fa/ingestion/graph.py) wraps the extraction function. The function signature follows the LangGraph convention (per current docs):

```python
def pdf_extractor_node(state: IngestionState) -> dict:
```

Nodes accept `state` (the graph's `TypedDict`), and optionally `config` (`RunnableConfig`) or `runtime` (`Runtime`). This node needs neither — it performs no LLM calls and requires no runtime context. It returns a partial state update dict, which LangGraph applies via the default `LastValue` channel reducer.

## State Schema Change

Add `extracted_blocks` to `IngestionState` in [schema.py](file:///e:/file1/fa/ingestion/schema.py):

```python
from typing_extensions import TypedDict, NotRequired

class IngestionState(TypedDict):
    file_path: str
    file_format: NotRequired[str]
    extracted_blocks: NotRequired[list[dict]]  # Set by extractor nodes
    extracted_requirements: dict[str, str]
    ingestion_config: IngestionConfig
    filter_config: FilterConfig
```

`extracted_blocks` uses `NotRequired` because it is set mid-pipeline by the extractor node, not provided as graph input. Each dict in the list has:

| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | The candidate requirement text |
| `source_page` | `int \| None` | 1-indexed page number, or `None` |
| `source_section` | `str \| None` | Section heading context if detected, or `None` |

## Extraction Pipeline

The `extract_from_pdf` function in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) is rewritten to implement five sequential steps:

### Step 1: Page Iteration

Open the PDF using the engine specified by `ingestion_config.pdf_engine` (`"pdfplumber"` or `"pymupdf"`). Iterate page by page, extracting text from each page into a `list[tuple[int, str]]` of `(page_number, page_text)` pairs.

If no text is extractable from any page (scanned-image PDF), raise `ExtractionError("No extractable text; OCR not supported")`.

If the file cannot be opened (corrupt PDF), raise `ExtractionError` with the library's error message. If the file opens but is not a valid PDF, raise `FormatMismatchError`.

Both exception types are already defined in [exceptions.py](file:///e:/file1/fa/ingestion/exceptions.py).

### Step 2: Header/Footer Stripping

After all pages are extracted, collect all text lines across pages and compute their frequency (how many pages each line appears on, after whitespace normalisation via `" ".join(line.split())`).

**Rule**: A line that appears identically on more than `header_footer_threshold` fraction of pages (default 0.6, sourced from `ingestion_config.header_footer_threshold`) is classified as a header/footer and removed from every page.

The comparison is strict: verbatim match after whitespace normalisation. Near-duplicates like incrementing page numbers pass through and are handled later by the normaliser's minimum-length filter (Phase 6).

### Step 3: Table Detection

Use the PDF library's built-in table extraction (`pdfplumber.Page.extract_tables()` or the equivalent for PyMuPDF). For each table:

1. Extract column headers from the first row.
2. Classify headers as **semantic** if they contain any of: `ID`, `Requirement`, `Description`, `Shall`, `Must`, `Functional`, `Non-Functional`, `Constraint` (case-insensitive substring match).
3. For each data row, concatenate cells into a block:
   - If headers are semantic: `"Header1: Cell1 | Header2: Cell2 | ..."`.
   - If headers are not semantic: `"Cell1 Cell2 ..."` (space-joined, no header prepending).
4. Each resulting string becomes one candidate block with `source_page` set to the page number.

Table regions are excluded from the text used in Step 4 to avoid double-counting.

### Step 4: Text Block Segmentation

After header/footer stripping and table extraction, the remaining text on each page is segmented using a three-tier fallback:

1. **Numbered list detection (preferred)**: A regex pattern `^\s*(\d+[\.\\)]\s+|[a-zA-Z][\.\\)]\s+|•\s+|[-–]\s+)` identifies list items. If any matches are found on a page, each match boundary becomes one candidate block.

2. **Paragraph splitting (fallback)**: If no numbered structure is detected, double newlines (`\n\n`) separate paragraphs. Each paragraph becomes one candidate block.

3. **Sentence-level fallback**: If a paragraph exceeds 500 characters with no list structure, it is split on sentence boundaries (a period followed by a space and an uppercase letter: `\.\s+[A-Z]`). This prevents multi-hundred-character blobs from becoming single blocks.

### Step 5: Encoding Cleanup

Every extracted block (from both tables and text segmentation) passes through a cleanup function:

- Strip non-printable characters (characters below `\x20` except `\n`, `\t`).
- Normalise Unicode to NFKD form (`unicodedata.normalize("NFKD", text)`).
- Replace smart quotes (`\u2018`, `\u2019` → `'`; `\u201c`, `\u201d` → `"`) and other typographic characters with ASCII equivalents.

A block is emitted if it contains at least one non-whitespace character after cleanup. There is no minimum length enforcement at this stage — that belongs to the normaliser (Phase 6).

## Node Update

In [graph.py](file:///e:/file1/fa/ingestion/graph.py), the `pdf_extractor_node` changes from:

```python
def pdf_extractor_node(state: IngestionState) -> dict:
    cfg = state["ingestion_config"]
    file_path = state["file_path"]
    blocks = extract_from_pdf(file_path, pdf_engine=cfg.pdf_engine, header_footer_threshold=cfg.header_footer_threshold)
    requirements = generate_ids_for_blocks(blocks, cfg)
    if not requirements:
        raise EmptyRequirementsError("No requirements found.")
    return {"extracted_requirements": requirements}
```

To:

```python
def pdf_extractor_node(state: IngestionState) -> dict:
    cfg = state["ingestion_config"]
    file_path = state["file_path"]
    blocks = extract_from_pdf(
        file_path,
        pdf_engine=cfg.pdf_engine,
        header_footer_threshold=cfg.header_footer_threshold,
    )
    return {"extracted_blocks": blocks}
```

The node writes to the `extracted_blocks` channel. The normaliser (Phase 6) will consume `extracted_blocks` and produce `extracted_requirements`. Until Phase 6 is implemented, the `normaliser_node` pass-through in [graph.py](file:///e:/file1/fa/ingestion/graph.py) will need a temporary bridge to convert `extracted_blocks` into `extracted_requirements` for downstream compatibility.

## Error Handling

| Condition | Exception | Raised By |
|-----------|-----------|-----------|
| No extractable text on any page (scanned image) | `ExtractionError("No extractable text; OCR not supported")` | `extract_from_pdf` |
| PDF file is corrupt or cannot be opened | `ExtractionError` with library error message | `extract_from_pdf` |
| File opens but content is not valid PDF | `FormatMismatchError` | `extract_from_pdf` |

All exception types are defined in [exceptions.py](file:///e:/file1/fa/ingestion/exceptions.py) (Phase 1).

## Design Decisions

1. **`extracted_blocks` as a separate state channel**: The PRD defines a two-stage pipeline — extractors produce raw candidate blocks, the normaliser applies length/dedup/ID logic. Using a separate `extracted_blocks` channel (rather than writing directly to `extracted_requirements`) preserves this separation. The channel uses `NotRequired` + `LastValue` semantics, matching the `file_format` pattern.
2. **Table regions excluded from text segmentation**: Tables detected in Step 3 are removed from the text processed in Step 4 to prevent double-counting rows as both table entries and text paragraphs.
3. **No `runtime` parameter**: This node performs no LLM calls and needs no injected context. It only reads `state`, keeping the function signature minimal and testable.
4. **Temporary normaliser bridge**: Until Phase 6 refactors the normaliser, a bridge in `normaliser_node` will convert `extracted_blocks` → `extracted_requirements` so the RFA continues to work.
