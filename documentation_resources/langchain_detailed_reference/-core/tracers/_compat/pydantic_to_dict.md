<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/_compat/pydantic_to_dict -->

Functionv1.2.21 (latest)●Since v1.2

# pydantic\_to\_dict

Convert any Pydantic model to dict, compatible with both v1 and v2.


```
pydantic_to_dict(
    obj: Any,
    **kwargs: Any = {},
) -> dict[str, Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `obj`\* | `Any` | The Pydantic model to convert. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments passed to `model_dump`/`dict`. |


