<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/base/BasePromptTemplate/partial -->

Methodv1.2.21 (latest)●Since v0.1

# partial

Return a partial of the prompt template.


```
partial(
    self,
    **kwargs: str | Callable[[], str] = {},
) -> BasePromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**kwargs` | `str | Callable[[], str]` | Default:`{}`  Partial variables to set. |


