<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/aget_by_ids -->

Methodv1.2.21 (latest)●Since v0.2

# aget\_by\_ids

Async get documents by their IDs.

The returned documents are expected to have the ID field set to the ID of the
document in the vector store.

Fewer documents may be returned than requested if some IDs are not found or
if there are duplicated IDs.

Users should not assume that the order of the returned documents matches
the order of the input IDs. Instead, users should rely on the ID field of the
returned documents.

This method should **NOT** raise exceptions if no documents are found for
some IDs.


```
aget_by_ids(
    self,
    ids: Sequence[str],
    ,
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `ids`\* | `Sequence[str]` | List of IDs to retrieve. |


