<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# VectorStoreRetrieverMemory


```
VectorStoreRetrieverMemory()
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

retriever: VectorStoreRetriever](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/retriever)

[attribute

memory\_key: str](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/memory_key)

[attribute

input\_key: str | None](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/input_key)

[attribute

return\_docs: bool](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/return_docs)

[attribute

exclude\_input\_keys: Sequence[str]](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/exclude_input_keys)

[attribute

memory\_variables: list[str]](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/memory_variables)

[method

load\_memory\_variables](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/load_memory_variables)

[method

aload\_memory\_variables](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/aload_memory_variables)

[method

save\_context](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/save_context)

[method

asave\_context](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/asave_context)

[method

clear](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/clear)

[method

aclear](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory/aclear)

Vector Store Retriever Memory.

Store the conversation history in a vector store and retrieves the relevant
parts of past conversation based on the input.

VectorStoreRetriever object to connect to.

Key name to locate the memories in the result of load\_memory\_variables.

Key name to index the inputs to load\_memory\_variables.

Whether or not to return the result of querying the database directly.

Input keys to exclude in addition to memory key when constructing the document

The list of keys emitted from the load\_memory\_variables method.

Return history buffer.

Return history buffer.

Save context from this conversation to buffer.

Save context from this conversation to buffer.

Nothing to clear.

Nothing to clear.