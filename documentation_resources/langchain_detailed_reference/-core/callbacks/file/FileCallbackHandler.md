<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/file/FileCallbackHandler -->

Classv1.2.21 (latest)●Since v0.1

# FileCallbackHandler

Callback handler that writes to a file.

This handler supports both context manager usage (recommended) and direct
instantiation (deprecated) for backwards compatibility.


```
FileCallbackHandler(
  self,
  filename: str,
  mode: str = 'a',
  color: str | None = None
)
```

## Bases

`BaseCallbackHandler`

When not used as a context manager, a deprecation warning will be issued on
first use. The file will be opened immediately in `__init__` and closed in
`__del__` or when `close()` is called explicitly.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `filename`\* | `str` | The file path to write to. |
| `mode` | `str` | Default:`'a'`  The file open mode. Defaults to `'a'` (append). |
| `color` | `str | None` | Default:`None`  Default color for text output. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| filename | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| mode | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| color | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |

## Attributes

[attribute

filename: filename](/python/langchain-core/callbacks/file/FileCallbackHandler/filename)[attribute

mode: mode](/python/langchain-core/callbacks/file/FileCallbackHandler/mode)[attribute

color: color](/python/langchain-core/callbacks/file/FileCallbackHandler/color)[attribute

file: TextIO](/python/langchain-core/callbacks/file/FileCallbackHandler/file)

## Methods

[method

close

Close the file if it's open.

This method is safe to call multiple times and will only close
the file if it's currently open.](/python/langchain-core/callbacks/file/FileCallbackHandler/close)[method

on\_chain\_start

Print that we are entering a chain.](/python/langchain-core/callbacks/file/FileCallbackHandler/on_chain_start)[method

on\_chain\_end

Print that we finished a chain.](/python/langchain-core/callbacks/file/FileCallbackHandler/on_chain_end)[method

on\_agent\_action

Handle agent action by writing the action log.](/python/langchain-core/callbacks/file/FileCallbackHandler/on_agent_action)[method

on\_tool\_end

Handle tool end by writing the output with optional prefixes.](/python/langchain-core/callbacks/file/FileCallbackHandler/on_tool_end)[method

on\_text

Handle text output.](/python/langchain-core/callbacks/file/FileCallbackHandler/on_text)[method

on\_agent\_finish

Handle agent finish by writing the finish log.](/python/langchain-core/callbacks/file/FileCallbackHandler/on_agent_finish)

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

[Mon\_chain\_error

—

Run when chain errors.](/python/langchain-core/callbacks/base/ChainManagerMixin/on_chain_error)

## Inherited from[ToolManagerMixin](/python/langchain-core/callbacks/base/ToolManagerMixin)

### Methods

[Mon\_tool\_error

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

Run when the `Retriever` starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start)[Mon\_tool\_start

—

Run when the tool starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start)

## Inherited from[RunManagerMixin](/python/langchain-core/callbacks/base/RunManagerMixin)

### Methods

[Mon\_retry

—

Run on a retry event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_retry)[Mon\_custom\_event

—

Override to define a handler for a custom event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)


