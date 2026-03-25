<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/RunManagerMixin/on_text -->

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
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


