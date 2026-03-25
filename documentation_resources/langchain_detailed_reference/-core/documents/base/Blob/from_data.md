<!-- Source: https://reference.langchain.com/python/langchain-core/documents/base/Blob/from_data -->

Methodv1.2.21 (latest)●Since v0.2

# from\_data

Initialize the `Blob` from in-memory data.


```
from_data(
  cls,
  data: str | bytes,
  *,
  encoding: str = 'utf-8',
  mime_type: str | None = None,
  path: str | None = None,
  metadata: dict | None = None
) -> Blob
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `data`\* | `str | bytes` | The in-memory data associated with the `Blob` |
| `encoding` | `str` | Default:`'utf-8'`  Encoding to use if decoding the bytes into a string |
| `mime_type` | `str | None` | Default:`None`  If provided, will be set as the MIME type of the data |
| `path` | `str | None` | Default:`None`  If provided, will be set as the source from which the data came |
| `metadata` | `dict | None` | Default:`None`  Metadata to associate with the `Blob` |


