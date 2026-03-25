<!-- Source: https://reference.langchain.com/python/langchain/agents/structured_output -->

Modulev1.2.13 (latest)●Since v0.3

# structured\_output

Types for setting agent response formats.

## Attributes

[attribute

SchemaT](/python/langchain/agents/structured_output/SchemaT)[attribute

SchemaKind: Literal['pydantic', 'dataclass', 'typeddict', 'json\_schema']](/python/langchain/agents/structured_output/SchemaKind)

## Classes

[class

StructuredOutputError

Base class for structured output errors.](/python/langchain/agents/structured_output/StructuredOutputError)[class

MultipleStructuredOutputsError

Raised when model returns multiple structured output tool calls when only one is expected.](/python/langchain/agents/structured_output/MultipleStructuredOutputsError)[class

StructuredOutputValidationError

Raised when structured output tool call arguments fail to parse according to the schema.](/python/langchain/agents/structured_output/StructuredOutputValidationError)[class

ToolStrategy

Use a tool calling strategy for model responses.](/python/langchain/agents/structured_output/ToolStrategy)[class

ProviderStrategy

Use the model provider's native structured output method.](/python/langchain/agents/structured_output/ProviderStrategy)[class

OutputToolBinding

Information for tracking structured output tool metadata.

This contains all necessary information to handle structured responses generated via
tool calls, including the original schema, its type classification, and the
corresponding tool implementation used by the tools strategy.](/python/langchain/agents/structured_output/OutputToolBinding)[class

ProviderStrategyBinding

Information for tracking native structured output metadata.

This contains all necessary information to handle structured responses generated via
native provider output, including the original schema, its type classification, and
parsing logic for provider-enforced JSON.](/python/langchain/agents/structured_output/ProviderStrategyBinding)[class

AutoStrategy

Automatically select the best strategy for structured output.](/python/langchain/agents/structured_output/AutoStrategy)

## Type Aliases

[typeAlias

ResponseFormat: ToolStrategy[SchemaT] | ProviderStrategy[SchemaT] | AutoStrategy[SchemaT]

Union type for all supported response format strategies.](/python/langchain/agents/structured_output/ResponseFormat)


