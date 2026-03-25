<!-- Source: https://reference.langchain.com/python/langchain-core/chat_history/BaseChatMessageHistory/add_user_message -->

Methodv1.2.21 (latest)●Since v0.1

# add\_user\_message

Convenience method for adding a human message string to the store.

Note

This is a convenience method. Code should favor the bulk `add_messages`
interface instead to save on round-trips to the persistence layer.

This method may be deprecated in a future release.


```
add_user_message(
    self,
    message: HumanMessage | str,
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `message`\* | `HumanMessage | str` | The `HumanMessage` to add to the store. |


