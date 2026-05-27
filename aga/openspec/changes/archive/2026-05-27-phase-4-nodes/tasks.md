## 1. Server Guard Node

- [x] 1.1 Create `aga/nodes/server_guard.py` with standard node signature receiving state and config.
- [x] 1.2 Implement the `MultiServerMCPClient` initialization (from `langchain-mcp-adapters`) and call `get_tools()` to verify the Architecture MCP tools are reachable.
- [x] 1.3 Raise `ServerUnavailableException` explicitly if the MCP server connection fails or times out.
- [x] 1.4 Add unit tests for `server_guard.py` covering both success and failure connection scenarios.

## 2. Input Parsing Node

- [x] 2.1 Create `aga/nodes/input_parsing.py`.
- [x] 2.2 Implement entity discovery logic to extract all `c4_type = "system"` and `c4_type = "container"` entities from the flat JSON model.
- [x] 2.3 Implement diagram scope derivation: for each potential diagram, verify if relationships matching the required scope (`context`, `container`, `component`) exist.
- [x] 2.4 Implement `DiagramSpec` instantiation with canonical IDs (`ctx-{id}`, `cnt-{id}`, `cmp-{id}`) and mapped output filenames (`.png`, `.puml`, `_metadata.json`).
- [x] 2.5 Update the state by placing the generated `DiagramSpec` objects into `diagram_queue` and setting `diagram_cursor = 0`.
- [x] 2.6 Add unit tests for `input_parsing.py` using mock flat JSON data to verify correct queue ordering and scope filtering.

## 3. Integration

- [x] 3.1 Create/update `aga/nodes/__init__.py` to expose `server_guard` and `input_parsing`.
- [x] 3.2 Add integration test using `arch_model_test_result-1.json` to verify the end-to-end derivation of the diagram queue.
