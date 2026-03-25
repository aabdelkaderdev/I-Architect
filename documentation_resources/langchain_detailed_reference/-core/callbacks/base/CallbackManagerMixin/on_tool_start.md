<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_start

Run when the tool starts running.


```
on_tool_start(
  self,
  serialized: dict[str, Any],
  input_str: str,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  inputs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized chain. |
| `input_str`\* | `str` | The input string. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata. |
| `inputs` | `dict[str, Any] | None` | Default:`None`  The inputs. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


