<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_agent/base/OpenAIFunctionsAgent/return_stopped_response -->

Methodv1.2.13 (latest)●Since v1.0

# return\_stopped\_response

Return response when agent has been stopped due to max iterations.


```
return_stopped_response(
  self,
  early_stopping_method: str,
  intermediate_steps: list[tuple[AgentAction, str]],
  **kwargs: Any = {}
) -> AgentFinish
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `early_stopping_method`\* | `str` | The early stopping method to use. |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | Intermediate steps. |
| `**kwargs` | `Any` | Default:`{}`  User inputs. |


