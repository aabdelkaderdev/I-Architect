<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/tool_call -->

Functionv1.2.21 (latest)●Since v0.2

# tool\_call

Create a tool call.


```
tool_call(
  *,
  name: str,
  args: dict[str, Any],
  id: str | None
) -> ToolCall
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name`\* | `str` | The name of the tool to be called. |
| `args`\* | `dict[str, Any]` | The arguments to the tool call as a dictionary. |
| `id`\* | `str | None` | An identifier associated with the tool call. |


