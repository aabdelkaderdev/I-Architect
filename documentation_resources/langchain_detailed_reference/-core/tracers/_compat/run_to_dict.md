<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/_compat/run_to_dict -->

Functionv1.2.21 (latest)●Since v1.2

# run\_to\_dict

Convert run to dict, compatible with both Pydantic v1 and v2.


```
run_to_dict(
    run: Run,
    **kwargs: Any = {},
) -> dict[str, Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `run`\* | `Run` | The run to convert. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments passed to `model_dump`/`dict`. |


