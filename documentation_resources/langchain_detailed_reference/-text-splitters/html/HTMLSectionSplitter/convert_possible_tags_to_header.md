<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/html/HTMLSectionSplitter/convert_possible_tags_to_header -->

Methodv1.1.1 (latest)●Since v0.0

# convert\_possible\_tags\_to\_header

Convert specific HTML tags to headers using an XSLT transformation.

This method uses an XSLT file to transform the HTML content, converting
certain tags into headers for easier parsing. If no XSLT path is provided,
the HTML content is returned unchanged.


```
convert_possible_tags_to_header(
    self,
    html_content: str,
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `html_content`\* | `str` | The HTML content to be transformed. |


