<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/asimilarity_search_by_vector -->

Methodv1.2.21 (latest)●Since v0.2

# asimilarity\_search\_by\_vector

Async return docs most similar to embedding vector.


```
asimilarity_search_by_vector(
  self,
  embedding: list[float],
  k: int = 4,
  **kwargs: Any = {}
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `embedding`\* | `list[float]` | Embedding to look up documents similar to. |
| `k` | `int` | Default:`4`  Number of `Document` objects to return. |
| `**kwargs` | `Any` | Default:`{}`  Arguments to pass to the search method. |


