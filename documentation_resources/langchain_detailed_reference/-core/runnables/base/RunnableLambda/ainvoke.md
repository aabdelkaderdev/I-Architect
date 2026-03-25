<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLambda/ainvoke -->

Methodv1.2.21 (latest)●Since v0.1

# ainvoke

Invoke this `Runnable` asynchronously.


```
ainvoke(
  self,
  input: Input,
  config: RunnableConfig | None = None,
  **kwargs: Any | None = {}
) -> Output
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `Input` | The input to this `Runnable`. |
| `config` | `RunnableConfig | None` | Default:`None`  The config to use. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments. |


