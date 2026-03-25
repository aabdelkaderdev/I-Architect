<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/stream -->

Methodv1.2.21 (latest)●Since v0.1

# stream

Default implementation of `stream`, which calls `invoke`.

Subclasses must override this method if they support streaming output.


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
| `config` | `RunnableConfig | None` | Default:`None`  The config to use for the `Runnable`. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


