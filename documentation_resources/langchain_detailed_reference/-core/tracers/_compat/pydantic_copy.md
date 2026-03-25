<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/_compat/pydantic_copy -->

Functionv1.2.21 (latest)●Since v1.2

# pydantic\_copy

Copy any Pydantic model, compatible with both v1 and v2.


```
pydantic_copy(
    obj: T,
    **kwargs: Any = {},
) -> T
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `obj`\* | `T` | The Pydantic model to copy. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments passed to `model_copy`/`copy`. |


