<!-- Source: https://reference.langchain.com/python/langchain-classic/storage/encoder_backed/EncoderBackedStore/yield_keys -->

Methodv1.2.13 (latest)●Since v1.0

# yield\_keys

Get an iterator over keys that match the given prefix.


```
yield_keys(
  self,
  *,
  prefix: str | None = None
) -> Iterator[K] | Iterator[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prefix` | `str | None` | Default:`None`  The prefix to match. |


