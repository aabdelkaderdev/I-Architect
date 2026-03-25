<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_redaction/detect_credit_card -->

Functionv1.2.13 (latest)●Since v1.0

# detect\_credit\_card

Detect credit card numbers in content using Luhn validation.


```
detect_credit_card(
    content: str,
) -> list[PIIMatch]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `content`\* | `str` | The text content to scan for credit card numbers. |


