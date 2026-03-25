<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitMiddleware/aafter_model -->

Methodv1.2.13 (latest)●Since v1.0

# aafter\_model

Async increment tool call counts after a model call and check limits.


```
aafter_model(
  self,
  state: ToolCallLimitState[ResponseT],
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `ToolCallLimitState[ResponseT]` | The current agent state. |
| `runtime`\* | `Runtime[ContextT]` | The langgraph runtime. |


