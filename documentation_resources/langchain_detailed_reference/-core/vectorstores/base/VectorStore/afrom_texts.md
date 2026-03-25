<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/afrom_texts -->

Methodv1.2.21 (latest)●Since v0.2

# afrom\_texts

Async return `VectorStore` initialized from texts and embeddings.


```
afrom_texts(
  cls,
  texts: list[str],
  embedding: Embeddings,
  metadatas: list[dict] | None = None,
  *,
  ids: list[str] | None = None,
  **kwargs: Any = {}
) -> Self
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `texts`\* | `list[str]` | Texts to add to the `VectorStore`. |
| `embedding`\* | `Embeddings` | Embedding function to use. |
| `metadatas` | `list[dict] | None` | Default:`None`  Optional list of metadatas associated with the texts. |
| `ids` | `list[str] | None` | Default:`None`  Optional list of IDs associated with the texts. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


