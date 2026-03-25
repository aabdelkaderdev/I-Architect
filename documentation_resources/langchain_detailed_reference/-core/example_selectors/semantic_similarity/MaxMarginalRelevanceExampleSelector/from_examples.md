<!-- Source: https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector/from_examples -->

Methodv1.2.21 (latest)●Since v0.1

# from\_examples

Create k-shot example selector using example list and embeddings.

Reshuffles examples dynamically based on Max Marginal Relevance.


```
from_examples(
  cls,
  examples: list[dict],
  embeddings: Embeddings,
  vectorstore_cls: type[VectorStore],
  k: int = 4,
  input_keys: list[str] | None = None,
  fetch_k: int = 20,
  example_keys: list[str] | None = None,
  vectorstore_kwargs: dict | None = None,
  **vectorstore_cls_kwargs: Any = {}
) -> MaxMarginalRelevanceExampleSelector
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `examples`\* | `list[dict]` | List of examples to use in the prompt. |
| `embeddings`\* | `Embeddings` | An initialized embedding API interface, e.g. OpenAIEmbeddings(). |
| `vectorstore_cls`\* | `type[VectorStore]` | A vector store DB interface class, e.g. FAISS. |
| `k` | `int` | Default:`4`  Number of examples to select. |
| `fetch_k` | `int` | Default:`20`  Number of `Document` objects to fetch to pass to MMR algorithm. |
| `input_keys` | `list[str] | None` | Default:`None`  If provided, the search is based on the input variables instead of all variables. |
| `example_keys` | `list[str] | None` | Default:`None`  If provided, keys to filter examples to. |
| `vectorstore_kwargs` | `dict | None` | Default:`None`  Extra arguments passed to similarity\_search function of the `VectorStore`. |
| `vectorstore_cls_kwargs` | `Any` | Default:`{}`  optional kwargs containing url for vector store |


