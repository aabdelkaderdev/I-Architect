<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/HumanInTheLoopMiddleware/aafter_model -->

Methodv1.2.13 (latest)●Since v1.0

# aafter\_model

Async trigger interrupt flows for relevant tool calls after an `AIMessage`.


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
| `runtime`\* | `Runtime[ContextT]` | The runtime context. |


