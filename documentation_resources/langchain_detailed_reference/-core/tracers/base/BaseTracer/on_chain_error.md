<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_chain_error -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_error

Handle an error for a chain run.


```
on_chain_error(
  self,
  error: BaseException,
  *,
  inputs: dict[str, Any] | None = None,
  run_id: UUID,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `error`\* | `BaseException` | The error. |
| `inputs` | `dict[str, Any] | None` | Default:`None`  The inputs for the chain. |
| `run_id`\* | `UUID` | The run ID. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


