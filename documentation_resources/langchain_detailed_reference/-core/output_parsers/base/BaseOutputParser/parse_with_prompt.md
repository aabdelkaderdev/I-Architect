<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/base/BaseOutputParser/parse_with_prompt -->

Methodv1.2.21 (latest)●Since v0.1

# parse\_with\_prompt

Parse the output of an LLM call with the input prompt for context.

The prompt is largely provided in the event the `OutputParser` wants to retry or
fix the output in some way, and needs information from the prompt to do so.


```
parse_with_prompt(
  self,
  completion: str,
  prompt: PromptValue
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `completion`\* | `str` | String output of a language model. |
| `prompt`\* | `PromptValue` | Input `PromptValue`. |


