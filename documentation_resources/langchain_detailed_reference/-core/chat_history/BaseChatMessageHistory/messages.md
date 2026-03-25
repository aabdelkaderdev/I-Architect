<!-- Source: https://reference.langchain.com/python/langchain-core/chat_history/BaseChatMessageHistory/messages -->

Attributev1.2.21 (latest)●Since v0.1

# messages

A property or attribute that returns a list of messages.

In general, getting the messages may involve IO to the underlying persistence
layer, so this operation is expected to incur some latency.


```
messages: list[BaseMessage]
```


