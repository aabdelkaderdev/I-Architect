<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/create_text_block -->

Functionv1.2.21 (latest)●Since v1.0

# create\_text\_block

Create a `TextContentBlock`.


```
create_text_block(
  text: str,
  *,
  id: str | None = None,
  annotations: list[Annotation] | None = None,
  index: int | str | None = None,
  **kwargs: Any = {}
) -> TextContentBlock
```

The `id` is generated automatically if not provided, using a UUID4 format
prefixed with `'lc_'` to indicate it is a LangChain-generated ID.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text content of the block. |
| `id` | `str | None` | Default:`None`  Content block identifier.  Generated automatically if not provided. |
| `annotations` | `list[Annotation] | None` | Default:`None`  `Citation`s and other annotations for the text. |
| `index` | `int | str | None` | Default:`None`  Index of block in aggregate response.  Used during streaming. |


