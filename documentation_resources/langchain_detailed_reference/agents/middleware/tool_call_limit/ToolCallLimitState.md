<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitState -->

Classv1.2.13 (latest)●Since v1.0

# ToolCallLimitState

State schema for `ToolCallLimitMiddleware`.

Extends `AgentState` with tool call tracking fields.

The count fields are dictionaries mapping tool names to execution counts. This
allows multiple middleware instances to track different tools independently. The
special key `'__all__'` is used for tracking all tool calls globally.


```
ToolCallLimitState()
```

## Bases

`AgentState[ResponseT]`

## Attributes

[attribute

thread\_tool\_call\_count: NotRequired[Annotated[dict[str, int], PrivateStateAttr]]](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitState/thread_tool_call_count)[attribute

run\_tool\_call\_count: NotRequired[Annotated[dict[str, int], UntrackedValue, PrivateStateAttr]]](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitState/run_tool_call_count)

## Inherited from[AgentState](/python/langchain/agents/middleware/types/AgentState)

### Attributes

[Amessages: Required[Annotated[list[AnyMessage], add\_messages]]](/python/langchain/agents/middleware/types/AgentState/messages)[Ajump\_to: NotRequired[Annotated[JumpTo | None, EphemeralValue, PrivateStateAttr]]](/python/langchain/agents/middleware/types/AgentState/jump_to)[Astructured\_response: NotRequired[Annotated[ResponseT, OmitFromInput]]](/python/langchain/agents/middleware/types/AgentState/structured_response)


