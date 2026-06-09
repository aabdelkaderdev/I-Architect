## 1. Schema & Context

- [x] 1.1 Verify `IngestionState` TypedDict in `ingestion/schema.py` has all required channels (`file_path`, `file_format`, `extracted_blocks`, `ingestion_config`, `filter_config`, `filter_report`, `extracted_requirements`).
- [x] 1.2 Verify `IngestionContext` dataclass in `ingestion/schema.py` holds the `llm: BaseChatModel` field.

## 2. Node Assembly

- [x] 2.1 Import `format_router_node` and `route_by_format` from `ingestion.format_router`.
- [x] 2.2 Import `extract_from_pdf`, `extract_from_docx`, `extract_from_txt`, `extract_from_json` from `ingestion.extractors`.
- [x] 2.3 Import `normalise_blocks` from `ingestion.normaliser`.
- [x] 2.4 Import `filter_requirements` from `ingestion.rfa`.
- [x] 2.5 Implement Node 5 (Output Assembly) function in `graph.py` that raises `EmptyRequirementsError` when `extracted_requirements` has zero entries.

## 3. Graph Wiring

- [x] 3.1 Create `StateGraph(IngestionState, context_schema=IngestionContext)`.
- [x] 3.2 Add all nodes via `builder.add_node(name, fn)`.
- [x] 3.3 Set entry point via `builder.add_edge(START, "format_router")`.
- [x] 3.4 Add the conditional edge via `builder.add_conditional_edges("format_router", route_by_format, {"pdf": ..., "docx": ..., "txt": ..., "json": ...})`.
- [x] 3.5 Add edges from each extractor/validator to the normaliser via `builder.add_edge(extractor, "normaliser")`.
- [x] 3.6 Add sequential edge from normaliser to RFA via `builder.add_edge("normaliser", "rfa")`.
- [x] 3.7 Add sequential edge from RFA to Output Assembly via `builder.add_edge("rfa", "output_assembly")`.
- [x] 3.8 Add edge from Output Assembly to `END` via `builder.add_edge("output_assembly", END)`.

## 4. RFA @task Integration

- [x] 4.1 Wrap each batch LLM call in the RFA with `@task` (from `langgraph.func`) for fine-grained checkpointing.
- [x] 4.2 Ensure the RFA node accesses the LLM via `runtime: Runtime[IngestionContext]` and reads `runtime.context.llm`.

## 5. Checkpointing & Compilation

- [x] 5.1 Create a `build_ingestion_graph(db_path: str)` function.
- [x] 5.2 Initialise `SqliteSaver` (from `langgraph.checkpoint.sqlite`) using the provided `db_path`.
- [x] 5.3 Compile the graph with `builder.compile(checkpointer=saver)`.
- [x] 5.4 Add error handling for checkpoint database unavailability (log warning, compile without checkpointer).

## 6. Testing

- [x] 6.1 Write a unit test verifying conditional routing for each format (`add_conditional_edges` path map).
- [x] 6.2 Write a unit test verifying `EmptyRequirementsError` in the output assembly node.
- [x] 6.3 Write a test verifying thread ID derivation and checkpointing resume behaviour.
- [x] 6.4 Write a test verifying context injection (`Runtime[IngestionContext]`) is accessible in the RFA node.
