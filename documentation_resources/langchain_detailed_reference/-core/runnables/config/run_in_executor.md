<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/config/run_in_executor -->

Functionv1.2.21 (latest)●Since v0.1

# run\_in\_executor

Run a function in an executor.


```
run_in_executor(
  executor_or_config: Executor | RunnableConfig | None,
  func: Callable[P, T],
  *args: P.args = (),
  **kwargs: P.kwargs = {}
) -> T
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `executor_or_config`\* | `Executor | RunnableConfig | None` | The executor or config to run in. |
| `func`\* | `Callable[P, T]` | The function. |
| `*args` | `P.args` | Default:`()`  The positional arguments to the function. |
| `**kwargs` | `P.kwargs` | Default:`{}`  The keyword arguments to the function. |


