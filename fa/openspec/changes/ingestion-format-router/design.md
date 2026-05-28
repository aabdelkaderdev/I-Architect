# Design: Format Detection & Routing (Phase 3)

## Architecture

The format router becomes Node 1 in the ingestion graph. It is a plain Python function registered with `StateGraph.add_node()`. The graph then uses `add_conditional_edges` to route to per-format extractors based on the `file_format` state channel.

```
START → format_router → [conditional edge on file_format] → extractor node(s) → normaliser → rfa → END
```

## State Schema Change

Add `file_format` to `IngestionState` in [schema.py](file:///e:/file1/fa/ingestion/schema.py):

```python
from typing import NotRequired
from typing_extensions import TypedDict

class IngestionState(TypedDict):
    file_path: str
    file_format: NotRequired[str]  # Set by format_router_node
    extracted_requirements: dict[str, str]
    ingestion_config: IngestionConfig
    filter_config: FilterConfig
```

`file_format` uses `NotRequired` because it is not part of the graph input — it is set by the router node. This follows the LangGraph pattern where nodes return partial state updates as dicts, and the default `LastValue` channel stores the most recent value.

## Node: `format_router_node`

A synchronous function with signature:

```python
def format_router_node(state: IngestionState) -> dict:
```

Per the LangGraph Python docs, nodes accept `state` (the graph's `TypedDict`) and optionally `config` (`RunnableConfig`) or `runtime` (`Runtime`). This node needs neither `config` nor `runtime` — it performs no LLM calls and needs no runtime context.

### Processing Steps

1. **File validation**: Read `state["file_path"]`. Check `os.path.getsize()` — if 0, raise `EmptyFileError`. File-not-found is a standard `FileNotFoundError` propagated by `os.path.getsize()` itself; the router does not catch it (orchestrator responsibility per PRD §4 Step 1).

2. **Extension detection**: Extract the extension with `os.path.splitext()`, lowercase it, and look up in a static dict:

```python
_FORMAT_MAP: dict[str, str] = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".txt": "txt",
    ".json": "json",
}
```

If the extension is not in `_FORMAT_MAP`, raise `UnsupportedFormatError(ext)`.

3. **State update**: Return `{"file_format": canonical_format}`. The `file_path` is already in state and does not need to be re-emitted — LangGraph's default `LastValue` reducer preserves existing channel values unless overwritten.

### Return value

```python
return {"file_format": "pdf"}  # example
```

This is a partial state update, following the LangGraph convention (nodes return dicts with only the channels they modify).

## Graph Wiring

In [graph.py](file:///e:/file1/fa/ingestion/graph.py), replace the current monolithic `data_ingestion_node` flow with:

```python
from langgraph.graph import StateGraph, START, END

def route_by_format(state: IngestionState) -> str:
    """Routing function for add_conditional_edges. Returns the node name."""
    return state["file_format"]

def build_ingestion_graph():
    builder = StateGraph(IngestionState, context_schema=IngestionContext)

    builder.add_node("format_router", format_router_node)
    builder.add_node("pdf_extractor", pdf_extractor_node)
    builder.add_node("docx_extractor", docx_extractor_node)
    builder.add_node("txt_extractor", txt_extractor_node)
    builder.add_node("json_validator", json_validator_node)
    builder.add_node("normaliser", normaliser_node)
    builder.add_node("rfa", rfa_node)

    builder.add_edge(START, "format_router")
    builder.add_conditional_edges(
        "format_router",
        route_by_format,
        {
            "pdf": "pdf_extractor",
            "docx": "docx_extractor",
            "txt": "txt_extractor",
            "json": "json_validator",
        },
    )

    # All extractors converge to normaliser, then RFA
    for extractor in ["pdf_extractor", "docx_extractor", "txt_extractor", "json_validator"]:
        builder.add_edge(extractor, "normaliser")
    builder.add_edge("normaliser", "rfa")
    builder.add_edge("rfa", END)

    return builder.compile()
```

Key LangGraph API details (verified against current docs):
- `add_conditional_edges(source, routing_fn, path_map)` — the routing function reads state and returns a string key; the `path_map` dict maps those keys to destination node names.
- The routing function has the same signature as a node: `(state) -> str`.
- All four extractors converge back to a single `normaliser` node via fixed `add_edge` calls.

## Error Handling

| Condition | Exception | Raised By |
|-----------|-----------|-----------|
| File is 0 bytes | `EmptyFileError` | `format_router_node` |
| Extension not in `_FORMAT_MAP` | `UnsupportedFormatError(ext)` | `format_router_node` |
| File does not exist | `FileNotFoundError` | Python stdlib (`os.path.getsize`) |
| Extension doesn't match content | `FormatMismatchError` | Extractor nodes (not the router) |

All exception types are defined in [exceptions.py](file:///e:/file1/fa/ingestion/exceptions.py) (Phase 1).

## Design Decisions

1. **No content sniffing**: The router does not inspect file bytes to verify format. This is intentional per PRD §5 — format mismatch is detected by the extractor at parse time.
2. **`NotRequired` for `file_format`**: The channel is absent from graph input and set mid-pipeline. Using `typing.NotRequired` is the idiomatic way to express this in a `TypedDict` state schema.
3. **Routing function is separate from the node**: `route_by_format` is a pure state-reader passed to `add_conditional_edges`. It contains no side effects. This keeps the router node responsible only for validation + detection, and the edge logic responsible only for dispatch.
