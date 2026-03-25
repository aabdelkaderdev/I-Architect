<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models/agenerate_from_stream -->

Functionv1.2.21 (latest)●Since v0.1

# agenerate\_from\_stream

Async generate from a stream.


```
agenerate_from_stream(
    stream: AsyncIterator[ChatGenerationChunk],
) -> ChatResult
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `stream`\* | `AsyncIterator[ChatGenerationChunk]` | AsyncIterator of `ChatGenerationChunk`. |


