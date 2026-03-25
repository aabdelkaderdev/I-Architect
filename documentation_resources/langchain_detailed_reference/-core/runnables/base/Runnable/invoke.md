<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/invoke -->

Methodv1.2.21 (latest)●Since v0.1

# invoke

Transform a single input into an output.


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
| `config` | `RunnableConfig | None` | Default:`None`  A config to use when invoking the `Runnable`.  The config supports standard keys like `'tags'`, `'metadata'` for tracing purposes, `'max_concurrency'` for controlling how much work to do in parallel, and other keys.  Please refer to `RunnableConfig` for more details. |


