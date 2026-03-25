<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/CallbackManager/on_tool_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_start

Run when tool starts running.


```
on_tool_start(
  self,
  serialized: dict[str, Any] | None,
  input_str: str,
  run_id: UUID | None = None,
  parent_run_id: UUID | None = None,
  inputs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> CallbackManagerForToolRun
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any] | None` | Serialized representation of the tool. |
| `input_str`\* | `str` | The input to the tool as a string.  Non-string inputs are cast to strings. |
| `run_id` | `UUID | None` | Default:`None`  ID for the run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `inputs` | `dict[str, Any] | None` | Default:`None`  The original input to the tool if provided.  Recommended for usage instead of input\_str when the original input is needed.  If provided, the inputs are expected to be formatted as a dict. The keys will correspond to the named-arguments in the tool. |
| `**kwargs` | `Any` | Default:`{}`  The keyword arguments to pass to the event handler |


