<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/summarization -->

Modulev1.2.13 (latest)●Since v0.3

# summarization

## Attributes

## Functions

## Classes

## Type Aliases



[attribute

ResponseT](/python/langchain/agents/middleware/summarization/ResponseT)

[attribute

TokenCounter: Callable[[Iterable[MessageLikeRepresentation]], int]](/python/langchain/agents/middleware/summarization/TokenCounter)

[attribute

DEFAULT\_SUMMARY\_PROMPT: str](/python/langchain/agents/middleware/summarization/DEFAULT_SUMMARY_PROMPT)

[attribute

ContextFraction: tuple[Literal['fraction'], float]](/python/langchain/agents/middleware/summarization/ContextFraction)

[attribute

ContextTokens: tuple[Literal['tokens'], int]](/python/langchain/agents/middleware/summarization/ContextTokens)

[attribute

ContextMessages: tuple[Literal['messages'], int]](/python/langchain/agents/middleware/summarization/ContextMessages)

[function

init\_chat\_model](/python/langchain/agents/middleware/summarization/init_chat_model)

[class

AgentMiddleware](/python/langchain/agents/middleware/summarization/AgentMiddleware)

[class

AgentState](/python/langchain/agents/middleware/summarization/AgentState)

[class

SummarizationMiddleware](/python/langchain/agents/middleware/summarization/SummarizationMiddleware)

[typeAlias

ContextSize](/python/langchain/agents/middleware/summarization/ContextSize)

Summarization middleware.

Fraction of model's maximum input tokens.

Absolute number of tokens.

Absolute number of messages.

Initialize a chat model from any supported provider using a unified interface.

**Two main use cases:**

1. **Fixed model** – specify the model upfront and get a ready-to-use chat model.
2. **Configurable model** – choose to specify parameters (including model name) at
   runtime via `config`. Makes it easy to switch between models/providers without
   changing your code

Installation requirements

Requires the integration package for the chosen model provider to be installed.

See the `model_provider` parameter below for specific package names
(e.g., `pip install langchain-openai`).

Refer to the [provider integration's API reference](https://docs.langchain.com/oss/python/integrations/providers)
for supported model parameters to use as `**kwargs`.

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.

State schema for the agent.

Summarizes conversation history when token limits are approached.

This middleware monitors message token counts and automatically summarizes older
messages when a threshold is reached, preserving recent messages and maintaining
context continuity by ensuring AI/Tool message pairs remain together.

Union type for context size specifications.

Can be either:

- [`ContextFraction`](/python/langchain/agents/middleware/summarization/ContextFraction): A
  fraction of the model's maximum input tokens.
- [`ContextTokens`](/python/langchain/agents/middleware/summarization/ContextTokens): An absolute
  number of tokens.
- [`ContextMessages`](/python/langchain/agents/middleware/summarization/ContextMessages): An
  absolute number of messages.

Depending on use with `trigger` or `keep` parameters, this type indicates either
when to trigger summarization or how much context to retain.