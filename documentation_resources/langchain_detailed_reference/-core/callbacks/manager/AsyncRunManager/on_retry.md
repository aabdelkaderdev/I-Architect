<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncRunManager/on_retry -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retry

Async run when a retry is received.


```
on_retry(
  self,
  retry_state: RetryCallState,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retry_state`\* | `RetryCallState` | The retry state. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


