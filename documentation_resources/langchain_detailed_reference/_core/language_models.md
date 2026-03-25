<!-- Source: https://reference.langchain.com/python/langchain_core/language_models -->

Modulev1.2.21 (latest)●Since v0.1

# language\_models

## Attributes

## Functions

## Classes

## Type Aliases

## Modules



[attribute

LanguageModelLike: Runnable[LanguageModelInput, LanguageModelOutput]

Input/output interface for a language model.](/python/langchain-core/language_models/base/LanguageModelLike)

[attribute

ModelProfileRegistry: dict[str, ModelProfile]

Registry mapping model identifiers or names to their ModelProfile.](/python/langchain-core/language_models/model_profile/ModelProfileRegistry)

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)

[function

is\_openai\_data\_block

Check whether a block contains multimodal data in OpenAI Chat Completions format.

Supports both data and ID-style blocks (e.g. `'file_data'` and `'file_id'`)

If additional keys are present, they are ignored / will not affect outcome as long
as the required keys are present and valid.](/python/langchain-core/language_models/_utils/is_openai_data_block)

[function

get\_tokenizer

Get a GPT-2 tokenizer instance.

This function is cached to avoid re-loading the tokenizer every time it is called.](/python/langchain-core/language_models/base/get_tokenizer)

[class

BaseLanguageModel

Abstract base class for interfacing with language models.

All language model wrappers inherited from `BaseLanguageModel`.](/python/langchain-core/language_models/base/BaseLanguageModel)

[class

LangSmithParams

LangSmith parameters for tracing.](/python/langchain-core/language_models/base/LangSmithParams)

[class

BaseChatModel

Base class for chat models.](/python/langchain-core/language_models/chat_models/BaseChatModel)

[class

SimpleChatModel

Simplified implementation for a chat model to inherit from.

Note

This implementation is primarily here for backwards compatibility. For new
implementations, please use `BaseChatModel` directly.](/python/langchain-core/language_models/chat_models/SimpleChatModel)

[class

FakeListLLM

Fake LLM for testing purposes.](/python/langchain-core/language_models/fake/FakeListLLM)

[class

FakeStreamingListLLM

Fake streaming list LLM for testing purposes.

An LLM that will return responses from a list in order.

This model also supports optionally sleeping between successive
chunks in a streaming implementation.](/python/langchain-core/language_models/fake/FakeStreamingListLLM)

[class

FakeListChatModel

Fake chat model for testing purposes.](/python/langchain-core/language_models/fake_chat_models/FakeListChatModel)

[class

FakeMessagesListChatModel

Fake chat model for testing purposes.](/python/langchain-core/language_models/fake_chat_models/FakeMessagesListChatModel)

[class

GenericFakeChatModel

Generic fake chat model that can be used to test the chat model interface.

- Chat model should be usable in both sync and async tests
- Invokes `on_llm_new_token` to allow for testing of callback related code for new
  tokens.
- Includes logic to break messages into message chunk to facilitate testing of
  streaming.](/python/langchain-core/language_models/fake_chat_models/GenericFakeChatModel)

[class

ParrotFakeChatModel

Generic fake chat model that can be used to test the chat model interface.

- Chat model should be usable in both sync and async tests](/python/langchain-core/language_models/fake_chat_models/ParrotFakeChatModel)

[class

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

[class

BaseLLM

Base LLM abstract interface.

It should take in a prompt and return a string.](/python/langchain-core/language_models/llms/BaseLLM)

[class

ModelProfile

Model profile.

Beta feature

This is a beta feature. The format of model profiles is subject to change.

Provides information about chat model capabilities, such as context window sizes
and supported features.](/python/langchain-core/language_models/model_profile/ModelProfile)

[typeAlias

LanguageModelInput

Input to a language model.](/python/langchain-core/language_models/base/LanguageModelInput)

[typeAlias

LanguageModelOutput

Output from a language model.](/python/langchain-core/language_models/base/LanguageModelOutput)

[module

chat\_models

Chat models for conversational AI.](/python/langchain-core/language_models/chat_models)

[module

fake\_chat\_models

Fake chat models for testing purposes.](/python/langchain-core/language_models/fake_chat_models)

[module

llms

Base interface for traditional large language models (LLMs) to expose.

These are traditionally older models (newer models generally are chat models).](/python/langchain-core/language_models/llms)

[module

base

Base language models class.](/python/langchain-core/language_models/base)

[module

fake

Fake LLMs for testing purposes.](/python/langchain-core/language_models/fake)

[module

model\_profile

Model profile types and utilities.](/python/langchain-core/language_models/model_profile)

Core language model abstractions.

LangChain has two main classes to work with language models: chat models and
"old-fashioned" LLMs (string-in, string-out).

**Chat models**

Language models that use a sequence of messages as inputs and return chat messages
as outputs (as opposed to using plain text).

Chat models support the assignment of distinct roles to conversation messages, helping
to distinguish messages from the AI, users, and instructions such as system messages.

The key abstraction for chat models is
[`BaseChatModel`](/python/langchain-core/language_models/chat_models/BaseChatModel). Implementations should
inherit from this class.

See existing [chat model integrations](https://docs.langchain.com/oss/python/integrations/chat).

**LLMs (legacy)**

Language models that takes a string as input and returns a string.

These are traditionally older models (newer models generally are chat models).

Although the underlying models are string in, string out, the LangChain wrappers also
allow these models to take messages as input. This gives them the same interface as
chat models. When messages are passed in as input, they will be formatted into a string
under the hood before being passed to the underlying model.