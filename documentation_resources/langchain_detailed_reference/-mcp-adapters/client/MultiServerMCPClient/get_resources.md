<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/client/MultiServerMCPClient/get_resources -->

Methodv0.2.2 (latest)●Since v0.0

# get\_resources

Get resources from MCP server(s).


```
get_resources(
  self,
  server_name: str | None = None,
  *,
  uris: str | list[str] | None = None
) -> list[Blob]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `server_name` | `str | None` | Default:`None`  Optional name of the server to get resources from. If `None`, all resources from all servers will be returned. |
| `uris` | `str | list[str] | None` | Default:`None`  Optional resource URI or list of URIs to load. If not provided, all resources will be loaded. |


