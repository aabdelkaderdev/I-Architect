<!-- Source: https://reference.langchain.com/python/langchain-core/chat_history/BaseChatMessageHistory/aget_messages -->

Methodv1.2.21 (latest)●Since v0.1

# aget\_messages

Async version of getting messages.

Can over-ride this method to provide an efficient async implementation.

In general, fetching messages may involve IO to the underlying persistence
layer.


```
aget_messages(
    self,
) -> list[BaseMessage]
```


