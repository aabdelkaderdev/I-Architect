<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory -->

Classv1.2.13 (latest)●Since v1.0

# AgentTokenBufferMemory


```
AgentTokenBufferMemory()
```

## Bases

`BaseChatMemory`

## Attributes

## Methods

## Inherited from[BaseChatMemory](/python/langchain-classic/memory/chat_memory/BaseChatMemory)

### Attributes

[Achat\_memory: BaseChatMessageHistory](/python/langchain-classic/memory/chat_memory/BaseChatMemory/chat_memory)[Ainput\_key: str | None](/python/langchain-classic/memory/chat_memory/BaseChatMemory/input_key)

### Methods

[Masave\_context

—

Save context from this conversation to buffer.](/python/langchain-classic/memory/chat_memory/BaseChatMemory/asave_context)[Mclear](/python/langchain-classic/memory/chat_memory/BaseChatMemory/clear)



—

Clear memory contents.

[Maclear

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

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `human_prefix`\* | `unknown` | Prefix for human messages. |
| `ai_prefix`\* | `unknown` | Prefix for AI messages. |
| `llm`\* | `unknown` | Language model. |
| `memory_key`\* | `unknown` | Key to save memory under. |
| `max_token_limit`\* | `unknown` | Maximum number of tokens to keep in the buffer. Once the buffer exceeds this many tokens, the oldest messages will be pruned. |
| `return_messages`\* | `unknown` | Whether to return messages. |
| `output_key`\* | `unknown` |  |
| `intermediate_steps_key`\* | `unknown` |  |
| `format_as_tools`\* | `unknown` |  |

[attribute

human\_prefix: str](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/human_prefix)

[attribute

ai\_prefix: str](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/ai_prefix)

[attribute

llm: BaseLanguageModel](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/llm)

[attribute

memory\_key: str](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/memory_key)

[attribute

max\_token\_limit: int

The max number of tokens to keep in the buffer.
Once the buffer exceeds this many tokens, the oldest messages will be pruned.](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/max_token_limit)

[attribute

return\_messages: bool](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/return_messages)

[attribute

output\_key: str](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/output_key)

[attribute

intermediate\_steps\_key: str](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/intermediate_steps_key)

[attribute

format\_as\_tools: bool](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/format_as_tools)

[attribute

buffer: list[BaseMessage]

String buffer of memory.](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/buffer)

[attribute

memory\_variables: list[str]

Always return list of memory variables.](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/memory_variables)

[method

load\_memory\_variables

Return history buffer.](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/load_memory_variables)

[method

save\_context

Save context from this conversation to buffer. Pruned.](/python/langchain-classic/agents/openai_functions_agent/agent_token_buffer_memory/AgentTokenBufferMemory/save_context)

Memory used to save agent output AND intermediate steps.

Key to save output under.

Key to save intermediate steps under.

Whether to format as tools.