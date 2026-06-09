# Design: Data Ingestion & Requirement Filtering

## Architecture
The pipeline is a standalone LangGraph `StateGraph`, compiled into a `Pregel` instance and invoked by a parent orchestrator. It consists of two stages:
1. **Data Ingestion (Stage 1)**: Deterministic extraction using format-specific Python libraries:
   - PDF: `pdfplumber`
   - DOCX: `python-docx`
   - TXT: `chardet` + raw read
   - JSON: `json.load`
   It auto-assigns IDs and normalises output to a standard format.
2. **Requirement Filtering Agent (Stage 2)**: An LLM-based classifier to separate Signal from Noise, which can be disabled via configuration.

## State Schema (TypedDict)
The graph state is defined as a `TypedDict` (the primary documented method for LangGraph Python state schemas). A `dataclass` can be used if defaults are needed; Pydantic `BaseModel` is also supported but less performant.

```python
from typing_extensions import TypedDict

class IngestionState(TypedDict):
    file_path: str
    extracted_requirements: dict[str, str]
```

- **`file_path`**: Absolute path to the uploaded file (PDF, DOCX, TXT, or JSON).
- **`extracted_requirements`**: The final clean requirement set — a flat `dict[str, str]` where keys are requirement IDs (e.g., `REQ-1`) and values are non-empty strings.

## LLM Injection via Runtime Context
The LLM model instance is **not** placed in state channels (state must remain serialisable). Instead, it is passed through LangGraph's **runtime context** mechanism:

1. Define a `context_schema` dataclass:
   ```python
   from dataclasses import dataclass
   from langchain_core.language_models import BaseChatModel

   @dataclass
   class IngestionContext:
       llm: BaseChatModel
   ```

2. Attach it to the `StateGraph`:
   ```python
   from langgraph.graph import StateGraph

   builder = StateGraph(IngestionState, context_schema=IngestionContext)
   ```

3. Pass the context at invocation time:
   ```python
   from langchain.chat_models import init_chat_model

   llm = init_chat_model("gpt-4o", model_provider="openai")
   graph.invoke({"file_path": "/path/to/file.pdf"}, context={"llm": llm})
   ```

4. Access from nodes via `Runtime`:
   ```python
   from langgraph.runtime import Runtime

   def rfa_node(state: IngestionState, runtime: Runtime[IngestionContext]):
       llm = runtime.context.llm
       # Use llm for classification calls
       ...
   ```

## JSON Passthrough Rule
Compliant JSON files bypass extraction and filtering entirely if they already match the standard requirement format.

## Exception Taxonomy
- `EmptyFileError` (ValueError)
- `UnsupportedFormatError` (ValueError)
- `ExtractionError` (RuntimeError)
- `EmptyRequirementsError` (ValueError)
- `NonStandardJSONError` (ValueError)
- `FormatMismatchError` (ValueError)
