<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_llm_error -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_error

Handle an error for an LLM run.


```
on_llm_error(
  self,
  error: BaseException,
  *,
  run_id: UUID,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `error`\* | `BaseException` | The error. |
| `run_id`\* | `UUID` | The run ID. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


