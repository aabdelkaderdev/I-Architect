<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DocumentIndex/aget -->

Methodv1.2.21 (latest)●Since v0.2

# aget

Get documents by id.

Fewer documents may be returned than requested if some IDs are not found or
if there are duplicated IDs.

Users should not assume that the order of the returned documents matches
the order of the input IDs. Instead, users should rely on the ID field of the
returned documents.

This method should **NOT** raise exceptions if no documents are found for
some IDs.


```
aget(
  self,
  ids: Sequence[str],
  ,
  **kwargs: Any = {}
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `ids`\* | `Sequence[str]` | List of IDs to get. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. These are up to the implementation. |


