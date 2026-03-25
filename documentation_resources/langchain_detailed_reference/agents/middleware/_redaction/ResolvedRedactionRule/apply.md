<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_redaction/ResolvedRedactionRule/apply -->

Methodv1.2.13 (latest)●Since v1.0

# apply

Apply this rule to content, returning new content and matches.


```
apply(
    self,
    content: str,
) -> tuple[str, list[PIIMatch]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `content`\* | `str` | The text content to scan and redact. |


