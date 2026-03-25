<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/aadd_texts -->

Methodv1.2.21 (latest)●Since v0.2

# aadd\_texts

Async run more texts through the embeddings and add to the `VectorStore`.


```
aadd_texts(
  self,
  texts: Iterable[str],
  metadatas: list[dict] | None = None,
  *,
  ids: list[str] | None = None,
  **kwargs: Any = {}
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `texts`\* | `Iterable[str]` | Iterable of strings to add to the `VectorStore`. |
| `metadatas` | `list[dict] | None` | Default:`None`  Optional list of metadatas associated with the texts. |
| `ids` | `list[str] | None` | Default:`None`  Optional list |
| `**kwargs` | `Any` | Default:`{}`  `VectorStore` specific parameters. |


