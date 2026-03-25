<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/summarization/SummarizationMiddleware/abefore_model -->

Methodv1.2.13 (latest)●Since v1.1

# abefore\_model

Process messages before model invocation, potentially triggering summarization.


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
| `state`\* | `AgentState[Any]` | The agent state. |
| `runtime`\* | `Runtime[ContextT]` | The runtime environment. |


