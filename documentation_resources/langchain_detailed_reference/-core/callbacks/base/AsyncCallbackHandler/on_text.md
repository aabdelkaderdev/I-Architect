<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_text -->

Methodv1.2.21 (latest)●Since v0.1

# on\_text

Run on an arbitrary text.


```
on_text(
  self,
  text: str,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


