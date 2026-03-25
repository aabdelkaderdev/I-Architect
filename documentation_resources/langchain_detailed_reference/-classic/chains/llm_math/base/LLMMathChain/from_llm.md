<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_math/base/LLMMathChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a LLMMathChain from a language model.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  prompt: BasePromptTemplate = PROMPT,
  **kwargs: Any = {}
) -> LLMMathChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | a language model |
| `prompt` | `BasePromptTemplate` | Default:`PROMPT`  a prompt template |
| `**kwargs` | `Any` | Default:`{}`  additional arguments |


