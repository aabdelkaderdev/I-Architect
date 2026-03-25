<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/asearch -->

Methodv1.2.21 (latest)●Since v0.2

# asearch

Async return docs most similar to query using a specified search type.


```
asearch(
  self,
  query: str,
  search_type: str,
  **kwargs: Any = {}
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | Input text. |
| `search_type`\* | `str` | Type of search to perform.  Can be `'similarity'`, `'mmr'`, or `'similarity_score_threshold'`. |
| `**kwargs` | `Any` | Default:`{}`  Arguments to pass to the search method. |


