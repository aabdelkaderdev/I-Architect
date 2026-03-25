<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/batch -->

Methodv1.2.21 (latest)●Since v0.1

# batch

Default implementation runs invoke in parallel using a thread pool executor.

The default implementation of batch works well for IO bound runnables.

Subclasses must override this method if they can batch more efficiently;
e.g., if the underlying `Runnable` uses an API which supports a batch mode.


```
batch(
  self,
  inputs: list[Input],
  config: RunnableConfig | list[RunnableConfig] | None = None,
  *,
  return_exceptions: bool = False,
  **kwargs: Any | None = {}
) -> list[Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `inputs`\* | `list[Input]` | A list of inputs to the `Runnable`. |
| `config` | `RunnableConfig | list[RunnableConfig] | None` | Default:`None`  A config to use when invoking the `Runnable`. The config supports standard keys like `'tags'`, `'metadata'` for tracing purposes, `'max_concurrency'` for controlling how much work to do in parallel, and other keys.  Please refer to `RunnableConfig` for more details. |
| `return_exceptions` | `bool` | Default:`False`  Whether to return exceptions instead of raising them. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


