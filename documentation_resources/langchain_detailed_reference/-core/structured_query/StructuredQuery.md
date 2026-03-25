<!-- Source: https://reference.langchain.com/python/langchain-core/structured_query/StructuredQuery -->

Classv1.2.21 (latest)●Since v0.1

# StructuredQuery

Structured query.


```
StructuredQuery(
  self,
  query: str,
  filter: FilterDirective | None,
  limit: int | None = None,
  **kwargs: Any = {}
)
```

## Bases

`Expr`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `query`\* | `str` | The query string. |
| `filter`\* | `FilterDirective | None` | The filtering expression. |
| `limit` | `int | None` | Default:`None`  The limit on the number of results. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| query | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| filter | [FilterDirective](/python/langchain-core/structured_query/FilterDirective) | None |
| limit | [int](https://docs.python.org/3/library/functions.html#int) | None |

## Attributes

[attribute

query: str

Query string.](/python/langchain-core/structured_query/StructuredQuery/query)[attribute

filter: FilterDirective | None

Filtering expression.](/python/langchain-core/structured_query/StructuredQuery/filter)[attribute

limit: int | None

Limit on the number of results.](/python/langchain-core/structured_query/StructuredQuery/limit)

## Inherited from[Expr](/python/langchain-core/structured_query/Expr)

### Methods

[Maccept

—

Accept a visitor.](/python/langchain-core/structured_query/Expr/accept)


