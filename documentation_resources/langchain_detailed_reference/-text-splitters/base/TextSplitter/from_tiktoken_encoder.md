<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/base/TextSplitter/from_tiktoken_encoder -->

Methodv1.1.1 (latest)●Since v0.0

# from\_tiktoken\_encoder

Text splitter that uses `tiktoken` encoder to count length.


```
from_tiktoken_encoder(
  cls,
  encoding_name: str = 'gpt2',
  model_name: str | None = None,
  allowed_special: Literal['all'] | AbstractSet[str] | None = None,
  disallowed_special: Literal['all'] | Collection[str] = 'all',
  **kwargs: Any = {}
) -> Self
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `encoding_name` | `str` | Default:`'gpt2'`  The name of the tiktoken encoding to use. |
| `model_name` | `str | None` | Default:`None`  The name of the model to use.  If provided, this will override the `encoding_name`. |
| `allowed_special` | `Literal['all'] | AbstractSet[str] | None` | Default:`None`  Special tokens that are allowed during encoding. |
| `disallowed_special` | `Literal['all'] | Collection[str]` | Default:`'all'`  Special tokens that are disallowed during encoding. |


