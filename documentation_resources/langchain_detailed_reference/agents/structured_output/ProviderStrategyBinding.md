<!-- Source: https://reference.langchain.com/python/langchain/agents/structured_output/ProviderStrategyBinding -->

Classv1.2.13 (latest)●Since v0.3

# ProviderStrategyBinding

Information for tracking native structured output metadata.

This contains all necessary information to handle structured responses generated via
native provider output, including the original schema, its type classification, and
parsing logic for provider-enforced JSON.


```
ProviderStrategyBinding(
  self,
  schema: type[SchemaT] | dict[str, Any],
  schema_kind: SchemaKind
)
```

## Bases

`Generic[SchemaT]`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| schema | [type](https://docs.python.org/3/library/functions.html#type)[[SchemaT](/python/langchain/agents/structured_output/SchemaT)] | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| schema\_kind | [SchemaKind](/python/langchain/agents/structured_output/SchemaKind) |

## Attributes

[attribute

schema: type[SchemaT] | dict[str, Any]

The original schema provided for structured output (Pydantic model, `dataclass`,
`TypedDict`, or JSON schema dict).](/python/langchain/agents/structured_output/ProviderStrategyBinding/schema)[attribute

schema\_kind: SchemaKind

Classification of the schema type for proper response construction.](/python/langchain/agents/structured_output/ProviderStrategyBinding/schema_kind)

## Methods

[method

from\_schema\_spec

Create a `ProviderStrategyBinding` instance from a `SchemaSpec`.](/python/langchain/agents/structured_output/ProviderStrategyBinding/from_schema_spec)[method

parse

Parse `AIMessage` content according to the schema.](/python/langchain/agents/structured_output/ProviderStrategyBinding/parse)


