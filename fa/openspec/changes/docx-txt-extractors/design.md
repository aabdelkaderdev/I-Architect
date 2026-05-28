# Design: DOCX & TXT Extractors (Phase 5)

## Context

The ingestion pipeline is a LangGraph `StateGraph` defined in [graph.py](file:///e:/file1/fa/ingestion/graph.py). Nodes are plain Python functions that accept `state: IngestionState` and optionally `runtime: Runtime[IngestionContext]` (per [LangGraph Graph API docs](https://docs.langchain.com/oss/python/langgraph/graph-api)). Extractors that make no LLM calls only need `state`. Nodes return a partial state-update dict, which LangGraph applies via the default `LastValue` channel reducer.

Phase 4 established the `extracted_blocks` state channel (`NotRequired[list[dict]]`) and a `normaliser_node` bridge that converts `extracted_blocks` → `extracted_requirements`. The DOCX and TXT extractors follow this pattern: they write to `extracted_blocks`, the normaliser (Phase 6) will consume them.

Existing stubs in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) return `list[str]` and call `generate_ids_for_blocks` inline. The new implementations will return `list[dict]` with `text`, `source_page`, and `source_section` keys, aligning with the Phase 4 `extracted_blocks` contract. The graph nodes in [graph.py](file:///e:/file1/fa/ingestion/graph.py) will be updated to write to `extracted_blocks` instead of `extracted_requirements`, matching the `pdf_extractor_node` pattern.

## Goals / Non-Goals

**Goals:**
- Rewrite `extract_from_docx` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) to parse paragraphs, lists (via style names), tables (with header detection), and heading-based sections, returning `list[dict]` blocks.
- Rewrite `extract_from_txt` in [extractors.py](file:///e:/file1/fa/ingestion/extractors.py) to detect encoding via `chardet`, attempt structured `ID: Description` parsing, and fall back to line/paragraph segmentation, returning `list[dict]` blocks.
- Update `docx_extractor_node` and `txt_extractor_node` in [graph.py](file:///e:/file1/fa/ingestion/graph.py) to write to `extracted_blocks` and let `normaliser_node` handle the conversion, following the pattern established by `pdf_extractor_node`.

**Non-Goals:**
- Normalizing, validating, or deduplicating the extracted blocks (Phase 6).
- Assigning missing IDs or parsing complex nested/merged-cell table structures.
- Using LLMs for content extraction. These nodes do not use `runtime` — they only read from `state`.

## Decisions

- **DOCX Parsing with `python-docx`**:
  - *Rationale*: `python-docx` provides structured access to paragraphs, styles (to identify lists and headings), and tables. Already imported in the existing codebase.
  - *Alternative considered*: Converting to XML/HTML first. Rejected because it discards Word-specific semantic styles (like `List Paragraph`) that are crucial for requirement block segmentation.

- **TXT Encoding Detection with `chardet`**:
  - *Rationale*: Text files often lack BOMs or explicit encoding markers. `chardet` guesses encoding from byte sequences. Already imported in the existing codebase.
  - *Alternative considered*: Forcing UTF-8. Rejected because it causes decode errors on legacy text files. A fallback to `IngestionConfig.encoding_fallback` (defined in [schema.py](file:///e:/file1/fa/ingestion/schema.py)) handles low-confidence detections (<0.7).

- **TXT Structured vs. Unstructured Fallback**:
  - *Rationale*: To handle varying TXT formats, a 50% threshold determines whether structured lines (`ID: Description`) dominate. If not, average line length heuristics (<200 chars = line mode, ≥200 chars = paragraph mode) choose the segmentation strategy.

- **Table Header Heuristic**:
  - *Rationale*: The DOCX extractor detects header rows if ≥2 cells match keywords (`ID`, `Requirement`, `Description`, etc.). This covers the majority of typical requirement matrices without over-engineering.

- **Node signature: state-only**:
  - These extractor nodes perform no LLM calls and require no runtime dependencies. Per the [LangGraph Node docs](https://docs.langchain.com/oss/python/langgraph/graph-api), nodes can accept `state` alone when `runtime` / `config` are not needed. This matches the existing `pdf_extractor_node` pattern.

## Node Updates

In [graph.py](file:///e:/file1/fa/ingestion/graph.py), the `docx_extractor_node` changes from its current form (calling `generate_ids_for_blocks` inline and writing to `extracted_requirements`) to:

```python
def docx_extractor_node(state: IngestionState) -> dict:
    file_path = state["file_path"]
    blocks = extract_from_docx(file_path)
    return {"extracted_blocks": blocks}
```

Similarly, `txt_extractor_node`:

```python
def txt_extractor_node(state: IngestionState) -> dict:
    cfg = state["ingestion_config"]
    file_path = state["file_path"]
    blocks = extract_from_txt(file_path, encoding_fallback=cfg.encoding_fallback)
    return {"extracted_blocks": blocks}
```

Both now write to the `extracted_blocks` channel. The existing `normaliser_node` bridge in [graph.py](file:///e:/file1/fa/ingestion/graph.py) already handles `extracted_blocks` → `extracted_requirements` conversion for downstream compatibility.

## Risks / Trade-offs

- **Risk: `chardet` may fail or guess incorrectly.**
  → *Mitigation*: Fallback to `IngestionConfig.encoding_fallback` if confidence is <0.7 or a decoding error occurs.
- **Risk: Complex tables with merged cells.**
  → *Mitigation*: Table extraction reads cell text but won't perfectly reconstruct merged relationships. Unstructured concatenation is used as a safe default.
- **Risk: No `runtime` dependency injection for future needs.**
  → *Mitigation*: Node signatures can be extended to accept `runtime: Runtime[IngestionContext]` later without breaking the graph, per LangGraph's flexible node parameter injection.
