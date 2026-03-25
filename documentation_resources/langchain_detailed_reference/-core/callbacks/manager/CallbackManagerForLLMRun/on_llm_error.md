<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/CallbackManagerForLLMRun/on_llm_error -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_error

Run when LLM errors.


```
on_llm_error(
  self,
  error: BaseException,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `error`\* | `BaseException` | The error. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments.   - response (LLMResult): The response which was generated before   the error occurred. |


