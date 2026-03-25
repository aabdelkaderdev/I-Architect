<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/moderation -->

Modulev1.2.13 (latest)●Since v1.0

# moderation

Pass input through a moderation endpoint.

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

OpenAIModerationChain

Pass input through a moderation endpoint.

To use, you should have the `openai` python package installed, and the
environment variable `OPENAI_API_KEY` set with your API key.

Any parameters that are valid to be passed to the openai.create call can be passed
in, even if not explicitly saved on this class.](/python/langchain-classic/chains/moderation/OpenAIModerationChain)


