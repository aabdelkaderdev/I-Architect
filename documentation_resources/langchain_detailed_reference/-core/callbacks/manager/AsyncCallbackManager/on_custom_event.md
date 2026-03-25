<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_custom_event -->

Methodv1.2.21 (latest)●Since v0.2

# on\_custom\_event

Dispatch an adhoc event to the handlers (async version).

This event should NOT be used in any internal LangChain code. The event is meant
specifically for users of the library to dispatch custom events that are
tailored to their application.


```
on_custom_event(
  self,
  name: str,
  data: Any,
  run_id: UUID | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name`\* | `str` | The name of the adhoc event. |
| `data`\* | `Any` | The data for the adhoc event. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |


