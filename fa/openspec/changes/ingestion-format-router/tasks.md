# Tasks: Format Detection & Routing (Phase 3)

## 1. State Schema

- [x] Add `file_format: NotRequired[str]` to `IngestionState` in [schema.py](file:///e:/file1/fa/ingestion/schema.py). Import `NotRequired` from `typing` (Python 3.11+) or `typing_extensions`.

## 2. Format Router Node

- [x] Create `format_router.py` in `ingestion/` with:
  - A module-level `_FORMAT_MAP: dict[str, str]` mapping `.pdf`, `.docx`, `.txt`, `.json` to their canonical format strings.
  - `format_router_node(state: IngestionState) -> dict` function that:
    - Reads `state["file_path"]`.
    - Calls `os.path.getsize(file_path)` — raises `EmptyFileError` if size is 0. Lets `FileNotFoundError` propagate naturally.
    - Extracts extension via `os.path.splitext()`, lowercases it.
    - Looks up in `_FORMAT_MAP`; raises `UnsupportedFormatError(ext)` if missing.
    - Returns `{"file_format": canonical_format}` (partial state update).

## 3. Routing Function

- [x] Create `route_by_format(state: IngestionState) -> str` (in `format_router.py` or `graph.py`). Reads `state["file_format"]` and returns it. Used as the routing function for `add_conditional_edges`.

## 4. Graph Wiring

- [x] In [graph.py](file:///e:/file1/fa/ingestion/graph.py), refactor `build_ingestion_graph()`:
  - Replace `builder.add_edge(START, "data_ingestion")` with `builder.add_edge(START, "format_router")`.
  - Register `format_router_node` via `builder.add_node("format_router", format_router_node)`.
  - Add `builder.add_conditional_edges("format_router", route_by_format, {"pdf": "pdf_extractor", "docx": "docx_extractor", "txt": "txt_extractor", "json": "json_validator"})`.
  - Stub extractor nodes to wrap existing `extract_from_*` functions (full extractor refactoring is Phases 4–6).
  - Connect all extractor nodes to `"normaliser"` via `add_edge`, then `"normaliser"` to `"rfa"`, then `"rfa"` to `END`.
  - Remove the old monolithic `data_ingestion_node` registration.

## 5. Unit Tests

- [x] Create `tests/test_format_router.py` with tests for:
  - **Empty file** → `EmptyFileError` raised.
  - **Supported extensions** (`.pdf`, `.docx`, `.txt`, `.json`) → returns correct `file_format` string in state update dict.
  - **Unsupported extension** (e.g., `.xlsx`) → `UnsupportedFormatError` raised.
  - **Case insensitivity** → `.PDF`, `.Docx` handled correctly.
  - **Missing file** → `FileNotFoundError` propagates (not caught by router).
  - **`route_by_format`** → returns `state["file_format"]` unchanged.
