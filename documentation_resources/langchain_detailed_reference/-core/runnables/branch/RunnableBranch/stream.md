<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/branch/RunnableBranch/stream -->

Methodv1.2.21 (latest)●Since v0.1

# stream

First evaluates the condition, then delegate to `True` or `False` branch.


```
stream(
  self,
  input: Input,
  config: RunnableConfig | None = None,
  **kwargs: Any | None = {}
) -> Iterator[Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `Input` | The input to the `Runnable`. |
| `config` | `RunnableConfig | None` | Default:`None`  The configuration for the `Runnable`. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


