<!-- Source: https://reference.langchain.com/python/langchain-core/prompt_values -->

Modulev1.2.21 (latest)●Since v0.1

# prompt\_values

**Prompt values** for language model prompts.

Prompt values are used to represent different pieces of prompts. They can be used to
represent text, images, or chat message pieces.

## Attributes

[attribute

AnyMessage

A type representing any defined `Message` or `MessageChunk` type.](/python/langchain-core/messages/utils/AnyMessage)

## Functions

[function

get\_buffer\_string

Convert a sequence of messages to strings and concatenate them into one string.](/python/langchain-core/messages/utils/get_buffer_string)

## Classes

[class

Serializable

Serializable base class.

This class is used to serialize objects to JSON.

It relies on the following methods and properties:

- [`is_lc_serializable`](/python/langchain-core/load/serializable/Serializable/is_lc_serializable): Is this class serializable?

  By design, even if a class inherits from `Serializable`, it is not serializable
  by default. This is to prevent accidental serialization of objects that should
  not be serialized.
- [`get_lc_namespace`](/python/langchain-core/load/serializable/Serializable/get_lc_namespace): Get the namespace of the LangChain object.

  During deserialization, this namespace is used to identify
  the correct class to instantiate.

  Please see the `Reviver` class in `langchain_core.load.load` for more details.

  During deserialization an additional mapping is handle classes that have moved
  or been renamed across package versions.
- [`lc_secrets`](/python/langchain-core/load/serializable/Serializable/lc_secrets): A map of constructor argument names to secret ids.
- [`lc_attributes`](/python/langchain-core/load/serializable/Serializable/lc_attributes): List of additional attribute names that should be included
  as part of the serialized representation.](/python/langchain-core/load/serializable/Serializable)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

HumanMessage

Message from the user.

A `HumanMessage` is a message that is passed in from a user to the model.](/python/langchain-core/messages/human/HumanMessage)[class

PromptValue

Base abstract class for inputs to any language model.

`PromptValues` can be converted to both LLM (pure text-generation) inputs and
chat model inputs.](/python/langchain-core/prompt_values/PromptValue)[class

StringPromptValue

String prompt value.](/python/langchain-core/prompt_values/StringPromptValue)[class

ChatPromptValue

Chat prompt value.

A type of a prompt value that is built from messages.](/python/langchain-core/prompt_values/ChatPromptValue)[class

ImageURL

Image URL for multimodal model inputs (OpenAI format).

Represents the inner `image_url` object in OpenAI's Chat Completion API format. This
is used by `ImagePromptTemplate` and `ChatPromptTemplate`.](/python/langchain-core/prompt_values/ImageURL)[class

ImagePromptValue

Image prompt value.](/python/langchain-core/prompt_values/ImagePromptValue)[class

ChatPromptValueConcrete

Chat prompt value which explicitly lists out the message types it accepts.

For use in external schemas.](/python/langchain-core/prompt_values/ChatPromptValueConcrete)


