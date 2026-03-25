<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/ChainManagerMixin/on_chain_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_end

Run when chain ends running.


```
on_chain_end(
  self,
  outputs: dict[str, Any],
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `outputs`\* | `dict[str, Any]` | The outputs of the chain. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


