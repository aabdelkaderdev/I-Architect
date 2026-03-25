<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base/TextAccessor -->

Classv1.2.21 (latest)●Since v1.0

# TextAccessor

String-like object that supports both property and method access patterns.

Exists to maintain backward compatibility while transitioning from method-based to
property-based text access in message objects. In LangChain <v1.0, message text was
accessed via `.text()` method calls. In v1.0=<, the preferred pattern is property
access via `.text`.

Rather than breaking existing code immediately, `TextAccessor` allows both
patterns:

- Modern property access: `message.text` (returns string directly)
- Legacy method access: `message.text()` (callable, emits deprecation warning)


```
TextAccessor()
```

## Bases

`str`


