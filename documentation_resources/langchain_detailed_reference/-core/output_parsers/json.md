<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/json -->

Modulev1.2.21 (latest)●Since v0.1

# json

Parser for JSON output.

## Attributes

[attribute

JSON\_FORMAT\_INSTRUCTIONS: str](/python/langchain-core/output_parsers/format_instructions/JSON_FORMAT_INSTRUCTIONS)[attribute

TBaseModel](/python/langchain-core/output_parsers/json/TBaseModel)[attribute

SimpleJsonOutputParser: JsonOutputParser](/python/langchain-core/output_parsers/json/SimpleJsonOutputParser)

## Functions

[function

parse\_and\_check\_json\_markdown

Parse and check a JSON string from a Markdown string.

Checks that it contains the expected keys.](/python/langchain-core/utils/json/parse_and_check_json_markdown)[function

parse\_json\_markdown

Parse a JSON string from a Markdown string.](/python/langchain-core/utils/json/parse_json_markdown)[function

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

Generation

A single text generation output.

Generation represents the response from an "old-fashioned" LLM (string-in,
string-out) that generates regular text (not chat messages).

This model is used internally by chat model and will eventually be mapped to a more
general `LLMResult` object, and then projected into an `AIMessage` object.

LangChain users working with chat models will usually access information via
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks). Please refer to `AIMessage` and `LLMResult` for more information.](/python/langchain-core/outputs/generation/Generation)[class

JsonOutputParser

Parse the output of an LLM call to a JSON object.

Probably the most reliable output parser for getting structured data that does *not*
use function calling.

When used in streaming mode, it will yield partial JSON objects containing all the
keys that have been returned so far.

In streaming, if `diff` is set to `True`, yields `JSONPatch` operations describing
the difference between the previous and the current object.](/python/langchain-core/output_parsers/json/JsonOutputParser)

## Type Aliases

[typeAlias

PydanticBaseModel](/python/langchain-core/output_parsers/json/PydanticBaseModel)


