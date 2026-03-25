<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/RetrieverManagerMixin/on_retriever_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retriever\_end

Run when `Retriever` ends running.


```
on_retriever_end(
  self,
  documents: Sequence[Document],
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `Sequence[Document]` | The documents retrieved. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


