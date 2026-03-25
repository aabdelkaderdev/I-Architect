<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/create_non_standard_block -->

Functionv1.2.21 (latest)●Since v1.0

# create\_non\_standard\_block

Create a `NonStandardContentBlock`.


```
create_non_standard_block(
  value: dict[str, Any],
  *,
  id: str | None = None,
  index: int | str | None = None
) -> NonStandardContentBlock
```

The `id` is generated automatically if not provided, using a UUID4 format
prefixed with `'lc_'` to indicate it is a LangChain-generated ID.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `value`\* | `dict[str, Any]` | Provider-specific content data. |
| `id` | `str | None` | Default:`None`  Content block identifier.  Generated automatically if not provided. |
| `index` | `int | str | None` | Default:`None`  Index of block in aggregate response.  Used during streaming. |


