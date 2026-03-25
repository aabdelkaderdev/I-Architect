<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/config_schema -->

Methodv1.2.21 (latest)●Since v0.1

# config\_schema

The type of config this `Runnable` accepts specified as a Pydantic model.

To mark a field as configurable, see the `configurable_fields`
and `configurable_alternatives` methods.


```
config_schema(
  self,
  *,
  include: Sequence[str] | None = None
) -> type[BaseModel]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `include` | `Sequence[str] | None` | Default:`None`  A list of fields to include in the config schema. |


