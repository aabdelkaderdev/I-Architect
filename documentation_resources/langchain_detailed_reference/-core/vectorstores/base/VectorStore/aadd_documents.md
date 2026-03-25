<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/aadd_documents -->

Methodv1.2.21 (latest)●Since v0.2

# aadd\_documents

Async run more documents through the embeddings and add to the `VectorStore`.


```
aadd_documents(
  self,
  documents: list[Document],
  **kwargs: Any = {}
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `list[Document]` | Documents to add to the `VectorStore`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


