<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/create_citation -->

Functionv1.2.21 (latest)●Since v1.0

# create\_citation

Create a `Citation`.


```
create_citation(
  *,
  url: str | None = None,
  title: str | None = None,
  start_index: int | None = None,
  end_index: int | None = None,
  cited_text: str | None = None,
  id: str | None = None,
  **kwargs: Any = {}
) -> Citation
```

The `id` is generated automatically if not provided, using a UUID4 format
prefixed with `'lc_'` to indicate it is a LangChain-generated ID.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `url` | `str | None` | Default:`None`  URL of the document source. |
| `title` | `str | None` | Default:`None`  Source document title. |
| `start_index` | `int | None` | Default:`None`  Start index in the response text where citation applies. |
| `end_index` | `int | None` | Default:`None`  End index in the response text where citation applies. |
| `cited_text` | `str | None` | Default:`None`  Excerpt of source text being cited. |
| `id` | `str | None` | Default:`None`  Content block identifier.  Generated automatically if not provided. |


