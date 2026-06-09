# Design: Ingestion Configuration Dataclasses

## Architecture

### State & Runtime Split (per LangGraph docs)

| Concern | Where it lives | Why |
|---------|---------------|-----|
| Tunable config (`IngestionConfig`, `FilterConfig`) | `IngestionState` TypedDict channels | Serialisable primitives; checkpointable; read by every node from `state` dict |
| LLM instance | `IngestionContext` dataclass via `context_schema` | Non-serialisable dependency; injected at invocation via `context=` kwarg; accessed in nodes via `runtime.context.llm` |

### How it fits together

```python
from dataclasses import dataclass, field
from typing import Optional
from typing_extensions import TypedDict
from langchain_core.language_models import BaseChatModel

# ── Config dataclasses (serialisable, live in state) ──────────────

@dataclass
class IngestionConfig:
    """Controls Stage 1: extraction and normalisation."""
    id_prefix: str = "REQ-"
    min_block_length: int = 15
    max_block_length: int = 2000
    dedup_enabled: bool = True
    encoding_fallback: str = "utf-8"
    pdf_engine: str = "pdfplumber"           # "pdfplumber" | "pymupdf"
    header_footer_threshold: float = 0.6

@dataclass
class FilterConfig:
    """Controls Stage 2: the Requirement Filtering Agent."""
    enabled: bool = True
    confidence_threshold: float = 0.7
    filter_batch_size: int = 20
    log_dropped: bool = True
    emit_report: bool = True
    skip_filter_for_json: bool = True


# ── State (TypedDict — the LangGraph-endorsed schema) ────────────

class IngestionState(TypedDict):
    file_path: str
    extracted_requirements: dict[str, str]
    ingestion_config: IngestionConfig          # NEW
    filter_config: FilterConfig                # NEW


# ── Runtime context (dataclass — non-serialisable deps) ──────────

@dataclass
class IngestionContext:
    llm: BaseChatModel
```

### Graph construction

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(IngestionState, context_schema=IngestionContext)

builder.add_node("data_ingestion", data_ingestion_node)
builder.add_node("rfa", rfa_node)

builder.add_edge(START, "data_ingestion")
builder.add_edge("data_ingestion", "rfa")
builder.add_edge("rfa", END)

graph = builder.compile()
```

### Node signatures

Nodes that need the LLM accept `runtime: Runtime[IngestionContext]`:

```python
from langgraph.runtime import Runtime

def data_ingestion_node(state: IngestionState) -> dict:
    cfg = state["ingestion_config"]
    # Use cfg.pdf_engine, cfg.min_block_length, etc.
    ...

def rfa_node(state: IngestionState, runtime: Runtime[IngestionContext]) -> dict:
    fcfg = state["filter_config"]
    if not fcfg.enabled:
        return {"extracted_requirements": state["extracted_requirements"]}

    llm = runtime.context.llm
    # Use fcfg.confidence_threshold, fcfg.filter_batch_size, etc.
    ...
```

### Invocation by orchestrator

```python
graph.invoke(
    {
        "file_path": "/path/to/requirements.pdf",
        "ingestion_config": IngestionConfig(),     # or user-provided
        "filter_config": FilterConfig(),           # or user-provided
    },
    context=IngestionContext(llm=my_llm_instance),
)
```

---

## Component Breakdown

### 1. `IngestionConfig`

| Field | Type | Default | Governance |
|-------|------|---------|------------|
| `id_prefix` | `str` | `"REQ-"` | Normaliser, Format Router |
| `min_block_length` | `int` | `15` | Normaliser |
| `max_block_length` | `int` | `2000` | Normaliser |
| `dedup_enabled` | `bool` | `True` | Normaliser |
| `encoding_fallback` | `str` | `"utf-8"` | TXT Extractor |
| `pdf_engine` | `str` | `"pdfplumber"` | PDF Extractor |
| `header_footer_threshold` | `float` | `0.6` | PDF Extractor |

### 2. `FilterConfig`

| Field | Type | Default | Governance |
|-------|------|---------|------------|
| `enabled` | `bool` | `True` | RFA master switch |
| `confidence_threshold` | `float` | `0.7` | RFA noise drop threshold |
| `filter_batch_size` | `int` | `20` | RFA batching |
| `log_dropped` | `bool` | `True` | RFA logging |
| `emit_report` | `bool` | `True` | RFA report generation |
| `skip_filter_for_json` | `bool` | `True` | RFA JSON bypass |

---

## Validation Logic (orchestrator responsibility)

| Field | Rule |
|-------|------|
| `id_prefix` | Non-empty; alphabetic + hyphens only; must end with hyphen |
| `min_block_length` | `int >= 1`; must be `< max_block_length` |
| `max_block_length` | `int >= min_block_length` |
| `header_footer_threshold` | `float` in `[0.0, 1.0]` |
| `confidence_threshold` | `float` in `[0.0, 1.0]` |
| `filter_batch_size` | `int >= 1` |
| `pdf_engine` | One of `"pdfplumber"`, `"pymupdf"` |

Validation runs before `graph.invoke()`. If invalid config reaches the pipeline,
behaviour is undefined — the pipeline does not re-validate.
