<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DocumentIndex/aupsert -->

Methodv1.2.21 (latest)●Since v0.2

# aupsert

Add or update documents in the `VectorStore`. Async version of `upsert`.

The upsert functionality should utilize the ID field of the item
if it is provided. If the ID is not provided, the upsert method is free
to generate an ID for the item.

When an ID is specified and the item already exists in the `VectorStore`,
the upsert method should update the item with the new data. If the item
does not exist, the upsert method should add the item to the `VectorStore`.


```
aupsert(
  self,
  items: Sequence[Document],
  ,
  **kwargs: Any = {}
) -> UpsertResponse
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `items`\* | `Sequence[Document]` | Sequence of documents to add to the `VectorStore`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


