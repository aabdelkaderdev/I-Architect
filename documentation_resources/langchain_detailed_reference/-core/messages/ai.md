<!-- Source: https://reference.langchain.com/python/langchain-core/messages/ai -->

Modulev1.2.21 (latest)●Since v0.1

# ai

AI message.

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

logger](/python/langchain-core/messages/ai/logger)

## Functions

[function

merge\_content

Merge multiple message contents.](/python/langchain-core/messages/base/merge_content)[function

default\_tool\_chunk\_parser

Best-effort parsing of tool chunks.](/python/langchain-core/messages/tool/default_tool_chunk_parser)[function

default\_tool\_parser

Best-effort parsing of tools.](/python/langchain-core/messages/tool/default_tool_parser)[function

create\_invalid\_tool\_call

Create an invalid tool call.](/python/langchain-core/messages/tool/invalid_tool_call)[function

create\_tool\_call

Create a tool call.](/python/langchain-core/messages/tool/tool_call)[function

create\_tool\_call\_chunk

Create a tool call chunk.](/python/langchain-core/messages/tool/tool_call_chunk)[function

merge\_dicts

Merge dictionaries.

Merge many dicts, handling specific scenarios where a key exists in both
dictionaries but has a value of `None` in `'left'`. In such cases, the method uses
the value from `'right'` for that key in the merged dictionary.](/python/langchain-core/utils/_merge/merge_dicts)[function

merge\_lists

Add many lists, handling `None`.](/python/langchain-core/utils/_merge/merge_lists)[function

parse\_partial\_json

Parse a JSON string that may be missing closing braces.](/python/langchain-core/utils/json/parse_partial_json)[function

add\_ai\_message\_chunks

Add multiple `AIMessageChunk`s together.](/python/langchain-core/messages/ai/add_ai_message_chunks)[function

add\_usage

Recursively add two UsageMetadata objects.](/python/langchain-core/messages/ai/add_usage)[function

subtract\_usage

Recursively subtract two `UsageMetadata` objects.

Token counts cannot be negative so the actual operation is `max(left - right, 0)`.](/python/langchain-core/messages/ai/subtract_usage)

## Classes

[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

BaseMessageChunk

Message chunk, which can be concatenated with other Message chunks.](/python/langchain-core/messages/base/BaseMessageChunk)[class

InvalidToolCall

Allowance for errors made by LLM.

Here we add an `error` key to surface errors made during generation
(e.g., invalid JSON arguments.)](/python/langchain-core/messages/content/InvalidToolCall)[class

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

InputTokenDetails

Breakdown of input token counts.

Does *not* need to sum to full input token count. Does *not* need to have all keys.](/python/langchain-core/messages/ai/InputTokenDetails)[class

OutputTokenDetails

Breakdown of output token counts.

Does *not* need to sum to full output token count. Does *not* need to have all keys.](/python/langchain-core/messages/ai/OutputTokenDetails)[class

UsageMetadata

Usage metadata for a message, such as token counts.

This is a standard representation of token usage that is consistent across models.](/python/langchain-core/messages/ai/UsageMetadata)[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

AIMessageChunk

Message chunk from an AI (yielded when streaming).](/python/langchain-core/messages/ai/AIMessageChunk)

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


