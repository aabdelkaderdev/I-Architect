<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/adelete -->

Methodv1.2.21 (latest)●Since v0.2

# adelete

Async delete by vector ID or other criteria.


```
adelete(
  self,
  ids: list[str] | None = None,
  **kwargs: Any = {}
) -> bool | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `ids` | `list[str] | None` | Default:`None`  List of IDs to delete. If `None`, delete all. |
| `**kwargs` | `Any` | Default:`{}`  Other keyword arguments that subclasses might use. |


