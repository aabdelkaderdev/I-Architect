<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/base/BaseCombineDocumentsChain/combine_docs -->

Methodv1.2.13 (latest)●Since v1.0

# combine\_docs

Combine documents into a single string.


```
combine_docs(
  self,
  docs: list[Document],
  **kwargs: Any = {}
) -> tuple[str, dict]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `docs`\* | `list[Document]` | List[Document], the documents to combine |
| `**kwargs` | `Any` | Default:`{}`  Other parameters to use in combining documents, often other inputs to the prompt. |


