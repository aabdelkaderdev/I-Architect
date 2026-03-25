<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_summarization_checker/base/LLMSummarizationCheckerChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a LLMSummarizationCheckerChain from a language model.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  create_assertions_prompt: PromptTemplate = CREATE_ASSERTIONS_PROMPT,
  check_assertions_prompt: PromptTemplate = CHECK_ASSERTIONS_PROMPT,
  revised_summary_prompt: PromptTemplate = REVISED_SUMMARY_PROMPT,
  are_all_true_prompt: PromptTemplate = ARE_ALL_TRUE_PROMPT,
  verbose: bool = False,
  **kwargs: Any = {}
) -> LLMSummarizationCheckerChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | a language model |
| `create_assertions_prompt` | `PromptTemplate` | Default:`CREATE_ASSERTIONS_PROMPT`  prompt to create assertions |
| `check_assertions_prompt` | `PromptTemplate` | Default:`CHECK_ASSERTIONS_PROMPT`  prompt to check assertions |
| `revised_summary_prompt` | `PromptTemplate` | Default:`REVISED_SUMMARY_PROMPT`  prompt to revise summary |
| `are_all_true_prompt` | `PromptTemplate` | Default:`ARE_ALL_TRUE_PROMPT`  prompt to check if all assertions are true |
| `verbose` | `bool` | Default:`False`  whether to print verbose output |
| `**kwargs` | `Any` | Default:`{}`  additional arguments |


