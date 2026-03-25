<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/base/BasePromptTemplate/ainvoke -->

Methodv1.2.21 (latest)●Since v0.1

# ainvoke

Async invoke the prompt.


```
ainvoke(
  self,
  input: dict,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> PromptValue
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `dict` | Input to the prompt. |
| `config` | `RunnableConfig | None` | Default:`None`  Configuration for the prompt. |


