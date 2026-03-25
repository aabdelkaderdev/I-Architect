<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/flare/base/FlareChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Creates a FlareChain from a language model.


```
from_llm(
  cls,
  llm: BaseLanguageModel | None,
  max_generation_len: int = 32,
  **kwargs: Any = {}
) -> FlareChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel | None` | Language model to use. |
| `max_generation_len` | `int` | Default:`32`  Maximum length of the generated response. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments to pass to the constructor. |


