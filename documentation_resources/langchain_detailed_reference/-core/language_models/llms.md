<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/llms -->

Modulev1.2.21 (latest)●Since v0.1

# llms

Base interface for traditional large language models (LLMs) to expose.

These are traditionally older models (newer models generally are chat models).

## Attributes

[attribute

logger](/python/langchain-core/language_models/llms/logger)

## Functions

[function

get\_llm\_cache

Get the value of the `llm_cache` global setting.](/python/langchain-core/globals/get_llm_cache)[function

dumpd

Return a dict representation of an object.](/python/langchain-core/load/dump/dumpd)[function

convert\_to\_messages

Convert a sequence of messages to a list of messages.](/python/langchain-core/messages/utils/convert_to_messages)[function

ensure\_config

Ensure that a config is a dict with all keys present.](/python/langchain-core/runnables/config/ensure_config)[function

get\_config\_list

Get a list of configs from a single config or a list of configs.

It is useful for subclasses overriding batch() or abatch().](/python/langchain-core/runnables/config/get_config_list)[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)[function

create\_base\_retry\_decorator

Create a retry decorator for a given LLM and provided a list of error types.](/python/langchain-core/language_models/llms/create_base_retry_decorator)[function

get\_prompts

Get prompts that are already cached.](/python/langchain-core/language_models/llms/get_prompts)[function

aget\_prompts

Get prompts that are already cached. Async version.](/python/langchain-core/language_models/llms/aget_prompts)[function

update\_cache

Update the cache and get the LLM output.](/python/langchain-core/language_models/llms/update_cache)[function

aupdate\_cache

Update the cache and get the LLM output. Async version.](/python/langchain-core/language_models/llms/aupdate_cache)

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

BaseCallbackManager

Base callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager)[class

CallbackManager

Callback manager for LangChain.](/python/langchain-core/callbacks/manager/CallbackManager)[class

CallbackManagerForLLMRun

Callback manager for LLM run.](/python/langchain-core/callbacks/manager/CallbackManagerForLLMRun)[class

BaseLanguageModel

Abstract base class for interfacing with language models.

All language model wrappers inherited from `BaseLanguageModel`.](/python/langchain-core/language_models/base/BaseLanguageModel)[class

LangSmithParams

LangSmith parameters for tracing.](/python/langchain-core/language_models/base/LangSmithParams)[class

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

BaseLLM

Base LLM abstract interface.

It should take in a prompt and return a string.](/python/langchain-core/language_models/llms/BaseLLM)[class

LLM

Simple interface for implementing a custom LLM.

You should subclass this class and implement the following:

- `_call` method: Run the LLM on the given prompt and input (used by `invoke`).
- `_identifying_params` property: Return a dictionary of the identifying parameters
  This is critical for caching and tracing purposes. Identifying parameters
  is a dict that identifies the LLM.
  It should mostly include a `model_name`.

Optional: Override the following methods to provide more optimizations:

- `_acall`: Provide a native async version of the `_call` method.
  If not provided, will delegate to the synchronous version using
  `run_in_executor`. (Used by `ainvoke`).
- `_stream`: Stream the LLM on the given prompt and input.
  `stream` will use `_stream` if provided, otherwise it
  use `_call` and output will arrive in one chunk.
- `_astream`: Override to provide a native async version of the `_stream` method.
  `astream` will use `_astream` if provided, otherwise it will implement
  a fallback behavior that will use `_stream` if `_stream` is implemented,
  and use `_acall` if `_stream` is not implemented.](/python/langchain-core/language_models/llms/LLM)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)[typeAlias

LanguageModelInput

Input to a language model.](/python/langchain-core/language_models/base/LanguageModelInput)


