<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/html/HTMLHeaderTextSplitter/split_text_from_file -->

Methodv1.1.1 (latest)●Since v0.0

# split\_text\_from\_file

Split HTML content from a file into a list of `Document` objects.


```
split_text_from_file(
    self,
    file: str | IO[str],
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `file`\* | `str | IO[str]` | A file path or a file-like object containing HTML content. |


