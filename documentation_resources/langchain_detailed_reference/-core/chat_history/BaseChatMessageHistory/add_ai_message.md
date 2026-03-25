<!-- Source: https://reference.langchain.com/python/langchain-core/chat_history/BaseChatMessageHistory/add_ai_message -->

Methodv1.2.21 (latest)●Since v0.1

# add\_ai\_message

Convenience method for adding an `AIMessage` string to the store.

Note

This is a convenience method. Code should favor the bulk `add_messages`
interface instead to save on round-trips to the persistence layer.

This method may be deprecated in a future release.


```
add_ai_message(
    self,
    message: AIMessage | str,
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `message`\* | `AIMessage | str` | The `AIMessage` to add. |


