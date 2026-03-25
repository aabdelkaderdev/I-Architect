<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/sessions/SSEConnection -->

Classv0.2.2 (latest)●Since v0.1

# SSEConnection

Configuration for Server-Sent Events (SSE) transport connections to MCP.


```
SSEConnection()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| transport | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['sse'] |
| url | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| headers | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None] |
| timeout | NotRequired[[float](https://docs.python.org/3/library/functions.html#float)] |
| sse\_read\_timeout | NotRequired[[float](https://docs.python.org/3/library/functions.html#float)] |
| session\_kwargs | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None] |
| httpx\_client\_factory | NotRequired[[McpHttpClientFactory](/python/langchain-mcp-adapters/sessions/McpHttpClientFactory) | None] |
| auth | NotRequired[httpx.[Auth](/python/langgraph-sdk/auth/Auth)] |

## Attributes

[attribute

transport: Literal['sse']](/python/langchain-mcp-adapters/sessions/SSEConnection/transport)[attribute

url: str

The URL of the SSE endpoint to connect to.](/python/langchain-mcp-adapters/sessions/SSEConnection/url)[attribute

headers: NotRequired[dict[str, Any] | None]

HTTP headers to send to the SSE endpoint.](/python/langchain-mcp-adapters/sessions/SSEConnection/headers)[attribute

timeout: NotRequired[float]

HTTP timeout.

Default is 5 seconds. If the server takes longer to respond,
you can increase this value.](/python/langchain-mcp-adapters/sessions/SSEConnection/timeout)[attribute

sse\_read\_timeout: NotRequired[float]

SSE read timeout.

Default is 300 seconds (5 minutes). This is how long the client will
wait for a new event before disconnecting.](/python/langchain-mcp-adapters/sessions/SSEConnection/sse_read_timeout)[attribute

session\_kwargs: NotRequired[dict[str, Any] | None]

Additional keyword arguments to pass to the ClientSession.](/python/langchain-mcp-adapters/sessions/SSEConnection/session_kwargs)[attribute

httpx\_client\_factory: NotRequired[McpHttpClientFactory | None]

Custom factory for httpx.AsyncClient (optional).](/python/langchain-mcp-adapters/sessions/SSEConnection/httpx_client_factory)[attribute

auth: NotRequired[httpx.Auth]

Optional authentication for the HTTP client.](/python/langchain-mcp-adapters/sessions/SSEConnection/auth)


