<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/BaseMultiActionAgent/plan -->

Methodv1.2.13 (latest)●Since v1.0

# plan

Given input, decided what to do.


```
plan(
  self,
  intermediate_steps: list[tuple[AgentAction, str]],
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> list[AgentAction] | AgentFinish
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | Steps the LLM has taken to date, along with the observations. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to run. |
| `**kwargs` | `Any` | Default:`{}`  User inputs. |


