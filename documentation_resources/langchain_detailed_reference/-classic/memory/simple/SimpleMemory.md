<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/simple/SimpleMemory -->

Classv1.2.13 (latest)●Since v1.0

# SimpleMemory


```
SimpleMemory()
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

memories: dict[str, Any]](/python/langchain-classic/memory/simple/SimpleMemory/memories)

[attribute

memory\_variables: list[str]](/python/langchain-classic/memory/simple/SimpleMemory/memory_variables)

[method

load\_memory\_variables](/python/langchain-classic/memory/simple/SimpleMemory/load_memory_variables)

[method

save\_context

Nothing should be saved or changed, my memory is set in stone.](/python/langchain-classic/memory/simple/SimpleMemory/save_context)

[method

clear

Nothing to clear, got a memory like a vault.](/python/langchain-classic/memory/simple/SimpleMemory/clear)

Simple Memory.

Simple memory for storing context or other information that shouldn't
ever change between prompts.