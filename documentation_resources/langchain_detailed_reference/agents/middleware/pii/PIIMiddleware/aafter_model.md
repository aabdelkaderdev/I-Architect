<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/pii/PIIMiddleware/aafter_model -->

Methodv1.2.13 (latest)●Since v1.0

# aafter\_model

Async check AI messages for PII after model invocation.


```
aafter_model(
  self,
  state: AgentState[Any],
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `AgentState[Any]` | The current agent state. |
| `runtime`\* | `Runtime[ContextT]` | The langgraph runtime. |


