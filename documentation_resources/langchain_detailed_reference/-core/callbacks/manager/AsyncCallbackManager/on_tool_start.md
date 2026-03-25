<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_tool_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_start

Run when the tool starts running.


```
on_tool_start(
  self,
  serialized: dict[str, Any] | None,
  input_str: str,
  run_id: UUID | None = None,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> AsyncCallbackManagerForToolRun
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any] | None` | The serialized tool. |
| `input_str`\* | `str` | The input to the tool. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


