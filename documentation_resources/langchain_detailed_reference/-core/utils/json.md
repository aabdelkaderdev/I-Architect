<!-- Source: https://reference.langchain.com/python/langchain-core/utils/json -->

Modulev1.2.21 (latest)●Since v0.1

# json

Utilities for JSON.

## Functions

[function

parse\_partial\_json

Parse a JSON string that may be missing closing braces.](/python/langchain-core/utils/json/parse_partial_json)[function

parse\_json\_markdown

Parse a JSON string from a Markdown string.](/python/langchain-core/utils/json/parse_json_markdown)[function

parse\_and\_check\_json\_markdown

Parse and check a JSON string from a Markdown string.

Checks that it contains the expected keys.](/python/langchain-core/utils/json/parse_and_check_json_markdown)

## Classes

[class

OutputParserException

Exception that output parsers should raise to signify a parsing error.

This exists to differentiate parsing errors from other code or execution errors
that also may arise inside the output parser.

`OutputParserException` will be available to catch and handle in ways to fix the
parsing error, while other errors will be raised.](/python/langchain-core/exceptions/OutputParserException)


