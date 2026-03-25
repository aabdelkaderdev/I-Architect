<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types/AgentMiddleware/abefore_agent -->

Methodv1.2.13 (latest)●Since v1.0

# abefore\_agent

Async logic to run before the agent execution starts.


```
abefore_agent(
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


