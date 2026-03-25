<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/router/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Base classes for chain routing.

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

Route

A route to a destination chain.](/python/langchain-classic/chains/router/base/Route)[class

RouterChain

Chain that outputs the name of a destination chain and the inputs to it.](/python/langchain-classic/chains/router/base/RouterChain)[class

MultiRouteChain

Use a single chain to route an input to one of multiple candidate chains.](/python/langchain-classic/chains/router/base/MultiRouteChain)


