<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/CallbackManagerForRetrieverRun/on_retriever_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retriever\_end


```
on_retriever_end(
  self,
  documents: Sequence[Document],
  **kwargs: Any = {}
)
```



->

None

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `Sequence[Document]` |  |
| `**kwargs` | `Any` | Default:`{}` |

Run when retriever ends running.

The retrieved documents.

Additional keyword arguments.