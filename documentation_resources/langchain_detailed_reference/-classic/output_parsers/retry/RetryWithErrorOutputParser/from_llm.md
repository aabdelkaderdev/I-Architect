<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/retry/RetryWithErrorOutputParser/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a RetryWithErrorOutputParser from an LLM.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  parser: BaseOutputParser[T],
  prompt: BasePromptTemplate = NAIVE_RETRY_WITH_ERROR_PROMPT,
  max_retries: int = 1
) -> RetryWithErrorOutputParser[T]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The LLM to use to retry the completion. |
| `parser`\* | `BaseOutputParser[T]` | The parser to use to parse the output. |
| `prompt` | `BasePromptTemplate` | Default:`NAIVE_RETRY_WITH_ERROR_PROMPT`  The prompt to use to retry the completion. |
| `max_retries` | `int` | Default:`1`  The maximum number of times to retry the completion. |


