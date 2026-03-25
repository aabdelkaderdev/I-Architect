<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base/BaseMessage/text -->

Attributev1.2.21 (latest)●Since v0.3

# text

Get the text content of the message as a string.

Can be used as both property (`message.text`) and method (`message.text()`).

Handles both string and list content types (e.g. for content blocks). Only
extracts blocks with `type: 'text'`; other block types are ignored.

Deprecated

As of `langchain-core` 1.0.0, calling `.text()` as a method is deprecated.
Use `.text` as a property instead. This method will be removed in 2.0.0.


```
text: TextAccessor
```


