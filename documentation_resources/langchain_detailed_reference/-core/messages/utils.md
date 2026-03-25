<!-- Source: https://reference.langchain.com/python/langchain-core/messages/utils -->

Modulev1.2.21 (latest)●Since v0.1

# utils

Module contains utility functions for working with messages.

Some examples of what you can do with these functions include:

- Convert messages to strings (serialization)
- Convert messages from dicts to Message objects (deserialization)
- Filter messages from a list of messages based on name, type or id etc.

## Attributes

[attribute

logger](/python/langchain-core/messages/utils/logger)[attribute

AnyMessage

A type representing any defined `Message` or `MessageChunk` type.](/python/langchain-core/messages/utils/AnyMessage)

## Functions

[function

create\_message

Create a message with a link to the LangChain troubleshooting guide.](/python/langchain-core/exceptions/create_message)[function

convert\_to\_openai\_data\_block

Format standard data content block to format expected by OpenAI.

"Standard data content block" can include old-style LangChain v0 blocks
(URLContentBlock, Base64ContentBlock, IDContentBlock) or new ones.](/python/langchain-core/messages/block_translators/openai/convert_to_openai_data_block)[function

is\_data\_content\_block

Check if the provided content block is a data content block.

Returns True for both v0 (old-style) and v1 (new-style) multimodal data blocks.](/python/langchain-core/messages/content/is_data_content_block)[function

convert\_to\_openai\_tool

Convert a tool-like object to an OpenAI tool schema.

[OpenAI tool schema reference](https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools)](/python/langchain-core/utils/function_calling/convert_to_openai_tool)[function

get\_buffer\_string

Convert a sequence of messages to strings and concatenate them into one string.](/python/langchain-core/messages/utils/get_buffer_string)[function

messages\_from\_dict

Convert a sequence of messages from dicts to `Message` objects.](/python/langchain-core/messages/utils/messages_from_dict)[function

message\_chunk\_to\_message

Convert a message chunk to a `Message`.](/python/langchain-core/messages/utils/message_chunk_to_message)[function

convert\_to\_messages

Convert a sequence of messages to a list of messages.](/python/langchain-core/messages/utils/convert_to_messages)[function

filter\_messages

Filter messages based on `name`, `type` or `id`.](/python/langchain-core/messages/utils/filter_messages)[function

merge\_message\_runs

Merge consecutive Messages of the same type.

Note

`ToolMessage` objects are not merged, as each has a distinct tool call id that
can't be merged.](/python/langchain-core/messages/utils/merge_message_runs)[function

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
consistent with the above properties.](/python/langchain-core/messages/utils/trim_messages)[function

convert\_to\_openai\_messages

Convert LangChain messages into OpenAI message dicts.](/python/langchain-core/messages/utils/convert_to_openai_messages)[function

count\_tokens\_approximately

Approximate the total number of tokens in messages.

The token count includes stringified message content, role, and (optionally) name.

- For AI messages, the token count also includes stringified tool calls.
- For tool messages, the token count also includes the tool call ID.
- For multimodal messages with images, applies a fixed token penalty per image
  instead of counting base64-encoded characters.
- If tools are provided, the token count also includes stringified tool schemas.](/python/langchain-core/messages/utils/count_tokens_approximately)

## Classes

[class

ErrorCode

Error codes.](/python/langchain-core/exceptions/ErrorCode)[class

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

BaseMessageChunk

Message chunk, which can be concatenated with other Message chunks.](/python/langchain-core/messages/base/BaseMessageChunk)[class

ChatMessage

Message that can be assigned an arbitrary speaker (i.e. role).](/python/langchain-core/messages/chat/ChatMessage)[class

ChatMessageChunk

Chat Message chunk.](/python/langchain-core/messages/chat/ChatMessageChunk)[class

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

ToolMessage

Message for passing the result of executing a tool back to a model.

`ToolMessage` objects contain the result of a tool invocation. Typically, the result
is encoded inside the `content` field.

`tool_call_id` is used to associate the tool call request with the tool call
response. Useful in situations where a chat model is able to request multiple tool
calls in parallel.](/python/langchain-core/messages/tool/ToolMessage)[class

ToolMessageChunk

Tool Message chunk.](/python/langchain-core/messages/tool/ToolMessageChunk)[class

BaseLanguageModel

Abstract base class for interfacing with language models.

All language model wrappers inherited from `BaseLanguageModel`.](/python/langchain-core/language_models/base/BaseLanguageModel)[class

PromptValue

Base abstract class for inputs to any language model.

`PromptValues` can be converted to both LLM (pure text-generation) inputs and
chat model inputs.](/python/langchain-core/prompt_values/PromptValue)[class

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

BaseTool

Base class for all LangChain tools.

This abstract class defines the interface that all LangChain tools must implement.

Tools are components that can be called by agents to perform specific actions.](/python/langchain-core/tools/base/BaseTool)

## Type Aliases

[typeAlias

MessageLikeRepresentation

A type representing the various ways a message can be represented.](/python/langchain-core/messages/utils/MessageLikeRepresentation)


