<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/retry/RetryOutputParser/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create an RetryOutputParser from a language model and a parser.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  parser: BaseOutputParser[T],
  prompt: BasePromptTemplate = NAIVE_RETRY_PROMPT,
  max_retries: int = 1
) -> RetryOutputParser[T]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | llm to use for fixing |
| `parser`\* | `BaseOutputParser[T]` | parser to use for parsing |
| `prompt` | `BasePromptTemplate` | Default:`NAIVE_RETRY_PROMPT`  prompt to use for fixing |
| `max_retries` | `int` | Default:`1`  Maximum number of retries to parse. |


