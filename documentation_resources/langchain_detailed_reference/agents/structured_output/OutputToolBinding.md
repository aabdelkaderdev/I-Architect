<!-- Source: https://reference.langchain.com/python/langchain/agents/structured_output/OutputToolBinding -->

Classv1.2.13 (latest)●Since v0.3

# OutputToolBinding

Information for tracking structured output tool metadata.

This contains all necessary information to handle structured responses generated via
tool calls, including the original schema, its type classification, and the
corresponding tool implementation used by the tools strategy.


```
OutputToolBinding(
  self,
  schema: type[SchemaT] | dict[str, Any],
  schema_kind: SchemaKind,
  tool: BaseTool
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
| tool | [BaseTool](/python/langchain-core/tools/base/BaseTool) |

## Attributes

[attribute

schema: type[SchemaT] | dict[str, Any]

The original schema provided for structured output (Pydantic model, dataclass,
TypedDict, or JSON schema dict).](/python/langchain/agents/structured_output/OutputToolBinding/schema)[attribute

schema\_kind: SchemaKind

Classification of the schema type for proper response construction.](/python/langchain/agents/structured_output/OutputToolBinding/schema_kind)[attribute

tool: BaseTool

LangChain tool instance created from the schema for model binding.](/python/langchain/agents/structured_output/OutputToolBinding/tool)

## Methods

[method

from\_schema\_spec

Create an `OutputToolBinding` instance from a `SchemaSpec`.](/python/langchain/agents/structured_output/OutputToolBinding/from_schema_spec)[method

parse

Parse tool arguments according to the schema.](/python/langchain/agents/structured_output/OutputToolBinding/parse)


