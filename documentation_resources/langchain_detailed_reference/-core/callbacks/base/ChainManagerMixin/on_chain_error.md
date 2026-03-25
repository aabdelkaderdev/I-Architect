<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/ChainManagerMixin/on_chain_error -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_error

Run when chain errors.


```
on_chain_error(
  self,
  error: BaseException,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `error`\* | `BaseException` | The error that occurred. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


