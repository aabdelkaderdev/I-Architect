<!-- Source: https://reference.langchain.com/python/langchain-core/retrievers/BaseRetriever/ainvoke -->

Methodv1.2.21 (latest)●Since v0.1

# ainvoke

Asynchronously invoke the retriever to get relevant documents.

Main entry point for asynchronous retriever invocations.


```
ainvoke(
  self,
  input: str,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> list[Document]
```

Examples:

```
await retriever.ainvoke("query")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `str` | The query string. |
| `config` | `RunnableConfig | None` | Default:`None`  Configuration for the retriever. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments to pass to the retriever. |


