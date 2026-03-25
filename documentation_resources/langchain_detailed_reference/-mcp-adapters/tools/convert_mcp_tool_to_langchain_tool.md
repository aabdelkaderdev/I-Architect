<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/tools/convert_mcp_tool_to_langchain_tool -->

Functionv0.2.2 (latest)●Since v0.0

# convert\_mcp\_tool\_to\_langchain\_tool

Convert an MCP tool to a LangChain tool.

NOTE: this tool can be executed only in a context of an active MCP client session.


```
convert_mcp_tool_to_langchain_tool(
  session: ClientSession | None,
  tool: MCPTool,
  *,
  connection: Connection | None = None,
  callbacks: Callbacks | None = None,
  tool_interceptors: list[ToolCallInterceptor] | None = None,
  server_name: str | None = None,
  tool_name_prefix: bool = False
) -> BaseTool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `session`\* | `ClientSession | None` | MCP client session |
| `tool`\* | `MCPTool` | MCP tool to convert |
| `connection` | `Connection | None` | Default:`None`  Optional connection config to use to create a new session if a `session` is not provided |
| `callbacks` | `Callbacks | None` | Default:`None`  Optional callbacks for handling notifications and events |
| `tool_interceptors` | `list[ToolCallInterceptor] | None` | Default:`None`  Optional list of interceptors for tool call processing |
| `server_name` | `str | None` | Default:`None`  Name of the server this tool belongs to |
| `tool_name_prefix` | `bool` | Default:`False`  If `True` and `server_name` is provided, the tool name will be prefixed w/ server name (e.g., `"weather_search"` instead of `"search"`) |


