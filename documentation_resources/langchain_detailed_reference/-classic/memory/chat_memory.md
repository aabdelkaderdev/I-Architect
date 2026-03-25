<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/chat_memory -->

Modulev1.2.13 (latest)●Since v1.0

# chat\_memory

## Functions

[function

get\_prompt\_input\_key

Get the prompt input key.](/python/langchain-classic/memory/utils/get_prompt_input_key)

## Classes

[deprecatedclass

BaseMemory

Abstract base class for memory in Chains.

Memory refers to state in Chains. Memory can be used to store information about
past executions of a Chain and inject that information into the inputs of
future executions of the Chain. For example, for conversational Chains Memory
can be used to store conversations and automatically add them to future model
prompts so that the model has the necessary context to respond coherently to
the latest input.](/python/langchain-classic/base_memory/BaseMemory)[deprecatedclass

BaseChatMemory

Abstract base class for chat memory.

**ATTENTION** This abstraction was created prior to when chat models had
native tool calling capabilities.
It does **NOT** support native tool calling capabilities for chat models and
will fail SILENTLY if used with a chat model that has native tool calling.

DO NOT USE THIS ABSTRACTION FOR NEW CODE.](/python/langchain-classic/memory/chat_memory/BaseChatMemory)


