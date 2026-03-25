<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_redaction/PIIDetectionError -->

Classv1.2.13 (latest)●Since v1.0

# PIIDetectionError

Raised when configured to block on detected sensitive values.


```
PIIDetectionError(
  self,
  pii_type: str,
  matches: Sequence[PIIMatch]
)
```

## Bases

`Exception`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `pii_type`\* | `str` | Name of the detected sensitive type. |
| `matches`\* | `Sequence[PIIMatch]` | All matches that were detected for that type. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| pii\_type | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| matches | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[PIIMatch](/python/langchain/agents/middleware/_redaction/PIIMatch)] |

## Attributes

[attribute

pii\_type: pii\_type](/python/langchain/agents/middleware/_redaction/PIIDetectionError/pii_type)[attribute

matches](/python/langchain/agents/middleware/_redaction/PIIDetectionError/matches)


