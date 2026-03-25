<!-- Source: https://reference.langchain.com/python/langchain-core/structured_query/Operation -->

Classv1.2.21 (latest)●Since v0.1

# Operation

Logical operation over other directives.


```
Operation(
  self,
  operator: Operator,
  arguments: list[FilterDirective],
  **kwargs: Any = {}
)
```

## Bases

`FilterDirective`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `operator`\* | `Operator` | The operator to use. |
| `arguments`\* | `list[FilterDirective]` | The arguments to the operator. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| operator | [Operator](/python/langchain-core/structured_query/Operator) |
| arguments | [list](https://docs.python.org/3/library/stdtypes.html#list)[[FilterDirective](/python/langchain-core/structured_query/FilterDirective)] |

## Attributes

[attribute

operator: Operator

The operator to use.](/python/langchain-core/structured_query/Operation/operator)[attribute

arguments: list[FilterDirective]

The arguments to the operator.](/python/langchain-core/structured_query/Operation/arguments)

## Inherited from[Expr](/python/langchain-core/structured_query/Expr)

### Methods

[Maccept

—

Accept a visitor.](/python/langchain-core/structured_query/Expr/accept)


