<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer -->

Classv1.2.21 (latest)●Since v0.2

# AsyncBaseTracer

Async base interface for tracers.


```
AsyncBaseTracer(
  self,
  *,
  _schema_format: Literal['original', 'streaming_events', 'original+chat'] = 'original',
  **kwargs: Any = {}
)
```

## Bases

`_TracerCore``AsyncCallbackHandler``ABC`

## Methods

[method

on\_chat\_model\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chat_model_start)[method

on\_llm\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_start)[method

on\_llm\_new\_token](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_new_token)[method

on\_retry](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retry)[method

on\_llm\_end

End a trace for an LLM or chat model run.](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_end)[method

on\_llm\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_error)[method

on\_chain\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chain_start)[method

on\_chain\_end](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chain_end)[method

on\_chain\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_chain_error)[method

on\_tool\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_start)[method

on\_tool\_end](/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_end)[method

on\_tool\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_tool_error)[method

on\_retriever\_start](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retriever_start)[method

on\_retriever\_error](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retriever_error)[method

on\_retriever\_end](/python/langchain-core/tracers/base/AsyncBaseTracer/on_retriever_end)

## Inherited from[AsyncCallbackHandler](/python/langchain-core/callbacks/base/AsyncCallbackHandler)

### Methods

[Mon\_text

—

Run on an arbitrary text.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_text)[Mon\_agent\_action

—

Run on agent action.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_action)[Mon\_agent\_finish

—

Run on the agent end.](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_finish)[Mon\_custom\_event

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

## Inherited from[ChainManagerMixin](/python/langchain-core/callbacks/base/ChainManagerMixin)

### Methods

[Mon\_agent\_action

—

Run on agent action.](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_action)[Mon\_agent\_finish

—

Run on the agent end.](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_finish)

## Inherited from[RunManagerMixin](/python/langchain-core/callbacks/base/RunManagerMixin)

### Methods

[Mon\_text

—

Run on an arbitrary text.](/python/langchain-core/callbacks/base/RunManagerMixin/on_text)[Mon\_custom\_event

—

Override to define a handler for a custom event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)


