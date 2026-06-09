## Why

We need to build the core toolset for the agent to render PlantUML architectures and perform OS/architecture detection for binary resolution. In alignment with the current LangChain MCP (Model Context Protocol) documentation, we will implement these tools as an MCP Server using `fastmcp`.

## What Changes

We will introduce a FastMCP server exposing two tools:
1. OS/architecture detection for binary resolution (internal helper).
2. PlantUML encoding via the `planturl` binary (`encode_plantuml`).
3. PNG fetching with SVG-based error detection (`fetch_plantuml_png`).

These tools will be consumed by the LangChain agent via `MultiServerMCPClient` from `langchain-mcp-adapters`. Error handling for tool failures will use `tool_interceptors` on the MCP client.

## Capabilities

### New Capabilities
- `encode-plantuml`: Wraps the `planturl` binary to encode PlantUML code. Exposed via FastMCP.
- `fetch-plantuml-png`: Fetches the PNG image from the encoded URL. Exposed via FastMCP.
- `mcp_server`: A FastMCP stdio server hosting the architecture tools.

## Impact

- **New files**: `aga/tools/mcp_server.py`, `aga/tools/os_detection.py`, `aga/tools/encode_plantuml.py`, `aga/tools/fetch_plantuml_png.py`.
- **Dependencies**: `fastmcp`, `langchain-mcp-adapters`, `langchain`.
- **System**: The tools are decoupled into an MCP server, making them usable across different agents and environments.
