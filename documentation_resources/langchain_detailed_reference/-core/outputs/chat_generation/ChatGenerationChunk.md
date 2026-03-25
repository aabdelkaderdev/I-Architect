<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/chat_generation/ChatGenerationChunk -->

Classv1.2.21 (latest)●Since v0.1

# ChatGenerationChunk

`ChatGeneration` chunk.

`ChatGeneration` chunks can be concatenated with other `ChatGeneration` chunks.


```
ChatGenerationChunk(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`ChatGeneration`

## Attributes

[attribute

message: BaseMessageChunk

The message chunk output by the chat model.](/python/langchain-core/outputs/chat_generation/ChatGenerationChunk/message)[attribute

type: Literal['ChatGenerationChunk']

Type is used exclusively for serialization purposes.](/python/langchain-core/outputs/chat_generation/ChatGenerationChunk/type)

## Inherited from[ChatGeneration](/python/langchain-core/outputs/chat_generation/ChatGeneration)

### Attributes

[Atext: str

—

The text contents of the output message.](/python/langchain-core/outputs/chat_generation/ChatGeneration/text)

### Methods

[Mset\_text

—

Set the text attribute to be the contents of the message.](/python/langchain-core/outputs/chat_generation/ChatGeneration/set_text)

## Inherited from[Generation](/python/langchain-core/outputs/generation/Generation)

### Attributes

[Atext: str

—

Generated text output.](/python/langchain-core/outputs/generation/Generation/text)[Ageneration\_info: dict[str, Any] | None

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


