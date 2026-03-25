<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/afrom_documents -->

Methodv1.2.21 (latest)●Since v0.2

# afrom\_documents

Async return `VectorStore` initialized from documents and embeddings.


```
afrom_documents(
  cls,
  documents: list[Document],
  embedding: Embeddings,
  **kwargs: Any = {}
) -> Self
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `list[Document]` | List of `Document` objects to add to the `VectorStore`. |
| `embedding`\* | `Embeddings` | Embedding function to use. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


