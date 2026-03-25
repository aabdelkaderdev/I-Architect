<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/client -->

Modulev0.2.2 (latest)●Since v0.0

# client

Client for connecting to multiple MCP servers and loading LC tools/resources.

This module provides the `MultiServerMCPClient` class for managing connections
to multiple MCP servers and loading tools, prompts, and resources from them.

## Attributes

[attribute

ASYNC\_CONTEXT\_MANAGER\_ERROR: str](/python/langchain-mcp-adapters/client/ASYNC_CONTEXT_MANAGER_ERROR)

## Functions

[function

load\_mcp\_prompt

Load MCP prompt and convert to LangChain [messages](https://docs.langchain.com/oss/python/langchain/messages).](/python/langchain-mcp-adapters/prompts/load_mcp_prompt)[function

load\_mcp\_resources

Load MCP resources and convert them to LangChain [Blob objects](/python/langchain-core/documents/base/Blob).](/python/langchain-mcp-adapters/resources/load_mcp_resources)[function

create\_session

Create a new session to an MCP server.](/python/langchain-mcp-adapters/sessions/create_session)[function

load\_mcp\_tools

Load all available MCP tools and convert them to LangChain [tools](https://docs.langchain.com/oss/python/langchain/tools).](/python/langchain-mcp-adapters/tools/load_mcp_tools)

## Classes

[class

CallbackContext

LangChain MCP client callback context.](/python/langchain-mcp-adapters/callbacks/CallbackContext)[class

Callbacks

Callbacks for the LangChain MCP client.](/python/langchain-mcp-adapters/callbacks/Callbacks)[class

ToolCallInterceptor

Protocol for tool call interceptors using handler callback pattern.

Interceptors wrap tool execution to enable request/response modification,
retry logic, caching, rate limiting, and other cross-cutting concerns.
Multiple interceptors compose in "onion" pattern (first is outermost).

The handler can be called multiple times (retry), skipped (caching/short-circuit),
or wrapped with error handling. Each handler call is independent.

Similar to LangChain's middleware pattern but adapted for MCP remote tools.](/python/langchain-mcp-adapters/interceptors/ToolCallInterceptor)[class

McpHttpClientFactory

Protocol for creating httpx.AsyncClient instances for MCP connections.](/python/langchain-mcp-adapters/sessions/McpHttpClientFactory)[class

SSEConnection

Configuration for Server-Sent Events (SSE) transport connections to MCP.](/python/langchain-mcp-adapters/sessions/SSEConnection)[class

StdioConnection

Configuration for stdio transport connections to MCP servers.](/python/langchain-mcp-adapters/sessions/StdioConnection)[class

StreamableHttpConnection

Connection configuration for Streamable HTTP transport.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection)[class

WebsocketConnection

Configuration for WebSocket transport connections to MCP servers.](/python/langchain-mcp-adapters/sessions/WebsocketConnection)[class

MultiServerMCPClient

Client for connecting to multiple MCP servers.

Loads LangChain-compatible tools, prompts and resources from MCP servers.](/python/langchain-mcp-adapters/client/MultiServerMCPClient)

## Type Aliases

[typeAlias

Connection](/python/langchain-mcp-adapters/sessions/Connection)


