<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/json/RecursiveJsonSplitter/create_documents -->

Methodv1.1.1 (latest)●Since v0.0

# create\_documents

Create a list of `Document` objects from a list of json objects (`dict`).


```
create_documents(
  self,
  texts: list[dict[str, Any]],
  convert_lists: bool = False,
  ensure_ascii: bool = True,
  metadatas: list[dict[Any, Any]] | None = None
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `texts`\* | `list[dict[str, Any]]` | A list of JSON data to be split and converted into documents. |
| `convert_lists` | `bool` | Default:`False`  Whether to convert lists to dictionaries before splitting. |
| `ensure_ascii` | `bool` | Default:`True`  Whether to ensure ASCII encoding in the JSON strings. |
| `metadatas` | `list[dict[Any, Any]] | None` | Default:`None`  Optional list of metadata to associate with each document. |


