<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/RecordManager/list_keys -->

Methodv1.2.21 (latest)●Since v0.1

# list\_keys

List records in the database based on the provided filters.


```
list_keys(
  self,
  *,
  before: float | None = None,
  after: float | None = None,
  group_ids: Sequence[str] | None = None,
  limit: int | None = None
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `before` | `float | None` | Default:`None`  Filter to list records updated before this time. |
| `after` | `float | None` | Default:`None`  Filter to list records updated after this time. |
| `group_ids` | `Sequence[str] | None` | Default:`None`  Filter to list records with specific group IDs. |
| `limit` | `int | None` | Default:`None`  optional limit on the number of records to return. |


