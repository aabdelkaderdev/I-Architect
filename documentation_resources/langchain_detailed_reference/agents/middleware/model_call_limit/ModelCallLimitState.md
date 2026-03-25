<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/model_call_limit/ModelCallLimitState -->

Classv1.2.13 (latest)●Since v1.0

# ModelCallLimitState

State schema for `ModelCallLimitMiddleware`.

Extends `AgentState` with model call tracking fields.


```
ModelCallLimitState()
```

## Bases

`AgentState[ResponseT]`

## Attributes

[attribute

thread\_model\_call\_count: NotRequired[Annotated[int, PrivateStateAttr]]](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitState/thread_model_call_count)[attribute

run\_model\_call\_count: NotRequired[Annotated[int, UntrackedValue, PrivateStateAttr]]](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitState/run_model_call_count)

## Inherited from[AgentState](/python/langchain/agents/middleware/types/AgentState)

### Attributes

[Amessages: Required[Annotated[list[AnyMessage], add\_messages]]](/python/langchain/agents/middleware/types/AgentState/messages)[Ajump\_to: NotRequired[Annotated[JumpTo | None, EphemeralValue, PrivateStateAttr]]](/python/langchain/agents/middleware/types/AgentState/jump_to)[Astructured\_response: NotRequired[Annotated[ResponseT, OmitFromInput]]](/python/langchain/agents/middleware/types/AgentState/structured_response)


