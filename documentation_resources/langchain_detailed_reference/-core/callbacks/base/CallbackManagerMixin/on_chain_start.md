<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chain_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_chain\_start

Run when a chain starts running.


```
on_chain_start(
  self,
  serialized: dict[str, Any],
  inputs: dict[str, Any],
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
| `serialized`\* | `dict[str, Any]` | The serialized chain. |
| `inputs`\* | `dict[str, Any]` | The inputs. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


