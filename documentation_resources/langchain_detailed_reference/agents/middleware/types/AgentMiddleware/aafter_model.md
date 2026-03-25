<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types/AgentMiddleware/aafter_model -->

Methodv1.2.13 (latest)●Since v0.3

# aafter\_model

Async logic to run after the model is called.


```
aafter_model(
  self,
  state: StateT,
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `StateT` | The current agent state. |
| `runtime`\* | `Runtime[ContextT]` | The runtime context. |


