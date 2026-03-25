<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever/aadd_documents -->

Methodv1.2.13 (latest)●Since v1.0

# aadd\_documents

Adds documents to the docstore and vectorstores.


```
aadd_documents(
  self,
  documents: list[Document],
  ids: list[str] | None = None,
  add_to_docstore: bool = True,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `list[Document]` | List of documents to add |
| `ids` | `list[str] | None` | Default:`None`  Optional list of IDs for documents. If provided should be the same length as the list of documents. Can be provided if parent documents are already in the document store and you don't want to re-add to the docstore. If not provided, random UUIDs will be used as idIDss. |
| `add_to_docstore` | `bool` | Default:`True`  Boolean of whether to add documents to docstore. This can be false if and only if `ids` are provided. You may want to set this to False if the documents are already in the docstore and you don't want to re-add them. |
| `**kwargs` | `Any` | Default:`{}`  additional keyword arguments passed to the `VectorStore`. |


