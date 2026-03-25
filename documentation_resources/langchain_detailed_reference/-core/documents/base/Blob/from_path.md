<!-- Source: https://reference.langchain.com/python/langchain-core/documents/base/Blob/from_path -->

Methodv1.2.21 (latest)●Since v0.2

# from\_path

Load the blob from a path like object.


```
from_path(
  cls,
  path: PathLike,
  *,
  encoding: str = 'utf-8',
  mime_type: str | None = None,
  guess_type: bool = True,
  metadata: dict | None = None
) -> Blob
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `path`\* | `PathLike` | Path-like object to file to be read |
| `encoding` | `str` | Default:`'utf-8'`  Encoding to use if decoding the bytes into a string |
| `mime_type` | `str | None` | Default:`None`  If provided, will be set as the MIME type of the data |
| `guess_type` | `bool` | Default:`True`  If `True`, the MIME type will be guessed from the file extension, if a MIME type was not provided |
| `metadata` | `dict | None` | Default:`None`  Metadata to associate with the `Blob` |


