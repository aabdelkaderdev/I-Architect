## Context

Phase 10 defines the final boundaries between the ingestion pipeline (which processes documents to extract requirements) and the rest of the system (the orchestrator that coordinates everything, and downstream systems like ARLO). The pipeline consists of two distinct stages: a deterministic extraction phase and an LLM-based filtering phase. It requires strict input validation, precise file layout, and clear operational boundaries to ensure robust execution.

## Goals / Non-Goals

**Goals:**
- Clearly define the contract for how the orchestrator invokes the ingestion pipeline.
- Detail exactly what the orchestrator must supply and what it receives in return.
- Establish the physical directory layout for code (`ingestion/`) and resources (`Skills/Ingestion/`).
- Formalise 8 core design principles to guide future development and maintenance.
- Document downstream consumers to ensure interface alignment.

**Non-Goals:**
- Modifying the internal logic of any existing extractor or filter.
- Adding new configuration fields or state channels.
- Building the actual ARLO, RAA, AGA, or SA components.

## Decisions

- **Strict Orchestrator Delegation**: The pipeline explicitly refuses to handle infrastructure concerns like directory creation, file existence checks, or checkpoint lifecycle management. 
  - *Rationale*: Keeps the ingestion graph pure and focused entirely on data transformation.
- **Two Distinct Stages in One Module**: Extraction is deterministic Python, filtering is LLM-based. They share a module but their internals do not bleed.
  - *Rationale*: Maximises testability and predictability for the extraction phase.
- **Library-Native Over Abstraction**: Direct use of `pdfplumber`, `python-docx`, and `chardet` instead of LangChain loaders.
  - *Rationale*: We need fine-grained control over text blocks, which generic loaders obscure.
- **Fail Loud, Fail Early**: The pipeline rejects non-compliant inputs rather than silently coercing them.
  - *Rationale*: Silent coercion hides upstream data quality issues.
- **LLM Lives in Context, Not State**: A `BaseChatModel` instance is passed via LangGraph's `context=` kwarg on `invoke()` / `stream()`, typed by a `context_schema` dataclass on the `StateGraph`. Nodes access it via `runtime.context.llm` (using `langgraph.runtime.Runtime`).
  - *Rationale*: State must remain serialisable for checkpointing.
- **Separation of Code and Skills**: Runtime code goes in `ingestion/`, documentation/methodology goes in `Skills/Ingestion/`.
  - *Rationale*: Follows the established project-wide convention for agents.

## Risks / Trade-offs

- **Risk: Orchestrator fails to provide valid input** → Mitigation: Document exactly what the orchestrator must validate (config rules from Phase 2, file existence) before invoking the graph. The graph will throw explicit exceptions if these constraints are violated.
- **Risk: Tightly coupled downstream dependencies** → Mitigation: The ingestion pipeline returns a simple `dict[str, str]` and does not import or know about ARLO. The orchestrator maps the output to `ARLOInput`.
