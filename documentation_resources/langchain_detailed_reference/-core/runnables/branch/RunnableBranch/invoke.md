<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/branch/RunnableBranch/invoke -->

Methodv1.2.21 (latest)●Since v0.1

# invoke

First evaluates the condition, then delegate to `True` or `False` branch.


```
invoke(
  self,
  input: Input,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> Output
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `Input` | The input to the `Runnable`. |
| `config` | `RunnableConfig | None` | Default:`None`  The configuration for the `Runnable`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


