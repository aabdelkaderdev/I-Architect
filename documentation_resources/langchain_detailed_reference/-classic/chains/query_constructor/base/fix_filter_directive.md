<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/base/fix_filter_directive -->

Functionv1.2.13 (latest)●Since v1.0

# fix\_filter\_directive

Fix invalid filter directive.


```
fix_filter_directive(
  filter: FilterDirective | None,
  *,
  allowed_comparators: Sequence[Comparator] | None = None,
  allowed_operators: Sequence[Operator] | None = None,
  allowed_attributes: Sequence[str] | None = None
) -> FilterDirective | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `filter`\* | `FilterDirective | None` | Filter directive to fix. |
| `allowed_comparators` | `Sequence[Comparator] | None` | Default:`None`  allowed comparators. Defaults to all comparators. |
| `allowed_operators` | `Sequence[Operator] | None` | Default:`None`  allowed operators. Defaults to all operators. |
| `allowed_attributes` | `Sequence[str] | None` | Default:`None`  allowed attributes. Defaults to all attributes. |


