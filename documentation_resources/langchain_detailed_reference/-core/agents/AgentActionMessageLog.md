<!-- Source: https://reference.langchain.com/python/langchain-core/agents/AgentActionMessageLog -->

Classv1.2.21 (latest)●Since v0.1

# AgentActionMessageLog

Representation of an action to be executed by an agent.

This is similar to `AgentAction`, but includes a message log consisting of
chat messages.

This is useful when working with `ChatModels`, and is used to reconstruct
conversation history from the agent's perspective.


```
AgentActionMessageLog(
  self,
  tool: str,
  tool_input: str | dict,
  log: str,
  **kwargs: Any = {}
)
```

## Bases

`AgentAction`

## Attributes

[attribute

message\_log: Sequence[BaseMessage]

Similar to log, this can be used to pass along extra information about what exact
messages were predicted by the LLM before parsing out the `(tool, tool_input)`.

This is again useful if `(tool, tool_input)` cannot be used to fully recreate the
LLM prediction, and you need that LLM prediction (for future agent iteration).

Compared to `log`, this is useful when the underlying LLM is a chat model (and
therefore returns messages rather than a string).](/python/langchain-core/agents/AgentActionMessageLog/message_log)[attribute

type: Literal['AgentActionMessageLog']](/python/langchain-core/agents/AgentActionMessageLog/type)

## Inherited from[AgentAction](/python/langchain-core/agents/AgentAction)

### Attributes

[Atool: str

—

The name of the `Tool` to execute.](/python/langchain-core/agents/AgentAction/tool)[Atool\_input: str | dict

—

The input to pass in to the `Tool`.](/python/langchain-core/agents/AgentAction/tool_input)[Alog: str

—

Additional information to log about the action.](/python/langchain-core/agents/AgentAction/log)[Amessages: Sequence[BaseMessage]

—

Return the messages that correspond to this action.](/python/langchain-core/agents/AgentAction/messages)

### Methods

[Mis\_lc\_serializable

—

`AgentAction` is serializable.](/python/langchain-core/agents/AgentAction/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/agents/AgentAction/get_lc_namespace)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable

—

Is this class serializable?](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)


