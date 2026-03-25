<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/create_reasoning_block -->

Functionv1.2.21 (latest)●Since v1.0

# create\_reasoning\_block

Create a `ReasoningContentBlock`.


```
create_reasoning_block(
  reasoning: str | None = None,
  id: str | None = None,
  index: int | str | None = None,
  **kwargs: Any = {}
) -> ReasoningContentBlock
```

The `id` is generated automatically if not provided, using a UUID4 format
prefixed with `'lc_'` to indicate it is a LangChain-generated ID.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `reasoning` | `str | None` | Default:`None`  The reasoning text or thought summary. |
| `id` | `str | None` | Default:`None`  Content block identifier.  Generated automatically if not provided. |
| `index` | `int | str | None` | Default:`None`  Index of block in aggregate response.  Used during streaming. |


