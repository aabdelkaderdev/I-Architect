<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/build_extra_kwargs -->

Functionv1.2.21 (latest)●Since v0.1

# build\_extra\_kwargs

Build extra kwargs from values and extra\_kwargs.

DON'T USE

Kept for backwards-compatibility but should never have been public. Use the
internal `_build_model_kwargs` function instead.


```
build_extra_kwargs(
  extra_kwargs: dict[str, Any],
  values: dict[str, Any],
  all_required_field_names: set[str]
) -> dict[str, Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `extra_kwargs`\* | `dict[str, Any]` | Extra kwargs passed in by user. |
| `values`\* | `dict[str, Any]` | Values passed in by user. |
| `all_required_field_names`\* | `set[str]` | All required field names for the pydantic class. |


