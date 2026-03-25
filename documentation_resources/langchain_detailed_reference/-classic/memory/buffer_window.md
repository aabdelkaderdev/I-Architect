<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/buffer_window -->

Modulev1.2.13 (latest)●Since v1.0

# buffer\_window

## Classes

[deprecatedclass

BaseChatMemory

Abstract base class for chat memory.

**ATTENTION** This abstraction was created prior to when chat models had
native tool calling capabilities.
It does **NOT** support native tool calling capabilities for chat models and
will fail SILENTLY if used with a chat model that has native tool calling.

DO NOT USE THIS ABSTRACTION FOR NEW CODE.](/python/langchain-classic/memory/chat_memory/BaseChatMemory)[deprecatedclass

ConversationBufferWindowMemory

Use to keep track of the last k turns of a conversation.

If the number of messages in the conversation is more than the maximum number
of messages to keep, the oldest messages are dropped.](/python/langchain-classic/memory/buffer_window/ConversationBufferWindowMemory)


