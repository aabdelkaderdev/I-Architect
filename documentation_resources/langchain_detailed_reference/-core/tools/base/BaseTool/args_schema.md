<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/BaseTool/args_schema -->

Attributev1.2.21 (latest)●Since v0.2

# args\_schema

Pydantic model class to validate and parse the tool's input arguments.

Args schema should be either:

- A subclass of `pydantic.BaseModel`.
- A subclass of `pydantic.v1.BaseModel` if accessing v1 namespace in pydantic 2
- A JSON schema dict


```
args_schema: Annotated[ArgsSchema | None, SkipValidation(
  )] = Field(default=None, description='The tool schema.'
)
```


