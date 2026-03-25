<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/scoring/eval_chain/LabeledScoreStringEvalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Initialize the LabeledScoreStringEvalChain from an LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  *,
  prompt: PromptTemplate | None = None,
  criteria: CRITERIA_TYPE | str | None = None,
  normalize_by: float | None = None,
  **kwargs: Any = {}
) -> LabeledScoreStringEvalChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The LLM to use. |
| `prompt` | `PromptTemplate | None` | Default:`None`  The prompt to use. |
| `criteria` | `CRITERIA_TYPE | str | None` | Default:`None`  The criteria to use. |
| `normalize_by` | `float | None` | Default:`None`  The value to normalize the score by. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


