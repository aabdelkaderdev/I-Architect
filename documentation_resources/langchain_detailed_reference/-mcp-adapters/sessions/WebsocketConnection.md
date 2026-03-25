<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/sessions/WebsocketConnection -->

Classv0.2.2 (latest)●Since v0.1

# WebsocketConnection


```
WebsocketConnection()
```

## Bases

`TypedDict`

## Constructors

## Attributes



constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| transport | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['websocket'] |
| url | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| session\_kwargs | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None] |

[attribute

transport: Literal['websocket']](/python/langchain-mcp-adapters/sessions/WebsocketConnection/transport)

[attribute

url: str

The URL of the Websocket endpoint to connect to.](/python/langchain-mcp-adapters/sessions/WebsocketConnection/url)

[attribute

session\_kwargs: NotRequired[dict[str, Any] | None]

Additional keyword arguments to pass to the ClientSession](/python/langchain-mcp-adapters/sessions/WebsocketConnection/session_kwargs)

Configuration for WebSocket transport connections to MCP servers.