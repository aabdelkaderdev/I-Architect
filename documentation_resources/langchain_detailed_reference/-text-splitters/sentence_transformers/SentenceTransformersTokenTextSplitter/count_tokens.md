<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/sentence_transformers/SentenceTransformersTokenTextSplitter/count_tokens -->

Methodv1.1.1 (latest)●Since v0.0

# count\_tokens

Counts the number of tokens in the given text.

This method encodes the input text using a private `_encode` method and
calculates the total number of tokens in the encoded result.


```
count_tokens(
    self,
    *,
    text: str,
) -> int
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The input text for which the token count is calculated. |


