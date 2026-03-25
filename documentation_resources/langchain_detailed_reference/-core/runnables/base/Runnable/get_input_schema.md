<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/get_input_schema -->

Methodv1.2.21 (latest)●Since v0.1

# get\_input\_schema

Get a Pydantic model that can be used to validate input to the `Runnable`.

`Runnable` objects that leverage the `configurable_fields` and
`configurable_alternatives` methods will have a dynamic input schema that
depends on which configuration the `Runnable` is invoked with.

This method allows to get an input schema for a specific configuration.


```
get_input_schema(
    self,
    config: RunnableConfig | None = None,
) -> type[BaseModel]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config` | `RunnableConfig | None` | Default:`None`  A config to use when generating the schema. |


