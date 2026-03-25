<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers -->

Modulev1.2.13 (latest)●Since v1.0

# output\_parsers

**OutputParser** classes parse the output of an LLM call.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/output_parsers/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)

## Classes

[class

BooleanOutputParser

Parse the output of an LLM call to a boolean.](/python/langchain-classic/output_parsers/boolean/BooleanOutputParser)[class

CombiningOutputParser

Combine multiple output parsers into one.](/python/langchain-classic/output_parsers/combining/CombiningOutputParser)[class

DatetimeOutputParser

Parse the output of an LLM call to a datetime.](/python/langchain-classic/output_parsers/datetime/DatetimeOutputParser)[class

EnumOutputParser

Parse an output that is one of a set of values.](/python/langchain-classic/output_parsers/enum/EnumOutputParser)[class

OutputFixingParser

Wrap a parser and try to fix parsing errors.](/python/langchain-classic/output_parsers/fix/OutputFixingParser)[class

PandasDataFrameOutputParser

Parse an output using Pandas DataFrame format.](/python/langchain-classic/output_parsers/pandas_dataframe/PandasDataFrameOutputParser)[class

RegexParser

Parse the output of an LLM call using a regex.](/python/langchain-classic/output_parsers/regex/RegexParser)[class

RegexDictParser

Parse the output of an LLM call into a Dictionary using a regex.](/python/langchain-classic/output_parsers/regex_dict/RegexDictParser)[class

RetryOutputParser

Wrap a parser and try to fix parsing errors.

Does this by passing the original prompt and the completion to another
LLM, and telling it the completion did not satisfy criteria in the prompt.](/python/langchain-classic/output_parsers/retry/RetryOutputParser)[class

RetryWithErrorOutputParser

Wrap a parser and try to fix parsing errors.

Does this by passing the original prompt, the completion, AND the error
that was raised to another language model and telling it that the completion
did not work, and raised the given error. Differs from RetryOutputParser
in that this implementation provides the error that was raised back to the
LLM, which in theory should give it more information on how to fix it.](/python/langchain-classic/output_parsers/retry/RetryWithErrorOutputParser)[class

ResponseSchema

Schema for a response from a structured output parser.](/python/langchain-classic/output_parsers/structured/ResponseSchema)[class

StructuredOutputParser

Parse the output of an LLM call to a structured output.](/python/langchain-classic/output_parsers/structured/StructuredOutputParser)[class

YamlOutputParser

Parse YAML output using a Pydantic model.](/python/langchain-classic/output_parsers/yaml/YamlOutputParser)

## Modules

[module

prompts](/python/langchain-classic/output_parsers/prompts)[module

regex\_dict](/python/langchain-classic/output_parsers/regex_dict)[module

format\_instructions](/python/langchain-classic/output_parsers/format_instructions)[module

loading](/python/langchain-classic/output_parsers/loading)[module

list](/python/langchain-classic/output_parsers/list)[module

fix](/python/langchain-classic/output_parsers/fix)[module

datetime](/python/langchain-classic/output_parsers/datetime)[module

pandas\_dataframe](/python/langchain-classic/output_parsers/pandas_dataframe)[module

yaml](/python/langchain-classic/output_parsers/yaml)[module

rail\_parser](/python/langchain-classic/output_parsers/rail_parser)[module

json](/python/langchain-classic/output_parsers/json)[module

openai\_tools](/python/langchain-classic/output_parsers/openai_tools)[module

regex](/python/langchain-classic/output_parsers/regex)[module

enum](/python/langchain-classic/output_parsers/enum)[module

structured](/python/langchain-classic/output_parsers/structured)[module

combining](/python/langchain-classic/output_parsers/combining)[module

ernie\_functions](/python/langchain-classic/output_parsers/ernie_functions)[module

retry](/python/langchain-classic/output_parsers/retry)[module

pydantic](/python/langchain-classic/output_parsers/pydantic)[module

boolean](/python/langchain-classic/output_parsers/boolean)[module

openai\_functions](/python/langchain-classic/output_parsers/openai_functions)[module

xml](/python/langchain-classic/output_parsers/xml)


