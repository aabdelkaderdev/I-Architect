<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms/create_base_retry_decorator -->

Functionv1.2.21 (latest)●Since v0.1

# create\_base\_retry\_decorator

Create a retry decorator for a given LLM and provided a list of error types.


```
create_base_retry_decorator(
  error_types: list[type[BaseException]],
  max_retries: int = 1,
  run_manager: AsyncCallbackManagerForLLMRun | CallbackManagerForLLMRun | None = None
) -> Callable[[Any], Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `error_types`\* | `list[type[BaseException]]` | List of error types to retry on. |
| `max_retries` | `int` | Default:`1`  Number of retries. |
| `run_manager` | `AsyncCallbackManagerForLLMRun | CallbackManagerForLLMRun | None` | Default:`None`  Callback manager for the run. |


