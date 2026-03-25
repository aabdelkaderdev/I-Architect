<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base -->

Modulev1.2.21 (latest)●Since v0.1

# base

Base interfaces for tracing runs.

## Attributes

[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)[attribute

logger](/python/langchain-core/tracers/base/logger)

## Classes

[class

AsyncCallbackHandler

Base async callback handler.](/python/langchain-core/callbacks/base/AsyncCallbackHandler)[class

BaseCallbackHandler

Base callback handler.](/python/langchain-core/callbacks/base/BaseCallbackHandler)[class

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

ChatGenerationChunk

`ChatGeneration` chunk.

`ChatGeneration` chunks can be concatenated with other `ChatGeneration` chunks.](/python/langchain-core/outputs/chat_generation/ChatGenerationChunk)[class

GenerationChunk

`GenerationChunk`, which can be concatenated with other `Generation` chunks.](/python/langchain-core/outputs/generation/GenerationChunk)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)[class

BaseTracer

Base interface for tracers.](/python/langchain-core/tracers/base/BaseTracer)[class

AsyncBaseTracer

Async base interface for tracers.](/python/langchain-core/tracers/base/AsyncBaseTracer)


