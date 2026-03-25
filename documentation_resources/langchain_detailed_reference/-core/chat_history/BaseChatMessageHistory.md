<!-- Source: https://reference.langchain.com/python/langchain-core/chat_history/BaseChatMessageHistory -->

Classv1.2.21 (latest)●Since v0.1

# BaseChatMessageHistory

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
to avoid unnecessary round-trips to the underlying persistence layer.


```
BaseChatMessageHistory()
```

## Bases

`ABC`

**Example:**

```
import json
import os
from langchain_core.messages import messages_from_dict, message_to_dict

class FileChatMessageHistory(BaseChatMessageHistory):
    storage_path: str
    session_id: str

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(
                os.path.join(self.storage_path, self.session_id),
                "r",
                encoding="utf-8",
            ) as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)  # Existing messages
        all_messages.extend(messages)  # Add new messages

        serialized = [message_to_dict(message) for message in all_messages]
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def clear(self) -> None:
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
```

## Attributes

[attribute

messages: list[BaseMessage]

A property or attribute that returns a list of messages.

In general, getting the messages may involve IO to the underlying persistence
layer, so this operation is expected to incur some latency.](/python/langchain-core/chat_history/BaseChatMessageHistory/messages)

## Methods

[method

aget\_messages

Async version of getting messages.

Can over-ride this method to provide an efficient async implementation.

In general, fetching messages may involve IO to the underlying persistence
layer.](/python/langchain-core/chat_history/BaseChatMessageHistory/aget_messages)[method

add\_user\_message

Convenience method for adding a human message string to the store.

Note

This is a convenience method. Code should favor the bulk `add_messages`
interface instead to save on round-trips to the persistence layer.

This method may be deprecated in a future release.](/python/langchain-core/chat_history/BaseChatMessageHistory/add_user_message)[method

add\_ai\_message

Convenience method for adding an `AIMessage` string to the store.

Note

This is a convenience method. Code should favor the bulk `add_messages`
interface instead to save on round-trips to the persistence layer.

This method may be deprecated in a future release.](/python/langchain-core/chat_history/BaseChatMessageHistory/add_ai_message)[method

add\_message

Add a Message object to the store.](/python/langchain-core/chat_history/BaseChatMessageHistory/add_message)[method

add\_messages

Add a list of messages.

Implementations should over-ride this method to handle bulk addition of messages
in an efficient manner to avoid unnecessary round-trips to the underlying store.](/python/langchain-core/chat_history/BaseChatMessageHistory/add_messages)[method

aadd\_messages

Async add a list of messages.](/python/langchain-core/chat_history/BaseChatMessageHistory/aadd_messages)[method

clear

Remove all messages from the store.](/python/langchain-core/chat_history/BaseChatMessageHistory/clear)[method

aclear

Async remove all messages from the store.](/python/langchain-core/chat_history/BaseChatMessageHistory/aclear)


