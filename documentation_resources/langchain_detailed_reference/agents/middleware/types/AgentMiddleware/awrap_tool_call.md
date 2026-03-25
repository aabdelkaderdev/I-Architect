<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types/AgentMiddleware/awrap_tool_call -->

Methodv1.2.13 (latest)●Since v1.0

# awrap\_tool\_call


```
awrap_tool_call(
  self,
  request: ToolCallRequest,
  handler: Callable[[ToolCallRequest], Awaitable[ToolMessage
```



|

Command

[

Any

]

]

]

)

->

[ToolMessage](/python/langchain-core/messages/ToolMessage)

|

[Command](/python/langgraph/types/Command)

[

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

]

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `request`\* | `ToolCallRequest` |  |
| `handler`\* | `Callable[[ToolCallRequest], Awaitable[ToolMessage | Command[Any]]]` |  |

Intercept and control async tool execution via handler callback.

The handler callback executes the tool call and returns a `ToolMessage` or
`Command`. Middleware can call the handler multiple times for retry logic, skip
calling it to short-circuit, or modify the request/response. Multiple middleware
compose with first in list as outermost layer.

The handler `Callable` can be invoked multiple times for retry logic.

Each call to handler is independent and stateless.

Tool call request with call `dict`, `BaseTool`, state, and runtime.

Access state via `request.state` and runtime via `request.runtime`.

Async callable to execute the tool and returns `ToolMessage` or
`Command`.

Call this to execute the tool.

Can be called multiple times for retry logic.

Can skip calling it to short-circuit.