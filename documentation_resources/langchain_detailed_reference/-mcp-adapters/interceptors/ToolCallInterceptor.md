<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/interceptors/ToolCallInterceptor -->

Classv0.2.2 (latest)●Since v0.1

# ToolCallInterceptor

Protocol for tool call interceptors using handler callback pattern.

Interceptors wrap tool execution to enable request/response modification,
retry logic, caching, rate limiting, and other cross-cutting concerns.
Multiple interceptors compose in "onion" pattern (first is outermost).

The handler can be called multiple times (retry), skipped (caching/short-circuit),
or wrapped with error handling. Each handler call is independent.

Similar to LangChain's middleware pattern but adapted for MCP remote tools.


```
ToolCallInterceptor()
```

## Bases

`Protocol`


