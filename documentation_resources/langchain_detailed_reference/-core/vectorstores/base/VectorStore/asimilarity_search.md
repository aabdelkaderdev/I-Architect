<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/asimilarity_search -->

Methodv1.2.21 (latest)●Since v0.2

# asimilarity\_search

Async return docs most similar to query.


```
asimilarity_search(
  self,
  query: str,
  k: int = 4,
  **kwargs: Any = {}
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | Input text. |
| `k` | `int` | Default:`4`  Number of `Document` objects to return. |
| `**kwargs` | `Any` | Default:`{}`  Arguments to pass to the search method. |


