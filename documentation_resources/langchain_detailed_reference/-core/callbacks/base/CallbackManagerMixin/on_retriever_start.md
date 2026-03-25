<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start -->

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
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized `Retriever`. |
| `query`\* | `str` | The query. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


