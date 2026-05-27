## Why

The architecture model is provided as a flat JSON input which lacks a pre-built diagram manifest. To generate diagrams, the agent must systematically derive the diagram work queue from this flat data. Additionally, before processing the graph of diagrams, we must ensure the target PlantUML server is available to prevent cascading failures. This phase implements the entry-point nodes of the graph: `server_guard` and `input_parsing`.

## What Changes

- Implement `server_guard` node to initialize the `MultiServerMCPClient` and verify the FastMCP Architecture Server is reachable via `get_tools()`.
- Implement `input_parsing` node to parse the flat JSON input and derive a queue of diagrams (`diagram_queue` of `DiagramSpec` objects) based on unique systems, containers, and scoped relationships.
- Establish rules for focus entity resolution per diagram type (Context, Container, Component).
- Establish diagram ID and output filename conventions.
- Add robust error handling (halting execution if the MCP server is unavailable).

## Capabilities

### New Capabilities

- `diagram-scope-resolution`: Derivation of the diagram work queue (Context, Container, Component diagrams) from a flat architectural JSON model, including focus entity and relationship scoping.
- `server-guard`: Pre-flight checks for external dependencies (Architecture MCP server) before initiating the main processing graph.

### Modified Capabilities

- None

## Impact

- Adds `aga/nodes/server_guard.py` and `aga/nodes/input_parsing.py`.
- Introduces `aga/nodes/__init__.py`.
- Lays the operational foundation for graph processing, consuming the state models (`DiagramSpec`, `AGAState`, `AGAConfig`) introduced in Phase 1.
