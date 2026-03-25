<!-- Source: https://reference.langchain.com/python/langchain-classic/schema -->

Modulev1.2.13 (latest)●Since v1.0

# schema

**Schemas** are the LangChain Base Classes and Interfaces.

## Attributes

[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)[attribute

Memory: BaseMemory](/python/langchain-classic/schema/Memory)

## Classes

[deprecatedclass

BaseMemory](/python/langchain-classic/base_memory/BaseMemory)

## Modules

[module

messages](/python/langchain-classic/schema/messages)[module

prompt\_template](/python/langchain-classic/schema/prompt_template)



[module

embeddings](/python/langchain-classic/schema/embeddings)

[module

chat\_history](/python/langchain-classic/schema/chat_history)

[module

cache](/python/langchain-classic/schema/cache)

[module

document](/python/langchain-classic/schema/document)

[module

vectorstore](/python/langchain-classic/schema/vectorstore)

[module

storage](/python/langchain-classic/schema/storage)

[module

language\_model](/python/langchain-classic/schema/language_model)

[module

memory](/python/langchain-classic/schema/memory)

[module

exceptions](/python/langchain-classic/schema/exceptions)

[module

agent](/python/langchain-classic/schema/agent)

[module

prompt](/python/langchain-classic/schema/prompt)

[module

output](/python/langchain-classic/schema/output)

[module

chat](/python/langchain-classic/schema/chat)

[module

retriever](/python/langchain-classic/schema/retriever)

[module

output\_parser](/python/langchain-classic/schema/output_parser)

[module

callbacks](/python/langchain-classic/schema/callbacks)

[module

runnable](/python/langchain-classic/schema/runnable)

Abstract base class for memory in Chains.

Memory refers to state in Chains. Memory can be used to store information about
past executions of a Chain and inject that information into the inputs of
future executions of the Chain. For example, for conversational Chains Memory
can be used to store conversations and automatically add them to future model
prompts so that the model has the necessary context to respond coherently to
the latest input.

LangChain **Runnable** and the **LangChain Expression Language (LCEL)**.

The LangChain Expression Language (LCEL) offers a declarative method to build
production-grade programs that harness the power of LLMs.

Programs created using LCEL and LangChain Runnables inherently support
synchronous, asynchronous, batch, and streaming operations.

Support for **async** allows servers hosting LCEL based programs to scale better
for higher concurrent loads.

**Streaming** of intermediate outputs as they're being generated allows for
creating more responsive UX.

This module contains schema and implementation of LangChain Runnables primitives.