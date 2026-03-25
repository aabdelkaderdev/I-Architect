<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware/awrap_tool_call -->

Methodv1.2.13 (latest)●Since v1.0

# awrap\_tool\_call

Intercept and control async tool execution with retry logic.


```
awrap_tool_call(
  self,
  request: ToolCallRequest,
  handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command[Any]]]
) -> ToolMessage | Command[Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `request`\* | `ToolCallRequest` | Tool call request with call `dict`, `BaseTool`, state, and runtime. |
| `handler`\* | `Callable[[ToolCallRequest], Awaitable[ToolMessage | Command[Any]]]` | Async callable to execute the tool and returns `ToolMessage` or `Command`. |


