<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConversationTokenBufferMemory


```
ConversationTokenBufferMemory()
```

## Bases

`BaseChatMemory`

## Attributes

## Methods

## Inherited from[BaseChatMemory](/python/langchain-classic/memory/chat_memory/BaseChatMemory)

### Attributes

[Achat\_memory: BaseChatMessageHistory](/python/langchain-classic/memory/chat_memory/BaseChatMemory/chat_memory)[Aoutput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/output_key)[Ainput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/input_key)[Areturn\_messages: bool](/python/langchain-classic/memory/chat_memory/BaseChatMemory/return_messages)

### Methods



[Masave\_context

—

Save context from this conversation to buffer.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/asave_context)[Mclear

—

Clear memory contents.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/clear)[Maclear

—

Clear memory contents.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/aclear)

## Inherited from[BaseMemory](/python/langchain-classic/base_memory/BaseMemory)

### Attributes

[Amodel\_config](/python/langchain-classic/base_memory/BaseMemory/model_config)

### Methods

[Maload\_memory\_variables

—

Async return key-value pairs given the text input to the chain.](/python/langchain-classic/base_memory/BaseMemory/aload_memory_variables)[Masave\_context

—

Async save the context of this chain run to memory.](/python/langchain-classic/base_memory/BaseMemory/asave_context)[Mclear

—

Clear memory contents.](/python/langchain-classic/base_memory/BaseMemory/clear)[Maclear

—

Async clear memory contents.](/python/langchain-classic/base_memory/BaseMemory/aclear)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

human\_prefix: str](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/human_prefix)

[attribute

ai\_prefix: str](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/ai_prefix)

[attribute

llm: BaseLanguageModel](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/llm)

[attribute

memory\_key: str](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/memory_key)

[attribute

max\_token\_limit: int](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/max_token_limit)

[attribute

buffer: Any

String buffer of memory.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/buffer)

[attribute

buffer\_as\_str: str

Exposes the buffer as a string in case return\_messages is False.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/buffer_as_str)

[attribute

buffer\_as\_messages: list[BaseMessage]

Exposes the buffer as a list of messages in case return\_messages is True.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/buffer_as_messages)

[attribute

memory\_variables: list[str]

Will always return list of memory variables.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/memory_variables)

[method

load\_memory\_variables

Return history buffer.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/load_memory_variables)

[method

save\_context

Save context from this conversation to buffer. Pruned.](/python/langchain-classic/memory/token_buffer/ConversationTokenBufferMemory/save_context)

Conversation chat memory with token limit.

Keeps only the most recent messages in the conversation under the constraint
that the total number of tokens in the conversation does not exceed a certain limit.