<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes/_sql_record_manager/UpsertionRecord/uuid -->

Attributev1.2.13 (latest)●Since v1.0

# uuid


```
uuid = Column(
  String,
  index=True,
  default=(lambda: str(uuid.uuid4())),
  primary_key=True,
  nullable=False
)
```


