<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler -->

Classv1.2.21 (latest)●Since v0.1

# LogStreamCallbackHandler

Tracer that streams run logs to a stream.


```
LogStreamCallbackHandler(
  self,
  *,
  auto_close: bool = True,
  include_names: Sequence[str] | None = None,
  include_types: Sequence[str] | None = None,
  include_tags: Sequence[str] | None = None,
  exclude_names: Sequence[str] | None = None,
  exclude_types: Sequence[str] | None = None,
  exclude_tags: Sequence[str] | None = None,
  _schema_format: Literal['original', 'streaming_events'] = 'streaming_events'
)
```

## Bases

`BaseTracer``_StreamingCallbackHandler`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `auto_close` | `bool` | Default:`True`  Whether to close the stream when the root run finishes. |
| `include_names` | `Sequence[str] | None` | Default:`None`  Only include runs from `Runnable` objects with matching names. |
| `include_types` | `Sequence[str] | None` | Default:`None`  Only include runs from `Runnable` objects with matching types. |
| `include_tags` | `Sequence[str] | None` | Default:`None`  Only include runs from `Runnable` objects with matching tags. |
| `exclude_names` | `Sequence[str] | None` | Default:`None`  Exclude runs from `Runnable` objects with matching names. |
| `exclude_types` | `Sequence[str] | None` | Default:`None`  Exclude runs from `Runnable` objects with matching types. |
| `exclude_tags` | `Sequence[str] | None` | Default:`None`  Exclude runs from `Runnable` objects with matching tags. |
| `_schema_format` | `Literal['original', 'streaming_events']` | Default:`'streaming_events'`  Primarily changes how the inputs and outputs are handled.  **For internal use only. This API will change.**   - `'original'` is the format used by all current tracers. This format is   slightly inconsistent with respect to inputs and outputs. - 'streaming\_events' is used for supporting streaming events, for   internal usage. It will likely change in the future,   or be deprecated entirely in favor of a dedicated async   tracer for streaming events. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| auto\_close | [bool](https://docs.python.org/3/library/functions.html#bool) |
| include\_names | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| include\_types | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| include\_tags | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| exclude\_names | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| exclude\_types | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| exclude\_tags | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| \_schema\_format | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['original', 'streaming\_events'] |

## Attributes

[attribute

auto\_close: auto\_close](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/auto_close)[attribute

include\_names: include\_names](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/include_names)[attribute

include\_types: include\_types](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/include_types)[attribute

include\_tags: include\_tags](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/include_tags)[attribute

exclude\_names: exclude\_names](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/exclude_names)[attribute

exclude\_types: exclude\_types](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/exclude_types)[attribute

exclude\_tags: exclude\_tags](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/exclude_tags)[attribute

lock](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/lock)[attribute

send\_stream](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/send_stream)[attribute

receive\_stream](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/receive_stream)[attribute

root\_id: UUID | None](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/root_id)

## Methods

[method

send

Send a patch to the stream, return `False` if the stream is closed.](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/send)[method

tap\_output\_aiter

Tap an output async iterator to stream its values to the log.](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/tap_output_aiter)[method

tap\_output\_iter

Tap an output iterator to stream its values to the log.](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/tap_output_iter)[method

include\_run

Check if a `Run` should be included in the log.](/python/langchain-core/tracers/log_stream/LogStreamCallbackHandler/include_run)

## Inherited from[BaseTracer](/python/langchain-core/tracers/base/BaseTracer)

### Methods

[Mon\_chat\_model\_start

—

Start a trace for a chat model run.](/python/langchain-core/tracers/base/BaseTracer/on_chat_model_start)[Mon\_llm\_start

—

Start a trace for an LLM run.](/python/langchain-core/tracers/base/BaseTracer/on_llm_start)[Mon\_llm\_new\_token

—

Run on new LLM token.](/python/langchain-core/tracers/base/BaseTracer/on_llm_new_token)[Mon\_retry

—

Run on retry.](/python/langchain-core/tracers/base/BaseTracer/on_retry)[Mon\_llm\_end

—

End a trace for an LLM or chat model run.](/python/langchain-core/tracers/base/BaseTracer/on_llm_end)[Mon\_llm\_error

—

Handle an error for an LLM run.](/python/langchain-core/tracers/base/BaseTracer/on_llm_error)[Mon\_chain\_start

—

Start a trace for a chain run.](/python/langchain-core/tracers/base/BaseTracer/on_chain_start)[Mon\_chain\_end

—

End a trace for a chain run.](/python/langchain-core/tracers/base/BaseTracer/on_chain_end)[Mon\_chain\_error

—

Handle an error for a chain run.](/python/langchain-core/tracers/base/BaseTracer/on_chain_error)[Mon\_tool\_start

—

Start a trace for a tool run.](/python/langchain-core/tracers/base/BaseTracer/on_tool_start)[Mon\_tool\_end

—

End a trace for a tool run.](/python/langchain-core/tracers/base/BaseTracer/on_tool_end)[Mon\_tool\_error

—

Handle an error for a tool run.](/python/langchain-core/tracers/base/BaseTracer/on_tool_error)[Mon\_retriever\_start

—

Run when the `Retriever` starts running.](/python/langchain-core/tracers/base/BaseTracer/on_retriever_start)[Mon\_retriever\_error

—

Run when `Retriever` errors.](/python/langchain-core/tracers/base/BaseTracer/on_retriever_error)[Mon\_retriever\_end

—

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


