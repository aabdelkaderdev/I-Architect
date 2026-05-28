## 1. Documentation & Specification Updates

- [x] 1.1 Create or update `ingestion/README.md` to document the Orchestrator Interface: inputs (`file_path`, `ingestion_config`, `filter_config` in state; `BaseChatModel` via `context=IngestionContext(llm=...)` kwarg; `thread_id` via `config={"configurable": {"thread_id": ...}}`), the `build_ingestion_graph(db_path)` entry point, outputs (`extracted_requirements`, `filter_report`), and the 5 orchestrator responsibilities.
- [x] 1.2 Add the 8 core Design Principles to `ingestion/README.md` to serve as a guide for future development.
- [x] 1.3 Document the downstream consumers (ARLO, RAA, AGA, SA) and checkpoint storage path convention (`projects/{name}/checkpoints/ingestion.db`) in the README.

## 2. Directory Layout Verification & Enforcement

- [x] 2.1 Verify that the `ingestion/` code package matches the actual layout: `schema.py`, `format_router.py`, `extractors.py`, `normaliser.py`, `rfa.py`, `exceptions.py`, `validation.py`, `graph.py`, and `prompts/filter_classification.md`.
- [x] 2.2 Verify that `Skills/Ingestion/` contains only skill definitions and references (`SKILL.MD`, `references/Signal_Noise_Taxonomy.md`) and NO runtime Python code or prompt templates. Move any errant files to `ingestion/`.
- [x] 2.3 Verify that `ingestion/prompts/` contains the `filter_classification.md` runtime prompt template.

## 3. LangGraph API Alignment

- [x] 3.1 Verify that `graph.py` uses `StateGraph(IngestionState, context_schema=IngestionContext)` and that `IngestionContext` is a `@dataclass` with `llm: BaseChatModel` (per `langgraph.runtime.Runtime` docs).
- [x] 3.2 Verify that `rfa_node` uses the signature `(state: IngestionState, runtime: Runtime[IngestionContext])` and accesses the LLM via `runtime.context.llm`.
- [x] 3.3 Verify that `build_ingestion_graph(db_path)` compiles with `SqliteSaver` from `langgraph.checkpoint.sqlite` when `db_path` is provided, using `sqlite3.connect(db_path, check_same_thread=False)`.
