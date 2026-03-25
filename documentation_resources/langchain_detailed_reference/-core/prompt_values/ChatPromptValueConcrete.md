<!-- Source: https://reference.langchain.com/python/langchain-core/prompt_values/ChatPromptValueConcrete -->

Classv1.2.21 (latest)●Since v0.1

# ChatPromptValueConcrete

Chat prompt value which explicitly lists out the message types it accepts.

For use in external schemas.


```
ChatPromptValueConcrete(
  self,
  *args: Any = (),
  **kwargs: Any = {}
)
```

## Bases

`ChatPromptValue`

## Attributes

[attribute

messages: Sequence[AnyMessage]

Sequence of messages.](/python/langchain-core/prompt_values/ChatPromptValueConcrete/messages)[attribute

type: Literal['ChatPromptValueConcrete']](/python/langchain-core/prompt_values/ChatPromptValueConcrete/type)

## Inherited from[ChatPromptValue](/python/langchain-core/prompt_values/ChatPromptValue)

### Methods

[Mto\_string

—

Return prompt as string.](/python/langchain-core/prompt_values/ChatPromptValue/to_string)[Mto\_messages

—

Return prompt as a list of messages.](/python/langchain-core/prompt_values/ChatPromptValue/to_messages)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/prompt_values/ChatPromptValue/get_lc_namespace)

## Inherited from[PromptValue](/python/langchain-core/prompt_values/PromptValue)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/prompt_values/PromptValue/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/prompt_values/PromptValue/get_lc_namespace)[Mto\_string

—

Return prompt value as string.](/python/langchain-core/prompt_values/PromptValue/to_string)[Mto\_messages

—

Return prompt as a list of messages.](/python/langchain-core/prompt_values/PromptValue/to_messages)

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


