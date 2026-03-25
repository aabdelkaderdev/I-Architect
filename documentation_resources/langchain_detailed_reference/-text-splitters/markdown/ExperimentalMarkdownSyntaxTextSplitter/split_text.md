<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/markdown/ExperimentalMarkdownSyntaxTextSplitter/split_text -->

Methodv1.1.1 (latest)●Since v0.2

# split\_text

Split the input text into structured chunks.

This method processes the input text line by line, identifying and handling
specific patterns such as headers, code blocks, and horizontal rules to split it
into structured chunks based on headers, code blocks, and horizontal rules.


```
split_text(
    self,
    text: str,
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The input text to be split into chunks. |


