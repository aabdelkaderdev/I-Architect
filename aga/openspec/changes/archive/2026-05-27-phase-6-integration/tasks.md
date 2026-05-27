## 1. Output Contract

- [x] 1.1 Define `AGAOutput` TypedDict and `CompletedDiagram`, `FailedDiagram`, `SessionReport` Pydantic models (verify existing definitions in `state/models.py` and `state/schemas.py`).
- [x] 1.2 Update the graph's `output_assembly` node to ensure the returned state dict strictly conforms to the `AGAOutput` contract.

## 2. Configurable Paths & File Writing

- [x] 2.1 Update AGA graph nodes to accept `config: RunnableConfig` (from `langchain_core.runnables`) and read `config["configurable"]["output_dir"]` and `config["configurable"]["checkpoint_db_path"]` for runtime path configuration.
- [x] 2.2 Refactor file saving logic to write the PNG, `.puml`, and metadata sidecar files to the provided `output_dir` instead of hardcoded locations.
- [x] 2.3 Ensure the graph is compiled with `SqliteSaver` from `langgraph.checkpoint.sqlite` (package: `langgraph-checkpoint-sqlite`), instantiated as `SqliteSaver(sqlite3.connect(db_path))`.

## 3. Assumption Handling

- [x] 3.1 Update the PlantUML generator to check node metadata for the `assumed: true` flag.
- [x] 3.2 Modify the PlantUML generator to append `[assumed]` to the description text of assumed elements in the `.puml` output.

## 4. Public API Wiring

- [x] 4.1 Update `__init__.py` to export the graph factory (`create_aga_graph`), output types (`AGAOutput`), and data models (`CompletedDiagram`, `FailedDiagram`, `SessionReport`).
- [x] 4.2 Add comprehensive docstrings to the exported public API to guide downstream consumers (Orchestrator/SA/RGA).

## 5. Testing & Validation

- [x] 5.1 Implement unit tests for OS detection, PlantUML encoding, and derivation of the diagram queue. Use `InMemorySaver` from `langgraph.checkpoint.memory` for test checkpointers.
- [x] 5.2 Implement an end-to-end integration test using `arch_model_test_result-1.json` to validate the full workflow and file creation. Invoke the compiled graph with `config={"configurable": {"thread_id": "test-thread", "output_dir": "<temp_dir>"}}`.
- [x] 5.3 Write a test verifying that `[assumed]` tags correctly appear in `.puml` for nodes marked with `assumed: true`.

