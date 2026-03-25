<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/in_memory/InMemoryDocumentIndex/upsert -->

Methodv1.2.21 (latest)●Since v0.2

# upsert

Upsert documents into the index.


```
upsert(
  self,
  items: Sequence[Document],
  ,
  **kwargs: Any = {}
) -> UpsertResponse
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `items`\* | `Sequence[Document]` | Sequence of documents to add to the index. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


