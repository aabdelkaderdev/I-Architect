<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/client/MultiServerMCPClient/get_tools -->

Methodv0.2.2 (latest)●Since v0.0

# get\_tools

Get a list of all tools from all connected servers.


```
get_tools(
  self,
  *,
  server_name: str | None = None
) -> list[BaseTool]
```

A new session will be created for each tool call

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `server_name` | `str | None` | Default:`None`  Optional name of the server to get tools from. If `None`, all tools from all servers will be returned. |


