<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/AgentExecutor/from_agent_and_tools -->

Methodv1.2.13 (latest)●Since v1.0

# from\_agent\_and\_tools

Create from agent and tools.


```
from_agent_and_tools(
  cls,
  agent: BaseSingleActionAgent | BaseMultiActionAgent | Runnable,
  tools: Sequence[BaseTool],
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> AgentExecutor
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `agent`\* | `BaseSingleActionAgent | BaseMultiActionAgent | Runnable` | Agent to use. |
| `tools`\* | `Sequence[BaseTool]` | Tools to use. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to use. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments. |


