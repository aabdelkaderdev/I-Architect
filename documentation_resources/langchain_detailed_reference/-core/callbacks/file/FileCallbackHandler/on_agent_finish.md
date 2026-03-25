<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/file/FileCallbackHandler/on_agent_finish -->

Methodv1.2.21 (latest)●Since v0.1

# on\_agent\_finish

Handle agent finish by writing the finish log.


```
on_agent_finish(
  self,
  finish: AgentFinish,
  color: str | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `finish`\* | `AgentFinish` | The agent finish object containing the log to write. |
| `color` | `str | None` | Default:`None`  Color override for this specific output.  If `None`, uses `self.color`. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


