<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/llm_result -->

Modulev1.2.21 (latest)●Since v0.1

# llm\_result

`LLMResult` class.

## Classes

[class

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

Generation

A single text generation output.

Generation represents the response from an "old-fashioned" LLM (string-in,
string-out) that generates regular text (not chat messages).

This model is used internally by chat model and will eventually be mapped to a more
general `LLMResult` object, and then projected into an `AIMessage` object.

LangChain users working with chat models will usually access information via
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks). Please refer to `AIMessage` and `LLMResult` for more information.](/python/langchain-core/outputs/generation/Generation)[class

GenerationChunk

`GenerationChunk`, which can be concatenated with other `Generation` chunks.](/python/langchain-core/outputs/generation/GenerationChunk)[class

RunInfo

Class that contains metadata for a single execution of a chain or model.

Defined for backwards compatibility with older versions of `langchain_core`.

Users can acquire the `run_id` information from callbacks or via `run_id`
information present in the `astream_event` API (depending on the use case).](/python/langchain-core/outputs/run_info/RunInfo)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)


