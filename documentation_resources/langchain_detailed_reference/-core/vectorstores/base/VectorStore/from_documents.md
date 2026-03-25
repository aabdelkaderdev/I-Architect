<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/from_documents -->

Methodv1.2.21 (latest)●Since v0.2

# from\_documents

Return `VectorStore` initialized from documents and embeddings.


```
from_documents(
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


