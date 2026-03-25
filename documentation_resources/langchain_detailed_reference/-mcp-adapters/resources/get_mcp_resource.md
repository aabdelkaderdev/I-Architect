<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/resources/get_mcp_resource -->

Functionv0.2.2 (latest)●Since v0.0

# get\_mcp\_resource

Fetch a single MCP resource and convert it to LangChain [Blob objects](/python/langchain-core/documents/base/Blob).


```
get_mcp_resource(
    session: ClientSession,
    uri: str,
) -> list[Blob]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `session`\* | `ClientSession` | MCP client session. |
| `uri`\* | `str` | URI of the resource to fetch. |


