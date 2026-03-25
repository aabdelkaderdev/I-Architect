<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/retry/RetryOutputParser/parse_with_prompt -->

Methodv1.2.13 (latest)●Since v1.0

# parse\_with\_prompt

Parse the output of an LLM call using a wrapped parser.


```
parse_with_prompt(
  self,
  completion: str,
  prompt_value: PromptValue
) -> T
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `completion`\* | `str` | The chain completion to parse. |
| `prompt_value`\* | `PromptValue` | The prompt to use to parse the completion. |


