<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/chat_generation/ChatGeneration -->

Classv1.2.21 (latest)●Since v0.1

# ChatGeneration

A single chat generation output.

A subclass of `Generation` that represents the response from a chat model that
generates chat messages.

The `message` attribute is a structured representation of the chat message. Most of
the time, the message will be of type `AIMessage`.

Users working with chat models will usually access information via either
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks).


```
ChatGeneration(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`Generation`

## Attributes

[attribute

text: str

The text contents of the output message.](/python/langchain-core/outputs/chat_generation/ChatGeneration/text)[attribute

message: BaseMessage

The message output by the chat model.](/python/langchain-core/outputs/chat_generation/ChatGeneration/message)[attribute

type: Literal['ChatGeneration']

Type is used exclusively for serialization purposes.](/python/langchain-core/outputs/chat_generation/ChatGeneration/type)

## Methods

[method

set\_text

Set the text attribute to be the contents of the message.](/python/langchain-core/outputs/chat_generation/ChatGeneration/set_text)

## Inherited from[Generation](/python/langchain-core/outputs/generation/Generation)

### Attributes

[Ageneration\_info: dict[str, Any] | None

—

Raw response from the provider.](/python/langchain-core/outputs/generation/Generation/generation_info)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/outputs/generation/Generation/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/outputs/generation/Generation/get_lc_namespace)

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


