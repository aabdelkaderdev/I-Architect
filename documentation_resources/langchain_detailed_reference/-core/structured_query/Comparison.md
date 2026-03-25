<!-- Source: https://reference.langchain.com/python/langchain-core/structured_query/Comparison -->

Classv1.2.21 (latest)●Since v0.1

# Comparison

Comparison to a value.


```
Comparison(
  self,
  comparator: Comparator,
  attribute: str,
  value: Any,
  **kwargs: Any = {}
)
```

## Bases

`FilterDirective`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `comparator`\* | `Comparator` | The comparator to use. |
| `attribute`\* | `str` | The attribute to compare. |
| `value`\* | `Any` | The value to compare to. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| comparator | [Comparator](/python/langchain-core/structured_query/Comparator) |
| attribute | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| value | [Any](https://docs.python.org/3/library/typing.html#typing.Any) |

## Attributes

[attribute

comparator: Comparator

The comparator to use.](/python/langchain-core/structured_query/Comparison/comparator)[attribute

attribute: str

The attribute to compare.](/python/langchain-core/structured_query/Comparison/attribute)[attribute

value: Any

The value to compare to.](/python/langchain-core/structured_query/Comparison/value)

## Inherited from[Expr](/python/langchain-core/structured_query/Expr)

### Methods

[Maccept

—

Accept a visitor.](/python/langchain-core/structured_query/Expr/accept)


