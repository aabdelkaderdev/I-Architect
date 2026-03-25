<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Initialize the PairwiseStringEvalChain from an LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  *,
  prompt: PromptTemplate | None = None,
  criteria: CRITERIA_TYPE | str | None = None,
  **kwargs: Any = {}
) -> PairwiseStringEvalChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The LLM to use (GPT-4 recommended). |
| `prompt` | `PromptTemplate | None` | Default:`None`  The prompt to use. |
| `criteria` | `CRITERIA_TYPE | str | None` | Default:`None`  The criteria to use. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


