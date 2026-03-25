<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/fake_chat_models -->

Modulev1.2.21 (latest)●Since v0.1

# fake\_chat\_models

Fake chat models for testing purposes.

## Classes

[class

AsyncCallbackManagerForLLMRun

Async callback manager for LLM run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForLLMRun)[class

CallbackManagerForLLMRun

Callback manager for LLM run.](/python/langchain-core/callbacks/manager/CallbackManagerForLLMRun)[class

BaseChatModel

Base class for chat models.](/python/langchain-core/language_models/chat_models/BaseChatModel)[class

SimpleChatModel

Simplified implementation for a chat model to inherit from.

Note

This implementation is primarily here for backwards compatibility. For new
implementations, please use `BaseChatModel` directly.](/python/langchain-core/language_models/chat_models/SimpleChatModel)[class

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

FakeMessagesListChatModel

Fake chat model for testing purposes.](/python/langchain-core/language_models/fake_chat_models/FakeMessagesListChatModel)[class

FakeListChatModelError

Fake error for testing purposes.](/python/langchain-core/language_models/fake_chat_models/FakeListChatModelError)[class

FakeListChatModel

Fake chat model for testing purposes.](/python/langchain-core/language_models/fake_chat_models/FakeListChatModel)[class

FakeChatModel

Fake Chat Model wrapper for testing purposes.](/python/langchain-core/language_models/fake_chat_models/FakeChatModel)[class

GenericFakeChatModel

Generic fake chat model that can be used to test the chat model interface.

- Chat model should be usable in both sync and async tests
- Invokes `on_llm_new_token` to allow for testing of callback related code for new
  tokens.
- Includes logic to break messages into message chunk to facilitate testing of
  streaming.](/python/langchain-core/language_models/fake_chat_models/GenericFakeChatModel)[class

ParrotFakeChatModel

Generic fake chat model that can be used to test the chat model interface.

- Chat model should be usable in both sync and async tests](/python/langchain-core/language_models/fake_chat_models/ParrotFakeChatModel)


