<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_retry -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retry

Run on retry.


```
on_retry(
  self,
  retry_state: RetryCallState,
  *,
  run_id: UUID,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retry_state`\* | `RetryCallState` | The retry state. |
| `run_id`\* | `UUID` | The run ID. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


