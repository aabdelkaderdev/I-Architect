<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/chat_memory/BaseChatMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# BaseChatMemory


```
BaseChatMemory()
```

## Bases

`BaseMemory``ABC`

## Attributes

## Methods

## Inherited from[BaseMemory](/python/langchain-classic/base_memory/BaseMemory)

### Attributes

[Amodel\_config](/python/langchain-classic/base_memory/BaseMemory/model_config)[Amemory\_variables: list[str]

—

The string keys this memory class will add to chain inputs.](/python/langchain-classic/base_memory/BaseMemory/memory_variables)

### Methods

[Mload\_memory\_variables

—

Return key-value pairs given the text input to the chain.](/python/langchain-classic/base_memory/BaseMemory/load_memory_variables)



M

aload\_memory\_variables

—

Async return key-value pairs given the text input to the chain.

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

chat\_memory: BaseChatMessageHistory](/python/langchain-classic/memory/chat_memory/BaseChatMemory/chat_memory)

[attribute

output\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/output_key)

[attribute

input\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/input_key)

[attribute

return\_messages: bool](/python/langchain-classic/memory/chat_memory/BaseChatMemory/return_messages)

[method

save\_context

Save context from this conversation to buffer.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/save_context)

[method

asave\_context

Save context from this conversation to buffer.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/asave_context)

[method

clear

Clear memory contents.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/clear)

[method

aclear

Clear memory contents.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/aclear)

Abstract base class for chat memory.

**ATTENTION** This abstraction was created prior to when chat models had
native tool calling capabilities.
It does **NOT** support native tool calling capabilities for chat models and
will fail SILENTLY if used with a chat model that has native tool calling.

DO NOT USE THIS ABSTRACTION FOR NEW CODE.