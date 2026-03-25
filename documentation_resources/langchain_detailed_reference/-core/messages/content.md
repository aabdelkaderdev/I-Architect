<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content -->

Modulev1.2.21 (latest)●Since v1.0

# content

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
- No need to manually specify the `type` field

## Attributes

[attribute

KNOWN\_BLOCK\_TYPES: set

These are block types known to `langchain-core >= 1.0.0`.

If a block has a type not in this set, it is considered to be provider-specific.](/python/langchain-core/messages/content/KNOWN_BLOCK_TYPES)

## Functions

[function

ensure\_id

Ensure the ID is a valid string, generating a new UUID if not provided.

Auto-generated UUIDs are prefixed by `'lc_'` to indicate they are
LangChain-generated IDs.](/python/langchain-core/utils/utils/ensure_id)[function

is\_data\_content\_block

Check if the provided content block is a data content block.

Returns True for both v0 (old-style) and v1 (new-style) multimodal data blocks.](/python/langchain-core/messages/content/is_data_content_block)[function

create\_text\_block

Create a `TextContentBlock`.](/python/langchain-core/messages/content/create_text_block)[function

create\_image\_block

Create an `ImageContentBlock`.](/python/langchain-core/messages/content/create_image_block)[function

create\_video\_block

Create a `VideoContentBlock`.](/python/langchain-core/messages/content/create_video_block)[function

create\_audio\_block

Create an `AudioContentBlock`.](/python/langchain-core/messages/content/create_audio_block)[function

create\_file\_block

Create a `FileContentBlock`.](/python/langchain-core/messages/content/create_file_block)[function

create\_plaintext\_block

Create a `PlainTextContentBlock`.](/python/langchain-core/messages/content/create_plaintext_block)[function

create\_tool\_call

Create a `ToolCall`.](/python/langchain-core/messages/content/create_tool_call)[function

create\_reasoning\_block

Create a `ReasoningContentBlock`.](/python/langchain-core/messages/content/create_reasoning_block)[function

create\_citation

Create a `Citation`.](/python/langchain-core/messages/content/create_citation)[function

create\_non\_standard\_block

Create a `NonStandardContentBlock`.](/python/langchain-core/messages/content/create_non_standard_block)

## Classes

[class

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

NonStandardAnnotation

Provider-specific annotation format.](/python/langchain-core/messages/content/NonStandardAnnotation)[class

TextContentBlock

Text output from a LLM.

This typically represents the main text content of a message, such as the response
from a language model or the text of a user message.

Factory function

`create_text_block` may also be used as a factory to create a
`TextContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/TextContentBlock)[class

ToolCall

Represents an AI's request to call a tool.](/python/langchain-core/messages/content/ToolCall)[class

ToolCallChunk

A chunk of a tool call (yielded when streaming).

When merging `ToolCallChunks` (e.g., via `AIMessageChunk.__add__`),
all string attributes are concatenated. Chunks are only merged if their
values of `index` are equal and not `None`.

Example:

```
left_chunks = [ToolCallChunk(name="foo", args='{"a":', index=0)]
right_chunks = [ToolCallChunk(name=None, args="1}", index=0)]

(
    AIMessageChunk(content="", tool_call_chunks=left_chunks)
    + AIMessageChunk(content="", tool_call_chunks=right_chunks)
).tool_call_chunks == [ToolCallChunk(name="foo", args='{"a":1}', index=0)]
```](/python/langchain-core/messages/content/ToolCallChunk)[class

InvalidToolCall

Allowance for errors made by LLM.

Here we add an `error` key to surface errors made during generation
(e.g., invalid JSON arguments.)](/python/langchain-core/messages/content/InvalidToolCall)[class

ServerToolCall

Tool call that is executed server-side.

For example: code execution, web search, etc.](/python/langchain-core/messages/content/ServerToolCall)[class

ServerToolCallChunk

A chunk of a server-side tool call (yielded when streaming).](/python/langchain-core/messages/content/ServerToolCallChunk)[class

ServerToolResult

Result of a server-side tool call.](/python/langchain-core/messages/content/ServerToolResult)[class

ReasoningContentBlock

Reasoning output from a LLM.

Factory function

`create_reasoning_block` may also be used as a factory to create a
`ReasoningContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/ReasoningContentBlock)[class

ImageContentBlock

Image data.

Factory function

`create_image_block` may also be used as a factory to create an
`ImageContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/ImageContentBlock)[class

VideoContentBlock

Video data.

Factory function

`create_video_block` may also be used as a factory to create a
`VideoContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/VideoContentBlock)[class

AudioContentBlock

Audio data.

Factory function

`create_audio_block` may also be used as a factory to create an
`AudioContentBlock`. Benefits include:

- Automatic ID generation (when not provided)
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/AudioContentBlock)[class

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
- Required arguments strictly validated at creation time](/python/langchain-core/messages/content/NonStandardContentBlock)

## Type Aliases

[typeAlias

Annotation

A union of all defined `Annotation` types.](/python/langchain-core/messages/content/Annotation)[typeAlias

DataContentBlock

A union of all defined multimodal data `ContentBlock` types.](/python/langchain-core/messages/content/DataContentBlock)[typeAlias

ToolContentBlock](/python/langchain-core/messages/content/ToolContentBlock)[typeAlias

ContentBlock

A union of all defined `ContentBlock` types and aliases.](/python/langchain-core/messages/content/ContentBlock)


