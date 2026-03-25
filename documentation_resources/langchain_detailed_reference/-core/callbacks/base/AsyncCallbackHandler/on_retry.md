<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retry -->

Methodv1.2.21 (latest)●Since v0.1

# on\_retry

Run on a retry event.


```
on_retry(
  self,
  retry_state: RetryCallState,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retry_state`\* | `RetryCallState` | The retry state. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


