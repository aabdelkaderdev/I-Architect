<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/file/FileCallbackHandler/on_agent_action -->

Methodv1.2.21 (latest)●Since v0.1

# on\_agent\_action

Handle agent action by writing the action log.


```
on_agent_action(
  self,
  action: AgentAction,
  color: str | None = None,
  **kwargs: Any = {}
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `action`\* | `AgentAction` | The agent action containing the log to write. |
| `color` | `str | None` | Default:`None`  Color override for this specific output.  If `None`, uses `self.color`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


