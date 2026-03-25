<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_agent_finish -->

Methodv1.2.21 (latest)●Since v0.1

# on\_agent\_finish

Run on the agent end.


```
on_agent_finish(
  self,
  finish: AgentFinish,
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
| `finish`\* | `AgentFinish` | The agent finish. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


