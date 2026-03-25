<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_finish -->

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
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `finish`\* | `AgentFinish` | The agent finish. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


