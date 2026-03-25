<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/combined/CombinedMemory -->

Classv1.2.13 (latest)●Since v1.0

# CombinedMemory


```
CombinedMemory()
```

## Bases

`BaseMemory`

## Attributes

## Methods

## Inherited from[BaseMemory](/python/langchain-classic/base_memory/BaseMemory)

### Attributes

[Amodel\_config](/python/langchain-classic/base_memory/BaseMemory/model_config)

### Methods

[Maload\_memory\_variables

—

Async return key-value pairs given the text input to the chain.](/python/langchain-classic/base_memory/BaseMemory/aload_memory_variables)[Masave\_context

—

Async save the context of this chain run to memory.](/python/langchain-classic/base_memory/BaseMemory/asave_context)[M](/python/langchain-classic/base_memory/BaseMemory/aclear)



aclear

—

Async clear memory contents.

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

memories: list[BaseMemory]

For tracking all the memories that should be accessed.](/python/langchain-classic/memory/combined/CombinedMemory/memories)

[attribute

memory\_variables: list[str]

All the memory variables that this instance provides.](/python/langchain-classic/memory/combined/CombinedMemory/memory_variables)

[method

check\_input\_key

Check that if memories are of type BaseChatMemory that input keys exist.](/python/langchain-classic/memory/combined/CombinedMemory/check_input_key)

[method

load\_memory\_variables

Load all vars from sub-memories.](/python/langchain-classic/memory/combined/CombinedMemory/load_memory_variables)

[method

save\_context

Save context from this session for every memory.](/python/langchain-classic/memory/combined/CombinedMemory/save_context)

[method

clear

Clear context from this session for every memory.](/python/langchain-classic/memory/combined/CombinedMemory/clear)

Combining multiple memories' data together.