<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/map_rerank/MapRerankDocumentsChain/acombine_docs -->

Methodv1.2.13 (latest)●Since v1.0

# acombine\_docs

Combine documents in a map rerank manner.

Combine by mapping first chain over all documents, then reranking the results.


```
acombine_docs(
  self,
  docs: list[Document],
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> tuple[str, dict]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `docs`\* | `list[Document]` | List of documents to combine |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to be passed through |
| `**kwargs` | `Any` | Default:`{}`  additional parameters to be passed to LLM calls (like other input variables besides the documents) |


