<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter/from_huggingface_tokenizer -->

Methodv1.1.1 (latest)●Since v0.0

# from\_huggingface\_tokenizer


```
from_huggingface_tokenizer(
  cls,
  tokenizer: PreTrainedTokenizerBase,
  **kwargs: Any = {}
) -> TextSplitter
```



## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tokenizer`\* | `PreTrainedTokenizerBase` |  |

Text splitter that uses Hugging Face tokenizer to count length.

The Hugging Face tokenizer to use.