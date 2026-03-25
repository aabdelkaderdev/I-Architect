<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/scoring/eval_chain/ScoreStringEvalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Initialize the ScoreStringEvalChain from an LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  *,
  prompt: PromptTemplate | None = None,
  criteria: CRITERIA_TYPE | str | None = None,
  normalize_by: float | None = None,
  **kwargs: Any = {}
) -> ScoreStringEvalChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The LLM to use (GPT-4 recommended). |
| `prompt` | `PromptTemplate | None` | Default:`None`  The prompt to use. |
| `criteria` | `CRITERIA_TYPE | str | None` | Default:`None`  The criteria to use. |
| `normalize_by` | `float | None` | Default:`None`  The value to normalize the score by. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


