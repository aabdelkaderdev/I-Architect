<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/entity/ConversationEntityMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# ConversationEntityMemory


```
ConversationEntityMemory()
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

Save context from this conversation to buffer.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/asave_context)[Maclear

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

Async save the context of this chain run to memory.](/python/langchain-classic/base_memory/BaseMemory/asave_context)[Maclear

—

Async clear memory contents.](/python/langchain-classic/base_memory/BaseMemory/aclear)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

human\_prefix: str](/python/langchain-classic/memory/entity/ConversationEntityMemory/human_prefix)

[attribute

ai\_prefix: str](/python/langchain-classic/memory/entity/ConversationEntityMemory/ai_prefix)

[attribute

llm: BaseLanguageModel](/python/langchain-classic/memory/entity/ConversationEntityMemory/llm)

[attribute

entity\_extraction\_prompt: BasePromptTemplate](/python/langchain-classic/memory/entity/ConversationEntityMemory/entity_extraction_prompt)

[attribute

entity\_summarization\_prompt: BasePromptTemplate](/python/langchain-classic/memory/entity/ConversationEntityMemory/entity_summarization_prompt)

[attribute

entity\_cache: list[str]](/python/langchain-classic/memory/entity/ConversationEntityMemory/entity_cache)

[attribute

k: int](/python/langchain-classic/memory/entity/ConversationEntityMemory/k)

[attribute

chat\_history\_key: str](/python/langchain-classic/memory/entity/ConversationEntityMemory/chat_history_key)

[attribute

entity\_store: BaseEntityStore](/python/langchain-classic/memory/entity/ConversationEntityMemory/entity_store)

[attribute

buffer: list[BaseMessage]

Access chat memory messages.](/python/langchain-classic/memory/entity/ConversationEntityMemory/buffer)

[attribute

memory\_variables: list[str]

Will always return list of memory variables.](/python/langchain-classic/memory/entity/ConversationEntityMemory/memory_variables)

[method

load\_memory\_variables

Load memory variables.

Returns chat history and all generated entities with summaries if available,
and updates or clears the recent entity cache.

New entity name can be found when calling this method, before the entity
summaries are generated, so the entity cache values may be empty if no entity
descriptions are generated yet.](/python/langchain-classic/memory/entity/ConversationEntityMemory/load_memory_variables)

[method

save\_context

Save context from this conversation history to the entity store.

Generates a summary for each entity in the entity cache by prompting
the model, and saves these summaries to the entity store.](/python/langchain-classic/memory/entity/ConversationEntityMemory/save_context)

[method

clear

Clear memory contents.](/python/langchain-classic/memory/entity/ConversationEntityMemory/clear)

Entity extractor & summarizer memory.

Extracts named entities from the recent chat history and generates summaries.
With a swappable entity store, persisting entities across conversations.
Defaults to an in-memory entity store, and can be swapped out for a Redis,
SQLite, or other entity store.