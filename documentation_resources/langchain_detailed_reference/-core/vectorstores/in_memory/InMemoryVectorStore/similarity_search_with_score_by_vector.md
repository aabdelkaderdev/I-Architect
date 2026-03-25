<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/in_memory/InMemoryVectorStore/similarity_search_with_score_by_vector -->

Methodv1.2.21 (latest)●Since v0.2

# similarity\_search\_with\_score\_by\_vector

Search for the most similar documents to the given embedding.


```
similarity_search_with_score_by_vector(
  self,
  embedding: list[float],
  k: int = 4,
  filter: Callable[[Document], bool] | None = None,
  **_kwargs: Any = {}
) -> list[tuple[Document, float]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `embedding`\* | `list[float]` | The embedding to search for. |
| `k` | `int` | Default:`4`  The number of documents to return. |
| `filter` | `Callable[[Document], bool] | None` | Default:`None`  A function to filter the documents. |


