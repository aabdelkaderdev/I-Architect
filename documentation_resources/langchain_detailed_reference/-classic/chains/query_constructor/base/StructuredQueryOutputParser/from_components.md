<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/base/StructuredQueryOutputParser/from_components -->

Methodv1.2.13 (latest)●Since v1.0

# from\_components

Create a structured query output parser from components.


```
from_components(
  cls,
  allowed_comparators: Sequence[Comparator] | None = None,
  allowed_operators: Sequence[Operator] | None = None,
  allowed_attributes: Sequence[str] | None = None,
  fix_invalid: bool = False
) -> StructuredQueryOutputParser
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `allowed_comparators` | `Sequence[Comparator] | None` | Default:`None`  allowed comparators |
| `allowed_operators` | `Sequence[Operator] | None` | Default:`None`  allowed operators |
| `allowed_attributes` | `Sequence[str] | None` | Default:`None`  allowed attributes |
| `fix_invalid` | `bool` | Default:`False`  whether to fix invalid filter directives |


