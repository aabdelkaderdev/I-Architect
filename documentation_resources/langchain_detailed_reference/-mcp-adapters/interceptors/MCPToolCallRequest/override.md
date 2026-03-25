<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/interceptors/MCPToolCallRequest/override -->

Methodv0.2.2 (latest)●Since v0.1

# override

Replace the request with a new request with the given overrides.

Returns a new `MCPToolCallRequest` instance with the specified
attributes replaced. This follows an immutable pattern, leaving the
original request unchanged.


```
override(
  self,
  **overrides: Unpack[_MCPToolCallRequestOverrides] = {}
) -> MCPToolCallRequest
```

**Note:**

Context fields (server\_name, runtime) cannot be overridden as
they are read-only.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**overrides` | `Unpack[_MCPToolCallRequestOverrides]` | Default:`{}`  Keyword arguments for attributes to override. Supported keys:   - name: Tool name - args: Tool arguments - headers: HTTP headers |


