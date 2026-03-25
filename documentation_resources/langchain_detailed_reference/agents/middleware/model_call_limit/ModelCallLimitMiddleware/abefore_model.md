<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware/abefore_model -->

Methodv1.2.13 (latest)●Since v1.0

# abefore\_model

Async check model call limits before making a model call.


```
abefore_model(
  self,
  state: ModelCallLimitState[ResponseT],
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `ModelCallLimitState[ResponseT]` | The current agent state containing call counts. |
| `runtime`\* | `Runtime[ContextT]` | The langgraph runtime. |


