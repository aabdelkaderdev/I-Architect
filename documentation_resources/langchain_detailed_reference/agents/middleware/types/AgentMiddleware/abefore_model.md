<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types/AgentMiddleware/abefore_model -->

Methodv1.2.13 (latest)●Since v0.3

# abefore\_model

Async logic to run before the model is called.


```
abefore_model(
  self,
  state: StateT,
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `StateT` | The agent state. |
| `runtime`\* | `Runtime[ContextT]` | The runtime context. |


