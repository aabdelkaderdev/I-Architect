<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce/ReduceDocumentsChain/acombine_docs -->

Methodv1.2.13 (latest)●Since v1.0

# acombine\_docs

Async combine multiple documents recursively.


```
acombine_docs(
  self,
  docs: list[Document],
  token_max: int | None = None,
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> tuple[str, dict]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `docs`\* | `list[Document]` | List of documents to combine, assumed that each one is less than `token_max`. |
| `token_max` | `int | None` | Default:`None`  Recursively creates groups of documents less than this number of tokens. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to be passed through |
| `**kwargs` | `Any` | Default:`{}`  additional parameters to be passed to LLM calls (like other input variables besides the documents) |


