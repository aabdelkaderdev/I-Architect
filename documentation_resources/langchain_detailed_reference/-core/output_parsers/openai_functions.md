<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_functions -->

Modulev1.2.21 (latest)●Since v0.1

# openai\_functions

Parsers for OpenAI functions output.

## Functions

[function

parse\_partial\_json

Parse a JSON string that may be missing closing braces.](/python/langchain-core/utils/json/parse_partial_json)

## Classes

[class

OutputParserException

Exception that output parsers should raise to signify a parsing error.

This exists to differentiate parsing errors from other code or execution errors
that also may arise inside the output parser.

`OutputParserException` will be available to catch and handle in ways to fix the
parsing error, while other errors will be raised.](/python/langchain-core/exceptions/OutputParserException)[class

BaseCumulativeTransformOutputParser

Base class for an output parser that can handle streaming input.](/python/langchain-core/output_parsers/transform/BaseCumulativeTransformOutputParser)[class

BaseGenerationOutputParser

Base class to parse the output of an LLM call.](/python/langchain-core/output_parsers/base/BaseGenerationOutputParser)[class

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

OutputFunctionsParser

Parse an output that is one of sets of values.](/python/langchain-core/output_parsers/openai_functions/OutputFunctionsParser)[class

JsonOutputFunctionsParser

Parse an output as the JSON object.](/python/langchain-core/output_parsers/openai_functions/JsonOutputFunctionsParser)[class

JsonKeyOutputFunctionsParser

Parse an output as the element of the JSON object.](/python/langchain-core/output_parsers/openai_functions/JsonKeyOutputFunctionsParser)[class

PydanticOutputFunctionsParser

Parse an output as a Pydantic object.

This parser is used to parse the output of a chat model that uses OpenAI function
format to invoke functions.

The parser extracts the function call invocation and matches them to the Pydantic
schema provided.

An exception will be raised if the function call does not match the provided schema.](/python/langchain-core/output_parsers/openai_functions/PydanticOutputFunctionsParser)[class

PydanticAttrOutputFunctionsParser

Parse an output as an attribute of a Pydantic object.](/python/langchain-core/output_parsers/openai_functions/PydanticAttrOutputFunctionsParser)


