<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/core -->

Modulev1.2.21 (latest)●Since v0.2

# core

Utilities for the root listener.

## Attributes

[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)[attribute

logger](/python/langchain-core/tracers/core/logger)[attribute

SCHEMA\_FORMAT\_TYPE: Literal['original', 'streaming\_events']](/python/langchain-core/tracers/core/SCHEMA_FORMAT_TYPE)

## Functions

[function

dumpd

Return a dict representation of an object.](/python/langchain-core/load/dump/dumpd)

## Classes

[class

TracerException

Base class for exceptions in tracers module.](/python/langchain-core/exceptions/TracerException)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

ChatGeneration

A single chat generation output.

A subclass of `Generation` that represents the response from a chat model that
generates chat messages.

The `message` attribute is a structured representation of the chat message. Most of
the time, the message will be of type `AIMessage`.

Users working with chat models will usually access information via either
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks).](/python/langchain-core/outputs/chat_generation/ChatGeneration)[class

ChatGenerationChunk

`ChatGeneration` chunk.

`ChatGeneration` chunks can be concatenated with other `ChatGeneration` chunks.](/python/langchain-core/outputs/chat_generation/ChatGenerationChunk)[class

GenerationChunk

`GenerationChunk`, which can be concatenated with other `Generation` chunks.](/python/langchain-core/outputs/generation/GenerationChunk)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)


