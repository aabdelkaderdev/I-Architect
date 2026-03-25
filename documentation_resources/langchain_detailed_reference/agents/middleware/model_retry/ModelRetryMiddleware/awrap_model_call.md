<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_retry/ModelRetryMiddleware/awrap_model_call -->

Methodv1.2.13 (latest)●Since v1.1

# awrap\_model\_call

Intercept and control async model execution with retry logic.


```
awrap_model_call(
  self,
  request: ModelRequest[ContextT],
  handler: Callable[[ModelRequest[ContextT]], Awaitable[ModelResponse[ResponseT]]]
) -> ModelResponse[ResponseT] | AIMessage
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `request`\* | `ModelRequest[ContextT]` | Model request with model, messages, state, and runtime. |
| `handler`\* | `Callable[[ModelRequest[ContextT]], Awaitable[ModelResponse[ResponseT]]]` | Async callable to execute the model and returns `ModelResponse`. |


