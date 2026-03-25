<!-- Source: https://reference.langchain.com/python/langchain-core/retrievers/BaseRetriever/invoke -->

Methodv1.2.21 (latest)●Since v0.1

# invoke

Invoke the retriever to get relevant documents.

Main entry point for synchronous retriever invocations.


```
invoke(
  self,
  input: str,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> list[Document]
```

Examples:

```
retriever.invoke("query")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `str` | The query string. |
| `config` | `RunnableConfig | None` | Default:`None`  Configuration for the retriever. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments to pass to the retriever. |


