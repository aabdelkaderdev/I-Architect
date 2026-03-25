<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/openapi/openapi_spec_to_openai_fn -->

Functionv1.2.13 (latest)●Since v1.0

# openapi\_spec\_to\_openai\_fn

OpenAPI spec to OpenAI function JSON Schema.

Convert a valid OpenAPI spec to the JSON Schema format expected for OpenAI
functions.


```
openapi_spec_to_openai_fn(
    spec: OpenAPISpec,
) -> tuple[list[dict[str, Any]], Callable]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `spec`\* | `OpenAPISpec` | OpenAPI spec to convert. |


