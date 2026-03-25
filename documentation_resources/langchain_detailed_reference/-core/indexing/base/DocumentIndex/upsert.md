<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DocumentIndex/upsert -->

Methodv1.2.21 (latest)●Since v0.2

# upsert

Upsert documents into the index.

The upsert functionality should utilize the ID field of the content object
if it is provided. If the ID is not provided, the upsert method is free
to generate an ID for the content.

When an ID is specified and the content already exists in the `VectorStore`,
the upsert method should update the content with the new data. If the content
does not exist, the upsert method should add the item to the `VectorStore`.


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
| `items`\* | `Sequence[Document]` | Sequence of documents to add to the `VectorStore`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


