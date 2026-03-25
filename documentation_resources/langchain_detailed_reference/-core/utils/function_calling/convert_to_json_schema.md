<!-- Source: https://reference.langchain.com/python/langchain-core/utils/function_calling/convert_to_json_schema -->

Functionv1.2.21 (latest)●Since v0.3

# convert\_to\_json\_schema

Convert a schema representation to a JSON schema.


```
convert_to_json_schema(
  schema: dict[str, Any] | type[BaseModel] | Callable | BaseTool,
  *,
  strict: bool | None = None
) -> dict[str, Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `schema`\* | `dict[str, Any] | type[BaseModel] | Callable | BaseTool` | The schema to convert. |
| `strict` | `bool | None` | Default:`None`  If `True`, model output is guaranteed to exactly match the JSON Schema provided in the function definition.  If `None`, `strict` argument will not be included in function definition. |


