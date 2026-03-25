<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/add_documents -->

Methodv1.2.21 (latest)●Since v0.2

# add\_documents

Add or update documents in the `VectorStore`.


```
add_documents(
  self,
  documents: list[Document],
  **kwargs: Any = {}
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `documents`\* | `list[Document]` | Documents to add to the `VectorStore`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments.  If kwargs contains IDs and documents contain ids, the IDs in the kwargs will receive precedence. |


