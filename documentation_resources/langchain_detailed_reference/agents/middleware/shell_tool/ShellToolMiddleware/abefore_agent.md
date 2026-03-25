<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/shell_tool/ShellToolMiddleware/abefore_agent -->

Methodv1.2.13 (latest)●Since v1.0

# abefore\_agent

Async start the shell session and run startup commands.


```
abefore_agent(
  self,
  state: ShellToolState[ResponseT],
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `ShellToolState[ResponseT]` | The current agent state. |
| `runtime`\* | `Runtime[ContextT]` | The runtime context. |


