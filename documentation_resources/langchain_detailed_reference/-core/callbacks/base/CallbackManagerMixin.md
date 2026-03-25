<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/CallbackManagerMixin -->

Classv1.2.21 (latest)●Since v0.1

# CallbackManagerMixin

Mixin for callback manager.


```
CallbackManagerMixin()
```

## Methods

[method

on\_llm\_start

Run when LLM starts running.

Warning

This method is called for non-chat models (regular text completion LLMs). If
you're implementing a handler for a chat model, you should use
`on_chat_model_start` instead.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_llm_start)[method

on\_chat\_model\_start

Run when a chat model starts running.

Warning

This method is called for chat models. If you're implementing a handler for
a non-chat model, you should use `on_llm_start` instead.

Note

When overriding this method, the signature **must** include the two
required positional arguments `serialized` and `messages`. Avoid
using `*args` in your override — doing so causes an `IndexError`
in the fallback path when the callback system converts `messages`
to prompt strings for `on_llm_start`. Always declare the
signature explicitly:

.. code-block:: python

```
def on_chat_model_start(
    self,
    serialized: dict[str, Any],
    messages: list[list[BaseMessage]],
    **kwargs: Any,
) -> None:
    raise NotImplementedError  # triggers fallback to on_llm_start
```](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chat_model_start)[method

on\_retriever\_start

Run when the `Retriever` starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start)[method

on\_chain\_start

Run when a chain starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chain_start)[method

on\_tool\_start

Run when the tool starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start)


