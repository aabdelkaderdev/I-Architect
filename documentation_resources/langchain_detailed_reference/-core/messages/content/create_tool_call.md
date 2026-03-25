<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/create_tool_call -->

Functionv1.2.21 (latest)●Since v1.0

# create\_tool\_call

Create a `ToolCall`.


```
create_tool_call(
  name: str,
  args: dict[str, Any],
  *,
  id: str | None = None,
  index: int | str | None = None,
  **kwargs: Any = {}
) -> ToolCall
```

The `id` is generated automatically if not provided, using a UUID4 format
prefixed with `'lc_'` to indicate it is a LangChain-generated ID.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name`\* | `str` | The name of the tool to be called. |
| `args`\* | `dict[str, Any]` | The arguments to the tool call. |
| `id` | `str | None` | Default:`None`  An identifier for the tool call.  Generated automatically if not provided. |
| `index` | `int | str | None` | Default:`None`  Index of block in aggregate response.  Used during streaming. |


