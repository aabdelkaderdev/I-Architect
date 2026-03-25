<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_redaction/resolve_detector -->

Functionv1.2.13 (latest)●Since v1.0

# resolve\_detector

Return a callable detector for the given configuration.


```
resolve_detector(
    pii_type: str,
    detector: Detector | str | None,
) -> Detector
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `pii_type`\* | `str` | The PII type name. |
| `detector`\* | `Detector | str | None` | Optional custom detector or regex pattern. If `None`, a built-in detector for the given PII type will be used. |


