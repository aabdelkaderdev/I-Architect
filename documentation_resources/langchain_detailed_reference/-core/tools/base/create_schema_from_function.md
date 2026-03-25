<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/create_schema_from_function -->

Functionv1.2.21 (latest)●Since v0.2

# create\_schema\_from\_function

Create a Pydantic schema from a function's signature.


```
create_schema_from_function(
  model_name: str,
  func: Callable,
  *,
  filter_args: Sequence[str] | None = None,
  parse_docstring: bool = False,
  error_on_invalid_docstring: bool = False,
  include_injected: bool = True
) -> type[BaseModel]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `model_name`\* | `str` | Name to assign to the generated Pydantic schema. |
| `func`\* | `Callable` | Function to generate the schema from. |
| `filter_args` | `Sequence[str] | None` | Default:`None`  Optional list of arguments to exclude from the schema.  Defaults to `FILTERED_ARGS`. |
| `parse_docstring` | `bool` | Default:`False`  Whether to parse the function's docstring for descriptions for each argument. |
| `error_on_invalid_docstring` | `bool` | Default:`False`  If `parse_docstring` is provided, configure whether to raise `ValueError` on invalid Google Style docstrings. |
| `include_injected` | `bool` | Default:`True`  Whether to include injected arguments in the schema.  Defaults to `True`, since we want to include them in the schema when *validating* tool inputs. |


