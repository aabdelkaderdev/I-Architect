<!-- Source: https://reference.langchain.com/python/langchain-classic/model_laboratory/ModelLaboratory/from_llms -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llms

Initialize the ModelLaboratory with LLMs and an optional prompt.


```
from_llms(
  cls,
  llms: list[BaseLLM],
  prompt: PromptTemplate | None = None
) -> ModelLaboratory
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llms`\* | `list[BaseLLM]` | A list of LLMs to experiment with. |
| `prompt` | `PromptTemplate | None` | Default:`None`  An optional prompt to use with the LLMs. If provided, the prompt must contain exactly one input variable. |


