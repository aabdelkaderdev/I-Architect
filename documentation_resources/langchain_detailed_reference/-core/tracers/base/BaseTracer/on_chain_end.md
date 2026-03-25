<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_chain_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_end

End a trace for a chain run.


```
on_chain_end(
  self,
  outputs: dict[str, Any],
  *,
  run_id: UUID,
  inputs: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `outputs`\* | `dict[str, Any]` | The outputs for the chain. |
| `run_id`\* | `UUID` | The run ID. |
| `inputs` | `dict[str, Any] | None` | Default:`None`  The inputs for the chain. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


