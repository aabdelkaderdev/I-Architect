<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/transform -->

Methodv1.2.21 (latest)●Since v0.1

# transform

Transform inputs to outputs.

Default implementation of transform, which buffers input and calls `astream`.

Subclasses must override this method if they can start producing output while
input is still being generated.


```
transform(
  self,
  input: Iterator[Input],
  config: RunnableConfig | None = None,
  **kwargs: Any | None = {}
) -> Iterator[Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `Iterator[Input]` | An iterator of inputs to the `Runnable`. |
| `config` | `RunnableConfig | None` | Default:`None`  The config to use for the `Runnable`. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


