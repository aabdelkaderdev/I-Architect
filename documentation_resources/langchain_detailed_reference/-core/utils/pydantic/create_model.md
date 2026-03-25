<!-- Source: https://reference.langchain.com/python/langchain-core/utils/pydantic/create_model -->

Functionv1.2.21 (latest)●Since v0.3

# create\_model

Create a Pydantic model with the given field definitions.

Please use `create_model_v2` instead of this function.


```
create_model(
  model_name: str,
  module_name: str | None = None,
  ,
  **field_definitions: Any = {}
) -> type[BaseModel]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `model_name`\* | `str` | The name of the model. |
| `module_name` | `str | None` | Default:`None`  The name of the module where the model is defined.  This is used by Pydantic to resolve any forward references. |
| `**field_definitions` | `Any` | Default:`{}`  The field definitions for the model. |


