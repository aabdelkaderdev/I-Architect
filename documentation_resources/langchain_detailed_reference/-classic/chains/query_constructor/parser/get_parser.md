<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/parser/get_parser -->

Functionv1.2.13 (latest)●Since v1.0

# get\_parser

Return a parser for the query language.


```
get_parser(
  allowed_comparators: Sequence[Comparator] | None = None,
  allowed_operators: Sequence[Operator] | None = None,
  allowed_attributes: Sequence[str] | None = None
) -> Lark
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `allowed_comparators` | `Sequence[Comparator] | None` | Default:`None`  The allowed comparators. |
| `allowed_operators` | `Sequence[Operator] | None` | Default:`None`  The allowed operators. |
| `allowed_attributes` | `Sequence[str] | None` | Default:`None`  The allowed attributes. |


