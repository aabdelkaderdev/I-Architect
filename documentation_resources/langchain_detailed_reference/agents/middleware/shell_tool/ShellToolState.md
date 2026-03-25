<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/shell_tool/ShellToolState -->

Classv1.2.13 (latest)●Since v1.0

# ShellToolState

Agent state extension for tracking shell session resources.


```
ShellToolState()
```

## Bases

`AgentState[ResponseT]`

## Attributes

[attribute

shell\_session\_resources: NotRequired[Annotated[\_SessionResources | None, UntrackedValue, PrivateStateAttr]]](/python/langchain/agents/middleware/shell_tool/ShellToolState/shell_session_resources)

## Inherited from[AgentState](/python/langchain/agents/middleware/types/AgentState)

### Attributes

[Amessages: Required[Annotated[list[AnyMessage], add\_messages]]](/python/langchain/agents/middleware/types/AgentState/messages)[Ajump\_to: NotRequired[Annotated[JumpTo | None, EphemeralValue, PrivateStateAttr]]](/python/langchain/agents/middleware/types/AgentState/jump_to)[Astructured\_response: NotRequired[Annotated[ResponseT, OmitFromInput]]](/python/langchain/agents/middleware/types/AgentState/structured_response)


