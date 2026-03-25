<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/sentence_transformers/SentenceTransformersTokenTextSplitter/split_text -->

Methodv1.1.1 (latest)●Since v0.0

# split\_text

Splits the input text into smaller components by splitting text on tokens.

This method encodes the input text using a private `_encode` method, then
strips the start and stop token IDs from the encoded result. It returns the
processed segments as a list of strings.


```
split_text(
    self,
    text: str,
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The input text to be split. |


