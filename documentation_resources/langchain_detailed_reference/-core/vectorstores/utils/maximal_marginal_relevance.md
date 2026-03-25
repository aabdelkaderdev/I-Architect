<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/utils/maximal_marginal_relevance -->

Functionv1.2.21 (latest)●Since v0.2

# maximal\_marginal\_relevance

Calculate maximal marginal relevance.


```
maximal_marginal_relevance(
  query_embedding: np.ndarray,
  embedding_list: list,
  lambda_mult: float = 0.5,
  k: int = 4
) -> list[int]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query_embedding`\* | `np.ndarray` | The query embedding. |
| `embedding_list`\* | `list` | A list of embeddings. |
| `lambda_mult` | `float` | Default:`0.5`  The lambda parameter for MMR. |
| `k` | `int` | Default:`4`  The number of embeddings to return. |


