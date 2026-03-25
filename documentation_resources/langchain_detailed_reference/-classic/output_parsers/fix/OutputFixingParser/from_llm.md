<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/fix/OutputFixingParser/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create an OutputFixingParser from a language model and a parser.


```
from_llm(
  cls,
  llm: Runnable,
  parser: BaseOutputParser[T],
  prompt: BasePromptTemplate = NAIVE_FIX_PROMPT,
  max_retries: int = 1
) -> OutputFixingParser[T]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `Runnable` | llm to use for fixing |
| `parser`\* | `BaseOutputParser[T]` | parser to use for parsing |
| `prompt` | `BasePromptTemplate` | Default:`NAIVE_FIX_PROMPT`  prompt to use for fixing |
| `max_retries` | `int` | Default:`1`  Maximum number of retries to parse. |


