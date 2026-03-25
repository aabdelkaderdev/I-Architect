<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DocumentIndex/delete -->

Methodv1.2.21 (latest)●Since v0.2

# delete

Delete by IDs or other criteria.

Calling delete without any input parameters should raise a ValueError!


```
delete(
  self,
  ids: list[str] | None = None,
  **kwargs: Any = {}
) -> DeleteResponse
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `ids` | `list[str] | None` | Default:`None`  List of IDs to delete. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. This is up to the implementation. For example, can include an option to delete the entire index, or else issue a non-blocking delete etc. |


