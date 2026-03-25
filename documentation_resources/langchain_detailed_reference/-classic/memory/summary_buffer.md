<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/summary_buffer -->

Modulev1.2.13 (latest)●Since v1.0

# summary\_buffer

## Classes

[deprecatedclass

BaseChatMemory

Abstract base class for chat memory.

**ATTENTION** This abstraction was created prior to when chat models had
native tool calling capabilities.
It does **NOT** support native tool calling capabilities for chat models and
will fail SILENTLY if used with a chat model that has native tool calling.

DO NOT USE THIS ABSTRACTION FOR NEW CODE.](/python/langchain-classic/memory/chat_memory/BaseChatMemory)[deprecatedclass

SummarizerMixin

Mixin for summarizer.](/python/langchain-classic/memory/summary/SummarizerMixin)[deprecatedclass

ConversationSummaryBufferMemory

Buffer with summarizer for storing conversation memory.

Provides a running summary of the conversation together with the most recent
messages in the conversation under the constraint that the total number of
tokens in the conversation does not exceed a certain limit.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory)


