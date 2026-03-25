<!-- Source: https://reference.langchain.com/python/langchain-core/messages -->

Modulev1.2.21 (latest)●Since v0.1

# messages

**Messages** are objects used in prompts and chat conversations.

## Attributes

[attribute

LC\_AUTO\_PREFIX: str

LangChain auto-generated ID prefix for messages and content blocks.](/python/langchain-core/utils/utils/LC_AUTO_PREFIX)[attribute

LC\_ID\_PREFIX: str

Internal tracing/callback system identifier.

Used for:

- Tracing. Every LangChain operation (LLM call, chain execution, tool use, etc.)
  gets a unique run\_id (UUID)
- Enables tracking parent-child relationships between operations](/python/langchain-core/utils/utils/LC_ID_PREFIX)[attribute

AnyMessage

A type representing any defined `Message` or `MessageChunk` type.](/python/langchain-core/messages/utils/AnyMessage)

## Functions

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)[function

ensure\_id

Ensure the ID is a valid string, generating a new UUID if not provided.

Auto-generated UUIDs are prefixed by `'lc_'` to indicate they are
LangChain-generated IDs.](/python/langchain-core/utils/utils/ensure_id)[function

merge\_content

Merge multiple message contents.](/python/langchain-core/messages/base/merge_content)[function

message\_to\_dict

Convert a Message to a dictionary.](/python/langchain-core/messages/base/message_to_dict)[function

messages\_to\_dict

Convert a sequence of Messages to a list of dictionaries.](/python/langchain-core/messages/base/messages_to_dict)[function

convert\_to\_openai\_data\_block

Format standard data content block to format expected by OpenAI.

"Standard data content block" can include old-style LangChain v0 blocks
(URLContentBlock, Base64ContentBlock, IDContentBlock) or new ones.](/python/langchain-core/messages/block_translators/openai/convert_to_openai_data_block)[function

convert\_to\_openai\_image\_block

Convert `ImageContentBlock` to format expected by OpenAI Chat Completions.](/python/langchain-core/messages/block_translators/openai/convert_to_openai_image_block)[function

is\_data\_content\_block

Check if the provided content block is a data content block.

Returns True for both v0 (old-style) and v1 (new-style) multimodal data blocks.](/python/langchain-core/messages/content/is_data_content_block)[function

convert\_to\_messages

Convert a sequence of messages to a list of messages.](/python/langchain-core/messages/utils/convert_to_messages)[function

convert\_to\_openai\_messages

Convert LangChain messages into OpenAI message dicts.](/python/langchain-core/messages/utils/convert_to_openai_messages)[function

filter\_messages

Filter messages based on `name`, `type` or `id`.](/python/langchain-core/messages/utils/filter_messages)[function

get\_buffer\_string

Convert a sequence of messages to strings and concatenate them into one string.](/python/langchain-core/messages/utils/get_buffer_string)[function

merge\_message\_runs

Merge consecutive Messages of the same type.

Note

`ToolMessage` objects are not merged, as each has a distinct tool call id that
can't be merged.](/python/langchain-core/messages/utils/merge_message_runs)[function

message\_chunk\_to\_message

Convert a message chunk to a `Message`.](/python/langchain-core/messages/utils/message_chunk_to_message)[function

messages\_from\_dict

Convert a sequence of messages from dicts to `Message` objects.](/python/langchain-core/messages/utils/messages_from_dict)[function

trim\_messages

Trim messages to be below a token count.

`trim_messages` can be used to reduce the size of a chat history to a specified
token or message count.

In either case, if passing the trimmed chat history back into a chat model
directly, the resulting chat history should usually satisfy the following
properties:

1. The resulting chat history should be valid. Most chat models expect that chat
   history starts with either (1) a `HumanMessage` or (2) a `SystemMessage`
   followed by a `HumanMessage`. To achieve this, set `start_on='human'`.
   In addition, generally a `ToolMessage` can only appear after an `AIMessage`
   that involved a tool call.
2. It includes recent messages and drops old messages in the chat history.
   To achieve this set the `strategy='last'`.
3. Usually, the new chat history should include the `SystemMessage` if it
   was present in the original chat history since the `SystemMessage` includes
   special instructions to the chat model. The `SystemMessage` is almost always
   the first message in the history if present. To achieve this set the
   `include_system=True`.

Note

The examples below show how to configure `trim_messages` to achieve a behavior
consistent with the above properties.](/python/langchain-core/messages/utils/trim_messages)

## Classes

[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

AIMessageChunk

Message chunk from an AI (yielded when streaming).](/python/langchain-core/messages/ai/AIMessageChunk)[class

InputTokenDetails

Breakdown of input token counts.

Does *not* need to sum to full input token count. Does *not* need to have all keys.](/python/langchain-core/messages/ai/InputTokenDetails)[class

OutputTokenDetails

Breakdown of output token counts.

Does *not* need to sum to full output token count. Does *not* need to have all keys.](/python/langchain-core/messages/ai/OutputTokenDetails)[class

UsageMetadata

Usage metadata for a message, such as token counts.

This is a standard representation of token usage that is consistent across models.](/python/langchain-core/messages/ai/UsageMetadata)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

BaseMessageChunk

Message chunk, which can be concatenated with other Message chunks.](/python/langchain-core/messages/base/BaseMessageChunk)[class

ChatMessage

Message that can be assigned an arbitrary speaker (i.e. role).](/python/langchain-core/messages/chat/ChatMessage)[class

ChatMessageChunk

Chat Message chunk.](/python/langchain-core/messages/chat/ChatMessageChunk)[class

AudioContentBlock

Audio data.

Factory function

`create_audio_block` may also be used as a factory to create an
`AudioContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/AudioContentBlock)[class

Citation

Annotation for citing data from a document.

Note

`start`/`end` indices refer to the **response text**,
not the source text. This means that the indices are relative to the model's
response, not the original document (as specified in the `url`).

Factory function

`create_citation` may also be used as a factory to create a `Citation`.
Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/Citation)[class

FileContentBlock

File data that doesn't fit into other multimodal block types.

This block is intended for files that are not images, audio, or plaintext. For
example, it can be used for PDFs, Word documents, etc.

If the file is an image, audio, or plaintext, you should use the corresponding
content block type (e.g., `ImageContentBlock`, `AudioContentBlock`,
`PlainTextContentBlock`).

Factory function

`create_file_block` may also be used as a factory to create a
`FileContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/FileContentBlock)[class

ImageContentBlock

Image data.

Factory function

`create_image_block` may also be used as a factory to create an
`ImageContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/ImageContentBlock)[class

InvalidToolCall

Allowance for errors made by LLM.

Here we add an `error` key to surface errors made during generation
(e.g., invalid JSON arguments.)](/python/langchain-core/messages/content/InvalidToolCall)[class

NonStandardAnnotation

Provider-specific annotation format.](/python/langchain-core/messages/content/NonStandardAnnotation)[class

NonStandardContentBlock

Provider-specific content data.

This block contains data for which there is not yet a standard type.

The purpose of this block should be to simply hold a provider-specific payload.
If a provider's non-standard output includes reasoning and tool calls, it should be
the adapter's job to parse that payload and emit the corresponding standard
`ReasoningContentBlock` and `ToolCalls`.

Has no `extras` field, as provider-specific data should be included in the
`value` field.

Factory function

`create_non_standard_block` may also be used as a factory to create a
`NonStandardContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/NonStandardContentBlock)[class

PlainTextContentBlock

Plaintext data (e.g., from a `.txt` or `.md` document).

Note

A `PlainTextContentBlock` existed in `langchain-core<1.0.0`. Although the
name has carried over, the structure has changed significantly. The only shared
keys between the old and new versions are `type` and `text`, though the
`type` value has changed from `'text'` to `'text-plain'`.

Note

Title and context are optional fields that may be passed to the model. See
Anthropic [example](https://platform.claude.com/docs/en/build-with-claude/citations#citable-vs-non-citable-content).

Factory function

`create_plaintext_block` may also be used as a factory to create a
`PlainTextContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/PlainTextContentBlock)[class

ReasoningContentBlock

Reasoning output from a LLM.

Factory function

`create_reasoning_block` may also be used as a factory to create a
`ReasoningContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/ReasoningContentBlock)[class

ServerToolCall

Tool call that is executed server-side.

For example: code execution, web search, etc.](/python/langchain-core/messages/content/ServerToolCall)[class

ServerToolCallChunk

A chunk of a server-side tool call (yielded when streaming).](/python/langchain-core/messages/content/ServerToolCallChunk)[class

ServerToolResult

Result of a server-side tool call.](/python/langchain-core/messages/content/ServerToolResult)[class

TextContentBlock

Text output from a LLM.

This typically represents the main text content of a message, such as the response
from a language model or the text of a user message.

Factory function

`create_text_block` may also be used as a factory to create a
`TextContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/TextContentBlock)[class

VideoContentBlock

Video data.

Factory function

`create_video_block` may also be used as a factory to create a
`VideoContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/VideoContentBlock)[class

FunctionMessage

Message for passing the result of executing a tool back to a model.

`FunctionMessage` are an older version of the `ToolMessage` schema, and
do not contain the `tool_call_id` field.

The `tool_call_id` field is used to associate the tool call request with the
tool call response. Useful in situations where a chat model is able
to request multiple tool calls in parallel.](/python/langchain-core/messages/function/FunctionMessage)[class

FunctionMessageChunk

Function Message chunk.](/python/langchain-core/messages/function/FunctionMessageChunk)[class

HumanMessage

Message from the user.

A `HumanMessage` is a message that is passed in from a user to the model.](/python/langchain-core/messages/human/HumanMessage)[class

HumanMessageChunk

Human Message chunk.](/python/langchain-core/messages/human/HumanMessageChunk)[class

RemoveMessage

Message responsible for deleting other messages.](/python/langchain-core/messages/modifier/RemoveMessage)[class

SystemMessage

Message for priming AI behavior.

The system message is usually passed in as the first of a sequence
of input messages.](/python/langchain-core/messages/system/SystemMessage)[class

SystemMessageChunk

System Message chunk.](/python/langchain-core/messages/system/SystemMessageChunk)[class

ToolCall

Represents an AI's request to call a tool.](/python/langchain-core/messages/tool/ToolCall)[class

ToolCallChunk

A chunk of a tool call (yielded when streaming).

When merging `ToolCallChunk` objects (e.g., via `AIMessageChunk.__add__`), all
string attributes are concatenated. Chunks are only merged if their values of
`index` are equal and not `None`.

Example:

```
left_chunks = [ToolCallChunk(name="foo", args='{"a":', index=0)]
right_chunks = [ToolCallChunk(name=None, args="1}", index=0)]

(
    AIMessageChunk(content="", tool_call_chunks=left_chunks)
    + AIMessageChunk(content="", tool_call_chunks=right_chunks)
).tool_call_chunks == [ToolCallChunk(name="foo", args='{"a":1}', index=0)]
```](/python/langchain-core/messages/tool/ToolCallChunk)[class

ToolMessage

Message for passing the result of executing a tool back to a model.

`ToolMessage` objects contain the result of a tool invocation. Typically, the result
is encoded inside the `content` field.

`tool_call_id` is used to associate the tool call request with the tool call
response. Useful in situations where a chat model is able to request multiple tool
calls in parallel.](/python/langchain-core/messages/tool/ToolMessage)[class

ToolMessageChunk

Tool Message chunk.](/python/langchain-core/messages/tool/ToolMessageChunk)

## Type Aliases

[typeAlias

Annotation

A union of all defined `Annotation` types.](/python/langchain-core/messages/content/Annotation)[typeAlias

ContentBlock

A union of all defined `ContentBlock` types and aliases.](/python/langchain-core/messages/content/ContentBlock)[typeAlias

DataContentBlock

A union of all defined multimodal data `ContentBlock` types.](/python/langchain-core/messages/content/DataContentBlock)[typeAlias

MessageLikeRepresentation

A type representing the various ways a message can be represented.](/python/langchain-core/messages/utils/MessageLikeRepresentation)

## Modules

[module

tool

Messages for tools.](/python/langchain-core/messages/tool)[module

ai

AI message.](/python/langchain-core/messages/ai)[module

content

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
- No need to manually specify the `type` field](/python/langchain-core/messages/content)[module

base

Base message.](/python/langchain-core/messages/base)[module

modifier

Message responsible for deleting other messages.](/python/langchain-core/messages/modifier)[module

utils

Module contains utility functions for working with messages.

Some examples of what you can do with these functions include:

- Convert messages to strings (serialization)
- Convert messages from dicts to Message objects (deserialization)
- Filter messages from a list of messages based on name, type or id etc.](/python/langchain-core/messages/utils)[module

system

System message.](/python/langchain-core/messages/system)[module

function

Function Message.](/python/langchain-core/messages/function)[module

human

Human message.](/python/langchain-core/messages/human)[module

chat

Chat Message.](/python/langchain-core/messages/chat)[module

block\_translators

Derivations of standard content blocks from provider content.

`AIMessage` will first attempt to use a provider-specific translator if
`model_provider` is set in `response_metadata` on the message. Consequently, each
provider translator must handle all possible content response types from the provider,
including text.

If no provider is set, or if the provider does not have a registered translator,
`AIMessage` will fall back to best-effort parsing of the content into blocks using
the implementation in `BaseMessage`.](/python/langchain-core/messages/block_translators)


