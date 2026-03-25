<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/xml -->

Modulev1.2.21 (latest)●Since v0.1

# xml

Output parser for XML format.

## Attributes

[attribute

XML\_FORMAT\_INSTRUCTIONS: str](/python/langchain-core/output_parsers/xml/XML_FORMAT_INSTRUCTIONS)

## Functions

[function

nested\_element

Get nested element from path.](/python/langchain-core/output_parsers/xml/nested_element)

## Classes

[class

OutputParserException

Exception that output parsers should raise to signify a parsing error.

This exists to differentiate parsing errors from other code or execution errors
that also may arise inside the output parser.

`OutputParserException` will be available to catch and handle in ways to fix the
parsing error, while other errors will be raised.](/python/langchain-core/exceptions/OutputParserException)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

BaseTransformOutputParser

Base class for an output parser that can handle streaming input.](/python/langchain-core/output_parsers/transform/BaseTransformOutputParser)[class

AddableDict

Dictionary that can be added to another dictionary.](/python/langchain-core/runnables/utils/AddableDict)[class

XMLOutputParser

Parse an output using xml format.

Returns a dictionary of tags.](/python/langchain-core/output_parsers/xml/XMLOutputParser)


