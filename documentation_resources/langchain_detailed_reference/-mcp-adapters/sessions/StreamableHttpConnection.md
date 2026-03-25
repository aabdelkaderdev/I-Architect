<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/sessions/StreamableHttpConnection -->

Classv0.2.2 (latest)●Since v0.1

# StreamableHttpConnection

Connection configuration for Streamable HTTP transport.


```
StreamableHttpConnection()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| transport | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['streamable\_http'] |
| url | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| headers | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None] |
| timeout | NotRequired[[timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta)] |
| sse\_read\_timeout | NotRequired[[timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta)] |
| terminate\_on\_close | NotRequired[[bool](https://docs.python.org/3/library/functions.html#bool)] |
| session\_kwargs | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None] |
| httpx\_client\_factory | NotRequired[[McpHttpClientFactory](/python/langchain-mcp-adapters/sessions/McpHttpClientFactory) | None] |
| auth | NotRequired[httpx.[Auth](/python/langgraph-sdk/auth/Auth)] |

## Attributes

[attribute

transport: Literal['streamable\_http']](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/transport)[attribute

url: str

The URL of the endpoint to connect to.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/url)[attribute

headers: NotRequired[dict[str, Any] | None]

HTTP headers to send to the endpoint.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/headers)[attribute

timeout: NotRequired[timedelta]

HTTP timeout.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/timeout)[attribute

sse\_read\_timeout: NotRequired[timedelta]

How long (in seconds) the client will wait for a new event before disconnecting.
All other HTTP operations are controlled by `timeout`.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/sse_read_timeout)[attribute

terminate\_on\_close: NotRequired[bool]

Whether to terminate the session on close.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/terminate_on_close)[attribute

session\_kwargs: NotRequired[dict[str, Any] | None]

Additional keyword arguments to pass to the ClientSession.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/session_kwargs)[attribute

httpx\_client\_factory: NotRequired[McpHttpClientFactory | None]

Custom factory for httpx.AsyncClient (optional).](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/httpx_client_factory)[attribute

auth: NotRequired[httpx.Auth]

Optional authentication for the HTTP client.](/python/langchain-mcp-adapters/sessions/StreamableHttpConnection/auth)


