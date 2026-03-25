<!-- Source: https://reference.langchain.com/python/langchain/agents/factory -->

Modulev1.2.13 (latest)●Since v1.0

# factory

Agent factory for creating agents with middleware support.

## Attributes

[attribute

JumpTo: Literal['tools', 'model', 'end']

Destination to jump to when a middleware node returns.](/python/langchain/agents/factory/JumpTo)[attribute

ResponseT](/python/langchain/agents/factory/ResponseT)[attribute

StateT\_co](/python/langchain/agents/factory/StateT_co)[attribute

STRUCTURED\_OUTPUT\_ERROR\_TEMPLATE: str](/python/langchain/agents/factory/STRUCTURED_OUTPUT_ERROR_TEMPLATE)[attribute

DYNAMIC\_TOOL\_ERROR\_TEMPLATE: str](/python/langchain/agents/factory/DYNAMIC_TOOL_ERROR_TEMPLATE)[attribute

FALLBACK\_MODELS\_WITH\_STRUCTURED\_OUTPUT: list](/python/langchain/agents/factory/FALLBACK_MODELS_WITH_STRUCTURED_OUTPUT)

## Functions

[function

init\_chat\_model

Initialize a chat model from any supported provider using a unified interface.

**Two main use cases:**

1. **Fixed model** – specify the model upfront and get a ready-to-use chat model.
2. **Configurable model** – choose to specify parameters (including model name) at
   runtime via `config`. Makes it easy to switch between models/providers without
   changing your code

Installation requirements

Requires the integration package for the chosen model provider to be installed.

See the `model_provider` parameter below for specific package names
(e.g., `pip install langchain-openai`).

Refer to the [provider integration's API reference](https://docs.langchain.com/oss/python/integrations/providers)
for supported model parameters to use as `**kwargs`.](/python/langchain/agents/factory/init_chat_model)[function

create\_agent

Creates an agent graph that calls tools in a loop until a stopping condition is met.

For more details on using `create_agent`,
visit the [Agents](https://docs.langchain.com/oss/python/langchain/agents) docs.](/python/langchain/agents/factory/create_agent)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/factory/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/factory/AgentState)[class

ExtendedModelResponse

Model response with an optional 'Command' from 'wrap\_model\_call' middleware.

Use this to return a 'Command' alongside the model response from a
'wrap\_model\_call' handler. The command is applied as an additional state
update after the model node completes, using the graph's reducers (e.g.
'add\_messages' for the 'messages' key).

Because each 'Command' is applied through the reducer, messages in the
command are **added alongside** the model response messages rather than
replacing them. For non-reducer state fields, later commands overwrite
earlier ones (outermost middleware wins over inner).](/python/langchain/agents/factory/ExtendedModelResponse)[class

ModelRequest

Model request information for the agent.](/python/langchain/agents/factory/ModelRequest)[class

ModelResponse

Response from model execution including messages and optional structured output.

The result will usually contain a single `AIMessage`, but may include an additional
`ToolMessage` if the model used a tool for structured output.](/python/langchain/agents/factory/ModelResponse)[class

OmitFromSchema

Annotation used to mark state attributes as omitted from input or output schemas.](/python/langchain/agents/factory/OmitFromSchema)[class

AutoStrategy

Automatically select the best strategy for structured output.](/python/langchain/agents/factory/AutoStrategy)[class

MultipleStructuredOutputsError

Raised when model returns multiple structured output tool calls when only one is expected.](/python/langchain/agents/factory/MultipleStructuredOutputsError)[class

OutputToolBinding

Information for tracking structured output tool metadata.

This contains all necessary information to handle structured responses generated via
tool calls, including the original schema, its type classification, and the
corresponding tool implementation used by the tools strategy.](/python/langchain/agents/factory/OutputToolBinding)[class

ProviderStrategy

Use the model provider's native structured output method.](/python/langchain/agents/factory/ProviderStrategy)[class

ProviderStrategyBinding

Information for tracking native structured output metadata.

This contains all necessary information to handle structured responses generated via
native provider output, including the original schema, its type classification, and
parsing logic for provider-enforced JSON.](/python/langchain/agents/factory/ProviderStrategyBinding)[class

StructuredOutputError

Base class for structured output errors.](/python/langchain/agents/factory/StructuredOutputError)[class

StructuredOutputValidationError

Raised when structured output tool call arguments fail to parse according to the schema.](/python/langchain/agents/factory/StructuredOutputValidationError)[class

ToolStrategy

Use a tool calling strategy for model responses.](/python/langchain/agents/factory/ToolStrategy)

## Type Aliases

[typeAlias

ResponseFormat: ToolStrategy[SchemaT] | ProviderStrategy[SchemaT] | AutoStrategy[SchemaT]

Union type for all supported response format strategies.](/python/langchain/agents/factory/ResponseFormat)


