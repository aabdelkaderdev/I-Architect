<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer -->

Classv1.2.21 (latest)●Since v0.1

# BaseTracer

Base interface for tracers.


```
BaseTracer(
  self,
  *,
  _schema_format: Literal['original', 'streaming_events', 'original+chat'] = 'original',
  **kwargs: Any = {}
)
```

## Bases

`_TracerCore``BaseCallbackHandler``ABC`

## Methods

[method

on\_chat\_model\_start

Start a trace for a chat model run.](/python/langchain-core/tracers/base/BaseTracer/on_chat_model_start)[method

on\_llm\_start

Start a trace for an LLM run.](/python/langchain-core/tracers/base/BaseTracer/on_llm_start)[method

on\_llm\_new\_token

Run on new LLM token.

Only available when streaming is enabled.](/python/langchain-core/tracers/base/BaseTracer/on_llm_new_token)[method

on\_retry

Run on retry.](/python/langchain-core/tracers/base/BaseTracer/on_retry)[method

on\_llm\_end

End a trace for an LLM or chat model run.](/python/langchain-core/tracers/base/BaseTracer/on_llm_end)[method

on\_llm\_error

Handle an error for an LLM run.](/python/langchain-core/tracers/base/BaseTracer/on_llm_error)[method

on\_chain\_start

Start a trace for a chain run.](/python/langchain-core/tracers/base/BaseTracer/on_chain_start)[method

on\_chain\_end

End a trace for a chain run.](/python/langchain-core/tracers/base/BaseTracer/on_chain_end)[method

on\_chain\_error

Handle an error for a chain run.](/python/langchain-core/tracers/base/BaseTracer/on_chain_error)[method

on\_tool\_start

Start a trace for a tool run.](/python/langchain-core/tracers/base/BaseTracer/on_tool_start)[method

on\_tool\_end

End a trace for a tool run.](/python/langchain-core/tracers/base/BaseTracer/on_tool_end)[method

on\_tool\_error

Handle an error for a tool run.](/python/langchain-core/tracers/base/BaseTracer/on_tool_error)[method

on\_retriever\_start

Run when the `Retriever` starts running.](/python/langchain-core/tracers/base/BaseTracer/on_retriever_start)[method

on\_retriever\_error

Run when `Retriever` errors.](/python/langchain-core/tracers/base/BaseTracer/on_retriever_error)[method

on\_retriever\_end

Run when the `Retriever` ends running.](/python/langchain-core/tracers/base/BaseTracer/on_retriever_end)

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


