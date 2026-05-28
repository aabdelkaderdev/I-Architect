## ADDED Requirements

### Requirement: Ingestion Directory Layout
The ingestion runtime code SHALL be organised within the `ingestion/` package. The current layout includes: `schema.py` (state schema, config dataclasses, Pydantic models, and `IngestionContext`), `format_router.py` (format detection and routing), `extractors.py` (PDF, DOCX, TXT, JSON extraction), `normaliser.py` (ID assignment, dedup, length filtering), `rfa.py` (Requirement Filtering Agent — LLM-based), `exceptions.py` (custom exceptions), `validation.py` (input validation), `graph.py` (graph construction and compilation), and `prompts/` (runtime prompt templates).

#### Scenario: Runtime Code Location
- **WHEN** a developer inspects the `ingestion` module
- **THEN** they find `filter_classification.md` in `ingestion/prompts/`, extractors in `ingestion/extractors.py`, the RFA in `ingestion/rfa.py`, and state/config definitions in `ingestion/schema.py`.

### Requirement: Skills Resource Bundle Layout
Skill definitions and references SHALL reside in `Skills/Ingestion/` and MUST NEVER contain runtime code or prompt templates.

#### Scenario: Skill Definition Validation
- **WHEN** the `Skills/Ingestion/` directory is populated
- **THEN** it contains `SKILL.MD` and `references/Signal_Noise_Taxonomy.md` but no Python files or prompt templates.

### Requirement: Checkpoint Storage Convention
Checkpoint databases SHALL be project-scoped at `projects/{project_name}/checkpoints/ingestion.db`. The ingestion module writes only to the path provided by the orchestrator via the `db_path` parameter to `build_ingestion_graph()`. The `SqliteSaver` from `langgraph.checkpoint.sqlite` SHALL be used, instantiated with `sqlite3.connect(db_path, check_same_thread=False)`.

#### Scenario: Checkpointer Initialisation
- **WHEN** `build_ingestion_graph(db_path="projects/myproject/checkpoints/ingestion.db")` is called
- **THEN** a `SqliteSaver` is created with a `sqlite3` connection to that path and passed to `builder.compile(checkpointer=saver)`.

### Requirement: Design Principles Adherence
The ingestion module SHALL adhere to the 8 core design principles: (1) two distinct stages in one module, (2) library-native over abstraction, (3) fail loud fail early, (4) deterministic where possible, (5) configuration flows one way, (6) LLM lives in context not state, (7) orchestrator owns the boundary, (8) passthrough for clean input.

#### Scenario: Passthrough of Clean Input
- **WHEN** the pipeline receives a compliant JSON file that matches the standard format
- **THEN** it bypasses extraction and normalisation, processing it with near-zero cost.
