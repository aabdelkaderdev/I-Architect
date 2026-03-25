<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/in_memory/InMemoryVectorStore/max_marginal_relevance_search_by_vector -->

Methodv1.2.21 (latest)●Since v0.2

# max\_marginal\_relevance\_search\_by\_vector


```
max_marginal_relevance_search_by_vector(
  self,
  embedding: list[float],
  k: int = 4,
  fetch_k: int = 20,
  lambda_mult: float = 0.5,
  *,
  filter: Callable[[Document], bool] | None = None,
  **kwargs: Any = {}
) -> list[Document]
```


