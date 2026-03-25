<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/config/acall_func_with_variable_args -->

Functionv1.2.21 (latest)●Since v0.1

# acall\_func\_with\_variable\_args

Async call function that may optionally accept a run\_manager and/or config.


```
acall_func_with_variable_args(
  func: Callable[[Input], Awaitable[Output]] | Callable[[Input, RunnableConfig], Awaitable[Output]] | Callable[[Input, AsyncCallbackManagerForChainRun], Awaitable[Output]] | Callable[[Input, AsyncCallbackManagerForChainRun, RunnableConfig], Awaitable[Output]],
  input: Input,
  config: RunnableConfig,
  run_manager: AsyncCallbackManagerForChainRun | None = None,
  **kwargs: Any = {}
) -> Awaitable[Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `func`\* | `Callable[[Input], Awaitable[Output]] | Callable[[Input, RunnableConfig], Awaitable[Output]] | Callable[[Input, AsyncCallbackManagerForChainRun], Awaitable[Output]] | Callable[[Input, AsyncCallbackManagerForChainRun, RunnableConfig], Awaitable[Output]]` | The function to call. |
| `input`\* | `Input` | The input to the function. |
| `config`\* | `RunnableConfig` | The config to pass to the function. |
| `run_manager` | `AsyncCallbackManagerForChainRun | None` | Default:`None`  The run manager to pass to the function. |
| `**kwargs` | `Any` | Default:`{}`  The keyword arguments to pass to the function. |


