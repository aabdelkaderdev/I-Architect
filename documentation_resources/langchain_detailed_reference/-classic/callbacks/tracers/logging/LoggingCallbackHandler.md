<!-- Source: https://reference.langchain.com/python/langchain-classic/callbacks/tracers/logging/LoggingCallbackHandler -->

Classv1.2.13 (latest)●Since v1.0

# LoggingCallbackHandler


```
LoggingCallbackHandler(
  self,
  logger: logging.Logger,
  log_level: int = logging.INFO,
  extra: dict
```

## Bases

`FunctionCallbackHandler`

## Constructors

## Attributes

## Methods

## Inherited from[FunctionCallbackHandler](/python/langchain-core/tracers/stdout/FunctionCallbackHandler)(langchain\_core)

### Attributes

[Afunction\_callback](/python/langchain-core/tracers/stdout/FunctionCallbackHandler/function_callback)

### Methods

[Mget\_parents](/python/langchain-core/tracers/stdout/FunctionCallbackHandler/get_parents)[Mget\_breadcrumbs](/python/langchain-core/tracers/stdout/FunctionCallbackHandler/get_breadcrumbs)

## Inherited from[BaseTracer](/python/langchain-core/tracers/base/BaseTracer)(langchain\_core)



|

None

=

None

,

\*\*

kwargs

:

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

=

{

}

)

### Methods

[Mon\_chat\_model\_start](/python/langchain-core/tracers/base/BaseTracer/on_chat_model_start)[Mon\_llm\_start](/python/langchain-core/tracers/base/BaseTracer/on_llm_start)[Mon\_llm\_new\_token](/python/langchain-core/tracers/base/BaseTracer/on_llm_new_token)[Mon\_retry](/python/langchain-core/tracers/base/BaseTracer/on_retry)[Mon\_llm\_end](/python/langchain-core/tracers/base/BaseTracer/on_llm_end)[Mon\_llm\_error](/python/langchain-core/tracers/base/BaseTracer/on_llm_error)[Mon\_chain\_start](/python/langchain-core/tracers/base/BaseTracer/on_chain_start)[Mon\_chain\_end](/python/langchain-core/tracers/base/BaseTracer/on_chain_end)[Mon\_chain\_error](/python/langchain-core/tracers/base/BaseTracer/on_chain_error)[Mon\_tool\_start](/python/langchain-core/tracers/base/BaseTracer/on_tool_start)[Mon\_tool\_end](/python/langchain-core/tracers/base/BaseTracer/on_tool_end)[Mon\_tool\_error](/python/langchain-core/tracers/base/BaseTracer/on_tool_error)[Mon\_retriever\_start](/python/langchain-core/tracers/base/BaseTracer/on_retriever_start)[Mon\_retriever\_error](/python/langchain-core/tracers/base/BaseTracer/on_retriever_error)[Mon\_retriever\_end](/python/langchain-core/tracers/base/BaseTracer/on_retriever_end)

## Inherited from[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)(langchain\_core)

### Attributes

[Araise\_error](/python/langchain-core/callbacks/base/BaseCallbackHandler/raise_error)[Arun\_inline](/python/langchain-core/callbacks/base/BaseCallbackHandler/run_inline)[Aignore\_llm](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_llm)[Aignore\_retry](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retry)[Aignore\_chain](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chain)[Aignore\_agent](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_agent)[Aignore\_retriever](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_retriever)[Aignore\_chat\_model](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_chat_model)[Aignore\_custom\_event](/python/langchain-core/callbacks/base/BaseCallbackHandler/ignore_custom_event)

## Inherited from[LLMManagerMixin](/python/langchain-core/callbacks/base/LLMManagerMixin)(langchain\_core)

### Methods

[Mon\_llm\_new\_token](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_new_token)[Mon\_llm\_end](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_end)[Mon\_llm\_error](/python/langchain-core/callbacks/base/LLMManagerMixin/on_llm_error)

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

[Mon\_llm\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_llm_start)[Mon\_chat\_model\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chat_model_start)[Mon\_retriever\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start)[Mon\_chain\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chain_start)[Mon\_tool\_start](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start)

## Inherited from[RunManagerMixin](/python/langchain-core/callbacks/base/RunManagerMixin)(langchain\_core)

### Methods

[Mon\_retry](/python/langchain-core/callbacks/base/RunManagerMixin/on_retry)[Mon\_custom\_event](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `logger`\* | `logging.Logger` | the logger to use for logging |
| `log_level` | `int` | Default:`logging.INFO`  the logging level (default: logging.INFO) |
| `extra` | `dict | None` | Default:`None`  the extra context to log (default: None) |
| `**kwargs` | `Any` | Default:`{}` |

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| logger | logging.Logger |
| log\_level | [int](https://docs.python.org/3/library/functions.html#int) |
| extra | [dict](https://docs.python.org/3/library/stdtypes.html#dict) | None |

[attribute

name: str](/python/langchain-classic/callbacks/tracers/logging/LoggingCallbackHandler/name)

[method

on\_text](/python/langchain-classic/callbacks/tracers/logging/LoggingCallbackHandler/on_text)

Tracer that logs via the input Logger.

additional keyword arguments.