<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/create_audio_block -->

Functionv1.2.21 (latest)●Since v1.0

# create\_audio\_block

Create an `AudioContentBlock`.


```
create_audio_block(
  *,
  url: str | None = None,
  base64: str | None = None,
  file_id: str | None = None,
  mime_type: str | None = None,
  id: str | None = None,
  index: int | str | None = None,
  **kwargs: Any = {}
) -> AudioContentBlock
```

The `id` is generated automatically if not provided, using a UUID4 format
prefixed with `'lc_'` to indicate it is a LangChain-generated ID.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `url` | `str | None` | Default:`None`  URL of the audio. |
| `base64` | `str | None` | Default:`None`  Base64-encoded audio data. |
| `file_id` | `str | None` | Default:`None`  ID of the audio file from a file storage system. |
| `mime_type` | `str | None` | Default:`None`  MIME type of the audio.  Required for base64 data. |
| `id` | `str | None` | Default:`None`  Content block identifier.  Generated automatically if not provided. |
| `index` | `int | str | None` | Default:`None`  Index of block in aggregate response.  Used during streaming. |


