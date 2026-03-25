<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router/embedding_router/EmbeddingRouterChain/from_names_and_descriptions -->

Methodv1.2.13 (latest)●Since v1.0

# from\_names\_and\_descriptions

Convenience constructor.


```
from_names_and_descriptions(
  cls,
  names_and_descriptions: Sequence[tuple[str, Sequence[str]]],
  vectorstore_cls: type[VectorStore],
  embeddings: Embeddings,
  **kwargs: Any = {}
) -> EmbeddingRouterChain
```


