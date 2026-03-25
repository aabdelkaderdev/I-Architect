<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware/aafter_model -->

Methodv1.2.13 (latest)●Since v1.0

# aafter\_model

Async increment model call counts after a model call.


```
aafter_model(
  self,
  state: ModelCallLimitState[ResponseT],
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `ModelCallLimitState[ResponseT]` | The current agent state. |
| `runtime`\* | `Runtime[ContextT]` | The langgraph runtime. |


