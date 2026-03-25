<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/streaming_stdout/StreamingStdOutCallbackHandler/on_llm_error -->

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
| `error`\* | `BaseException` | The error that occurred. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


