<!-- Source: https://reference.langchain.com/python/langchain-core/utils/function_calling/convert_to_openai_function -->

Functionv1.2.21 (latest)●Since v0.1

# convert\_to\_openai\_function

Convert a raw function/class to an OpenAI function.


```
convert_to_openai_function(
  function: Mapping[str, Any] | type | Callable | BaseTool,
  *,
  strict: bool | None = None
) -> dict[str, Any]
```

`description` and `parameters` keys are now optional. Only `name` is
required and guaranteed to be part of the output.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `function`\* | `Mapping[str, Any] | type | Callable | BaseTool` | A dictionary, Pydantic `BaseModel` class, `TypedDict` class, a LangChain `Tool` object, or a Python function.  If a dictionary is passed in, it is assumed to already be a valid OpenAI function, a JSON schema with top-level `title` key specified, an Anthropic format tool, or an Amazon Bedrock Converse format tool. |
| `strict` | `bool | None` | Default:`None`  If `True`, model output is guaranteed to exactly match the JSON Schema provided in the function definition.  If `None`, `strict` argument will not be included in function definition. |


