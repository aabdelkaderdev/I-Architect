<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/langchain_mcp_adapters -->

Modulev0.2.2 (latest)●Since v0.0

# langchain\_mcp\_adapters

LangChain MCP Adapters - Connect MCP servers with LangChain applications.

This package provides adapters to connect MCP (Model Context Protocol) servers
with LangChain applications, converting MCP tools, prompts, and resources into
LangChain-compatible formats.

## Modules



[module

callbacks](/python/langchain-mcp-adapters/callbacks)

[module

prompts](/python/langchain-mcp-adapters/prompts)

[module

interceptors](/python/langchain-mcp-adapters/interceptors)

[module

resources](/python/langchain-mcp-adapters/resources)

[module

client](/python/langchain-mcp-adapters/client)

[module

sessions](/python/langchain-mcp-adapters/sessions)

[module

tools](/python/langchain-mcp-adapters/tools)

Types for callbacks.

Prompts adapter for converting MCP prompts to LangChain [messages](https://docs.langchain.com/oss/python/langchain/messages).

This module provides functionality to convert MCP prompt messages into LangChain
message objects, handling both user and assistant message types.

Interceptor interfaces and types for MCP client tool call lifecycle management.

This module provides an interceptor interface for wrapping and controlling
MCP tool call execution with a handler callback pattern.

In the future, we might add more interceptors for other parts of the
request / result lifecycle, for example to support elicitation.

Resources adapter for converting MCP resources to LangChain [Blob objects](/python/langchain-core/documents/base/Blob).

This module provides functionality to convert MCP resources into LangChain Blob
objects, handling both text and binary resource content types.

Client for connecting to multiple MCP servers and loading LC tools/resources.

This module provides the `MultiServerMCPClient` class for managing connections
to multiple MCP servers and loading tools, prompts, and resources from them.

Session management for different MCP transport types.

This module provides connection configurations and session management for various
MCP transport types including stdio, SSE, WebSocket, and streamable HTTP.

Tools adapter for converting MCP tools to LangChain tools.

This module provides functionality to convert MCP tools into LangChain-compatible
tools, handle tool execution, and manage tool conversion between the two formats.