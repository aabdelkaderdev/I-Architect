<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/with_config -->

Methodv1.2.21 (latest)●Since v0.1

# with\_config

Bind config to a `Runnable`, returning a new `Runnable`.


```
with_config(
  self,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> Runnable[Input, Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config` | `RunnableConfig | None` | Default:`None`  The config to bind to the `Runnable`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


