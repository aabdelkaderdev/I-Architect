# Proposal: Format Detection & Routing (Phase 3)

## What

Refactor the ingestion graph to split the monolithic `data_ingestion_node` into a dedicated **format router node** followed by per-format extractor nodes, connected via a LangGraph `add_conditional_edges` conditional edge.

Currently, `data_ingestion_node` in `graph.py` performs file validation, extension detection, extraction dispatch, and normalisation in a single function. Phase 3 requires the format router to be an independent graph node (Node 1 of 5) that writes the detected format to a `file_format` state channel. The graph then uses a conditional edge reading `file_format` to route to the correct extractor node.

## Why

- **Separation of concerns**: The router validates and classifies; extractors parse. Combining them makes the node hard to test and extend independently.
- **Graph-level routing**: With `add_conditional_edges`, LangGraph handles dispatch natively. Adding a new format means adding a new extractor node and updating the edge map — no changes to the router.
- **Fail-fast semantics**: The router raises `EmptyFileError` or `UnsupportedFormatError` before any extraction work begins, giving clear error attribution.
- **PRD compliance**: Phases 4–6 define individual extractors as separate dispatch targets. The graph wiring in Phase 9 depends on `file_format` as a conditional-edge key.

## Scope

- Add `file_format: str` channel to `IngestionState` (in `schema.py`).
- Create `format_router_node` function (new file or in `graph.py`).
- Wire `format_router_node` as the first node after `START` with `add_conditional_edges` routing to per-format extractor nodes.
- Existing extractor functions in `extractors.py` will become individual graph nodes (or this is deferred to Phases 4–5 tasks, with the conditional edge stubbed to a single `data_extraction_node` for now).

## Out of scope

- Content sniffing / magic-byte detection (intentional — see PRD §5).
- Actual extractor refactoring into separate nodes (Phases 4–6).
- Normaliser, RFA, or graph compilation changes beyond wiring the router.
