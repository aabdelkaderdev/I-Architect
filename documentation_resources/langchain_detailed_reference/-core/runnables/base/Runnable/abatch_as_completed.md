<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/abatch_as_completed -->

Methodv1.2.21 (latest)●Since v0.1

# abatch\_as\_completed

Run `ainvoke` in parallel on a list of inputs.

Yields results as they complete.


```
abatch_as_completed(
  self,
  inputs: Sequence[Input],
  config: RunnableConfig | Sequence[RunnableConfig] | None = None,
  *,
  return_exceptions: bool = False,
  **kwargs: Any | None = {}
) -> AsyncIterator[tuple[int, Output | Exception]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `inputs`\* | `Sequence[Input]` | A list of inputs to the `Runnable`. |
| `config` | `RunnableConfig | Sequence[RunnableConfig] | None` | Default:`None`  A config to use when invoking the `Runnable`.  The config supports standard keys like `'tags'`, `'metadata'` for tracing purposes, `'max_concurrency'` for controlling how much work to do in parallel, and other keys.  Please refer to `RunnableConfig` for more details. |
| `return_exceptions` | `bool` | Default:`False`  Whether to return exceptions instead of raising them. |
| `**kwargs` | `Any | None` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


