<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce/acollapse_docs -->

Functionv1.2.13 (latest)●Since v1.0

# acollapse\_docs

Execute a collapse function on a set of documents and merge their metadatas.


```
acollapse_docs(
  docs: list[Document],
  combine_document_func: AsyncCombineDocsProtocol,
  **kwargs: Any = {}
) -> Document
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `docs`\* | `list[Document]` | A list of `Document` objects to combine. |
| `combine_document_func`\* | `AsyncCombineDocsProtocol` | A function that takes in a list of `Document` objects and optionally addition keyword parameters and combines them into a single string. |
| `**kwargs` | `Any` | Default:`{}`  Arbitrary additional keyword params to pass to the `combine_document_func`. |


