<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/aupdate -->

Methodv1.2.13 (latest)●Since v1.0

# aupdate

Upsert records into the SQLite database.


```
aupdate(
  self,
  keys: Sequence[str],
  *,
  group_ids: Sequence[str | None] | None = None,
  time_at_least: float | None = None
) -> None
```


