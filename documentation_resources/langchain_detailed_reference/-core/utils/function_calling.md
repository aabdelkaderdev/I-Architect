<!-- Source: https://reference.langchain.com/python/langchain-core/utils/function_calling -->

Modulev1.2.21 (latest)●Since v0.1

# function\_calling

Methods for creating function specs in the style of OpenAI Functions.

## Attributes

[attribute

logger](/python/langchain-core/utils/function_calling/logger)[attribute

PYTHON\_TO\_JSON\_TYPES: dict](/python/langchain-core/utils/function_calling/PYTHON_TO_JSON_TYPES)

## Functions

[function

beta

Decorator to mark a function, a class, or a property as beta.

When marking a classmethod, a staticmethod, or a property, the `@beta` decorator
should go *under* `@classmethod` and `@staticmethod` (i.e., `beta` should directly
decorate the underlying callable), but *over* `@property`.

When marking a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@beta` would mess up
`__init__` inheritance when installing its own (annotation-emitting) `C.__init__`).](/python/langchain-core/_api/beta_decorator/beta)[function

dereference\_refs

Resolve and inline JSON Schema `$ref` references in a schema object.

This function processes a JSON Schema and resolves all `$ref` references by
replacing them with the actual referenced content.

Handles both simple references and complex cases like circular references and mixed
`$ref` objects that contain additional properties alongside the `$ref`.](/python/langchain-core/utils/json_schema/dereference_refs)[function

is\_basemodel\_subclass

Check if the given class is a subclass of Pydantic `BaseModel`.

Check if the given class is a subclass of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x](/python/langchain-core/utils/pydantic/is_basemodel_subclass)[function

convert\_to\_openai\_function

Convert a raw function/class to an OpenAI function.](/python/langchain-core/utils/function_calling/convert_to_openai_function)[function

convert\_to\_openai\_tool

Convert a tool-like object to an OpenAI tool schema.

[OpenAI tool schema reference](https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools)](/python/langchain-core/utils/function_calling/convert_to_openai_tool)[function

convert\_to\_json\_schema

Convert a schema representation to a JSON schema.](/python/langchain-core/utils/function_calling/convert_to_json_schema)[function

tool\_example\_to\_messages

Convert an example into a list of messages that can be fed into an LLM.

This code is an adapter that converts a single example to a list of messages
that can be fed into a chat model.

The list of messages per example by default corresponds to:

1. `HumanMessage`: contains the content from which content should be extracted.
2. `AIMessage`: contains the extracted information from the model
3. `ToolMessage`: contains confirmation to the model that the model requested a
   tool correctly.

If `ai_response` is specified, there will be a final `AIMessage` with that
response.

The `ToolMessage` is required because some chat models are hyper-optimized for
agents rather than for an extraction use case.](/python/langchain-core/utils/function_calling/tool_example_to_messages)

## Classes

[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

HumanMessage

Message from the user.

A `HumanMessage` is a message that is passed in from a user to the model.](/python/langchain-core/messages/human/HumanMessage)[class

ToolMessage

Message for passing the result of executing a tool back to a model.

`ToolMessage` objects contain the result of a tool invocation. Typically, the result
is encoded inside the `content` field.

`tool_call_id` is used to associate the tool call request with the tool call
response. Useful in situations where a chat model is able to request multiple tool
calls in parallel.](/python/langchain-core/messages/tool/ToolMessage)[class

BaseTool

Base class for all LangChain tools.

This abstract class defines the interface that all LangChain tools must implement.

Tools are components that can be called by agents to perform specific actions.](/python/langchain-core/tools/base/BaseTool)[class

FunctionDescription

Representation of a callable function to send to an LLM.](/python/langchain-core/utils/function_calling/FunctionDescription)[class

ToolDescription

Representation of a callable function to the OpenAI API.](/python/langchain-core/utils/function_calling/ToolDescription)

## Modules

[module

langchain\_core

`langchain-core` defines the base abstractions for the LangChain ecosystem.

The interfaces for core components like chat models, LLMs, vector stores, retrievers,
and more are defined here. The universal invocation protocol (Runnables) along with
a syntax for combining components are also defined here.

**No third-party integrations are defined here.** The dependencies are kept purposefully
very lightweight.](/python/langchain-core/langchain_core)


