<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_chain_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_start

Start a trace for a chain run.


```
on_chain_start(
  self,
  serialized: dict[str, Any],
  inputs: dict[str, Any],
  *,
  run_id: UUID,
  tags: list[str] | None = None,
  parent_run_id: UUID | None = None,
  metadata: dict[str, Any] | None = None,
  run_type: str | None = None,
  name: str | None = None,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized chain. |
| `inputs`\* | `dict[str, Any]` | The inputs for the chain. |
| `run_id`\* | `UUID` | The run ID. |
| `tags` | `list[str] | None` | Default:`None`  The tags for the run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The parent run ID. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata for the run. |
| `run_type` | `str | None` | Default:`None`  The type of the run. |
| `name` | `str | None` | Default:`None`  The name of the run. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


