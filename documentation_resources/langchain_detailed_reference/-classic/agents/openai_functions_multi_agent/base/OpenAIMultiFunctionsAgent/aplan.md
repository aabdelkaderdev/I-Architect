<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_multi_agent/base/OpenAIMultiFunctionsAgent/aplan -->

Methodv1.2.13 (latest)●Since v1.0

# aplan

Async given input, decided what to do.


```
aplan(
  self,
  intermediate_steps: list[tuple[AgentAction, str]],
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> list[AgentAction] | AgentFinish
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | Steps the LLM has taken to date, along with observations. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to use. |
| `**kwargs` | `Any` | Default:`{}`  User inputs. |


