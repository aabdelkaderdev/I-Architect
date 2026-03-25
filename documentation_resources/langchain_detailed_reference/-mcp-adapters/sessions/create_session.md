<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/sessions/create_session -->

Functionv0.2.2 (latest)●Since v0.1

# create\_session

Create a new session to an MCP server.


```
create_session(
  connection: Connection,
  *,
  mcp_callbacks: _MCPCallbacks | None = None
) -> AsyncIterator[ClientSession]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `connection`\* | `Connection` | Connection config to use to connect to the server |
| `mcp_callbacks` | `_MCPCallbacks | None` | Default:`None`  mcp sdk compatible callbacks to use for the ClientSession |


