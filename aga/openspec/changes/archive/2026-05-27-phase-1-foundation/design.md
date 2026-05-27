## Context

The Architecture Generation Agent (AGA) will function as a standalone LangGraph StateGraph, invoked by an orchestrator after the RAA (Requirements Analysis Agent) phase completes. It receives a flat JSON representation of a C4-compliant architecture model and is expected to produce PNG architecture diagrams and corresponding PlantUML (.puml) source files. Phase 1 sets up the necessary data structures for this processing, including the folder structure matching `arlo` and `raa`, as well as configuration and state representation schemas.

**LangChain/LangGraph API alignment (current docs):**
- `create_react_agent` (from `langgraph.prebuilt`) is **deprecated** in LangGraph v1. The replacement is `langchain.agents.create_agent` from LangChain v1. Downstream phases MUST use `create_agent` instead.
- `create_agent` only supports **TypedDict** for state schemas — Pydantic models and dataclasses are NOT supported as graph state schemas.
- Runtime context (e.g., the LLM instance) is now passed via a `context_schema` dataclass on the `StateGraph` constructor, and nodes access it via `runtime: Runtime[ContextSchema]` from `langgraph.runtime`. The old `config["configurable"]` pattern for custom runtime data is replaced by the `context` argument to `invoke`.
- Accumulator-style channels (e.g., `completed_diagrams`) use `Annotated[list[T], operator.add]` reducer syntax.
- `SqliteSaver` checkpointer requires the separate `langgraph-checkpoint-sqlite` package.

## Goals / Non-Goals

**Goals:**
- Create the structural foundation of the AGA module (`aga/state`, `aga/prompts`, `aga/graphs`, etc.).
- Define the `AGAConfig` as a `@dataclass` in `aga/state/config.py` — this will serve as the `context_schema` for the `StateGraph`, allowing nodes to access runtime configuration via `runtime: Runtime[AGAConfig]`.
- Define LangGraph state channels via TypedDicts (`AGAInput`, `AGAOutput`, `AGAState`) — this is the ONLY supported state schema type for `create_agent` and `StateGraph`.
- Define Pydantic models for structured processing (`DiagramSpec`, `CompletedDiagram`, `FailedDiagram`, `SessionReport`).
- Define Pydantic models for incoming `arch_model` validation (`ArchModel`, `Entity`, `Relationship`) based on flat JSON structure.

**Non-Goals:**
- Implementing any LangGraph nodes or graph execution logic (reserved for later phases).
- Implementing PlantUML code generation or tool wrappers.
- Building the `create_agent` or `StateGraph` graph definition (Phase 5).

## Decisions

**1. Pydantic Models for Input Validation**
- **Decision:** Use Pydantic models to represent the flat `arch_model` input JSON dictionary (`ArchModel`, `Entity`, `Relationship`).
- **Rationale:** While the AGA state graph channel (`AGAInput`) only requires a `dict`, mapping this dictionary to Pydantic models provides immediate runtime validation against the expected PRD contract, mitigating unexpected downstream errors in the nodes. These models are NOT used as graph state — they are used for validation inside the `input_parsing` node.
- **Alternatives Considered:** Relying strictly on raw `dict` structures as originally stated. Rejected due to decreased safety.

**2. Standard Validation (No `extra="forbid"`)**
- **Decision:** Do not enforce strict validation (`extra="forbid"`) on the Pydantic models.
- **Rationale:** Allowing extra fields ensures the AGA module is somewhat decoupled from orchestrator updates; if the orchestrator passes additional context or benign fields in the future, the AGA will not crash.

**3. Three-Schema Pattern with TypedDicts Only**
- **Decision:** Follow the `AGAInput`, `AGAOutput`, and `AGAState` TypedDict pattern.
- **Rationale:** Maintains consistency with the existing ARLO and RAA modules. Additionally, current LangGraph v1 and LangChain v1 docs confirm that **only TypedDict is supported for graph state schemas** — Pydantic and dataclass state schemas are no longer supported for `create_agent`.

**4. AGAConfig as @dataclass for context_schema**
- **Decision:** Define `AGAConfig` as a Python `@dataclass` (not a Pydantic model or plain dict).
- **Rationale:** Current LangGraph docs show that `StateGraph` accepts a `context_schema` parameter which must be a `@dataclass` or `TypedDict`. By making `AGAConfig` a dataclass, it can be passed directly as `StateGraph(AGAState, context_schema=AGAConfig)` in Phase 5. Nodes will then access config via `runtime: Runtime[AGAConfig]` from `langgraph.runtime`.
- **Alternatives Considered:** Passing config via `config["configurable"]` (old pattern). Rejected because the current docs explicitly recommend `context_schema` and the `context` argument to `invoke/stream`.

**5. Accumulator Channels via `Annotated` Reducers**
- **Decision:** Use `Annotated[list[dict], operator.add]` for `completed_diagrams` and `failed_diagrams` in `AGAState`.
- **Rationale:** This is the documented LangGraph pattern for append-only list channels. Without the `Annotated` reducer, each node update would overwrite the entire list instead of appending.

## Risks / Trade-offs

- **Risk:** Data model drift between the orchestrator's generated flat JSON and the AGA's `ArchModel` Pydantic schemas.
  - **Mitigation:** The lack of `extra="forbid"` provides some buffer for additions, but breaking changes in existing fields will still cause validation errors. Unit tests will be required to ensure the contract holds.
- **Risk:** The `create_react_agent` → `create_agent` migration may affect how the ARLO/RAA modules are structured if they haven't been updated yet.
  - **Mitigation:** For Phase 1, we only define data structures. The actual agent creation (Phase 5) will use the current `create_agent` API. If ARLO/RAA are still on the old API, that's their concern — AGA will follow the latest docs from the start.
