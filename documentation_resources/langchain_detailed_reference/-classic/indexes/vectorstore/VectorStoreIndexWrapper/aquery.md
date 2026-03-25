<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/vectorstore/VectorStoreIndexWrapper/aquery -->

Methodv1.2.13 (latest)●Since v1.0

# aquery

Asynchronously query the `VectorStore` using the provided LLM.


```
aquery(
  self,
  question: str,
  llm: BaseLanguageModel | None = None,
  retriever_kwargs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `question`\* | `str` | The question or prompt to query. |
| `llm` | `BaseLanguageModel | None` | Default:`None`  The language model to use. Must not be `None`. |
| `retriever_kwargs` | `dict[str, Any] | None` | Default:`None`  Optional keyword arguments for the retriever. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments forwarded to the chain. |


