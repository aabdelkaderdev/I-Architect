<!-- Source: https://reference.langchain.com/python/langchain-core/stores/InMemoryBaseStore/ayield_keys -->

Methodv1.2.21 (latest)●Since v0.1

# ayield\_keys

Async get an async iterator over keys that match the given prefix.


```
ayield_keys(
  self,
  *,
  prefix: str | None = None
) -> AsyncIterator[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prefix` | `str | None` | Default:`None`  The prefix to match. |


