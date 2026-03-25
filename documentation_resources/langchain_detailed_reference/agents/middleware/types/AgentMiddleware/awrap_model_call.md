<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types/AgentMiddleware/awrap_model_call -->

Methodv1.2.13 (latest)●Since v1.0

# awrap\_model\_call

Intercept and control async model execution via handler callback.

The handler callback executes the model request and returns a `ModelResponse`.

Middleware can call the handler multiple times for retry logic, skip calling
it to short-circuit, or modify the request/response. Multiple middleware
compose with first in list as outermost layer.


```
awrap_model_call(
  self,
  request: ModelRequest[ContextT],
  handler: Callable[[ModelRequest[ContextT]], Awaitable[ModelResponse[ResponseT]]]
) -> ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `request`\* | `ModelRequest[ContextT]` | Model request to execute (includes state and runtime). |
| `handler`\* | `Callable[[ModelRequest[ContextT]], Awaitable[ModelResponse[ResponseT]]]` | Async callback that executes the model request and returns `ModelResponse`.  Call this to execute the model.  Can be called multiple times for retry logic.  Can skip calling it to short-circuit. |


