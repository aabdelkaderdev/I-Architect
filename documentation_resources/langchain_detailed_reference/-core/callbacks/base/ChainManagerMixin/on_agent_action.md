<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/ChainManagerMixin/on_agent_action -->

Methodv1.2.21 (latest)●Since v0.1

# on\_agent\_action

Run on agent action.


```
on_agent_action(
  self,
  action: AgentAction,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `action`\* | `AgentAction` | The agent action. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


