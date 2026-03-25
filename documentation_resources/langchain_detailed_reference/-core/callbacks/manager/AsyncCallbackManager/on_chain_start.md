<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_chain_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_start

Async run when chain starts running.


```
on_chain_start(
  self,
  serialized: dict[str, Any] | None,
  inputs: dict[str, Any] | Any,
  run_id: UUID | None = None,
  **kwargs: Any = {}
) -> AsyncCallbackManagerForChainRun
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any] | None` | The serialized chain. |
| `inputs`\* | `dict[str, Any] | Any` | The inputs to the chain. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


