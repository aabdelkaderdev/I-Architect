<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/_redaction/ResolvedRedactionRule -->

Classv1.2.13 (latest)●Since v1.0

# ResolvedRedactionRule

Resolved redaction rule ready for execution.


```
ResolvedRedactionRule(
  self,
  pii_type: str,
  strategy: RedactionStrategy,
  detector: Detector
)
```

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| pii\_type | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| strategy | [RedactionStrategy](/python/langchain/agents/middleware/_redaction/RedactionStrategy) |
| detector | [Detector](/python/langchain/agents/middleware/_redaction/Detector) |

## Attributes

[attribute

pii\_type: str](/python/langchain/agents/middleware/_redaction/ResolvedRedactionRule/pii_type)[attribute

strategy: RedactionStrategy](/python/langchain/agents/middleware/_redaction/ResolvedRedactionRule/strategy)[attribute

detector: Detector](/python/langchain/agents/middleware/_redaction/ResolvedRedactionRule/detector)

## Methods

[method

apply

Apply this rule to content, returning new content and matches.](/python/langchain/agents/middleware/_redaction/ResolvedRedactionRule/apply)


