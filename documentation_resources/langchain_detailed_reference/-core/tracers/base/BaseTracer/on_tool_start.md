<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_tool_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_start

Start a trace for a tool run.


```
on_tool_start(
  self,
  serialized: dict[str, Any],
  input_str: str,
  *,
  run_id: UUID,
  tags: list[str] | None = None,
  parent_run_id: UUID | None = None,
  metadata: dict[str, Any] | None = None,
  name: str | None = None,
  inputs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized tool. |
| `input_str`\* | `str` | The input string. |
| `run_id`\* | `UUID` | The run ID. |
| `tags` | `list[str] | None` | Default:`None`  The tags for the run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The parent run ID. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata for the run. |
| `name` | `str | None` | Default:`None`  The name of the run. |
| `inputs` | `dict[str, Any] | None` | Default:`None`  The inputs for the tool. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


