# Data Ingestion & Requirement Filtering

This module implements the ingestion pipeline, transforming raw uploaded documents into a clean set of requirements (`dict[str, str]`). It features a two-stage pipeline: a deterministic extraction phase and an LLM-based filtering phase.

## Orchestrator Interface

This pipeline is invoked by the Orchestrator, which is responsible for coordinating the overall workflow and passing the output to downstream systems.

### Inputs
Before invoking the ingestion graph, the Orchestrator must provide:
- **State Channels:**
  - `file_path`: Absolute path to the uploaded file.
  - `ingestion_config`: Serialised `IngestionConfig`.
  - `filter_config`: Serialised `FilterConfig`.
- **Runtime Context:**
  - `llm`: A `BaseChatModel` instance passed via the `context=IngestionContext(llm=...)` kwarg on invocation. The LLM must never appear in a state channel.
- **Configuration:**
  - `thread_id`: Passed via `config={"configurable": {"thread_id": ...}}` for checkpointing.
- **Entry Point parameter:**
  - `db_path`: Passed directly to the graph compilation function: `build_ingestion_graph(db_path)`.

### Invocation
The pipeline is invoked as follows:
```python
graph = build_ingestion_graph(db_path=db_path)
result = graph.invoke(
    {
        "file_path": file_path,
        "ingestion_config": ingestion_config,
        "filter_config": filter_config,
        # 'experiment_config' and 'matrix' may also be passed here for passthrough
    },
    context=IngestionContext(llm=llm_instance),
    config={"configurable": {"thread_id": thread_id}},
)
```

### Outputs
The graph returns the final state dictionary. The Orchestrator reads:
- `extracted_requirements`: The clean requirement set. Mapped by the Orchestrator to `ARLOInput.requirements`.
- `filter_report`: Structured report for downstream audit.

The `experiment_config` and `matrix` channels are passed through the pipeline untouched.

### Orchestrator Responsibilities
The pipeline explicitly refuses to handle infrastructure concerns. The Orchestrator is responsible for:
1. **Directory Creation**: Creating the checkpoint directories (e.g., `projects/{name}/checkpoints/`).
2. **Config Validation**: Validating `IngestionConfig` and `FilterConfig` against their defined rules before invocation.
3. **File Existence Checks**: Verifying the file exists at `file_path`.
4. **Error Handling**: Catching and managing exceptions thrown by the ingestion graph.
5. **Checkpoint Lifecycles**: Managing the retention and pruning of checkpoints.

## Checkpoint Storage Convention

Checkpoint databases are project-scoped. The Orchestrator should provide a path like:
`projects/{project_name}/checkpoints/ingestion.db`

The pipeline uses the `SqliteSaver` from `langgraph.checkpoint.sqlite`, instantiated via `sqlite3.connect(db_path, check_same_thread=False)`.

## Downstream Consumers

The pipeline's output feeds downstream systems, though the pipeline has no direct dependency on them:
- **ARLO**: Receives the `extracted_requirements` to process them.
- **RAA**: (downstream of ARLO) Uses the processed requirements to build the architecture model.
- **AGA**: (downstream of RAA) Generates diagrams from the architecture model.
- **SA**: Evaluates the architecture against the original requirements.

## Design Principles

The ingestion module strictly adheres to 8 core design principles:

1. **Two distinct stages in one module**: Extraction is deterministic Python, filtering is LLM-based. They share a module but their internals do not bleed.
2. **Library-native over abstraction**: Direct use of `pdfplumber`, `python-docx`, and `chardet` instead of generic LangChain loaders to maintain fine-grained control over text blocks.
3. **Fail loud, fail early**: The pipeline rejects non-compliant inputs rather than silently coercing them.
4. **Deterministic where possible**: Only the classification step (RFA) uses an LLM. Everything else is pure, deterministic Python.
5. **Configuration flows one way**: The Orchestrator writes config once. Nodes read it; no node modifies it.
6. **LLM lives in context, not state**: To keep state serialisable for checkpointing, the `BaseChatModel` is injected via LangGraph runtime context.
7. **Orchestrator owns the boundary**: The pipeline delegates all infrastructure concerns (directories, files, lifecycles) to the Orchestrator.
8. **Passthrough for clean input**: A compliant JSON file that already matches the standard format bypasses extraction and normalisation, processing at near-zero cost.
