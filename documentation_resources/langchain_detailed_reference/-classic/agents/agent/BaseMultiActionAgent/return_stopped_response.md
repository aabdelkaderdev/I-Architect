<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/BaseMultiActionAgent/return_stopped_response -->

Methodv1.2.13 (latest)●Since v1.0

# return\_stopped\_response

Return response when agent has been stopped due to max iterations.


```
return_stopped_response(
  self,
  early_stopping_method: str,
  intermediate_steps: list[tuple[AgentAction, str]],
  **_: Any = {}
) -> AgentFinish
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `early_stopping_method`\* | `str` | Method to use for early stopping. |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | Steps the LLM has taken to date, along with observations. |


