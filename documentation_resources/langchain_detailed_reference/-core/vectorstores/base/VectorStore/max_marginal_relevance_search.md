<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/max_marginal_relevance_search -->

Methodv1.2.21 (latest)●Since v0.2

# max\_marginal\_relevance\_search

Return docs selected using the maximal marginal relevance.

Maximal marginal relevance optimizes for similarity to query AND diversity
among selected documents.


```
max_marginal_relevance_search(
  self,
  query: str,
  k: int = 4,
  fetch_k: int = 20,
  lambda_mult: float = 0.5,
  **kwargs: Any = {}
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | Text to look up documents similar to. |
| `k` | `int` | Default:`4`  Number of `Document` objects to return. |
| `fetch_k` | `int` | Default:`20`  Number of `Document` objects to fetch to pass to MMR algorithm. |
| `lambda_mult` | `float` | Default:`0.5`  Number between `0` and `1` that determines the degree of diversity among the results with `0` corresponding to maximum diversity and `1` to minimum diversity. |
| `**kwargs` | `Any` | Default:`{}`  Arguments to pass to the search method. |


