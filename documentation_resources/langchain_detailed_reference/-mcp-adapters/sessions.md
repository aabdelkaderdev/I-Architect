<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/sessions -->

Modulev0.2.2 (latest)●Since v0.1

# sessions

Session management for different MCP transport types.

This module provides connection configurations and session management for various
MCP transport types including stdio, SSE, WebSocket, and streamable HTTP.

## Attributes

[attribute

logger](/python/langchain-mcp-adapters/sessions/logger)[attribute

EncodingErrorHandler: Literal['strict', 'ignore', 'replace']](/python/langchain-mcp-adapters/sessions/EncodingErrorHandler)[attribute

DEFAULT\_ENCODING: str](/python/langchain-mcp-adapters/sessions/DEFAULT_ENCODING)[attribute

DEFAULT\_ENCODING\_ERROR\_HANDLER: EncodingErrorHandler](/python/langchain-mcp-adapters/sessions/DEFAULT_ENCODING_ERROR_HANDLER)[attribute

DEFAULT\_HTTP\_TIMEOUT: int](/python/langchain-mcp-adapters/sessions/DEFAULT_HTTP_TIMEOUT)[attribute

DEFAULT\_SSE\_READ\_TIMEOUT: int](/python/langchain-mcp-adapters/sessions/DEFAULT_SSE_READ_TIMEOUT)[attribute

DEFAULT\_STREAMABLE\_HTTP\_TIMEOUT](/python/langchain-mcp-adapters/sessions/DEFAULT_STREAMABLE_HTTP_TIMEOUT)[attribute

DEFAULT\_STREAMABLE\_HTTP\_SSE\_READ\_TIMEOUT](/python/langchain-mcp-adapters/sessions/DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT)

## Functions

## Classes

## Type Aliases



[function

create\_session](/python/langchain-mcp-adapters/sessions/create_session)

[class

McpHttpClientFactory](/python/langchain-mcp-adapters/sessions/McpHttpClientFactory)

[class

StdioConnection](/python/langchain-mcp-adapters/sessions/StdioConnection)

[class

SSEConnection](/python/langchain-mcp-adapters/sessions/SSEConnection)

[class

StreamableHttpConnection](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection)

[class

WebsocketConnection](/python/langchain-mcp-adapters/sessions/WebsocketConnection)

[typeAlias

Connection](/python/langchain-mcp-adapters/sessions/Connection)

Create a new session to an MCP server.

Protocol for creating httpx.AsyncClient instances for MCP connections.

Configuration for stdio transport connections to MCP servers.

Configuration for Server-Sent Events (SSE) transport connections to MCP.

Connection configuration for Streamable HTTP transport.

Configuration for WebSocket transport connections to MCP servers.