<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/html/HTMLSectionSplitter/split_html_by_headers -->

Methodv1.1.1 (latest)●Since v0.0

# split\_html\_by\_headers

Split an HTML document into sections based on specified header tags.

This method uses BeautifulSoup to parse the HTML content and divides it into
sections based on headers defined in `headers_to_split_on`. Each section
contains the header text, content under the header, and the tag name.


```
split_html_by_headers(
    self,
    html_doc: str,
) -> list[dict[str, str | None]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `html_doc`\* | `str` | The HTML document to be split into sections. |


