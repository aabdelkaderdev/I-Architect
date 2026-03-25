<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/chat_result -->

Modulev1.2.21 (latest)●Since v0.1

# chat\_result

Chat result schema.

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

ChatResult

Use to represent the result of a chat model call with a single prompt.

This container is used internally by some implementations of chat model, it will
eventually be mapped to a more general `LLMResult` object, and then projected into
an `AIMessage` object.

LangChain users working with chat models will usually access information via
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks). Please refer the `AIMessage` and `LLMResult` schema documentation for
more information.](/python/langchain-core/outputs/chat_result/ChatResult)


