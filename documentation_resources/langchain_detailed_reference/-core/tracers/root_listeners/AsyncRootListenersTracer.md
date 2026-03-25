<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/root_listeners/AsyncRootListenersTracer -->

Classv1.2.21 (latest)●Since v0.2

# AsyncRootListenersTracer

Async tracer that calls listeners on run start, end, and error.


```
AsyncRootListenersTracer(
  self,
  *,
  config: RunnableConfig,
  on_start: AsyncListener | None,
  on_end: AsyncListener | None,
  on_error: AsyncListener | None
)
```

## Bases

`AsyncBaseTracer`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config`\* | `RunnableConfig` | The runnable config. |
| `on_start`\* | `AsyncListener | None` | The listener to call on run start. |
| `on_end`\* | `AsyncListener | None` | The listener to call on run end. |
| `on_error`\* | `AsyncListener | None` | The listener to call on run error |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| config | [RunnableConfig](/python/langchain-core/runnables/config/RunnableConfig) |
| on\_start | [AsyncListener](/python/langchain-core/tracers/root_listeners/AsyncListener) | None |
| on\_end | [AsyncListener](/python/langchain-core/tracers/root_listeners/AsyncListener) | None |
| on\_error | [AsyncListener](/python/langchain-core/tracers/root_listeners/AsyncListener) | None |

## Attributes

[attribute

log\_missing\_parent: bool

Whether to log a warning if the parent is missing.](/python/langchain-core/tracers/root_listeners/AsyncRootListenersTracer/log_missing_parent)[attribute

config: config](/python/langchain-core/tracers/root_listeners/AsyncRootListenersTracer/config)[attribute

root\_id: UUID | None](/python/langchain-core/tracers/root_listeners/AsyncRootListenersTracer/root_id)

## Inherited from[AsyncBaseTracer](/python/langchain-core/tracers/base/AsyncBaseTracer)

### Methods

[Mon\_chat\_model\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chat_model_start)[Mon\_llm\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_start)[Mon\_llm\_new\_token](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_new_token)[Mon\_retry](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retry)[Mon\_llm\_end

—

End a trace for an LLM or chat model run.](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_end)[Mon\_llm\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_error)[Mon\_chain\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chain_start)[Mon\_chain\_end](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chain_end)[Mon\_chain\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chain_error)[Mon\_tool\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_start)[Mon\_tool\_end](/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_end)[Mon\_tool\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_error)[Mon\_retriever\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retriever_start)[Mon\_retriever\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retriever_error)[Mon\_retriever\_end](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retriever_end)

## Inherited from[AsyncCallbackHandler](/python/langchain-core/callbacks/base/AsyncCallbackHandler)

### Methods

[Mon\_llm\_start

—

Run when the model starts running.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_llm_start)[Mon\_chat\_model\_start

—

Run when a chat model starts running.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chat_model_start)[Mon\_llm\_new\_token

—

Run on new output token. Only available when streaming is enabled.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_llm_new_token)[Mon\_llm\_end

—

Run when the model ends running.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_llm_end)[Mon\_llm\_error

—

Run when LLM errors.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_llm_error)[Mon\_chain\_start

—

Run when a chain starts running.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_start)[Mon\_chain\_end

—

Run when a chain ends running.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_end)[Mon\_chain\_error

—

Run when chain errors.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_error)[Mon\_tool\_start

—

Run when the tool starts running.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_start)[Mon\_tool\_end

—

Run when the tool ends running.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_end)[Mon\_tool\_error

—

Run when tool errors.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_error)[Mon\_text

—

Run on an arbitrary text.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_text)[Mon\_retry

—

Run on a retry event.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retry)[Mon\_agent\_action

—

Run on agent action.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_action)[Mon\_agent\_finish

—

Run on the agent end.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_finish)[Mon\_retriever\_start

—

Run on the retriever start.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_start)[Mon\_retriever\_end

—

Run on the retriever end.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_end)[Mon\_retriever\_error

—

Run on retriever error.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_error)[Mon\_custom\_event

—

Override to define a handler for custom events.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_custom_event)

## Inherited from[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)

### Attributes

[Araise\_error: bool

—

Whether to raise an error if an exception occurs.](/python/langchain-core/callbacks/base/BaseCallbackHandler/raise_error)[Arun\_inline: bool

—

Whether to run the callback inline.](/python/langchain-core/callbacks/base/BaseCallbackHandler/run_inline)[Aignore\_llm: bool

—

Whether to ignore LLM callbacks.](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_llm)[Aignore\_retry: bool

—

Whether to ignore retry callbacks.](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retry)[Aignore\_chain: bool

—

Whether to ignore chain callbacks.](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chain)[Aignore\_agent: bool

—

Whether to ignore agent callbacks.](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_agent)[Aignore\_retriever: bool

—

Whether to ignore retriever callbacks.](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retriever)[Aignore\_chat\_model: bool

—

Whether to ignore chat model callbacks.](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chat_model)[Aignore\_custom\_event: bool

—

Ignore custom event.](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_custom_event)

## Inherited from[LLMManagerMixin](/python/langchain-core/callbacks/base/LLMManagerMixin)

### Methods

[Mon\_llm\_new\_token

—

Run on new output token.](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_new_token)[Mon\_llm\_end

—

Run when LLM ends running.](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_end)[Mon\_llm\_error

—

Run when LLM errors.](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_error)

## Inherited from[ChainManagerMixin](/python/langchain-core/callbacks/base/ChainManagerMixin)

### Methods

[Mon\_chain\_end

—

Run when chain ends running.](/python/langchain-core/callbacks/base/ChainManagerMixin/on_chain_end)[Mon\_chain\_error

—

Run when chain errors.](/python/langchain-core/callbacks/base/ChainManagerMixin/on_chain_error)[Mon\_agent\_action

—

Run on agent action.](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_action)[Mon\_agent\_finish

—

Run on the agent end.](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_finish)

## Inherited from[ToolManagerMixin](/python/langchain-core/callbacks/base/ToolManagerMixin)

### Methods

[Mon\_tool\_end

—

Run when the tool ends running.](/python/langchain-core/callbacks/base/ToolManagerMixin/on_tool_end)[Mon\_tool\_error

—

Run when tool errors.](/python/langchain-core/callbacks/base/ToolManagerMixin/on_tool_error)

## Inherited from[RetrieverManagerMixin](/python/langchain-core/callbacks/base/RetrieverManagerMixin)

### Methods

[Mon\_retriever\_error

—

Run when `Retriever` errors.](/python/langchain-core/callbacks/base/RetrieverManagerMixin/on_retriever_error)[Mon\_retriever\_end

—

Run when `Retriever` ends running.](/python/langchain-core/callbacks/base/RetrieverManagerMixin/on_retriever_end)

## Inherited from[CallbackManagerMixin](/python/langchain-core/callbacks/base/CallbackManagerMixin)

### Methods

[Mon\_llm\_start

—

Run when LLM starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_llm_start)[Mon\_chat\_model\_start

—

Run when a chat model starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chat_model_start)[Mon\_retriever\_start

—

Run when the `Retriever` starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start)[Mon\_chain\_start

—

Run when a chain starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chain_start)[Mon\_tool\_start

—

Run when the tool starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start)

## Inherited from[RunManagerMixin](/python/langchain-core/callbacks/base/RunManagerMixin)

### Methods

[Mon\_text

—

Run on an arbitrary text.](/python/langchain-core/callbacks/base/RunManagerMixin/on_text)[Mon\_retry

—

Run on a retry event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_retry)[Mon\_custom\_event

—

Override to define a handler for a custom event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)


