<!-- Source: https://reference.langchain.com/python/langchain-core/tools/convert/convert_runnable_to_tool -->

Functionv1.2.21 (latest)●Since v0.2

# convert\_runnable\_to\_tool

Convert a `Runnable` into a `BaseTool`.


```
convert_runnable_to_tool(
  runnable: Runnable,
  args_schema: type[BaseModel] | None = None,
  *,
  name: str | None = None,
  description: str | None = None,
  arg_types: dict[str, type] | None = None
) -> BaseTool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `runnable`\* | `Runnable` | The `Runnable` to convert. |
| `args_schema` | `type[BaseModel] | None` | Default:`None`  The schema for the tool's input arguments. |
| `name` | `str | None` | Default:`None`  The name of the tool. |
| `description` | `str | None` | Default:`None`  The description of the tool. |
| `arg_types` | `dict[str, type] | None` | Default:`None`  The types of the arguments. |


