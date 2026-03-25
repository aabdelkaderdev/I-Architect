<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/get_output_schema -->

Methodv1.2.21 (latest)●Since v0.1

# get\_output\_schema

Get a Pydantic model that can be used to validate output to the `Runnable`.

`Runnable` objects that leverage the `configurable_fields` and
`configurable_alternatives` methods will have a dynamic output schema that
depends on which configuration the `Runnable` is invoked with.

This method allows to get an output schema for a specific configuration.


```
get_output_schema(
    self,
    config: RunnableConfig | None = None,
) -> type[BaseModel]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config` | `RunnableConfig | None` | Default:`None`  A config to use when generating the schema. |


