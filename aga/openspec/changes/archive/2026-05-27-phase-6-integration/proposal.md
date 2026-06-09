## Why

This change represents Phase 6 of the AGA module development. It is necessary to fully integrate the internal agent workflow with the external Orchestrator and downstream agents (SA/RGA). It finalizes how the AGA module is invoked, how it structures its output, where it writes generated artifacts, and how it signals assumptions in diagrams, ensuring end-to-end functionality within the larger system.

## What Changes

- **Public API Wiring**: Export necessary functions and classes through `__init__.py`.
- **Configurable Output Paths**: Support runtime configuration of output and checkpoint directories by the Orchestrator via the LangChain v1 `context` parameter (dataclass-based `context_schema`) and LangGraph `RunnableConfig`. The `context` parameter is the recommended v1 approach; `config["configurable"]` remains available for backward compatibility (see [LangChain v1 migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1)).
- **Output Contract**: Implement the `AGAOutput`, `CompletedDiagram`, and `SessionReport` schema models.
- **Integration Points**: Implement logic to handle data threading from Orchestrator to AGA (via `context=` at invocation), and from AGA to SA/RGA (via `AGAOutput`).
- **Assumption Handling**: Add logic to append `[assumed]` to entity description strings in PlantUML code when an entity has the `assumed: true` metadata flag.
- **Testing Scaffolding**: Create unit, integration, and functional tests using the `arch_model_test_result-1.json` fixture.

## Capabilities

### New Capabilities
- `orchestrator-integration`: Defines the public API, runtime context schema (for output/checkpoint paths via `context_schema`), and the output contract returning artifacts and session reports for downstream use. Uses `langgraph.checkpoint.sqlite.SqliteSaver` (from `langgraph-checkpoint-sqlite`) for local persistence and `langgraph.checkpoint.memory.InMemorySaver` for tests.
- `assumption-handling`: Logic for modifying PlantUML rendering to explicitly annotate assumed entities.
- `aga-testing`: Scaffolding and tests for validating the AGA module's integration and correctness.

### Modified Capabilities

## Impact

- **Code impacted**: `__init__.py`, `state/config.py` (context schema), `graphs/aga_graph.py` (checkpointer wiring), PlantUML rendering components, and new test files.
- **System impacted**: Integration between the Orchestrator, AGA, SA, and RGA will now be enabled.
- **Dependencies**: Requires `langgraph-checkpoint-sqlite` package for `SqliteSaver`.
