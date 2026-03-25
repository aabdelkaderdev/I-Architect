<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter/create_documents -->

Methodv1.1.1 (latest)●Since v0.0

# create\_documents

Create a list of `Document` objects from a list of texts.


```
create_documents(
  self,
  texts: list[str],
  metadatas: list[dict[Any, Any]] | None = None
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `texts`\* | `list[str]` | A list of texts to be split and converted into documents. |
| `metadatas` | `list[dict[Any, Any]] | None` | Default:`None`  Optional list of metadata to associate with each document. |


