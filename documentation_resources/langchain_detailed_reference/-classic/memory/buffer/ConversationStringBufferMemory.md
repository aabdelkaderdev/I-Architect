<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/buffer/ConversationStringBufferMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConversationStringBufferMemory


```
ConversationStringBufferMemory()
```

## Bases

`BaseMemory`

## Attributes

## Methods

## Inherited from[BaseMemory](/python/langchain-classic/base_memory/BaseMemory)

### Attributes

[Amodel\_config](/python/langchain-classic/base_memory/BaseMemory/model_config)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)



A

model\_config

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

human\_prefix: str](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/human_prefix)

[attribute

ai\_prefix: str](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/ai_prefix)

[attribute

buffer: str](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/buffer)

[attribute

output\_key: str | None](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/output_key)

[attribute

input\_key: str | None](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/input_key)

[attribute

memory\_key: str](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/memory_key)

[attribute

memory\_variables: list[str]](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/memory_variables)

[method

validate\_chains](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/validate_chains)

[method

load\_memory\_variables](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/load_memory_variables)

[method

aload\_memory\_variables](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/aload_memory_variables)

[method

save\_context](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/save_context)

[method

asave\_context](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/asave_context)

[method

clear](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/clear)

[method

aclear](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory/aclear)

A basic memory implementation that simply stores the conversation history.

This stores the entire conversation history in memory without any
additional processing.

Equivalent to ConversationBufferMemory but tailored more specifically
for string-based conversations rather than chat models.

Note that additional processing may be required in some situations when the
conversation history is too large to fit in the context window of the model.

Prefix to use for AI generated responses.

Will always return list of memory variables.

Validate that return messages is not True.

Return history buffer.

Return history buffer.

Save context from this conversation to buffer.

Save context from this conversation to buffer.

Clear memory contents.