<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/asimilarity_search_with_relevance_scores -->

Methodv1.2.21 (latest)●Since v0.2

# asimilarity\_search\_with\_relevance\_scores

Async return docs and relevance scores in the range `[0, 1]`.

`0` is dissimilar, `1` is most similar.


```
asimilarity_search_with_relevance_scores(
  self,
  query: str,
  k: int = 4,
  **kwargs: Any = {}
) -> list[tuple[Document, float]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | Input text. |
| `k` | `int` | Default:`4`  Number of `Document` objects to return. |
| `**kwargs` | `Any` | Default:`{}`  Kwargs to be passed to similarity search.  Should include `score_threshold`, an optional floating point value between `0` to `1` to filter the resulting set of retrieved docs. |


