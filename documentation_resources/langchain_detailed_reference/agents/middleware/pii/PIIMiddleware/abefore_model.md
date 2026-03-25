<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/pii/PIIMiddleware/abefore_model -->

Methodv1.2.13 (latest)●Since v1.0

# abefore\_model

Async check user messages and tool results for PII before model invocation.


```
abefore_model(
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


