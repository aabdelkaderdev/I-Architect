<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/base/BaseLanguageModel/get_num_tokens -->

Methodv1.2.21 (latest)●Since v0.1

# get\_num\_tokens

Get the number of tokens present in the text.

Useful for checking if an input fits in a model's context window.

This should be overridden by model-specific implementations to provide accurate
token counts via model-specific tokenizers.


```
get_num_tokens(
    self,
    text: str,
) -> int
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The string input to tokenize. |


