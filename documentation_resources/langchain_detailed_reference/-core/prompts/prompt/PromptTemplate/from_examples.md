<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/prompt/PromptTemplate/from_examples -->

Methodv1.2.21 (latest)●Since v0.1

# from\_examples

Take examples in list format with prefix and suffix to create a prompt.

Intended to be used as a way to dynamically create a prompt from examples.


```
from_examples(
  cls,
  examples: list[str],
  suffix: str,
  input_variables: list[str],
  example_separator: str = '\n\n',
  prefix: str = '',
  **kwargs: Any = {}
) -> PromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `examples`\* | `list[str]` | List of examples to use in the prompt. |
| `suffix`\* | `str` | String to go after the list of examples.  Should generally set up the user's input. |
| `input_variables`\* | `list[str]` | A list of variable names the final prompt template will expect. |
| `example_separator` | `str` | Default:`'\n\n'`  The separator to use in between examples. |
| `prefix` | `str` | Default:`''`  String that should go before any examples.  Generally includes examples. |


