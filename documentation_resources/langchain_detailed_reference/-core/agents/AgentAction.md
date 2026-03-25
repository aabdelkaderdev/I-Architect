<!-- Source: https://reference.langchain.com/python/langchain-core/agents/AgentAction -->

Classv1.2.21 (latest)●Since v0.1

# AgentAction

Represents a request to execute an action by an agent.

The action consists of the name of the tool to execute and the input to pass
to the tool. The log is used to pass along extra information about the action.


```
AgentAction(
  self,
  tool: str,
  tool_input: str | dict,
  log: str,
  **kwargs: Any = {}
)
```

## Bases

`Serializable`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tool`\* | `str` | The name of the tool to execute. |
| `tool_input`\* | `str | dict` | The input to pass in to the `Tool`. |
| `log`\* | `str` | Additional information to log about the action. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| tool | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| tool\_input | [str](https://docs.python.org/3/library/stdtypes.html#str) | [dict](https://docs.python.org/3/library/stdtypes.html#dict) |
| log | [str](https://docs.python.org/3/library/stdtypes.html#str) |

## Attributes

[attribute

tool: str

The name of the `Tool` to execute.](/python/langchain-core/agents/AgentAction/tool)[attribute

tool\_input: str | dict

The input to pass in to the `Tool`.](/python/langchain-core/agents/AgentAction/tool_input)[attribute

log: str

Additional information to log about the action.

This log can be used in a few ways. First, it can be used to audit what exactly the
LLM predicted to lead to this `(tool, tool_input)`.

Second, it can be used in future iterations to show the LLMs prior thoughts. This is
useful when `(tool, tool_input)` does not contain full information about the LLM
prediction (for example, any `thought` before the tool/tool\_input).](/python/langchain-core/agents/AgentAction/log)[attribute

type: Literal['AgentAction']](/python/langchain-core/agents/AgentAction/type)[attribute

messages: Sequence[BaseMessage]

Return the messages that correspond to this action.](/python/langchain-core/agents/AgentAction/messages)

## Methods

[method

is\_lc\_serializable

`AgentAction` is serializable.](/python/langchain-core/agents/AgentAction/is_lc_serializable)[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/agents/AgentAction/get_lc_namespace)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)


