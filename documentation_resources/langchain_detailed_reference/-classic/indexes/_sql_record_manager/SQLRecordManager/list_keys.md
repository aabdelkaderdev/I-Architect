<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager/list_keys -->

Methodv1.2.13 (latest)●Since v1.0

# list\_keys

List records in the SQLite database based on the provided date range.


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


