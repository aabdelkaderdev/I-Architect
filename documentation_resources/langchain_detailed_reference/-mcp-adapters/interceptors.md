<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/interceptors -->

Modulev0.2.2 (latest)●Since v0.1

# interceptors

Interceptor interfaces and types for MCP client tool call lifecycle management.

This module provides an interceptor interface for wrapping and controlling
MCP tool call execution with a handler callback pattern.

In the future, we might add more interceptors for other parts of the
request / result lifecycle, for example to support elicitation.

## Attributes

## Classes

## Type Aliases



[attribute

LANGGRAPH\_PRESENT: bool](/python/langchain-mcp-adapters/interceptors/LANGGRAPH_PRESENT)

[class

MCPToolCallRequest](/python/langchain-mcp-adapters/interceptors/MCPToolCallRequest)

[class

ToolCallInterceptor](/python/langchain-mcp-adapters/interceptors/ToolCallInterceptor)

[typeAlias

MCPToolCallResult](/python/langchain-mcp-adapters/interceptors/MCPToolCallResult)

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