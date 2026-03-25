<!-- Source: https://reference.langchain.com/python/langchain-core/utils/html/find_all_links -->

Functionv1.2.21 (latest)●Since v0.1

# find\_all\_links

Extract all links from a raw HTML string.


```
find_all_links(
  raw_html: str,
  *,
  pattern: str | re.Pattern | None = None
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `raw_html`\* | `str` | original HTML. |
| `pattern` | `str | re.Pattern | None` | Default:`None`  Regex to use for extracting links from raw HTML. |


