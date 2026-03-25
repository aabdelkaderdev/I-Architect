<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Base interface that all chains should implement.

## Attributes

[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)[attribute

logger](/python/langchain-classic/chains/base/logger)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[deprecatedclass

BaseMemory

Abstract base class for memory in Chains.

Memory refers to state in Chains. Memory can be used to store information about
past executions of a Chain and inject that information into the inputs of
future executions of the Chain. For example, for conversational Chains Memory
can be used to store conversations and automatically add them to future model
prompts so that the model has the necessary context to respond coherently to
the latest input.](/python/langchain-classic/base_memory/BaseMemory)


