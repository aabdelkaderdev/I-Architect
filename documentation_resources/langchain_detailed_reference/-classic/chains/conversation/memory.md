<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/conversation/memory -->

Modulev1.2.13 (latest)●Since v1.0

# memory

Memory modules for conversation prompts.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/chains/conversation/memory/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)

## Classes

[class

CombinedMemory

Combining multiple memories' data together.](/python/langchain-classic/memory/combined/CombinedMemory)[deprecatedclass

ConversationBufferMemory

A basic memory implementation that simply stores the conversation history.

This stores the entire conversation history in memory without any
additional processing.

Note that additional processing may be required in some situations when the
conversation history is too large to fit in the context window of the model.](/python/langchain-classic/memory/buffer/ConversationBufferMemory)[deprecatedclass

ConversationStringBufferMemory

A basic memory implementation that simply stores the conversation history.

This stores the entire conversation history in memory without any
additional processing.

Equivalent to ConversationBufferMemory but tailored more specifically
for string-based conversations rather than chat models.

Note that additional processing may be required in some situations when the
conversation history is too large to fit in the context window of the model.](/python/langchain-classic/memory/buffer/ConversationStringBufferMemory)[deprecatedclass

ConversationBufferWindowMemory

Use to keep track of the last k turns of a conversation.

If the number of messages in the conversation is more than the maximum number
of messages to keep, the oldest messages are dropped.](/python/langchain-classic/memory/buffer_window/ConversationBufferWindowMemory)[deprecatedclass

ConversationEntityMemory

Entity extractor & summarizer memory.

Extracts named entities from the recent chat history and generates summaries.
With a swappable entity store, persisting entities across conversations.
Defaults to an in-memory entity store, and can be swapped out for a Redis,
SQLite, or other entity store.](/python/langchain-classic/memory/entity/ConversationEntityMemory)[deprecatedclass

ConversationSummaryMemory

Continually summarizes the conversation history.

The summary is updated after each conversation turn.
The implementations returns a summary of the conversation history which
can be used to provide context to the model.](/python/langchain-classic/memory/summary/ConversationSummaryMemory)[deprecatedclass

ConversationSummaryBufferMemory

Buffer with summarizer for storing conversation memory.

Provides a running summary of the conversation together with the most recent
messages in the conversation under the constraint that the total number of
tokens in the conversation does not exceed a certain limit.](/python/langchain-classic/memory/summary_buffer/ConversationSummaryBufferMemory)


