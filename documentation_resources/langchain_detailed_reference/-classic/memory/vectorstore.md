<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/vectorstore -->

Modulev1.2.13 (latest)●Since v1.0

# vectorstore

Class for a VectorStore-backed memory object.

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

VectorStoreRetrieverMemory

Vector Store Retriever Memory.

Store the conversation history in a vector store and retrieves the relevant
parts of past conversation based on the input.](/python/langchain-classic/memory/vectorstore/VectorStoreRetrieverMemory)


