<!-- Source: https://reference.langchain.com/python/langchain-core/documents/base/BaseMedia/id -->

Attributev1.2.21 (latest)●Since v0.2

# id

An optional identifier for the document.

Ideally this should be unique across the document collection and formatted
as a UUID, but this will not be enforced.


```
id: str | None = Field(default=None, coerce_numbers_to_str=True)
```


