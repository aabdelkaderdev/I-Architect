<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/create_plaintext_block -->

Functionv1.2.21 (latest)●Since v1.0

# create\_plaintext\_block

Create a `PlainTextContentBlock`.


```
create_plaintext_block(
  text: str | None = None,
  url: str | None = None,
  base64: str | None = None,
  file_id: str | None = None,
  title: str | None = None,
  context: str | None = None,
  id: str | None = None,
  index: int | str | None = None,
  **kwargs: Any = {}
) -> PlainTextContentBlock
```

The `id` is generated automatically if not provided, using a UUID4 format
prefixed with `'lc_'` to indicate it is a LangChain-generated ID.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text` | `str | None` | Default:`None`  The plaintext content. |
| `url` | `str | None` | Default:`None`  URL of the plaintext file. |
| `base64` | `str | None` | Default:`None`  Base64-encoded plaintext data. |
| `file_id` | `str | None` | Default:`None`  ID of the plaintext file from a file storage system. |
| `title` | `str | None` | Default:`None`  Title of the text data. |
| `context` | `str | None` | Default:`None`  Context or description of the text content. |
| `id` | `str | None` | Default:`None`  Content block identifier.  Generated automatically if not provided. |
| `index` | `int | str | None` | Default:`None`  Index of block in aggregate response.  Used during streaming. |


