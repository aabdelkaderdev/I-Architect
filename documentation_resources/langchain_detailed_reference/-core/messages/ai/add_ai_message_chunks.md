<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/add_ai_message_chunks -->

Functionv1.2.21 (latest)●Since v0.2

# add\_ai\_message\_chunks

Add multiple `AIMessageChunk`s together.


```
add_ai_message_chunks(
  left: AIMessageChunk,
  *others: AIMessageChunk = ()
) -> AIMessageChunk
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `left`\* | `AIMessageChunk` | The first `AIMessageChunk`. |
| `*others` | `AIMessageChunk` | Default:`()`  Other `AIMessageChunk`s to add. |


