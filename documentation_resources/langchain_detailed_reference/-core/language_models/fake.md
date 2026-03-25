<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/fake -->

Modulev1.2.21 (latest)●Since v0.1

# fake

Fake LLMs for testing purposes.

## Classes

[class

AsyncCallbackManagerForLLMRun

Async callback manager for LLM run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForLLMRun)[class

CallbackManagerForLLMRun

Callback manager for LLM run.](/python/langchain-core/callbacks/manager/CallbackManagerForLLMRun)[class

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
  and use `_acall` if `_stream` is not implemented.](/python/langchain-core/language_models/llms/LLM)[class

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

FakeListLLM

Fake LLM for testing purposes.](/python/langchain-core/language_models/fake/FakeListLLM)[class

FakeListLLMError

Fake error for testing purposes.](/python/langchain-core/language_models/fake/FakeListLLMError)[class

FakeStreamingListLLM

Fake streaming list LLM for testing purposes.

An LLM that will return responses from a list in order.

This model also supports optionally sleeping between successive
chunks in a streaming implementation.](/python/langchain-core/language_models/fake/FakeStreamingListLLM)

## Type Aliases

[typeAlias

LanguageModelInput

Input to a language model.](/python/langchain-core/language_models/base/LanguageModelInput)


