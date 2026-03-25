<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_retriever_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retriever\_start

Run when the retriever starts running.


```
on_retriever_start(
  self,
  serialized: dict[str, Any] | None,
  query: str,
  run_id: UUID | None = None,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> AsyncCallbackManagerForRetrieverRun
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any] | None` | The serialized retriever. |
| `query`\* | `str` | The query. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


