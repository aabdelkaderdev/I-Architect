<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_custom_event -->

Methodv1.2.21 (latest)●Since v0.2

# on\_custom\_event

Override to define a handler for custom events.


```
on_custom_event(
  self,
  name: str,
  data: Any,
  *,
  run_id: UUID,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name`\* | `str` | The name of the custom event. |
| `data`\* | `Any` | The data for the custom event.  Format will match the format specified by the user. |
| `run_id`\* | `UUID` | The ID of the run. |
| `tags` | `list[str] | None` | Default:`None`  The tags associated with the custom event (includes inherited tags). |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata associated with the custom event (includes inherited metadata). |


