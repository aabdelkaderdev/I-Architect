<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager -->

Modulev1.2.21 (latest)●Since v0.1

# manager

Run managers.

## Attributes

[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)[attribute

logger](/python/langchain-core/callbacks/manager/logger)[attribute

Func](/python/langchain-core/callbacks/manager/Func)[attribute

T](/python/langchain-core/callbacks/manager/T)

## Functions

[function

get\_debug

Get the value of the `debug` global setting.](/python/langchain-core/globals/get_debug)[function

get\_buffer\_string

Convert a sequence of messages to strings and concatenate them into one string.](/python/langchain-core/messages/utils/get_buffer_string)[function

env\_var\_is\_set

Check if an environment variable is set.](/python/langchain-core/utils/env/env_var_is_set)[function

uuid7

Generate a UUID from a Unix timestamp in nanoseconds and random bits.

UUIDv7 objects feature monotonicity within a millisecond.](/python/langchain-core/utils/uuid/uuid7)[function

trace\_as\_chain\_group

Get a callback manager for a chain group in a context manager.

Useful for grouping different calls together as a single run even if they aren't
composed in a single chain.](/python/langchain-core/callbacks/manager/trace_as_chain_group)[function

atrace\_as\_chain\_group

Get an async callback manager for a chain group in a context manager.

Useful for grouping different async calls together as a single run even if they
aren't composed in a single chain.](/python/langchain-core/callbacks/manager/atrace_as_chain_group)[function

shielded

Makes so an awaitable method is always shielded from cancellation.](/python/langchain-core/callbacks/manager/shielded)[function

handle\_event

Generic event handler for `CallbackManager`.](/python/langchain-core/callbacks/manager/handle_event)[function

ahandle\_event

Async generic event handler for `AsyncCallbackManager`.](/python/langchain-core/callbacks/manager/ahandle_event)[function

adispatch\_custom\_event

Dispatch an adhoc event to the handlers.](/python/langchain-core/callbacks/manager/adispatch_custom_event)[function

dispatch\_custom\_event

Dispatch an adhoc event.](/python/langchain-core/callbacks/manager/dispatch_custom_event)

## Classes

[class

BaseCallbackHandler

Base callback handler.](/python/langchain-core/callbacks/base/BaseCallbackHandler)[class

BaseCallbackManager

Base callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager)[class

ChainManagerMixin

Mixin for chain callbacks.](/python/langchain-core/callbacks/base/ChainManagerMixin)[class

LLMManagerMixin

Mixin for LLM callbacks.](/python/langchain-core/callbacks/base/LLMManagerMixin)[class

RetrieverManagerMixin

Mixin for `Retriever` callbacks.](/python/langchain-core/callbacks/base/RetrieverManagerMixin)[class

RunManagerMixin

Mixin for run manager.](/python/langchain-core/callbacks/base/RunManagerMixin)[class

ToolManagerMixin

Mixin for tool callbacks.](/python/langchain-core/callbacks/base/ToolManagerMixin)[class

StdOutCallbackHandler

Callback handler that prints to std out.](/python/langchain-core/callbacks/stdout/StdOutCallbackHandler)[class

BaseMessage

Base abstract message class.

Messages are the inputs and outputs of a chat model.

Examples include [`HumanMessage`](/python/langchain-core/messages/human/HumanMessage),
[`AIMessage`](/python/langchain-core/messages/ai/AIMessage), and
[`SystemMessage`](/python/langchain-core/messages/system/SystemMessage).](/python/langchain-core/messages/base/BaseMessage)[class

AgentAction

Represents a request to execute an action by an agent.

The action consists of the name of the tool to execute and the input to pass
to the tool. The log is used to pass along extra information about the action.](/python/langchain-core/agents/AgentAction)[class

AgentFinish

Final return value of an `ActionAgent`.

Agents return an `AgentFinish` when they have reached a stopping condition.](/python/langchain-core/agents/AgentFinish)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

ChatGenerationChunk

`ChatGeneration` chunk.

`ChatGeneration` chunks can be concatenated with other `ChatGeneration` chunks.](/python/langchain-core/outputs/chat_generation/ChatGenerationChunk)[class

GenerationChunk

`GenerationChunk`, which can be concatenated with other `Generation` chunks.](/python/langchain-core/outputs/generation/GenerationChunk)[class

LLMResult

A container for results of an LLM call.

Both chat models and LLMs generate an `LLMResult` object. This object contains the
generated outputs and any additional information that the model provider wants to
return.](/python/langchain-core/outputs/llm_result/LLMResult)[class

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

BaseRunManager

Base class for run manager (a bound callback manager).](/python/langchain-core/callbacks/manager/BaseRunManager)[class

RunManager

Synchronous run manager.](/python/langchain-core/callbacks/manager/RunManager)[class

ParentRunManager

Synchronous parent run manager.](/python/langchain-core/callbacks/manager/ParentRunManager)[class

AsyncRunManager

Async run manager.](/python/langchain-core/callbacks/manager/AsyncRunManager)[class

AsyncParentRunManager

Async parent run manager.](/python/langchain-core/callbacks/manager/AsyncParentRunManager)[class

CallbackManagerForLLMRun

Callback manager for LLM run.](/python/langchain-core/callbacks/manager/CallbackManagerForLLMRun)[class

AsyncCallbackManagerForLLMRun

Async callback manager for LLM run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForLLMRun)[class

CallbackManagerForChainRun

Callback manager for chain run.](/python/langchain-core/callbacks/manager/CallbackManagerForChainRun)[class

AsyncCallbackManagerForChainRun

Async callback manager for chain run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainRun)[class

CallbackManagerForToolRun

Callback manager for tool run.](/python/langchain-core/callbacks/manager/CallbackManagerForToolRun)[class

AsyncCallbackManagerForToolRun

Async callback manager for tool run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForToolRun)[class

CallbackManagerForRetrieverRun

Callback manager for retriever run.](/python/langchain-core/callbacks/manager/CallbackManagerForRetrieverRun)[class

AsyncCallbackManagerForRetrieverRun

Async callback manager for retriever run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForRetrieverRun)[class

CallbackManager

Callback manager for LangChain.](/python/langchain-core/callbacks/manager/CallbackManager)[class

CallbackManagerForChainGroup

Callback manager for the chain group.](/python/langchain-core/callbacks/manager/CallbackManagerForChainGroup)[class

AsyncCallbackManager

Async callback manager that handles callbacks from LangChain.](/python/langchain-core/callbacks/manager/AsyncCallbackManager)[class

AsyncCallbackManagerForChainGroup

Async callback manager for the chain group.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)


