<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/astream -->

Methodv1.2.21 (latest)●Since v0.1

# astream

Default implementation of `astream`, which calls `ainvoke`.

Subclasses must override this method if they support streaming output.


```
astream(
  self,
  input: Input,
  config: RunnableConfig | None = None,
  **kwargs: Any | None = {}
) -> AsyncIterator[Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `Input` | The input to the `Runnable`. |
| `config` | `RunnableConfig | None` | Default:`None`  The config to use for the `Runnable`. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


