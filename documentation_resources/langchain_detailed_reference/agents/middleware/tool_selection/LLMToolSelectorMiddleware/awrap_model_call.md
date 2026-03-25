<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_selection/LLMToolSelectorMiddleware/awrap_model_call -->

Methodv1.2.13 (latest)●Since v1.0

# awrap\_model\_call

Filter tools based on LLM selection before invoking the model via handler.


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
| `request`\* | `ModelRequest[ContextT]` | Model request to execute (includes state and runtime). |
| `handler`\* | `Callable[[ModelRequest[ContextT]], Awaitable[ModelResponse[ResponseT]]]` | Async callback that executes the model request and returns `ModelResponse`. |


