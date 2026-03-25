<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/invalid_tool_call -->

Functionv1.2.21 (latest)●Since v0.2

# invalid\_tool\_call

Create an invalid tool call.


```
invalid_tool_call(
  *,
  name: str | None = None,
  args: str | None = None,
  id: str | None = None,
  error: str | None = None
) -> InvalidToolCall
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str | None` | Default:`None`  The name of the tool to be called. |
| `args` | `str | None` | Default:`None`  The arguments to the tool call as a JSON string. |
| `id` | `str | None` | Default:`None`  An identifier associated with the tool call. |
| `error` | `str | None` | Default:`None`  An error message associated with the tool call. |


