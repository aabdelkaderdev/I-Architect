<!-- Source: https://reference.langchain.com/python/langchain/langchain -->

Modulev1.2.13 (latest)●Since v0.3

# langchain

Main entrypoint into LangChain.

## Modules

[module

messages

Message and message content types.

Includes message types for different roles (e.g., human, AI, system), as well as types
for message content blocks (e.g., text, image, audio) and tool calls.](/python/langchain/messages)[module

embeddings

Embeddings models.

Modules moved

With the release of `langchain 1.0.0`, several embeddings modules were moved to
`langchain-classic`, such as `CacheBackedEmbeddings` and all community
embeddings. See [list](https://github.com/langchain-ai/langchain/blob/bdf1cd383ce36dc18381a3bf3fb0a579337a32b5/libs/langchain/langchain/embeddings/__init__.py)
of moved modules to inform your migration.](/python/langchain/embeddings)[module

chat\_models

Entrypoint to using [chat models](https://docs.langchain.com/oss/python/langchain/models) in LangChain.](/python/langchain/chat_models)[module

agents

Entrypoint to building [Agents](https://docs.langchain.com/oss/python/langchain/agents) with LangChain.](/python/langchain/agents)[module

rate\_limiters

Base abstraction and in-memory implementation of rate limiters.

These rate limiters can be used to limit the rate of requests to an API.

The rate limiters can be used together with `BaseChatModel`.](/python/langchain/rate_limiters)[module

tools

Tools.](/python/langchain/tools)


