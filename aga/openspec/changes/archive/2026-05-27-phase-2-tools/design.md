# Phase 2 — Tools (MCP Server)

## Architecture

We use the Model Context Protocol (MCP) to decouple the diagram tools from the core agent.
- **FastMCP Server**: The tools (`encode_plantuml` and `fetch_plantuml_png`) are hosted in a `fastmcp` stdio server.
- **MultiServerMCPClient**: The agent accesses the tools using `langchain-mcp-adapters`.
- **Tool Interceptors**: We use `tool_interceptors` on `MultiServerMCPClient` with `MCPToolCallRequest` from `langchain_mcp_adapters.interceptors` for handling tool exceptions.

## Decisions
- **`fastmcp` for Server**: Replaces local `@tool` decorators.
- **`stdio` transport**: The server runs as a subprocess via standard input/output.
- **`langchain-mcp-adapters`**: Used by the ReAct agent to fetch tools dynamically.
- **`tool_interceptors`**: Current LangChain MCP pattern for tool execution error handling via async interceptor functions.
