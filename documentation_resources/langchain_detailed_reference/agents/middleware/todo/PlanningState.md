<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/todo/PlanningState -->

Classv1.2.13 (latest)●Since v1.0

# PlanningState

State schema for the todo middleware.


```
PlanningState()
```

## Bases

`AgentState[ResponseT]`

## Attributes

[attribute

todos: Annotated[NotRequired[list[Todo]], OmitFromInput]

List of todo items for tracking task progress.](/python/langchain/agents/middleware/todo/PlanningState/todos)

## Inherited from[AgentState](/python/langchain/agents/middleware/types/AgentState)

### Attributes

[Amessages: Required[Annotated[list[AnyMessage], add\_messages]]](/python/langchain/agents/middleware/types/AgentState/messages)[Ajump\_to: NotRequired[Annotated[JumpTo | None, EphemeralValue, PrivateStateAttr]]](/python/langchain/agents/middleware/types/AgentState/jump_to)[Astructured\_response: NotRequired[Annotated[ResponseT, OmitFromInput]]](/python/langchain/agents/middleware/types/AgentState/structured_response)


