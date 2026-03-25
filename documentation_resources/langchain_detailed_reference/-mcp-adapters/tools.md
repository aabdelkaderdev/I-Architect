<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/tools -->

Modulev0.2.2 (latest)●Since v0.0

# tools

Tools adapter for converting MCP tools to LangChain tools.

This module provides functionality to convert MCP tools into LangChain-compatible
tools, handle tool execution, and manage tool conversion between the two formats.

## Attributes

[attribute

LANGGRAPH\_PRESENT: bool](/python/langchain-mcp-adapters/tools/LANGGRAPH_PRESENT)[attribute

MAX\_ITERATIONS: int](/python/langchain-mcp-adapters/tools/MAX_ITERATIONS)

## Functions

## Classes

## Type Aliases



[function

create\_session](/python/langchain-mcp-adapters/sessions/create_session)

[function

convert\_mcp\_tool\_to\_langchain\_tool](/python/langchain-mcp-adapters/tools/convert_mcp_tool_to_langchain_tool)

[function

load\_mcp\_tools](/python/langchain-mcp-adapters/tools/load_mcp_tools)

[function

to\_fastmcp](/python/langchain-mcp-adapters/tools/to_fastmcp)

[class

CallbackContext](/python/langchain-mcp-adapters/callbacks/CallbackContext)

[class

Callbacks](/python/langchain-mcp-adapters/callbacks/Callbacks)

[class

MCPToolCallRequest](/python/langchain-mcp-adapters/interceptors/MCPToolCallRequest)

[class

ToolCallInterceptor](/python/langchain-mcp-adapters/interceptors/ToolCallInterceptor)

[class

MCPToolArtifact](/python/langchain-mcp-adapters/tools/MCPToolArtifact)

[typeAlias

MCPToolCallResult](/python/langchain-mcp-adapters/interceptors/MCPToolCallResult)

[typeAlias

Connection](/python/langchain-mcp-adapters/sessions/Connection)

[typeAlias

ToolMessageContentBlock](/python/langchain-mcp-adapters/tools/ToolMessageContentBlock)

[typeAlias

ConvertedToolResult: list[ToolMessageContentBlock] | ToolMessage | Command](/python/langchain-mcp-adapters/tools/ConvertedToolResult)

Create a new session to an MCP server.

Convert an MCP tool to a LangChain tool.

NOTE: this tool can be executed only in a context of an active MCP client session.

Load all available MCP tools and convert them to LangChain [tools](https://docs.langchain.com/oss/python/langchain/tools).

Convert LangChain tool to FastMCP tool.

LangChain MCP client callback context.

Callbacks for the LangChain MCP client.

Tool execution request passed to MCP tool call interceptors.

This tool call request follows a similar pattern to LangChain's
ToolCallRequest (flat namespace) rather than separating the call data
and context into nested objects.

Modifiable fields (override these to change behavior):
name: Tool name to invoke.
args: Tool arguments as key-value pairs.
headers: HTTP headers for applicable transports (SSE, HTTP).

Context fields (read-only, use for routing/logging):
server\_name: Name of the MCP server handling the tool.
runtime: LangGraph runtime context (optional, None if outside graph).

Protocol for tool call interceptors using handler callback pattern.

Interceptors wrap tool execution to enable request/response modification,
retry logic, caching, rate limiting, and other cross-cutting concerns.
Multiple interceptors compose in "onion" pattern (first is outermost).

The handler can be called multiple times (retry), skipped (caching/short-circuit),
or wrapped with error handling. Each handler call is independent.

Similar to LangChain's middleware pattern but adapted for MCP remote tools.

Artifact returned from MCP tool calls.

This TypedDict wraps the structured content from MCP tool calls,
allowing for future extension if MCP adds more fields to tool results.