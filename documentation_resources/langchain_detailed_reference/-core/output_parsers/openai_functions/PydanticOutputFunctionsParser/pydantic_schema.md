<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_functions/PydanticOutputFunctionsParser/pydantic_schema -->

Attributev1.2.21 (latest)●Since v0.1

# pydantic\_schema

The Pydantic schema to parse the output with.

If multiple schemas are provided, then the function name will be used to
determine which schema to use.


```
pydantic_schema: type[BaseModel] | dict[str, type[BaseModel]]
```


