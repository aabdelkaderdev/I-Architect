<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/base/BasePromptTemplate/aformat -->

Methodv1.2.21 (latest)●Since v0.1

# aformat

Async format the prompt with the inputs.


```
aformat(
    self,
    **kwargs: Any = {},
) -> FormatOutputType
```

**Example:**

```
await prompt.aformat(variable1="foo")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**kwargs` | `Any` | Default:`{}`  Any arguments to be passed to the prompt template. |


