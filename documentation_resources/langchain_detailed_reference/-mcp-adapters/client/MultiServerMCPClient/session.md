<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/client/MultiServerMCPClient/session -->

Methodv0.2.2 (latest)●Since v0.1

# session

Connect to an MCP server and initialize a session.


```
session(
  self,
  server_name: str,
  *,
  auto_initialize: bool = True
) -> AsyncIterator[ClientSession]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `server_name`\* | `str` | Name to identify this server connection |
| `auto_initialize` | `bool` | Default:`True`  Whether to automatically initialize the session |


