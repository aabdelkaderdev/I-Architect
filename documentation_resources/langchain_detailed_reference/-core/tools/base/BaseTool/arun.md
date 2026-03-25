<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/BaseTool/arun -->

Methodv1.2.21 (latest)●Since v0.2

# arun

Run the tool asynchronously.


```
arun(
  self,
  tool_input: str | dict,
  verbose: bool | None = None,
  start_color: str | None = 'green',
  color: str | None = 'green',
  callbacks: Callbacks = None,
  *,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  run_name: str | None = None,
  run_id: uuid.UUID | None = None,
  config: RunnableConfig | None = None,
  tool_call_id: str | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tool_input`\* | `str | dict` | The input to the tool. |
| `verbose` | `bool | None` | Default:`None`  Whether to log the tool's progress. |
| `start_color` | `str | None` | Default:`'green'`  The color to use when starting the tool. |
| `color` | `str | None` | Default:`'green'`  The color to use when ending the tool. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to be called during tool execution. |
| `tags` | `list[str] | None` | Default:`None`  Optional list of tags associated with the tool. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  Optional metadata associated with the tool. |
| `run_name` | `str | None` | Default:`None`  The name of the run. |
| `run_id` | `uuid.UUID | None` | Default:`None`  The id of the run. |
| `config` | `RunnableConfig | None` | Default:`None`  The configuration for the tool. |
| `tool_call_id` | `str | None` | Default:`None`  The id of the tool call. |
| `**kwargs` | `Any` | Default:`{}`  Keyword arguments to be passed to tool callbacks |


