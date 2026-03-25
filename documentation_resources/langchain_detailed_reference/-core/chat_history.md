<!-- Source: https://reference.langchain.com/python/langchain-core/chat_history -->

Modulev1.2.21 (latest)●Since v0.1

# chat\_history

Chat message history stores a history of the message interactions in a chat.

## Functions

[function

get\_buffer\_string

Convert a sequence of messages to strings and concatenate them into one string.](/python/langchain-core/messages/utils/get_buffer_string)[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

HumanMessage

Message from the user.

A `HumanMessage` is a message that is passed in from a user to the model.](/python/langchain-core/messages/human/HumanMessage)[class

BaseChatMessageHistory

Abstract base class for storing chat message history.

Implementations guidelines:

Implementations are expected to over-ride all or some of the following methods:

- `add_messages`: sync variant for bulk addition of messages
- `aadd_messages`: async variant for bulk addition of messages
- `messages`: sync variant for getting messages
- `aget_messages`: async variant for getting messages
- `clear`: sync variant for clearing messages
- `aclear`: async variant for clearing messages

`add_messages` contains a default implementation that calls `add_message`
for each message in the sequence. This is provided for backwards compatibility
with existing implementations which only had `add_message`.

Async variants all have default implementations that call the sync variants.
Implementers can choose to override the async implementations to provide
truly async implementations.

Usage guidelines:

When used for updating history, users should favor usage of `add_messages`
over `add_message` or other variants like `add_user_message` and `add_ai_message`
to avoid unnecessary round-trips to the underlying persistence layer.](/python/langchain-core/chat_history/BaseChatMessageHistory)[class

InMemoryChatMessageHistory

In memory implementation of chat message history.

Stores messages in a memory list.](/python/langchain-core/chat_history/InMemoryChatMessageHistory)


