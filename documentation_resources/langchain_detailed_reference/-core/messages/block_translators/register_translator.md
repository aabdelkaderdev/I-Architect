<!-- Source: https://reference.langchain.com/python/langchain-core/messages/block_translators/register_translator -->

Functionv1.2.21 (latest)●Since v1.0

# register\_translator

Register content translators for a provider in `PROVIDER_TRANSLATORS`.


```
register_translator(
  provider: str,
  translate_content: Callable[[AIMessage], list[types.ContentBlock]],
  translate_content_chunk: Callable[[AIMessageChunk], list[types.ContentBlock]]
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `provider`\* | `str` | The model provider name (e.g. `'openai'`, `'anthropic'`). |
| `translate_content`\* | `Callable[[AIMessage], list[types.ContentBlock]]` | Function to translate `AIMessage` content. |
| `translate_content_chunk`\* | `Callable[[AIMessageChunk], list[types.ContentBlock]]` | Function to translate `AIMessageChunk` content. |


