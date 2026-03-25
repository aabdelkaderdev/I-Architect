<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/vectorstore/VectorStoreIndexWrapper/query_with_sources -->

Methodv1.2.13 (latest)●Since v1.0

# query\_with\_sources

Query the `VectorStore` and retrieve the answer along with sources.


```
query_with_sources(
  self,
  question: str,
  llm: BaseLanguageModel | None = None,
  retriever_kwargs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> dict
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `question`\* | `str` | The question or prompt to query. |
| `llm` | `BaseLanguageModel | None` | Default:`None`  The language model to use. Must not be `None`. |
| `retriever_kwargs` | `dict[str, Any] | None` | Default:`None`  Optional keyword arguments for the retriever. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments forwarded to the chain. |


