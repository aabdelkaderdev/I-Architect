<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_retriever_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retriever\_end

Run when the `Retriever` ends running.


```
on_retriever_end(
  self,
  documents: Sequence[Document],
  *,
  run_id: UUID,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `Sequence[Document]` | The documents. |
| `run_id`\* | `UUID` | The run ID. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


