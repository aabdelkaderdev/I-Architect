<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models -->

Modulev1.2.21 (latest)●Since v0.1

# chat\_models

Chat models for conversational AI.

## Attributes

[attribute

AnyMessage

A type representing any defined `Message` or `MessageChunk` type.](/python/langchain-core/messages/utils/AnyMessage)[attribute

RunnableMap: RunnableParallel](/python/langchain-core/runnables/base/RunnableMap)[attribute

TypeBaseModel: type[BaseModel]](/python/langchain-core/utils/pydantic/TypeBaseModel)[attribute

LC\_ID\_PREFIX: str

Internal tracing/callback system identifier.

Used for:

- Tracing. Every LangChain operation (LLM call, chain execution, tool use, etc.)
  gets a unique run\_id (UUID)
- Enables tracking parent-child relationships between operations](/python/langchain-core/utils/utils/LC_ID_PREFIX)[attribute

OutputParserLike: Runnable[LanguageModelOutput, T]](/python/langchain-core/output_parsers/base/OutputParserLike)

## Functions

[function

get\_llm\_cache

Get the value of the `llm_cache` global setting.](/python/langchain-core/globals/get_llm_cache)[function

dumpd

Return a dict representation of an object.](/python/langchain-core/load/dump/dumpd)[function

dumps

Return a JSON string representation of an object.](/python/langchain-core/load/dump/dumps)[function

convert\_to\_messages

Convert a sequence of messages to a list of messages.](/python/langchain-core/messages/utils/convert_to_messages)[function

is\_data\_content\_block

Check if the provided content block is a data content block.

Returns True for both v0 (old-style) and v1 (new-style) multimodal data blocks.](/python/langchain-core/messages/content/is_data_content_block)[function

message\_chunk\_to\_message

Convert a message chunk to a `Message`.](/python/langchain-core/messages/utils/message_chunk_to_message)[function

convert\_to\_openai\_image\_block

Convert `ImageContentBlock` to format expected by OpenAI Chat Completions.](/python/langchain-core/messages/block_translators/openai/convert_to_openai_image_block)[function

merge\_chat\_generation\_chunks

Merge a list of `ChatGenerationChunk`s into a single `ChatGenerationChunk`.](/python/langchain-core/outputs/chat_generation/merge_chat_generation_chunks)[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)[function

convert\_to\_json\_schema

Convert a schema representation to a JSON schema.](/python/langchain-core/utils/function_calling/convert_to_json_schema)[function

convert\_to\_openai\_tool

Convert a tool-like object to an OpenAI tool schema.

[OpenAI tool schema reference](https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools)](/python/langchain-core/utils/function_calling/convert_to_openai_tool)[function

is\_basemodel\_subclass

Check if the given class is a subclass of Pydantic `BaseModel`.

Check if the given class is a subclass of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x](/python/langchain-core/utils/pydantic/is_basemodel_subclass)[function

from\_env

Create a factory method that gets a value from an environment variable.](/python/langchain-core/utils/utils/from_env)[function

generate\_from\_stream

Generate from a stream.](/python/langchain-core/language_models/chat_models/generate_from_stream)[function

agenerate\_from\_stream

Async generate from a stream.](/python/langchain-core/language_models/chat_models/agenerate_from_stream)

## Classes

[class

BaseCache

Interface for a caching layer for LLMs and Chat models.

The cache interface consists of the following methods:

- lookup: Look up a value based on a prompt and `llm_string`.
- update: Update the cache based on a prompt and `llm_string`.
- clear: Clear the cache.

In addition, the cache interface provides an async version of each method.

The default implementation of the async methods is to run the synchronous
method in an executor. It's recommended to override the async methods
and provide async implementations to avoid unnecessary overhead.](/python/langchain-core/caches/BaseCache)[class

AsyncCallbackManager

Async callback manager that handles callbacks from LangChain.](/python/langchain-core/callbacks/manager/AsyncCallbackManager)[class

AsyncCallbackManagerForLLMRun

Async callback manager for LLM run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForLLMRun)[class

CallbackManager

Callback manager for LangChain.](/python/langchain-core/callbacks/manager/CallbackManager)[class

CallbackManagerForLLMRun

Callback manager for LLM run.](/python/langchain-core/callbacks/manager/CallbackManagerForLLMRun)[class

BaseLanguageModel

Abstract base class for interfacing with language models.

All language model wrappers inherited from `BaseLanguageModel`.](/python/langchain-core/language_models/base/BaseLanguageModel)[class

LangSmithParams

LangSmith parameters for tracing.](/python/langchain-core/language_models/base/LangSmithParams)[class

ModelProfile

Model profile.

Beta feature

This is a beta feature. The format of model profiles is subject to change.

Provides information about chat model capabilities, such as context window sizes
and supported features.](/python/langchain-core/language_models/model_profile/ModelProfile)[class

AIMessage

Message from an AI.

An `AIMessage` is returned from a chat model as a response to a prompt.

This message represents the output of the model and consists of both
the raw output as returned by the model and standardized fields
(e.g., tool calls, usage metadata) added by the LangChain framework.](/python/langchain-core/messages/ai/AIMessage)[class

AIMessageChunk

Message chunk from an AI (yielded when streaming).](/python/langchain-core/messages/ai/AIMessageChunk)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

JsonOutputKeyToolsParser

Parse tools from OpenAI response.](/python/langchain-core/output_parsers/openai_tools/JsonOutputKeyToolsParser)[class

PydanticToolsParser

Parse tools from OpenAI response.](/python/langchain-core/output_parsers/openai_tools/PydanticToolsParser)[class

ChatGeneration

A single chat generation output.

A subclass of `Generation` that represents the response from a chat model that
generates chat messages.

The `message` attribute is a structured representation of the chat message. Most of
the time, the message will be of type `AIMessage`.

Users working with chat models will usually access information via either
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks).](/python/langchain-core/outputs/chat_generation/ChatGeneration)[class

ChatGenerationChunk

`ChatGeneration` chunk.

`ChatGeneration` chunks can be concatenated with other `ChatGeneration` chunks.](/python/langchain-core/outputs/chat_generation/ChatGenerationChunk)[class

ChatResult

Use to represent the result of a chat model call with a single prompt.

This container is used internally by some implementations of chat model, it will
eventually be mapped to a more general `LLMResult` object, and then projected into
an `AIMessage` object.

LangChain users working with chat models will usually access information via
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks). Please refer the `AIMessage` and `LLMResult` schema documentation for
more information.](/python/langchain-core/outputs/chat_result/ChatResult)[class

Generation

A single text generation output.

Generation represents the response from an "old-fashioned" LLM (string-in,
string-out) that generates regular text (not chat messages).

This model is used internally by chat model and will eventually be mapped to a more
general `LLMResult` object, and then projected into an `AIMessage` object.

LangChain users working with chat models will usually access information via
`AIMessage` (returned from runnable interfaces) or `LLMResult` (available via
callbacks). Please refer to `AIMessage` and `LLMResult` for more information.](/python/langchain-core/outputs/generation/Generation)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)[class

RunInfo

Information about a run.

This is used to keep track of the metadata associated with a run.](/python/langchain-core/tracers/event_stream/RunInfo)[class

ChatPromptValue

Chat prompt value.

A type of a prompt value that is built from messages.](/python/langchain-core/prompt_values/ChatPromptValue)[class

PromptValue

Base abstract class for inputs to any language model.

`PromptValues` can be converted to both LLM (pure text-generation) inputs and
chat model inputs.](/python/langchain-core/prompt_values/PromptValue)[class

StringPromptValue

String prompt value.](/python/langchain-core/prompt_values/StringPromptValue)[class

BaseRateLimiter

Base class for rate limiters.

Usage of the base limiter is through the acquire and aacquire methods depending
on whether running in a sync or async context.

Implementations are free to add a timeout parameter to their initialize method
to allow users to specify a timeout for acquiring the necessary tokens when
using a blocking call.

Current limitations:

- Rate limiting information is not surfaced in tracing or callbacks. This means
  that the total time it takes to invoke a chat model will encompass both
  the time spent waiting for tokens and the time spent making the request.](/python/langchain-core/rate_limiters/BaseRateLimiter)[class

RunnablePassthrough

Runnable to passthrough inputs unchanged or with additional keys.

This `Runnable` behaves almost like the identity function, except that it
can be configured to add additional keys to the output, if the input is a
dict.

The examples below demonstrate this `Runnable` works using a few simple
chains. The chains rely on simple lambdas to make the examples easy to execute
and experiment with.](/python/langchain-core/runnables/passthrough/RunnablePassthrough)[class

Runnable

A unit of work that can be invoked, batched, streamed, transformed and composed.

# Key Methods

- `invoke`/`ainvoke`: Transforms a single input into an output.
- `batch`/`abatch`: Efficiently transforms multiple inputs into outputs.
- `stream`/`astream`: Streams output from a single input as it's produced.
- `astream_log`: Streams output and selected intermediate results from an
  input.

Built-in optimizations:

- **Batch**: By default, batch runs invoke() in parallel using a thread pool
  executor. Override to optimize batching.
- **Async**: Methods with `'a'` prefix are asynchronous. By default, they execute
  the sync counterpart using asyncio's thread pool.
  Override for native async.

All methods accept an optional config argument, which can be used to configure
execution, add tags and metadata for tracing and debugging etc.

Runnables expose schematic information about their input, output and config via
the `input_schema` property, the `output_schema` property and `config_schema`
method.

# Composition

Runnable objects can be composed together to create chains in a declarative way.

Any chain constructed this way will automatically have sync, async, batch, and
streaming support.

The main composition primitives are `RunnableSequence` and `RunnableParallel`.

**`RunnableSequence`** invokes a series of runnables sequentially, with
one Runnable's output serving as the next's input. Construct using
the `|` operator or by passing a list of runnables to `RunnableSequence`.

**`RunnableParallel`** invokes runnables concurrently, providing the same input
to each. Construct it using a dict literal within a sequence or by passing a
dict to `RunnableParallel`.

For example,

```
from langchain_core.runnables import RunnableLambda

# A RunnableSequence constructed using the `|` operator
sequence = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2)
sequence.invoke(1)  # 4
sequence.batch([1, 2, 3])  # [4, 6, 8]

# A sequence that contains a RunnableParallel constructed using a dict literal
sequence = RunnableLambda(lambda x: x + 1) | {
    "mul_2": RunnableLambda(lambda x: x * 2),
    "mul_5": RunnableLambda(lambda x: x * 5),
}
sequence.invoke(1)  # {'mul_2': 4, 'mul_5': 10}
```

# Standard Methods

All `Runnable`s expose additional methods that can be used to modify their
behavior (e.g., add a retry policy, add lifecycle listeners, make them
configurable, etc.).

These methods will work on any `Runnable`, including `Runnable` chains
constructed by composing other `Runnable`s.
See the individual methods for details.

For example,

```
from langchain_core.runnables import RunnableLambda

import random

def add_one(x: int) -> int:
    return x + 1

def buggy_double(y: int) -> int:
    """Buggy code that will fail 70% of the time"""
    if random.random() > 0.3:
        print('This code failed, and will probably be retried!')  # noqa: T201
        raise ValueError('Triggered buggy code')
    return y * 2

sequence = (
    RunnableLambda(add_one) |
    RunnableLambda(buggy_double).with_retry( # Retry on failure
        stop_after_attempt=10,
        wait_exponential_jitter=False
    )
)

print(sequence.input_schema.model_json_schema()) # Show inferred input schema
print(sequence.output_schema.model_json_schema()) # Show inferred output schema
print(sequence.invoke(2)) # invoke the sequence (note the retry above!!)
```

# Debugging and tracing

As the chains get longer, it can be useful to be able to see intermediate results
to debug and trace the chain.

You can set the global debug flag to True to enable debug output for all chains:

```
from langchain_core.globals import set_debug

set_debug(True)
```

Alternatively, you can pass existing or custom callbacks to any given chain:

```
from langchain_core.tracers import ConsoleCallbackHandler

chain.invoke(..., config={"callbacks": [ConsoleCallbackHandler()]})
```

For a UI (and much more) checkout [LangSmith](https://docs.langchain.com/langsmith/home).](/python/langchain-core/runnables/base/Runnable)[class

RunnableConfig

Configuration for a `Runnable`.

Note

Custom values

The `TypedDict` has `total=False` set intentionally to:

- Allow partial configs to be created and merged together via `merge_configs`
- Support config propagation from parent to child runnables via
  `var_child_runnable_config` (a `ContextVar` that automatically passes
  config down the call stack without explicit parameter passing), where
  configs are merged rather than replaced

Example

```
# Parent sets tags
chain.invoke(input, config={"tags": ["parent"]})
# Child automatically inherits and can add:
# ensure_config({"tags": ["child"]}) -> {"tags": ["parent", "child"]}
```](/python/langchain-core/runnables/config/RunnableConfig)[class

BaseTool

Base class for all LangChain tools.

This abstract class defines the interface that all LangChain tools must implement.

Tools are components that can be called by agents to perform specific actions.](/python/langchain-core/tools/base/BaseTool)[class

BaseChatModel

Base class for chat models.](/python/langchain-core/language_models/chat_models/BaseChatModel)[class

SimpleChatModel

Simplified implementation for a chat model to inherit from.

Note

This implementation is primarily here for backwards compatibility. For new
implementations, please use `BaseChatModel` directly.](/python/langchain-core/language_models/chat_models/SimpleChatModel)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)[typeAlias

LanguageModelInput

Input to a language model.](/python/langchain-core/language_models/base/LanguageModelInput)

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


