<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/sessions/StdioConnection -->

Classv0.2.2 (latest)●Since v0.1

# StdioConnection


```
StdioConnection()
```

## Bases

`TypedDict`

## Constructors

## Attributes



constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| transport | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['stdio'] |
| command | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| args | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| env | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)] | None] |
| cwd | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str) | [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) | None] |
| encoding | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| encoding\_error\_handler | NotRequired[[EncodingErrorHandler](/python/langchain-mcp-adapters/sessions/EncodingErrorHandler)] |
| session\_kwargs | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None] |

[attribute

transport: Literal['stdio']](/python/langchain-mcp-adapters/sessions/StdioConnection/transport)

[attribute

command: str

The executable to run to start the server.](/python/langchain-mcp-adapters/sessions/StdioConnection/command)

[attribute

args: list[str]

Command line arguments to pass to the executable.](/python/langchain-mcp-adapters/sessions/StdioConnection/args)

[attribute

env: NotRequired[dict[str, str] | None]

The environment to use when spawning the process.

If not specified or set to None, a subset of the default environment
variables from the current process will be used.

Please refer to the MCP SDK documentation for details on which
environment variables are included by default. The behavior
varies by operating system.

<https://github.com/modelcontextprotocol/python-sdk/blob/c47c767ff437ee88a19e6b9001e2472cb6f7d5ed/src/mcp/client/stdio/__init__.py#L51>](/python/langchain-mcp-adapters/sessions/StdioConnection/env)

[attribute

cwd: NotRequired[str | Path | None]

The working directory to use when spawning the process.](/python/langchain-mcp-adapters/sessions/StdioConnection/cwd)

[attribute

encoding: NotRequired[str]

The text encoding used when sending/receiving messages to the server.

Default is 'utf-8'.](/python/langchain-mcp-adapters/sessions/StdioConnection/encoding)

[attribute

encoding\_error\_handler: NotRequired[EncodingErrorHandler]

The text encoding error handler.

See <https://docs.python.org/3/library/codecs.html#codec-base-classes> for
explanations of possible values.

Default is 'strict', which raises an error on encoding/decoding errors.](/python/langchain-mcp-adapters/sessions/StdioConnection/encoding_error_handler)

[attribute

session\_kwargs: NotRequired[dict[str, Any] | None]

Additional keyword arguments to pass to the ClientSession.](/python/langchain-mcp-adapters/sessions/StdioConnection/session_kwargs)

Configuration for stdio transport connections to MCP servers.