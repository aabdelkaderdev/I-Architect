<!-- Source: https://reference.langchain.com/python/langchain-core/messages/block_translators/get_translator -->

Functionv1.2.21 (latest)●Since v1.0

# get\_translator

Get the translator functions for a provider.


```
get_translator(
    provider: str,
) -> dict[str, Callable[..., list[types.ContentBlock]]] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `provider`\* | `str` | The model provider name. |


