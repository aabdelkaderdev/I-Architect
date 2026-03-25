<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/update -->

Methodv1.2.13 (latest)●Since v1.0

# update

Upsert records into the SQLite database.


```
update(
  self,
  keys: Sequence[str],
  *,
  group_ids: Sequence[str | None] | None = None,
  time_at_least: float | None = None
) -> None
```


