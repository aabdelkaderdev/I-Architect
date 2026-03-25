<!-- Source: https://reference.langchain.com/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler -->

Classv1.2.13 (latest)●Since v1.0

# AsyncIteratorCallbackHandler


```
AsyncIteratorCallbackHandler(
    self,
)
```

## Bases

`AsyncCallbackHandler`

## Constructors

## Attributes

## Methods

## Inherited from[AsyncCallbackHandler](/python/langchain-core/callbacks/base/AsyncCallbackHandler)(langchain\_core)

### Methods

[Mon\_chat\_model\_start](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chat_model_start)[Mon\_chain\_start](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_start)[Mon\_chain\_end](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_end)[Mon\_chain\_error](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_error)[M](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_start)



on\_tool\_start

[Mon\_tool\_end](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_end)

[Mon\_tool\_error](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_error)

[Mon\_text](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_text)

[Mon\_retry](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retry)

[Mon\_agent\_action](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_action)

[Mon\_agent\_finish](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_finish)

[Mon\_retriever\_start](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_start)

[Mon\_retriever\_end](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_end)

[Mon\_retriever\_error](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_error)

[Mon\_custom\_event](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_custom_event)

## Inherited from[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)(langchain\_core)

### Attributes

[Araise\_error](/python/langchain-core/callbacks/base/BaseCallbackHandler/raise_error)[Arun\_inline](/python/langchain-core/callbacks/base/BaseCallbackHandler/run_inline)[Aignore\_llm](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_llm)[Aignore\_retry](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retry)[Aignore\_chain](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chain)[Aignore\_agent](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_agent)[Aignore\_retriever](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retriever)[Aignore\_chat\_model](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chat_model)[Aignore\_custom\_event](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_custom_event)

## Inherited from[ChainManagerMixin](/python/langchain-core/callbacks/base/ChainManagerMixin)(langchain\_core)

### Methods

[Mon\_chain\_end](/python/langchain-core/callbacks/base/ChainManagerMixin/on_chain_end)[Mon\_chain\_error](/python/langchain-core/callbacks/base/ChainManagerMixin/on_chain_error)[Mon\_agent\_action](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_action)[Mon\_agent\_finish](/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_finish)

## Inherited from[ToolManagerMixin](/python/langchain-core/callbacks/base/ToolManagerMixin)(langchain\_core)

### Methods

[Mon\_tool\_end](/python/langchain-core/callbacks/base/ToolManagerMixin/on_tool_end)[Mon\_tool\_error](/python/langchain-core/callbacks/base/ToolManagerMixin/on_tool_error)

## Inherited from[RetrieverManagerMixin](/python/langchain-core/callbacks/base/RetrieverManagerMixin)(langchain\_core)

### Methods

[Mon\_retriever\_error](/python/langchain-core/callbacks/base/RetrieverManagerMixin/on_retriever_error)[Mon\_retriever\_end](/python/langchain-core/callbacks/base/RetrieverManagerMixin/on_retriever_end)

## Inherited from[CallbackManagerMixin](/python/langchain-core/callbacks/base/CallbackManagerMixin)(langchain\_core)

### Methods

[Mon\_chat\_model\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chat_model_start)[Mon\_retriever\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start)[Mon\_chain\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chain_start)[Mon\_tool\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start)

## Inherited from[RunManagerMixin](/python/langchain-core/callbacks/base/RunManagerMixin)(langchain\_core)

### Methods

[Mon\_text](/python/langchain-core/callbacks/base/RunManagerMixin/on_text)[Mon\_retry](/python/langchain-core/callbacks/base/RunManagerMixin/on_retry)[Mon\_custom\_event](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)

[constructor

\_\_init\_\_](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/__init__)

[attribute

queue: asyncio.Queue[str]](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/queue)

[attribute

done: asyncio.Event](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/done)

[attribute

always\_verbose: bool

Always verbose.](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/always_verbose)

[method

on\_llm\_start](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/on_llm_start)

[method

on\_llm\_new\_token](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/on_llm_new_token)

[method

on\_llm\_end](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/on_llm_end)

[method

on\_llm\_error](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/on_llm_error)

[method

aiter

Asynchronous iterator that yields tokens.](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/aiter)

Callback handler that returns an async iterator.