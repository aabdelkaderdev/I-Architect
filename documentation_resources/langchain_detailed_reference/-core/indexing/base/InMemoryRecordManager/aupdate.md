<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/InMemoryRecordManager/aupdate -->

Methodv1.2.21 (latest)●Since v0.2

# aupdate

Async upsert records into the database.


```
aupdate(
  self,
  keys: Sequence[str],
  *,
  group_ids: Sequence[str | None] | None = None,
  time_at_least: float | None = None
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `keys`\* | `Sequence[str]` | A list of record keys to upsert. |
| `group_ids` | `Sequence[str | None] | None` | Default:`None`  A list of group IDs corresponding to the keys. |
| `time_at_least` | `float | None` | Default:`None`  Optional timestamp. Implementation can use this to optionally verify that the timestamp IS at least this time in the system that stores. E.g., use to validate that the time in the postgres database is equal to or larger than the given timestamp, if not raise an error. This is meant to help prevent time-drift issues since time may not be monotonically increasing! |


