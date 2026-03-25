<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/natbot/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Implement an LLM driven browser.

## Attributes

[attribute

PROMPT](/python/langchain-classic/chains/natbot/prompt/PROMPT)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[deprecatedclass

NatBotChain

Implement an LLM driven browser.

**Security Note**: This toolkit provides code to control a web-browser.

```
The web-browser can be used to navigate to:

- Any URL (including any internal network URLs)
- And local files

Exercise care if exposing this chain to end-users. Control who is able to
access and use this chain, and isolate the network access of the server
that hosts this chain.

See https://docs.langchain.com/oss/python/security-policy for more information.
```](/python/langchain-classic/chains/natbot/base/NatBotChain)


