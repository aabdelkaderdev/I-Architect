<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/sequential -->

Modulev1.2.13 (latest)●Since v1.0

# sequential

Chain pipeline where the outputs of one step feed directly into next.

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

SequentialChain

Chain where the outputs of one chain feed directly into next.](/python/langchain-classic/chains/sequential/SequentialChain)[class

SimpleSequentialChain

Simple chain where the outputs of one step feed directly into next.](/python/langchain-classic/chains/sequential/SimpleSequentialChain)


