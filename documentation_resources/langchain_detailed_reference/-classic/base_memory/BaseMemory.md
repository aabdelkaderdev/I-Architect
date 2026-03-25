<!-- Source: https://reference.langchain.com/python/langchain-classic/base_memory/BaseMemory -->

Classv1.2.13 (latest)●Since v1.0Deprecated

# BaseMemory


```
BaseMemory()
```

## Bases

`Serializable``ABC`

## Attributes

## Methods

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)



M

lc\_id

[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)

[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

[attribute

model\_config](/python/langchain-classic/base_memory/BaseMemory/model_config)

[attribute

memory\_variables: list[str]](/python/langchain-classic/base_memory/BaseMemory/memory_variables)

[method

load\_memory\_variables](/python/langchain-classic/base_memory/BaseMemory/load_memory_variables)

[method

aload\_memory\_variables](/python/langchain-classic/base_memory/BaseMemory/aload_memory_variables)

[method

save\_context](/python/langchain-classic/base_memory/BaseMemory/save_context)

[method

asave\_context](/python/langchain-classic/base_memory/BaseMemory/asave_context)

[method

clear](/python/langchain-classic/base_memory/BaseMemory/clear)

[method

aclear](/python/langchain-classic/base_memory/BaseMemory/aclear)

Abstract base class for memory in Chains.

Memory refers to state in Chains. Memory can be used to store information about
past executions of a Chain and inject that information into the inputs of
future executions of the Chain. For example, for conversational Chains Memory
can be used to store conversations and automatically add them to future model
prompts so that the model has the necessary context to respond coherently to
the latest input.

**Example:**

```
class SimpleMemory(BaseMemory):
    memories: dict[str, Any] = dict()

    @property
    def memory_variables(self) -> list[str]:
        return list(self.memories.keys())

    def load_memory_variables(self, inputs: dict[str, Any]) -> dict[str, str]:
        return self.memories

    def save_context(
        self, inputs: dict[str, Any], outputs: dict[str, str]
    ) -> None:
        pass

    def clear(self) -> None:
        pass
```

The string keys this memory class will add to chain inputs.

Return key-value pairs given the text input to the chain.

Async return key-value pairs given the text input to the chain.

Save the context of this chain run to memory.

Async save the context of this chain run to memory.

Clear memory contents.

Async clear memory contents.