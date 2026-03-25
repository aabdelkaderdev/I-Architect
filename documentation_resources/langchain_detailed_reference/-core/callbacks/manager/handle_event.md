<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/handle_event -->

Functionv1.2.21 (latest)●Since v0.1

# handle\_event

Generic event handler for `CallbackManager`.


```
handle_event(
  handlers: list[BaseCallbackHandler],
  event_name: str,
  ignore_condition_name: str | None,
  *args: Any = (),
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `handlers`\* | `list[BaseCallbackHandler]` | The list of handlers that will handle the event. |
| `event_name`\* | `str` | The name of the event (e.g., `'on_llm_start'`). |
| `ignore_condition_name`\* | `str | None` | Name of the attribute defined on handler that if `True` will cause the handler to be skipped for the given event. |
| `*args` | `Any` | Default:`()`  The arguments to pass to the event handler. |
| `**kwargs` | `Any` | Default:`{}`  The keyword arguments to pass to the event handler |


