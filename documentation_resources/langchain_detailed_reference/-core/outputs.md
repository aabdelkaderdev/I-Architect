<!-- Source: https://reference.langchain.com/python/langchain-core/outputs -->

Modulev1.2.21 (latest)●Since v0.1

# outputs

Output classes.

Used to represent the output of a language model call and the output of a chat.

The top container for information is the `LLMResult` object. `LLMResult` is used by both
chat models and LLMs. This object contains the output of the language model and any
additional information that the model provider wants to return.

When invoking models via the standard runnable methods (e.g. invoke, batch, etc.):

- Chat models will return `AIMessage` objects.
- LLMs will return regular text strings.

In addition, users can access the raw output of either LLMs or chat models via
callbacks. The `on_chat_model_end` and `on_llm_end` callbacks will return an `LLMResult`
object containing the generated outputs and any additional information returned by the
model provider.

In general, if information is already available in the AIMessage object, it is
recommended to access it from there rather than from the `LLMResult` object.

## Functions

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)

## Classes

[class

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

GenerationChunk

`GenerationChunk`, which can be concatenated with other `Generation` chunks.](/python/langchain-core/outputs/generation/GenerationChunk)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)[class

RunInfo

Class that contains metadata for a single execution of a chain or model.

Defined for backwards compatibility with older versions of `langchain_core`.

Users can acquire the `run_id` information from callbacks or via `run_id`
information present in the `astream_event` API (depending on the use case).](/python/langchain-core/outputs/run_info/RunInfo)

## Modules

[module

chat\_result

Chat result schema.](/python/langchain-core/outputs/chat_result)[module

llm\_result

`LLMResult` class.](/python/langchain-core/outputs/llm_result)[module

run\_info

`RunInfo` class.](/python/langchain-core/outputs/run_info)[module

generation

Generation output schema.](/python/langchain-core/outputs/generation)[module

chat\_generation

Chat generation output classes.](/python/langchain-core/outputs/chat_generation)


