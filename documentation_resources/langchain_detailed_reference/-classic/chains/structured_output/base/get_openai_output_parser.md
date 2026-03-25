<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/structured_output/base/get_openai_output_parser -->

Functionv1.2.13 (latest)●Since v1.0

# get\_openai\_output\_parser

Get the appropriate function output parser given the user functions.


```
get_openai_output_parser(
  functions: Sequence[dict[str, Any] | type[BaseModel] | Callable]
) -> BaseOutputParser | BaseGenerationOutputParser
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `functions`\* | `Sequence[dict[str, Any] | type[BaseModel] | Callable]` | Sequence where element is a dictionary, a pydantic.BaseModel class, or a Python function. If a dictionary is passed in, it is assumed to already be a valid OpenAI function. |


