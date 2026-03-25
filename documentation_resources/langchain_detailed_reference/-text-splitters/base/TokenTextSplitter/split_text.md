<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/base/TokenTextSplitter/split_text -->

Methodv1.1.1 (latest)●Since v0.0

# split\_text

Splits the input text into smaller chunks based on tokenization.

This method uses a custom tokenizer configuration to encode the input text
into tokens, processes the tokens in chunks of a specified size with overlap,
and decodes them back into text chunks. The splitting is performed using the
`split_text_on_tokens` function.


```
split_text(
    self,
    text: str,
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The input text to be split into smaller chunks. |


