<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/AgentExecutor/iter -->

Methodv1.2.13 (latest)●Since v1.0

# iter

Enables iteration over steps taken to reach final output.


```
iter(
  self,
  inputs: Any,
  callbacks: Callbacks = None,
  *,
  include_run_info: bool = False,
  async_: bool = False
) -> AgentExecutorIterator
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `inputs`\* | `Any` | Inputs to the agent. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to run. |
| `include_run_info` | `bool` | Default:`False`  Whether to include run info. |
| `async_` | `bool` | Default:`False`  Whether to run async. (Ignored) |


