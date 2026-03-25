<!-- Source: https://reference.langchain.com/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/ayield_keys -->

Methodv1.2.13 (latest)●Since v1.0

# ayield\_keys

Async get an iterator over keys that match the given prefix.


```
ayield_keys(
  self,
  *,
  prefix: str | None = None
) -> AsyncIterator[K] | AsyncIterator[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prefix` | `str | None` | Default:`None`  The prefix to match. |


