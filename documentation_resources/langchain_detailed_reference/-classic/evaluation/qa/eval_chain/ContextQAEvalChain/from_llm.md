<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/qa/eval_chain/ContextQAEvalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Load QA Eval Chain from LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  prompt: PromptTemplate | None = None,
  **kwargs: Any = {}
) -> ContextQAEvalChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The base language model to use. |
| `prompt` | `PromptTemplate | None` | Default:`None`  A prompt template containing the `input_variables`: `'query'`, `'context'` and `'result'` that will be used as the prompt for evaluation.  Defaults to `PROMPT`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


