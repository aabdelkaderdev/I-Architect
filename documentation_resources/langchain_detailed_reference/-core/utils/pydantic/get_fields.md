<!-- Source: https://reference.langchain.com/python/langchain-core/utils/pydantic/get_fields -->

Functionv1.2.21 (latest)●Since v0.2

# get\_fields

Return the field names of a Pydantic model.


```
get_fields(
  model: type[BaseModel | BaseModelV1] | BaseModel | BaseModelV1
) -> dict[str, FieldInfoV2] | dict[str, ModelField]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `model`\* | `type[BaseModel | BaseModelV1] | BaseModel | BaseModelV1` | The Pydantic model or instance. |


