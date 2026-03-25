<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_tools -->

Modulev1.2.21 (latest)●Since v0.1

# openai\_tools

Parse tools for OpenAI tools output.

## Attributes

[attribute

TypeBaseModel: type[BaseModel]](/python/langchain-core/utils/pydantic/TypeBaseModel)[attribute

logger](/python/langchain-core/output_parsers/openai_tools/logger)

## Functions

[function

invalid\_tool\_call

Create an invalid tool call.](/python/langchain-core/messages/tool/invalid_tool_call)[function

create\_tool\_call

Create a tool call.](/python/langchain-core/messages/tool/tool_call)[function

parse\_partial\_json

Parse a JSON string that may be missing closing braces.](/python/langchain-core/utils/json/parse_partial_json)[function

is\_pydantic\_v1\_subclass

Check if the given class is Pydantic v1-like.](/python/langchain-core/utils/pydantic/is_pydantic_v1_subclass)[function

is\_pydantic\_v2\_subclass

Check if the given class is Pydantic v2-like.](/python/langchain-core/utils/pydantic/is_pydantic_v2_subclass)[function

parse\_tool\_call

Parse a single tool call.](/python/langchain-core/output_parsers/openai_tools/parse_tool_call)[function

make\_invalid\_tool\_call

Create an `InvalidToolCall` from a raw tool call.](/python/langchain-core/output_parsers/openai_tools/make_invalid_tool_call)[function

parse\_tool\_calls

Parse a list of tool calls.](/python/langchain-core/output_parsers/openai_tools/parse_tool_calls)

## Classes

[class

OutputParserException

Exception that output parsers should raise to signify a parsing error.

This exists to differentiate parsing errors from other code or execution errors
that also may arise inside the output parser.

`OutputParserException` will be available to catch and handle in ways to fix the
parsing error, while other errors will be raised.](/python/langchain-core/exceptions/OutputParserException)[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

InvalidToolCall

Allowance for errors made by LLM.

Here we add an `error` key to surface errors made during generation
(e.g., invalid JSON arguments.)](/python/langchain-core/messages/content/InvalidToolCall)[class

BaseCumulativeTransformOutputParser

Base class for an output parser that can handle streaming input.](/python/langchain-core/output_parsers/transform/BaseCumulativeTransformOutputParser)[class

ChatGeneration

A single chat generation output.

A subclass of `Generation` that represents the response from a chat model that
generates chat messages.

The `message` attribute is a structured representation of the chat message. Most of
the time, the message will be of type `AIMessage`.

Users working with chat models will usually access information via either
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks).](/python/langchain-core/outputs/chat_generation/ChatGeneration)[class

Generation

A single text generation output.

Generation represents the response from an "old-fashioned" LLM (string-in,
string-out) that generates regular text (not chat messages).

This model is used internally by chat model and will eventually be mapped to a more
general `LLMResult` object, and then projected into an `AIMessage` object.

LangChain users working with chat models will usually access information via
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks). Please refer to `AIMessage` and `LLMResult` for more information.](/python/langchain-core/outputs/generation/Generation)[class

JsonOutputToolsParser

Parse tools from OpenAI response.](/python/langchain-core/output_parsers/openai_tools/JsonOutputToolsParser)[class

JsonOutputKeyToolsParser

Parse tools from OpenAI response.](/python/langchain-core/output_parsers/openai_tools/JsonOutputKeyToolsParser)[class

PydanticToolsParser

Parse tools from OpenAI response.](/python/langchain-core/output_parsers/openai_tools/PydanticToolsParser)


