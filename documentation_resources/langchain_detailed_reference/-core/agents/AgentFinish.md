<!-- Source: https://reference.langchain.com/python/langchain-core/agents/AgentFinish -->

Classv1.2.21 (latest)●Since v0.1

# AgentFinish

Final return value of an `ActionAgent`.

Agents return an `AgentFinish` when they have reached a stopping condition.


```
AgentFinish(
  self,
  return_values: dict,
  log: str,
  **kwargs: Any = {}
)
```

## Bases

`Serializable`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| return\_values | [dict](https://docs.python.org/3/library/stdtypes.html#dict) |
| log | [str](https://docs.python.org/3/library/stdtypes.html#str) |

## Attributes

[attribute

return\_values: dict

Dictionary of return values.](/python/langchain-core/agents/AgentFinish/return_values)[attribute

log: str

Additional information to log about the return value.

This is used to pass along the full LLM prediction, not just the parsed out
return value.

For example, if the full LLM prediction was `Final Answer: 2` you may want to just
return `2` as a return value, but pass along the full string as a `log` (for
debugging or observability purposes).](/python/langchain-core/agents/AgentFinish/log)[attribute

type: Literal['AgentFinish']](/python/langchain-core/agents/AgentFinish/type)[attribute

messages: Sequence[BaseMessage]

Messages that correspond to this observation.](/python/langchain-core/agents/AgentFinish/messages)

## Methods

[method

is\_lc\_serializable

Return `True` as this class is serializable.](/python/langchain-core/agents/AgentFinish/is_lc_serializable)[method

get\_lc\_namespace

Get the namespace of the LangChain object.](/python/langchain-core/agents/AgentFinish/get_lc_namespace)

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


