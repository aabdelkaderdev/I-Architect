<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/atransform -->

Methodv1.2.21 (latest)●Since v0.1

# atransform

Transform inputs to outputs.

Default implementation of atransform, which buffers input and calls `astream`.

Subclasses must override this method if they can start producing output while
input is still being generated.


```
atransform(
  self,
  input: AsyncIterator[Input],
  config: RunnableConfig | None = None,
  **kwargs: Any | None = {}
) -> AsyncIterator[Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `AsyncIterator[Input]` | An async iterator of inputs to the `Runnable`. |
| `config` | `RunnableConfig | None` | Default:`None`  The config to use for the `Runnable`. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


