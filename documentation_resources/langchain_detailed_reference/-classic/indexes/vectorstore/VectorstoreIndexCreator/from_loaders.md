<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/vectorstore/VectorstoreIndexCreator/from_loaders -->

Methodv1.2.13 (latest)●Since v1.0

# from\_loaders

Create a `VectorStore` index from a list of loaders.


```
from_loaders(
    self,
    loaders: list[BaseLoader],
) -> VectorStoreIndexWrapper
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `loaders`\* | `list[BaseLoader]` | A list of `BaseLoader` instances to load documents. |


