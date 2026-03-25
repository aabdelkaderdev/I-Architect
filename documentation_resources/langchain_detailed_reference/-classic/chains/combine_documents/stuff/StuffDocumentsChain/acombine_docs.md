<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/stuff/StuffDocumentsChain/acombine_docs -->

Methodv1.2.13 (latest)●Since v1.0

# acombine\_docs

Async stuff all documents into one prompt and pass to LLM.


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
| `docs`\* | `list[Document]` | List of documents to join together into one variable |
| `callbacks` | `Callbacks` | Default:`None`  Optional callbacks to pass along |
| `**kwargs` | `Any` | Default:`{}`  additional parameters to use to get inputs to LLMChain. |


