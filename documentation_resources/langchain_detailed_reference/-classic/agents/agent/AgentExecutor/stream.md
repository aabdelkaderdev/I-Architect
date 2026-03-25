<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/AgentExecutor/stream -->

Methodv1.2.13 (latest)●Since v1.0

# stream

Enables streaming over steps taken to reach final output.


```
stream(
  self,
  input: dict[str, Any] | Any,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> Iterator[AddableDict]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `dict[str, Any] | Any` | Input to the agent. |
| `config` | `RunnableConfig | None` | Default:`None`  Config to use. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments. |


