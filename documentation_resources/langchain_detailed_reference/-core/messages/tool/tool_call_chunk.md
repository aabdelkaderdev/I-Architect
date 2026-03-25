<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/tool_call_chunk -->

Functionv1.2.21 (latest)●Since v0.2

# tool\_call\_chunk

Create a tool call chunk.


```
tool_call_chunk(
  *,
  name: str | None = None,
  args: str | None = None,
  id: str | None = None,
  index: int | None = None
) -> ToolCallChunk
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str | None` | Default:`None`  The name of the tool to be called. |
| `args` | `str | None` | Default:`None`  The arguments to the tool call as a JSON string. |
| `id` | `str | None` | Default:`None`  An identifier associated with the tool call. |
| `index` | `int | None` | Default:`None`  The index of the tool call in a sequence. |


