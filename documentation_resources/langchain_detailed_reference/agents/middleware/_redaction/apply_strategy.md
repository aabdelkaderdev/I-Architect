<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_redaction/apply_strategy -->

Functionv1.2.13 (latest)●Since v1.0

# apply\_strategy

Apply the configured strategy to matches within content.


```
apply_strategy(
  content: str,
  matches: list[PIIMatch],
  strategy: RedactionStrategy
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `content`\* | `str` | The content to apply strategy to. |
| `matches`\* | `list[PIIMatch]` | List of detected PII matches. |
| `strategy`\* | `RedactionStrategy` | The redaction strategy to apply. |


