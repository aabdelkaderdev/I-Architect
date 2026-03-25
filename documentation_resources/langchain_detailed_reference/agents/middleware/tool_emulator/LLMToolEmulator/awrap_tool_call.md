<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_emulator/LLMToolEmulator/awrap_tool_call -->

Methodv1.2.13 (latest)●Since v1.0

# awrap\_tool\_call

Async version of `wrap_tool_call`.

Emulate tool execution using LLM if tool should be emulated.


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
| `request`\* | `ToolCallRequest` | Tool call request to potentially emulate. |
| `handler`\* | `Callable[[ToolCallRequest], Awaitable[ToolMessage | Command[Any]]]` | Async callback to execute the tool (can be called multiple times). |


