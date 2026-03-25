<!-- Source: https://reference.langchain.com/python/langchain-core/utils/html/extract_sub_links -->

Functionv1.2.21 (latest)●Since v0.1

# extract\_sub\_links

Extract all links from a raw HTML string and convert into absolute paths.


```
extract_sub_links(
  raw_html: str,
  url: str,
  *,
  base_url: str | None = None,
  pattern: str | re.Pattern | None = None,
  prevent_outside: bool = True,
  exclude_prefixes: Sequence[str] = (),
  continue_on_failure: bool = False
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `raw_html`\* | `str` | Original HTML. |
| `url`\* | `str` | The url of the HTML. |
| `base_url` | `str | None` | Default:`None`  the base URL to check for outside links against. |
| `pattern` | `str | re.Pattern | None` | Default:`None`  Regex to use for extracting links from raw HTML. |
| `prevent_outside` | `bool` | Default:`True`  If `True`, ignore external links which are not children of the base URL. |
| `exclude_prefixes` | `Sequence[str]` | Default:`()`  Exclude any URLs that start with one of these prefixes. |
| `continue_on_failure` | `bool` | Default:`False`  If `True`, continue if parsing a specific link raises an exception. Otherwise, raise the exception. |


