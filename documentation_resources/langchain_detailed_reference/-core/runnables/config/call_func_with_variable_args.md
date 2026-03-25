<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/config/call_func_with_variable_args -->

Functionv1.2.21 (latest)●Since v0.1

# call\_func\_with\_variable\_args

Call function that may optionally accept a run\_manager and/or config.


```
call_func_with_variable_args(
  func: Callable[[Input], Output] | Callable[[Input, RunnableConfig], Output] | Callable[[Input, CallbackManagerForChainRun], Output] | Callable[[Input, CallbackManagerForChainRun, RunnableConfig], Output],
  input: Input,
  config: RunnableConfig,
  run_manager: CallbackManagerForChainRun | None = None,
  **kwargs: Any = {}
) -> Output
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `func`\* | `Callable[[Input], Output] | Callable[[Input, RunnableConfig], Output] | Callable[[Input, CallbackManagerForChainRun], Output] | Callable[[Input, CallbackManagerForChainRun, RunnableConfig], Output]` | The function to call. |
| `input`\* | `Input` | The input to the function. |
| `config`\* | `RunnableConfig` | The config to pass to the function. |
| `run_manager` | `CallbackManagerForChainRun | None` | Default:`None`  The run manager to pass to the function. |
| `**kwargs` | `Any` | Default:`{}`  The keyword arguments to pass to the function. |


