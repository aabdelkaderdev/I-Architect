<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_generation/base/QAGenerationChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a QAGenerationChain from a language model.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  prompt: BasePromptTemplate | None = None,
  **kwargs: Any = {}
) -> QAGenerationChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | a language model |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  a prompt template |
| `**kwargs` | `Any` | Default:`{}`  additional arguments |


