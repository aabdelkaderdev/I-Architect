<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DocumentIndex/adelete -->

Methodv1.2.21 (latest)●Since v0.2

# adelete

Delete by IDs or other criteria. Async variant.

Calling adelete without any input parameters should raise a ValueError!


```
adelete(
  self,
  ids: list[str] | None = None,
  **kwargs: Any = {}
) -> DeleteResponse
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `ids` | `list[str] | None` | Default:`None`  List of IDs to delete. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. This is up to the implementation. For example, can include an option to delete the entire index. |


