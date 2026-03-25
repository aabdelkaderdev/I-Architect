<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_agent/base/OpenAIFunctionsAgent/plan -->

Methodv1.2.13 (latest)●Since v1.0

# plan

Given input, decided what to do.


```
plan(
  self,
  intermediate_steps: list[tuple[AgentAction, str]],
  callbacks: Callbacks = None,
  with_functions: bool = True,
  **kwargs: Any = {}
) -> AgentAction | AgentFinish
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | Steps the LLM has taken to date, along with observations. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to use. |
| `with_functions` | `bool` | Default:`True`  Whether to use functions. |
| `**kwargs` | `Any` | Default:`{}`  User inputs. |


