<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_retriever_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retriever\_start

Run when the `Retriever` starts running.


```
on_retriever_start(
  self,
  serialized: dict[str, Any],
  query: str,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  name: str | None = None,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized retriever. |
| `query`\* | `str` | The query. |
| `run_id`\* | `UUID` | The run ID. |
| `parent_run_id` | `UUID | None` | Default:`None`  The parent run ID. |
| `tags` | `list[str] | None` | Default:`None`  The tags for the run. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata for the run. |
| `name` | `str | None` | Default:`None`  The name of the run. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


