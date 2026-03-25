<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create an LLMCheckerChain from a language model.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  create_draft_answer_prompt: PromptTemplate = CREATE_DRAFT_ANSWER_PROMPT,
  list_assertions_prompt: PromptTemplate = LIST_ASSERTIONS_PROMPT,
  check_assertions_prompt: PromptTemplate = CHECK_ASSERTIONS_PROMPT,
  revised_answer_prompt: PromptTemplate = REVISED_ANSWER_PROMPT,
  **kwargs: Any = {}
) -> LLMCheckerChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | a language model |
| `create_draft_answer_prompt` | `PromptTemplate` | Default:`CREATE_DRAFT_ANSWER_PROMPT`  prompt to create a draft answer |
| `list_assertions_prompt` | `PromptTemplate` | Default:`LIST_ASSERTIONS_PROMPT`  prompt to list assertions |
| `check_assertions_prompt` | `PromptTemplate` | Default:`CHECK_ASSERTIONS_PROMPT`  prompt to check assertions |
| `revised_answer_prompt` | `PromptTemplate` | Default:`REVISED_ANSWER_PROMPT`  prompt to revise the answer |
| `**kwargs` | `Any` | Default:`{}`  additional arguments |


