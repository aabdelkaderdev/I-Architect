<!-- Source: https://reference.langchain.com/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler -->

Classv1.2.13 (latest)●Since v1.0

# AsyncFinalIteratorCallbackHandler


```
AsyncFinalIteratorCallbackHandler(
  self,
  *,
  answer_prefix_tokens: list[str] | None = None,
  strip_tokens:
```

## Bases

`AsyncIteratorCallbackHandler`

## Constructors

## Attributes

## Methods

## Inherited from[AsyncIteratorCallbackHandler](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler)

### Attributes

[Aqueue: asyncio.Queue[str]](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/queue)[Adone: asyncio.Event](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/done)[Aalways\_verbose: bool

—

Always verbose.](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/always_verbose)

### Methods



[bool](https://docs.python.org/3/library/functions.html#bool)

=

True

,

stream\_prefix

:

[bool](https://docs.python.org/3/library/functions.html#bool)

=

False

)

M

on\_llm\_error

[Maiter

—

Asynchronous iterator that yields tokens.](/python/langchain-classic/callbacks/streaming_aiter/AsyncIteratorCallbackHandler/aiter)

## Inherited from[AsyncCallbackHandler](/python/langchain-core/callbacks/base/AsyncCallbackHandler)(langchain\_core)

### Methods

[Mon\_chat\_model\_start](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chat_model_start)[Mon\_llm\_error](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_llm_error)[Mon\_chain\_start](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_start)[Mon\_chain\_end](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_end)[Mon\_chain\_error](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_chain_error)[Mon\_tool\_start](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_start)[Mon\_tool\_end](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_end)[Mon\_tool\_error](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_tool_error)[Mon\_text](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_text)[Mon\_retry](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retry)[Mon\_agent\_action](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_action)[Mon\_agent\_finish](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_finish)[Mon\_retriever\_start](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_start)[Mon\_retriever\_end](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_end)[Mon\_retriever\_error](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_retriever_error)[Mon\_custom\_event](/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_custom_event)

## Inherited from[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)(langchain\_core)

### Attributes

[Araise\_error](/python/langchain-core/callbacks/base/BaseCallbackHandler/raise_error)[Arun\_inline](/python/langchain-core/callbacks/base/BaseCallbackHandler/run_inline)[Aignore\_llm](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_llm)[Aignore\_retry](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retry)[Aignore\_chain](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chain)[Aignore\_agent](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_agent)[Aignore\_retriever](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retriever)[Aignore\_chat\_model](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chat_model)[Aignore\_custom\_event](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_custom_event)

## Inherited from[LLMManagerMixin](/python/langchain-core/callbacks/base/LLMManagerMixin)(langchain\_core)

### Methods

[Mon\_llm\_error](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_error)

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

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `answer_prefix_tokens` | `list[str] | None` | Default:`None`  Token sequence that prefixes the answer. Default is ["Final", "Answer", ":"] |
| `strip_tokens` | `bool` | Default:`True`  Ignore white spaces and new lines when comparing answer\_prefix\_tokens to last tokens? (to determine if answer has been reached) |
| `stream_prefix` | `bool` | Default:`False` |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| answer\_prefix\_tokens | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| strip\_tokens | [bool](https://docs.python.org/3/library/functions.html#bool) |
| stream\_prefix | [bool](https://docs.python.org/3/library/functions.html#bool) |

[attribute

answer\_prefix\_tokens: DEFAULT\_ANSWER\_PREFIX\_TOKENS](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/answer_prefix_tokens)

[attribute

answer\_prefix\_tokens\_stripped: list](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/answer_prefix_tokens_stripped)

[attribute

last\_tokens: list](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/last_tokens)

[attribute

last\_tokens\_stripped: list](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/last_tokens_stripped)

[attribute

strip\_tokens: strip\_tokens](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/strip_tokens)

[attribute

stream\_prefix: stream\_prefix](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/stream_prefix)

[attribute

answer\_reached: bool](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/answer_reached)

[method

append\_to\_last\_tokens

Append token to the last tokens.](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/append_to_last_tokens)

[method

check\_if\_answer\_reached

Check if the answer has been reached.](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/check_if_answer_reached)

[method

on\_llm\_start](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/on_llm_start)

[method

on\_llm\_end](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/on_llm_end)

[method

on\_llm\_new\_token](/python/langchain-classic/callbacks/streaming_aiter_final_only/AsyncFinalIteratorCallbackHandler/on_llm_new_token)

Callback handler that returns an async iterator.

Only the final output of the agent will be iterated.

Should answer prefix itself also be streamed?