<!-- Source: https://reference.langchain.com/python/langchain-classic/base_memory -->

Modulev1.2.13 (latest)●Since v1.0

# base\_memory

**Memory** maintains Chain state, incorporating context from past runs.

This module contains memory abstractions from LangChain v0.0.x.

These abstractions are now deprecated and will be removed in LangChain v1.0.0.

## Classes

[deprecatedclass

BaseMemory

Abstract base class for memory in Chains.

Memory refers to state in Chains. Memory can be used to store information about
past executions of a Chain and inject that information into the inputs of
future executions of the Chain. For example, for conversational Chains Memory
can be used to store conversations and automatically add them to future model
prompts so that the model has the necessary context to respond coherently to
the latest input.](/python/langchain-classic/base_memory/BaseMemory)


