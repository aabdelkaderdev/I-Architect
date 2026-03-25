<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/AIMessageChunk/chunk_position -->

Attributev1.2.21 (latest)●Since v1.0

# chunk\_position

Optional span represented by an aggregated `AIMessageChunk`.

If a chunk with `chunk_position="last"` is aggregated into a stream,
`tool_call_chunks` in message content will be parsed into `tool_calls`.


```
chunk_position: Literal['last'] | None = None
```


