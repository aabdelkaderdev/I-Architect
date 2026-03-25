<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base -->

Modulev1.2.21 (latest)●Since v0.1

# base

Base message.

## Functions

[function

warn\_deprecated

Display a standardized deprecation.](/python/langchain-core/_api/deprecation/warn_deprecated)[function

get\_bolded\_text

Get bolded text.](/python/langchain-core/utils/input/get_bolded_text)[function

merge\_dicts

Merge dictionaries.

Merge many dicts, handling specific scenarios where a key exists in both
dictionaries but has a value of `None` in `'left'`. In such cases, the method uses
the value from `'right'` for that key in the merged dictionary.](/python/langchain-core/utils/_merge/merge_dicts)[function

merge\_lists

Add many lists, handling `None`.](/python/langchain-core/utils/_merge/merge_lists)[function

is\_interactive\_env

Determine if running within IPython or Jupyter.](/python/langchain-core/utils/interactive_env/is_interactive_env)[function

merge\_content

Merge multiple message contents.](/python/langchain-core/messages/base/merge_content)[function

message\_to\_dict

Convert a Message to a dictionary.](/python/langchain-core/messages/base/message_to_dict)[function

messages\_to\_dict

Convert a sequence of Messages to a list of dictionaries.](/python/langchain-core/messages/base/messages_to_dict)[function

get\_msg\_title\_repr

Get a title representation for a message.](/python/langchain-core/messages/base/get_msg_title_repr)

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

ChatPromptTemplate

Prompt template for chat models.

Use to create flexible templated prompts for chat models.

Example

```
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot. Your name is {name}."),
        ("human", "Hello, how are you doing?"),
        ("ai", "I'm doing well, thanks!"),
        ("human", "{user_input}"),
    ]
)

prompt_value = template.invoke(
    {
        "name": "Bob",
        "user_input": "What is your name?",
    }
)
# Output:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot. Your name is Bob.'),
#        HumanMessage(content='Hello, how are you doing?'),
#        AIMessage(content="I'm doing well, thanks!"),
#        HumanMessage(content='What is your name?')
#    ]
# )
```

Messages Placeholder

```
# In addition to Human/AI/Tool/Function messages,
# you can initialize the template with a MessagesPlaceholder
# either using the class directly or with the shorthand tuple syntax:

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot."),
        # Means the template will receive an optional list of messages under
        # the "conversation" key
        ("placeholder", "{conversation}"),
        # Equivalently:
        # MessagesPlaceholder(variable_name="conversation", optional=True)
    ]
)

prompt_value = template.invoke(
    {
        "conversation": [
            ("human", "Hi!"),
            ("ai", "How can I assist you today?"),
            ("human", "Can you make me an ice cream sundae?"),
            ("ai", "No."),
        ]
    }
)

# Output:
# ChatPromptValue(
#    messages=[
#        SystemMessage(content='You are a helpful AI bot.'),
#        HumanMessage(content='Hi!'),
#        AIMessage(content='How can I assist you today?'),
#        HumanMessage(content='Can you make me an ice cream sundae?'),
#        AIMessage(content='No.'),
#    ]
# )
```

Single-variable template

If your prompt has only a single input variable (i.e., one instance of
`'{variable_nams}'`), and you invoke the template with a non-dict object, the
prompt template will inject the provided argument into that variable location.

```
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful AI bot. Your name is Carl."),
        ("human", "{user_input}"),
    ]
)

prompt_value = template.invoke("Hello, there!")
# Equivalent to
# prompt_value = template.invoke({"user_input": "Hello, there!"})

# Output:
#  ChatPromptValue(
#     messages=[
#         SystemMessage(content='You are a helpful AI bot. Your name is Carl.'),
#         HumanMessage(content='Hello, there!'),
#     ]
# )
```](/python/langchain-core/prompts/chat/ChatPromptTemplate)[class

TextAccessor

String-like object that supports both property and method access patterns.

Exists to maintain backward compatibility while transitioning from method-based to
property-based text access in message objects. In LangChain <v1.0, message text was
accessed via `.text()` method calls. In v1.0=<, the preferred pattern is property
access via `.text`.

Rather than breaking existing code immediately, `TextAccessor` allows both
patterns:

- Modern property access: `message.text` (returns string directly)
- Legacy method access: `message.text()` (callable, emits deprecation warning)](/python/langchain-core/messages/base/TextAccessor)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

BaseMessageChunk

Message chunk, which can be concatenated with other Message chunks.](/python/langchain-core/messages/base/BaseMessageChunk)

## Modules

[module

types

Standard, multimodal content blocks for Large Language Model I/O.

This module provides standardized data structures for representing inputs to and outputs
from LLMs. The core abstraction is the **Content Block**, a `TypedDict`.

**Rationale**

Different LLM providers use distinct and incompatible API schemas. This module provides
a unified, provider-agnostic format to facilitate these interactions. A message to or
from a model is simply a list of content blocks, allowing for the natural interleaving
of text, images, and other content in a single ordered sequence.

An adapter for a specific provider is responsible for translating this standard list of
blocks into the format required by its API.

**Extensibility**

Data **not yet mapped** to a standard block may be represented using the
`NonStandardContentBlock`, which allows for provider-specific data to be included
without losing the benefits of type checking and validation.

Furthermore, provider-specific fields **within** a standard block are fully supported
by default in the `extras` field of each block. This allows for additional metadata
to be included without breaking the standard structure. For example, Google's thought
signature:

```
AIMessage(
    content=[
        {
            "type": "text",
            "text": "J'adore la programmation.",
            "extras": {"signature": "EpoWCpc..."},  # Thought signature
        }
    ], ...
)
```

Note

Following widespread adoption of [PEP 728](https://peps.python.org/pep-0728/), we
intend to add `extra_items=Any` as a param to Content Blocks. This will signify to
type checkers that additional provider-specific fields are allowed outside of the
`extras` field, and that will become the new standard approach to adding
provider-specific metadata.

Note

**Example with PEP 728 provider-specific fields:**

```
# Content block definition
# NOTE: `extra_items=Any`
class TextContentBlock(TypedDict, extra_items=Any):
    type: Literal["text"]
    id: NotRequired[str]
    text: str
    annotations: NotRequired[list[Annotation]]
    index: NotRequired[int]
```

```
from langchain_core.messages.content import TextContentBlock

# Create a text content block with provider-specific fields
my_block: TextContentBlock = {
    # Add required fields
    "type": "text",
    "text": "Hello, world!",
    # Additional fields not specified in the TypedDict
    # These are valid with PEP 728 and are typed as Any
    "openai_metadata": {"model": "gpt-4", "temperature": 0.7},
    "anthropic_usage": {"input_tokens": 10, "output_tokens": 20},
    "custom_field": "any value",
}

# Mutating an existing block to add provider-specific fields
openai_data = my_block["openai_metadata"]  # Type: Any
```

**Example Usage**

```
# Direct construction
from langchain_core.messages.content import TextContentBlock, ImageContentBlock

multimodal_message: AIMessage(
    content_blocks=[
        TextContentBlock(type="text", text="What is shown in this image?"),
        ImageContentBlock(
            type="image",
            url="https://www.langchain.com/images/brand/langchain_logo_text_w_white.png",
            mime_type="image/png",
        ),
    ]
)

# Using factories
from langchain_core.messages.content import create_text_block, create_image_block

multimodal_message: AIMessage(
    content=[
        create_text_block("What is shown in this image?"),
        create_image_block(
            url="https://www.langchain.com/images/brand/langchain_logo_text_w_white.png",
            mime_type="image/png",
        ),
    ]
)
```

Factory functions offer benefits such as:

- Automatic ID generation (when not provided)
- No need to manually specify the `type` field](/python/langchain-core/messages/content)


