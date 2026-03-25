<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/LLMSingleActionAgent/aplan -->

Methodv1.2.13 (latest)●Since v1.0

# aplan

Async given input, decided what to do.


```
aplan(
  self,
  intermediate_steps: list[tuple[AgentAction, str]],
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> AgentAction | AgentFinish
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | Steps the LLM has taken to date, along with observations. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to run. |
| `**kwargs` | `Any` | Default:`{}`  User inputs. |


