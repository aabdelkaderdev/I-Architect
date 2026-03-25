<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/AgentExecutor/astream -->

Methodv1.2.13 (latest)●Since v1.0

# astream

Async enables streaming over steps taken to reach final output.


```
astream(
  self,
  input: dict[str, Any] | Any,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> AsyncIterator[AddableDict]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `dict[str, Any] | Any` | Input to the agent. |
| `config` | `RunnableConfig | None` | Default:`None`  Config to use. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments. |


