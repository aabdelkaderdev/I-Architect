## ADDED Requirements

### Requirement: AGA Module Structure
The project SHALL implement a standard folder structure for the AGA module matching the existing RAA module layout.

#### Scenario: Module initialization
- **WHEN** the project is inspected
- **THEN** the `aga/state` directory MUST exist alongside `aga/graphs`, `aga/nodes`, `aga/Skills`, `aga/prompts`, `aga/tools`, and `aga/utils`.

### Requirement: AGA Configuration
The AGA module SHALL define an `AGAConfig` as a Python `@dataclass` in `aga/state/config.py` to hold runtime configuration provided by the orchestrator. This dataclass will serve as the `context_schema` for the LangGraph `StateGraph` (per current LangGraph docs: `StateGraph(AGAState, context_schema=AGAConfig)`). Nodes SHALL access it via `runtime: Runtime[AGAConfig]` from `langgraph.runtime`.

#### Scenario: Configuration definition
- **WHEN** inspecting `aga/state/config.py`
- **THEN** an `AGAConfig` decorated with `@dataclass` MUST exist with fields `max_retries` (int, default 5), `plantuml_server_url` (str, default `"http://www.plantuml.com/plantuml"`), `checkpoint_db_path` (str, no default), `output_dir_png` (str, no default), `output_dir_puml` (str, no default), `output_dir_diagrams` (str, no default), and `read_timeout_seconds` (int, default 30).

### Requirement: State TypedDicts
The AGA module SHALL define the LangGraph state channels using standard `TypedDict` schemas in `aga/state/schemas.py`. Per current LangGraph v1 and LangChain v1 documentation, TypedDict is the ONLY supported schema type for graph state.

#### Scenario: TypedDict creation
- **WHEN** inspecting `aga/state/schemas.py`
- **THEN** `AGAInput`, `AGAOutput`, and `AGAState` TypedDicts MUST exist.
- **THEN** `AGAInput` MUST contain the `arch_model` key of type `dict`.

#### Scenario: Accumulator channels use Annotated reducers
- **WHEN** inspecting the `AGAState` TypedDict in `aga/state/schemas.py`
- **THEN** the `completed_diagrams` and `failed_diagrams` fields MUST use `Annotated[list[dict], operator.add]` to enable append-only accumulation across node updates, following the documented LangGraph reducer pattern.

### Requirement: Internal Pydantic Models
The AGA module SHALL define Pydantic models for structured state entities in `aga/state/models.py`.

#### Scenario: Output models definition
- **WHEN** inspecting `aga/state/models.py`
- **THEN** `DiagramSpec`, `CompletedDiagram`, `FailedDiagram`, and `SessionReport` Pydantic models MUST exist.

### Requirement: Input Validation Models
The AGA module SHALL define Pydantic models mapping to the expected flat JSON structure of the architecture model to enable runtime validation. These models are used for validation inside nodes, NOT as LangGraph state schemas.

#### Scenario: Input validation models definition
- **WHEN** inspecting `aga/state/models.py`
- **THEN** `ArchModel`, `Entity`, and `Relationship` Pydantic models MUST exist.
- **THEN** these models MUST NOT use `extra="forbid"`.
