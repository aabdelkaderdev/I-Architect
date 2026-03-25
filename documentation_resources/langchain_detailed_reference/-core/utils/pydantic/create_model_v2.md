<!-- Source: https://reference.langchain.com/python/langchain-core/utils/pydantic/create_model_v2 -->

Functionv1.2.21 (latest)●Since v0.3

# create\_model\_v2

Create a Pydantic model with the given field definitions.

Warning

Do not use outside of langchain packages. This API is subject to change at any
time.


```
create_model_v2(
  model_name: str,
  *,
  module_name: str | None = None,
  field_definitions: dict[str, Any] | None = None,
  root: Any | None = None
) -> type[BaseModel]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `model_name`\* | `str` | The name of the model. |
| `module_name` | `str | None` | Default:`None`  The name of the module where the model is defined.  This is used by Pydantic to resolve any forward references. |
| `field_definitions` | `dict[str, Any] | None` | Default:`None`  The field definitions for the model. |
| `root` | `Any | None` | Default:`None`  Type for a root model (`RootModel`) |


