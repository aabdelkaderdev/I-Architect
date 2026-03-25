<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware/awrap_model_call -->

Methodv1.2.13 (latest)●Since v1.0

# awrap\_model\_call

Try fallback models in sequence on errors (async version).


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
| `request`\* | `ModelRequest[ContextT]` | Initial model request. |
| `handler`\* | `Callable[[ModelRequest[ContextT]], Awaitable[ModelResponse[ResponseT]]]` | Async callback to execute the model. |


