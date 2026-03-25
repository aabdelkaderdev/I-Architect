<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chat_model_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chat\_model\_start

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
```


```
on_chat_model_start(
  self,
  serialized: dict[str, Any],
  messages: list[list[BaseMessage]],
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized chat model. |
| `messages`\* | `list[list[BaseMessage]]` | The messages. Must be a list of message lists — this is a required positional argument and must be present in any override. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


