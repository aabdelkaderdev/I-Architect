<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/usage -->

Modulev1.2.21 (latest)●Since v0.3

# usage

Callback Handler that tracks `AIMessage.usage_metadata`.

## Functions

[function

add\_usage

Recursively add two UsageMetadata objects.](/python/langchain-core/messages/ai/add_usage)[function

register\_configure\_hook

Register a configure hook.](/python/langchain-core/tracers/context/register_configure_hook)[function

get\_usage\_metadata\_callback

Get usage metadata callback.

Get context manager for tracking usage metadata across chat model calls using
[`AIMessage.usage_metadata`](/python/langchain-core/callbacks/usage/UsageMetadataCallbackHandler/usage_metadata).](/python/langchain-core/callbacks/usage/get_usage_metadata_callback)

## Classes

[class

BaseCallbackHandler

Base callback handler.](/python/langchain-core/callbacks/base/BaseCallbackHandler)[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

UsageMetadata

Usage metadata for a message, such as token counts.

This is a standard representation of token usage that is consistent across models.](/python/langchain-core/messages/ai/UsageMetadata)[class

ChatGeneration

A single chat generation output.

A subclass of `Generation` that represents the response from a chat model that
generates chat messages.

The `message` attribute is a structured representation of the chat message. Most of
the time, the message will be of type `AIMessage`.

Users working with chat models will usually access information via either
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks).](/python/langchain-core/outputs/chat_generation/ChatGeneration)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)[class

UsageMetadataCallbackHandler

Callback Handler that tracks `AIMessage.usage_metadata`.](/python/langchain-core/callbacks/usage/UsageMetadataCallbackHandler)


