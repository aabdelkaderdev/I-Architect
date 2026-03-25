<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage/content_blocks -->

Attributev1.2.21 (latest)●Since v1.0

# content\_blocks

Return standard, typed `ContentBlock` dicts from the message.

If the message has a known model provider, use the provider-specific translator
first before falling back to best-effort parsing. For details, see the property
on `BaseMessage`.


```
content_blocks: list[types.ContentBlock]
```


