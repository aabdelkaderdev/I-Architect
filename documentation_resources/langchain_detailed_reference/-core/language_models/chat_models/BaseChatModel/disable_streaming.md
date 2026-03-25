<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/disable_streaming -->

Attributev1.2.21 (latest)●Since v0.2

# disable\_streaming

Whether to disable streaming for this model.

If streaming is bypassed, then `stream`/`astream`/`astream_events` will
defer to `invoke`/`ainvoke`.

- If `True`, will always bypass streaming case.
- If `'tool_calling'`, will bypass streaming case only when the model is called
  with a `tools` keyword argument. In other words, LangChain will automatically
  switch to non-streaming behavior (`invoke`) only when the tools argument is
  provided. This offers the best of both worlds.
- If `False` (Default), will always use streaming case if available.

The main reason for this flag is that code might be written using `stream` and
a user may want to swap out a given model for another model whose implementation
does not properly support streaming.


```
disable_streaming: bool | Literal['tool_calling'] = False
```


