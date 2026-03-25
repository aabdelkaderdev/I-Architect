<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/vectorstore/VectorstoreIndexCreator/afrom_loaders -->

Methodv1.2.13 (latest)●Since v1.0

# afrom\_loaders

Asynchronously create a `VectorStore` index from a list of loaders.


```
afrom_loaders(
    self,
    loaders: list[BaseLoader],
) -> VectorStoreIndexWrapper
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `loaders`\* | `list[BaseLoader]` | A list of `BaseLoader` instances to load documents. |


